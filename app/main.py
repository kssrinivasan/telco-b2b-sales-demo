"""FastAPI Backend for the Telco B2B AI Sales Agent Demo ("Agentic Deal Cockpit")."""

from contextlib import asynccontextmanager
from pathlib import Path
import time
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.capacity_agent import GOOGLE_MAPS_API_KEY, engine
from app.dataset import GROUNDING_DOCUMENTS, RFP_METADATA
from app.proposal_pdf import build_executive_proposal_pdf

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
DOCS_DIR = BASE_DIR / "docs"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-warm Spanner, BigQuery, and Vertex AI clients on startup so demo steps are sub-second
    engine.warm_up()
    yield


app = FastAPI(
    title="Telco B2B AI Sales Agent Demo — Agentic Deal Cockpit",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulateEconomicsRequest(BaseModel):
    amortization_months: int = 36
    discount_pct: float = 0.0
    include_near_net_sites: bool = True


class ApproveQuestionRequest(BaseModel):
    answer_text: str | None = None
    approved: bool = True


class SignOffRequest(BaseModel):
    approver_name: str = "Elena Rostova, SVP Commercial & Enterprise Markets"
    amortization_months: int = 36
    discount_override_pct: float = 0.0
    comments: str = "Approved 36-month Near-Net CAPEX amortization ($4,200); 42.4% Gross Margin verified."


class CopilotChatRequest(BaseModel):
    message: str


@app.get("/api/bootstrap")
def get_bootstrap() -> dict[str, Any]:
    """Returns the complete pre-warmed Deal Cockpit state for instant initial render."""
    auto_count = sum(1 for q in engine.live_questions if q["status"] == "Auto-Answered")
    review_count = len(engine.live_questions) - auto_count
    approved_review_count = sum(
        1 for q in engine.live_questions if q["status"] != "Auto-Answered" and q["sme_approved"]
    )
    econ = engine.simulate_deal_economics(
        amortization_months=engine.proposal_signoff_state["amortization_months"],
        discount_pct=engine.proposal_signoff_state["discount_override_pct"],
    )
    return {
        "rfp_metadata": RFP_METADATA,
        "google_maps_api_key": GOOGLE_MAPS_API_KEY,
        "pops": engine.live_pops,
        "backbone_links": engine.live_links,
        "sites": engine.live_sites,
        "splice_closures": engine.live_splices,
        "compliance_summary": {
            "total": len(engine.live_questions),
            "auto_answered": auto_count,
            "human_review": review_count,
            "approved_reviews": approved_review_count,
        },
        "economics": econ,
        "grounding_documents": GROUNDING_DOCUMENTS,
        "signoff_state": engine.proposal_signoff_state,
        "telemetry_log": engine.telemetry_log,
    }


@app.post("/api/step/{step_number}")
def execute_workflow_step(step_number: int) -> dict[str, Any]:
    if step_number not in (1, 2, 3, 4):
        raise HTTPException(status_code=400, detail="Step number must be between 1 and 4")
    payload = engine.get_step_payload(step_number)
    payload["telemetry_log"] = engine.telemetry_log[:15]
    return payload


@app.get("/api/sites/{site_id}")
def inspect_clinic_site(site_id: str) -> dict[str, Any]:
    result = engine.query_site_live_spanner(site_id)
    if not result.get("site"):
        raise HTTPException(status_code=404, detail=f"Site {site_id} not found")
    result["telemetry_log"] = engine.telemetry_log[:12]
    return result


@app.get("/api/questions")
def list_compliance_questions(
    status: str = Query("all", description="all | auto | review"),
    category: str = Query("ALL", description="ALL | SEC | NET | CLD | SLA | OPS"),
    search: str = Query("", description="Search substring"),
) -> dict[str, Any]:
    items = engine.live_questions
    if status == "auto":
        items = [q for q in items if q["status"] == "Auto-Answered"]
    elif status == "review":
        items = [q for q in items if q["status"] != "Auto-Answered"]

    if category and category != "ALL":
        items = [q for q in items if q["category"] == category]

    if search.strip():
        needle = search.strip().lower()
        items = [
            q
            for q in items
            if needle in q["question_id"].lower()
            or needle in q["question_text"].lower()
            or needle in q["answer_text"].lower()
            or needle in q["domain"].lower()
            or needle in q["source_doc"].lower()
        ]

    auto_total = sum(1 for q in engine.live_questions if q["status"] == "Auto-Answered")
    review_total = len(engine.live_questions) - auto_total
    review_approved = sum(
        1 for q in engine.live_questions if q["status"] != "Auto-Answered" and q["sme_approved"]
    )
    return {
        "total_matching": len(items),
        "counts": {
            "all": len(engine.live_questions),
            "auto": auto_total,
            "review": review_total,
            "review_approved": review_approved,
        },
        "questions": items,
    }


@app.post("/api/questions/{question_id}/approve")
def approve_compliance_question(question_id: str, req: ApproveQuestionRequest) -> dict[str, Any]:
    target = next((q for q in engine.live_questions if q["question_id"] == question_id), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"Question {question_id} not found")
    if req.answer_text is not None and req.answer_text.strip():
        target["answer_text"] = req.answer_text.strip()
    target["sme_approved"] = req.approved
    engine._log_telemetry(
        "BigQuery (compliance_knowledge_base)",
        f"SME Human-in-the-Loop Sign-Off ({question_id})",
        f"UPDATE `anthosbm-292404.telco_b2b_sales.compliance_knowledge_base` SET sme_approved = TRUE WHERE question_id = '{question_id}'",
        11.4,
        1,
    )
    review_approved = sum(
        1 for q in engine.live_questions if q["status"] != "Auto-Answered" and q["sme_approved"]
    )
    return {
        "updated": target,
        "review_approved_count": review_approved,
        "telemetry_log": engine.telemetry_log[:12],
    }


@app.post("/api/questions/approve-all-flagged")
def approve_all_flagged_questions() -> dict[str, Any]:
    count = 0
    for q in engine.live_questions:
        if q["status"] != "Auto-Answered" and not q["sme_approved"]:
            q["sme_approved"] = True
            count += 1
    engine._log_telemetry(
        "BigQuery (compliance_knowledge_base)",
        "Batch SME Approval (15 Flagged Questions)",
        "UPDATE `anthosbm-292404.telco_b2b_sales.compliance_knowledge_base` SET sme_approved = TRUE WHERE status = 'Flagged for Human Review'",
        18.2,
        count,
    )
    return {
        "approved_count": count,
        "telemetry_log": engine.telemetry_log[:12],
    }


@app.post("/api/simulate-economics")
def simulate_economics(req: SimulateEconomicsRequest) -> dict[str, Any]:
    engine.proposal_signoff_state["amortization_months"] = req.amortization_months
    engine.proposal_signoff_state["discount_override_pct"] = req.discount_pct
    econ = engine.simulate_deal_economics(
        amortization_months=req.amortization_months,
        discount_pct=req.discount_pct,
        include_near_net_sites=req.include_near_net_sites,
    )
    econ["telemetry_log"] = engine.telemetry_log[:12]
    return econ


@app.post("/api/signoff")
def commercial_vp_signoff(req: SignOffRequest) -> dict[str, Any]:
    engine.proposal_signoff_state = {
        "signed_off": True,
        "approver_name": req.approver_name,
        "approved_at": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "amortization_months": req.amortization_months,
        "discount_override_pct": req.discount_override_pct,
        "comments": req.comments,
    }
    econ = engine.simulate_deal_economics(
        amortization_months=req.amortization_months,
        discount_pct=req.discount_override_pct,
    )
    engine._log_telemetry(
        "Executive Governance & Deal Desk",
        "1-Click Commercial VP Proposal Sign-Off",
        f"APPROVE Proposal PROP-APEX-2026-1012 (TCV=${econ['total_contract_value_usd']:,.0f}, Margin={econ['gross_margin_pct']}%)",
        9.4,
        1,
    )
    return {
        "signoff_state": engine.proposal_signoff_state,
        "economics": econ,
        "telemetry_log": engine.telemetry_log[:12],
    }


@app.post("/api/chat")
def copilot_chat(req: CopilotChatRequest) -> dict[str, Any]:
    res = engine.chat_with_copilot(req.message)
    res["telemetry_log"] = engine.telemetry_log[:12]
    return res


@app.post("/api/refresh-live-db")
def refresh_live_db() -> dict[str, Any]:
    sp_res = engine.refresh_from_spanner()
    bq_res = engine.refresh_from_bigquery()
    return {
        "spanner": sp_res,
        "bigquery": bq_res,
        "telemetry_log": engine.telemetry_log[:15],
    }


@app.get("/api/docs/{filename}")
def serve_grounding_pdf(filename: str):
    safe_name = Path(filename).name
    file_path = DOCS_DIR / safe_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Document {safe_name} not found")
    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{safe_name}"'},
    )


@app.get("/api/proposal/pdf")
def download_executive_proposal_pdf():
    econ = engine.simulate_deal_economics(
        amortization_months=engine.proposal_signoff_state["amortization_months"],
        discount_pct=engine.proposal_signoff_state["discount_override_pct"],
    )
    pdf_bytes = build_executive_proposal_pdf(
        econ=econ,
        signoff_state=engine.proposal_signoff_state,
        sites=engine.live_sites,
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="Apex_Health_Executive_Proposal_PROP-APEX-2026-1012.pdf"'
        },
    )


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    index_file = STATIC_DIR / "index.html"
    return index_file.read_text(encoding="utf-8")
