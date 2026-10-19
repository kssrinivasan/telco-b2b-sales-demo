"""Generates the final branded RFx Executive Proposal PDF for Step 4."""

import io
from typing import Any
from fpdf import FPDF


def _clean(text: str) -> str:
    return (
        str(text)
        .replace("—", " - ")
        .replace("–", "-")
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("‘", "'")
        .replace("≥", ">=")
        .replace("≤", "<=")
        .replace("•", "*")
    )


def build_executive_proposal_pdf(
    econ: dict[str, Any],
    signoff_state: dict[str, Any],
    sites: list[dict[str, Any]],
) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()

    # Header Banner
    pdf.set_fill_color(11, 37, 69)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 11, "  EXECUTIVE COMMERCIAL & TECHNICAL PROPOSAL", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(
        0,
        8,
        "  Prepared for: Apex Health Regional Network  |  RFP #AH-2026-SDWAN-094  |  Proposal ID: PROP-APEX-2026-1012",
        fill=True,
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(5)
    pdf.set_text_color(25, 30, 40)

    # Executive Cover Letter
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 65, 130)
    pdf.cell(0, 7, "1. EXECUTIVE COVER LETTER & VALUE COMMITMENT", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 35, 45)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.multi_cell(
        0,
        5.2,
        _clean(
            "Dear Apex Health Executive Procurement & Clinical Infrastructure Committee,\n\n"
            "Thank you for inviting us to respond to RFP #AH-2026-SDWAN-094. Using our live Cloud Spanner optical "
            "inventory and BigQuery network telemetry engines, we have completed a 100% deterministic engineering "
            "and compliance validation across all 45 Apex Health clinical, surgical, and hospital sites in Washington, "
            "Oregon, Idaho, and Northern California.\n\n"
            "Key Highlights of Our Binding Proposal:\n"
            "* 43 of 45 Clinic Sites (95.6%) are 100% On-Net Lit Buildings today with 10Gbps SFP+ ports reserved and "
            "ready for immediate provisioning.\n"
            "* 2 Near-Net Clinic Sites - Site #28 (Wenatchee Valley Specialty Clinic, 82m from splice closure SC-QCY-028) "
            "and Site #33 (Hood River Gorge Medical Center, 118m from splice closure SC-PDX-033) - will be completed within "
            "11 business days. We are waiving 100% of the $4,200 lateral fiber construction CAPEX upfront by folding it "
            f"into a {econ['amortization_months']}-month amortization schedule.\n"
            "* Strict <12.0ms Epic EHR Latency Guarantee & 99.999% Five-Nines SLA: Every clinic operates between 1.5ms "
            "and 10.4ms RTD to the Quincy Epic EHR Primary Enclave (mean 4.8ms), backed by 2x 100Gbps Google Cloud "
            "Dedicated Interconnects and full acceptance of your 15% MRC latency credit schedule.\n"
            "* 200-Question Security & Architecture Compliance Matrix: 100% completed and grounded against our HITRUST CSF v11, "
            "ISO 27001, and HIPAA BAA attestations."
        ),
    )
    pdf.ln(3)

    # Commercial Pricing Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 65, 130)
    pdf.cell(0, 7, "2. COMMERCIAL PRICING SCHEDULE & 36-MONTH CAPEX AMORTIZATION", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(225, 232, 242)
    pdf.set_text_color(20, 25, 35)
    pdf.cell(28, 6, "SKU", border=1, fill=True)
    pdf.cell(92, 6, "Service Description", border=1, fill=True)
    pdf.cell(14, 6, "Qty", border=1, fill=True, align="C")
    pdf.cell(26, 6, "Unit MRC", border=1, fill=True, align="R")
    pdf.cell(30, 6, "Total Monthly", border=1, fill=True, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 7.5)
    for item in econ["pricing_line_items"]:
        pdf.cell(28, 6, _clean(item["sku_id"]), border=1)
        pdf.cell(92, 6, _clean(item["product_name"][:54]), border=1)
        pdf.cell(14, 6, str(item["quantity"]), border=1, align="C")
        pdf.cell(26, 6, f"${item['unit_proposed_mrc_usd']:,.2f}", border=1, align="R")
        pdf.cell(30, 6, f"${item['total_monthly_mrc_usd']:,.2f}", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_fill_color(240, 246, 252)
    pdf.cell(160, 7, "Total Monthly Recurring Charge (MRC) - 45 Clinics + 2x 100G Cloud Interconnects", border=1, fill=True)
    pdf.cell(30, 7, f"${econ['monthly_recurring_revenue_usd']:,.2f}", border=1, fill=True, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(160, 7, "Upfront Near-Net Fiber Construction NRE Charged to Apex Health ($4,200 Waived)", border=1, fill=True)
    pdf.cell(30, 7, f"${econ['upfront_nre_charged_usd']:,.2f}", border=1, fill=True, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(160, 7, f"Total Contract Value ({econ['amortization_months'] or 36} Months)", border=1, fill=True)
    pdf.cell(30, 7, f"${econ['total_contract_value_usd']:,.2f}", border=1, fill=True, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Near-Net Engineering Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 65, 130)
    pdf.cell(0, 7, "3. NEAR-NET LATERAL FIBER ENGINEERING (SITES #28 & #33)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 35, 45)
    for s in sites:
        if s["site_num"] in (28, 33):
            pdf.multi_cell(
                0,
                5,
                _clean(
                    f"* {s['site_id']} - {s['site_name']} ({s['address']}): {s['distance_to_splice_m']}m from splice closure "
                    f"{s['splice_closure_id']}. Construction: {s['construction_method']}. Post-Build Latency to Epic EHR: "
                    f"{s['estimated_ehr_latency_ms']}ms (vs. {s['legacy_wan_latency_ms']}ms legacy WAN). CAPEX: ${s['build_capex_usd']:,} (Amortized)."
                ),
            )
            pdf.ln(1)

    pdf.ln(3)
    # Executive Approval Block
    pdf.set_fill_color(235, 248, 242) if signoff_state.get("signed_off") else pdf.set_fill_color(250, 245, 232)
    pdf.set_font("Helvetica", "B", 10)
    status_str = (
        f"APPROVED & DIGITALLY SIGNED BY {signoff_state.get('approver_name')} AT {signoff_state.get('approved_at')}"
        if signoff_state.get("signed_off")
        else f"PENDING FINAL 1-CLICK SIGN-OFF BY {signoff_state.get('approver_name')}"
    )
    pdf.cell(0, 8, f"  COMMERCIAL GOVERNANCE STATUS: {_clean(status_str)}", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(
        0,
        7,
        f"  Internal Deal Gross Margin: {econ['gross_margin_pct']}% (Floor: 40.0%)  |  Win Probability: {econ['estimated_win_probability_pct']}%",
        border=1,
        fill=True,
        new_x="LMARGIN",
        new_y="NEXT",
    )

    buf = io.BytesIO()
    pdf.output(buf)
    return buf.getvalue()
