# Telco B2B AI Sales Agent Demo — "Agentic Deal Cockpit"

An end-to-end **Telco B2B AI Sales & Network Capacity Planning Demo** built on **Google Cloud Spanner**, **BigQuery**, **Vertex AI Search**, **Vertex AI Gemini 3.8 Flash**, **Vertex AI Agent Runtime**, and **Google Maps Platform**.

---

## 1. Executive Scenario: Apex Health Regional Network (`RFP #AH-2026-SDWAN-094`)

A regional healthcare network (**Apex Health**) issues a complex 36-month RFP (`Apex_Health_RFP_SDWAN_Cloud.pdf`) requiring:
1. **Low-latency redundant Dual-Transport SD-WAN + 10Gbps Optical Wavelengths** across **45 clinic & hospital sites** in WA, OR, ID, and CA.
2. **Direct Cloud Interconnects**: 2x 100Gbps Google Cloud Dedicated Interconnects (`us-west1`) and direct optical wave peering to the **Quincy, WA Epic EHR Primary Enclave**.
3. **Stringent SLAs & Penalty Clauses**: **99.999% ("Five Nines") availability**, full **HIPAA / HITRUST CSF v11 BAA** compliance, and a strict **15% MRC service credit penalty per 1.0ms** if round-trip latency exceeds **12.0ms** between any clinic and the Primary Epic EHR Data Center (with termination rights above **18.0ms**).
4. **200-Question Vendor Security & Architecture Compliance Matrix** across Security (`SEC`), Network (`NET`), Cloud (`CLD`), SLA (`SLA`), and Operations (`OPS`).

### Business Value Demonstrated
| Metric | Legacy Manual Telco Process | Agentic Deal Cockpit |
| :--- | :--- | :--- |
| **End-to-End Turnaround Time** | **3–4 Weeks (21 Days)** across 4 siloed teams | **< 15 Minutes (11 Mins)** automated orchestration |
| **Deal Qualification Score** | Manual / Unscored | **92% (High Fit — 95.6% Footprint On-Net)** |
| **200-Question Compliance Matrix** | 5–7 Days of manual InfoSec/Legal copy-paste | **185 Auto-Answered (100% Conf.) + 15 Flagged for SME Review** |
| **45-Site Fiber Feasibility** | 10–14 Days manual GIS & OSP checks | **< 0.5s Live Cloud Spanner Query (43 On-Net, 2 Near-Net)** |
| **Near-Net Build CAPEX & Margin** | Separate $4,200 NRE line item (causes bid loss) | **$4,200 folded into 36-Month Amortization ($116.67/mo) -> 42.4% Gross Margin Protected** |

---

## 2. Live GCP Resources Provisioned (`anthosbm-292404`)

- **Cloud Spanner**:
  - Instance: `networktopology-instance` (`regional-us-central1`)
  - Database: `b2b-sales-inventory-db`
  - Tables: `ClinicSites` (45 clinics), `FiberPoPs` (9 regional PoPs & Cloud Interconnects), `SpliceClosures` (45 splice closures including `SC-QCY-028` at 82m and `SC-PDX-033` at 118m), `FiberBackboneLinks` (10 DWDM trunk rings).
- **BigQuery**:
  - Dataset: `anthosbm-292404.telco_b2b_sales`
  - Tables: `fiber_build_cost_models`, `product_pricing_catalog`, `historical_bid_analytics`, `compliance_knowledge_base` (200 questions).
- **Vertex AI Search (Discovery Engine)**:
  - Data Store: `projects/322843095383/locations/global/collections/default_collection/dataStores/apex-health-rfx-grounding-store`
  - GCS Document Repository: `gs://rf_response_agent/apex_health_demo_docs/`
    - `Apex_Health_RFP_SDWAN_Cloud.pdf`
    - `Telco_HIPAA_ISO27001_Security_Compliance_Attestation_v4.2.pdf`
    - `Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf`
    - `Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf`
    - `Past_Winning_Bid_Pacific_Northwest_Health_Network_2025.pdf`

---

## 3. Running Locally

```bash
cd /usr/local/google/home/kssrinivasan/telco-b2b-sales-demo
/usr/local/google/home/kssrinivasan/.local/bin/uv sync --index https://pypi.org/simple
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
```
Open `http://localhost:8080` in your browser.
