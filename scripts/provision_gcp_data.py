"""Provisions and seeds Cloud Spanner, BigQuery, and Vertex AI Search in anthosbm-292404."""

import json
from pathlib import Path
import sys
import time

from google.api_core.exceptions import AlreadyExists, NotFound
from google.cloud import bigquery
from google.cloud import discoveryengine_v1 as discoveryengine
from google.cloud import spanner

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.dataset import (
    CLINIC_SITES,
    COMPLIANCE_QUESTIONS,
    FIBER_BACKBONE_LINKS,
    FIBER_BUILD_COST_MODELS,
    FIBER_POPS,
    GROUNDING_DOCUMENTS,
    HISTORICAL_BID_ANALYTICS,
    PRODUCT_PRICING_CATALOG,
    SPLICE_CLOSURES,
)

PROJECT_ID = "anthosbm-292404"
SPANNER_INSTANCE_ID = "networktopology-instance"
SPANNER_DB_ID = "b2b-sales-inventory-db"
BQ_DATASET_ID = "telco_b2b_sales"
DATA_STORE_ID = "apex-health-rfx-grounding-store"


def provision_spanner():
    print(f"=== [1/3] Provisioning Cloud Spanner ({SPANNER_INSTANCE_ID} / {SPANNER_DB_ID}) ===")
    spanner_client = spanner.Client(project=PROJECT_ID)
    instance = spanner_client.instance(SPANNER_INSTANCE_ID)
    database = instance.database(SPANNER_DB_ID)

    ddl_statements = [
        """CREATE TABLE FiberPoPs (
            pop_id STRING(32) NOT NULL,
            pop_name STRING(128) NOT NULL,
            city STRING(64) NOT NULL,
            state STRING(16) NOT NULL,
            address STRING(256) NOT NULL,
            lat FLOAT64 NOT NULL,
            lng FLOAT64 NOT NULL,
            pop_tier STRING(64) NOT NULL,
            router_platform STRING(128) NOT NULL,
            total_10g_ports INT64 NOT NULL,
            available_10g_ports INT64 NOT NULL,
            total_100g_ports INT64 NOT NULL,
            available_100g_ports INT64 NOT NULL,
            cloud_onramp STRING(256) NOT NULL,
            current_utilization_pct FLOAT64 NOT NULL,
            base_ehr_latency_ms FLOAT64 NOT NULL
        ) PRIMARY KEY (pop_id)""",
        """CREATE TABLE FiberBackboneLinks (
            link_id STRING(32) NOT NULL,
            from_pop STRING(32) NOT NULL,
            to_pop STRING(32) NOT NULL,
            capacity_gbps INT64 NOT NULL,
            rtd_ms FLOAT64 NOT NULL,
            route_name STRING(128) NOT NULL
        ) PRIMARY KEY (link_id)""",
        """CREATE TABLE SpliceClosures (
            splice_closure_id STRING(32) NOT NULL,
            pop_id STRING(32) NOT NULL,
            served_site_id STRING(32) NOT NULL,
            lat FLOAT64 NOT NULL,
            lng FLOAT64 NOT NULL,
            fiber_cable_id STRING(64) NOT NULL,
            total_strands INT64 NOT NULL,
            available_dark_strands INT64 NOT NULL,
            enclosure_type STRING(128) NOT NULL,
            splice_loss_db FLOAT64 NOT NULL
        ) PRIMARY KEY (splice_closure_id)""",
        """CREATE TABLE ClinicSites (
            site_id STRING(32) NOT NULL,
            site_num INT64 NOT NULL,
            site_name STRING(128) NOT NULL,
            address STRING(256) NOT NULL,
            city STRING(64) NOT NULL,
            state STRING(16) NOT NULL,
            lat FLOAT64 NOT NULL,
            lng FLOAT64 NOT NULL,
            pop_id STRING(32) NOT NULL,
            splice_closure_id STRING(32) NOT NULL,
            splice_lat FLOAT64 NOT NULL,
            splice_lng FLOAT64 NOT NULL,
            clinic_type STRING(128) NOT NULL,
            network_status STRING(32) NOT NULL,
            distance_to_splice_m INT64 NOT NULL,
            bandwidth_tier STRING(128) NOT NULL,
            port_readiness STRING(128) NOT NULL,
            estimated_ehr_latency_ms FLOAT64 NOT NULL,
            legacy_wan_latency_ms FLOAT64 NOT NULL,
            sla_compliant BOOL NOT NULL,
            build_capex_usd INT64 NOT NULL,
            construction_method STRING(256) NOT NULL,
            permit_requirement STRING(256) NOT NULL,
            cpe_nid_status STRING(256) NOT NULL,
            monthly_mrc_usd INT64 NOT NULL,
            optical_loss_budget_db FLOAT64 NOT NULL
        ) PRIMARY KEY (site_id)""",
    ]

    if not database.exists():
        print(f"Creating Spanner database {SPANNER_DB_ID}...")
        database = instance.database(SPANNER_DB_ID, ddl_statements=ddl_statements)
        op = database.create()
        op.result(timeout=180)
        print("Created Spanner database and tables.")
    else:
        print(f"Spanner database {SPANNER_DB_ID} already exists.")

    # Upsert rows into all 4 tables
    pop_cols = list(FIBER_POPS[0].keys())
    pop_vals = [[row[c] for c in pop_cols] for row in FIBER_POPS]

    link_cols = ["link_id", "from_pop", "to_pop", "capacity_gbps", "rtd_ms", "route_name"]
    link_vals = [
        [f"LINK-{i+1:02d}", r["from_pop"], r["to_pop"], r["capacity_gbps"], r["rtd_ms"], r["route_name"]]
        for i, r in enumerate(FIBER_BACKBONE_LINKS)
    ]

    splice_cols = list(SPLICE_CLOSURES[0].keys())
    splice_vals = [[row[c] for c in splice_cols] for row in SPLICE_CLOSURES]

    site_cols = list(CLINIC_SITES[0].keys())
    site_vals = [[row[c] for c in site_cols] for row in CLINIC_SITES]

    with database.batch() as batch:
        batch.insert_or_update(table="FiberPoPs", columns=pop_cols, values=pop_vals)
        batch.insert_or_update(table="FiberBackboneLinks", columns=link_cols, values=link_vals)
        batch.insert_or_update(table="SpliceClosures", columns=splice_cols, values=splice_vals)
        batch.insert_or_update(table="ClinicSites", columns=site_cols, values=site_vals)

    print(
        f"Seeded Spanner: {len(pop_vals)} FiberPoPs, {len(link_vals)} FiberBackboneLinks, "
        f"{len(splice_vals)} SpliceClosures, {len(site_vals)} ClinicSites."
    )


def provision_bigquery():
    print(f"=== [2/3] Provisioning BigQuery Dataset ({PROJECT_ID}.{BQ_DATASET_ID}) ===")
    bq_client = bigquery.Client(project=PROJECT_ID)
    dataset_ref = f"{PROJECT_ID}.{BQ_DATASET_ID}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "us-central1"
    bq_client.create_dataset(dataset, exists_ok=True)
    print(f"Dataset {dataset_ref} ready.")

    tables_to_load = {
        "fiber_build_cost_models": FIBER_BUILD_COST_MODELS,
        "product_pricing_catalog": PRODUCT_PRICING_CATALOG,
        "historical_bid_analytics": HISTORICAL_BID_ANALYTICS,
        "compliance_knowledge_base": COMPLIANCE_QUESTIONS,
    }

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )

    for table_name, rows in tables_to_load.items():
        table_id = f"{dataset_ref}.{table_name}"
        job = bq_client.load_table_from_json(rows, table_id, job_config=job_config)
        job.result()
        print(f"Loaded BigQuery table {table_id}: {len(rows)} rows.")


def provision_vertex_ai_search():
    print(f"=== [3/3] Provisioning Vertex AI Search Data Store ({DATA_STORE_ID}) ===")
    ds_client = discoveryengine.DataStoreServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global/collections/default_collection"
    ds_name = f"{parent}/dataStores/{DATA_STORE_ID}"

    try:
        ds = ds_client.get_data_store(name=ds_name)
        print(f"Data Store already exists: {ds.name}")
    except NotFound:
        print(f"Creating Data Store {DATA_STORE_ID}...")
        data_store = discoveryengine.DataStore(
            display_name="Apex Health RFx & Telco Compliance Grounding Store",
            industry_vertical=discoveryengine.IndustryVertical.GENERIC,
            solution_types=[discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH],
            content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED,
        )
        op = ds_client.create_data_store(
            parent=parent,
            data_store=data_store,
            data_store_id=DATA_STORE_ID,
        )
        ds = op.result(timeout=120)
        print(f"Created Data Store: {ds.name}")

    # Upsert rich grounding documents directly via DocumentServiceClient so they are immediately indexed
    doc_client = discoveryengine.DocumentServiceClient()
    branch_parent = f"{ds_name}/branches/default_branch"

    grounding_chunks = [
        {
            "id": "DOC-SEC-HIPAA-V42",
            "title": "Telco_HIPAA_ISO27001_Security_Compliance_Attestation_v4.2.pdf",
            "uri": "gs://rf_response_agent/apex_health_demo_docs/Telco_HIPAA_ISO27001_Security_Compliance_Attestation_v4.2.pdf",
            "content": (
                "Telco HIPAA, HITRUST CSF v11 & ISO/IEC 27001 Security Compliance Attestation v4.2. "
                "Section 1.2: Unconditional HIPAA/HITECH Business Associate Agreement (BAA) execution. "
                "Section 1.4: Active HITRUST CSF v11 r2 and ISO/IEC 27001:2022 certification across all 9 regional PoPs "
                "(POP-SEA-01 Seattle, POP-QCY-01 Quincy, POP-BEL-01 Bellevue, POP-TAC-01 Tacoma, POP-SPO-01 Spokane, "
                "POP-PDX-01 Portland, POP-EUG-01 Eugene, POP-BOI-01 Boise, POP-SAC-01 Sacramento). "
                "Section 2.1: FIPS 140-3 Level 3 validated AES-256-GCM IPsec encryption and IEEE 802.1AE MACsec optical encryption. "
                "Section 3.2: 16 isolated clinical VRFs for Epic EHR, PACS/DICOM imaging, and Tele-ICU. "
                "Section 4.3: FIPS 140-3 Cloud HSM BYOK key management with 60-minute standard IKEv2 re-keying and custom 15-minute option. "
                "Section 7.2: Customer penetration testing allowed with 24-hour SOC safelisting notice."
            ),
        },
        {
            "id": "DOC-ARCH-SDWAN-2026",
            "title": "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf",
            "uri": "gs://rf_response_agent/apex_health_demo_docs/Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf",
            "content": (
                "Enterprise Dual-Transport SD-WAN, 10G Wavelength & Multi-Cloud Reference Architecture (2026). "
                "Section 1.1: Dual-Transport Active/Active SD-WAN with sub-second FEC failover. "
                "Section 2.1: Non-oversubscribed 10Gbps MEF 3.0 Optical Wavelengths on Ciena 5170 and Nokia 7210 SAS NIDs. "
                "Section 2.2: 43 of 45 Apex Health clinics are On-Net lit buildings. 2 sites are Near-Net (<150m): "
                "Site #28 Wenatchee (82m micro-trenching from SC-QCY-028, $1,820 CAPEX) and Site #33 Hood River (118m conduit pull from SC-PDX-033, $2,380 CAPEX). "
                "Total $4,200 CAPEX is completed in 11 business days and amortized over 36 months. "
                "Section 3.4: Hardware-assisted BFD timers (3x 15ms = 45ms) and custom BGP community string tagging (65001:100-450) into Epic EHR VRFs. "
                "Section 4.1 & 4.3: 2x 100Gbps Google Cloud Dedicated Interconnects (Seattle & Portland) and Quincy Epic EHR Direct Wave (0.4ms campus RTD)."
            ),
        },
        {
            "id": "DOC-MSA-SLA-99999",
            "title": "Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf",
            "uri": "gs://rf_response_agent/apex_health_demo_docs/Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf",
            "content": (
                "Master Service Agreement (MSA) - Healthcare 99.999% SLA & <12ms Latency Schedule. "
                "Section 2.1: 99.999% Five-Nines monthly site availability (<26s downtime/month). "
                "Section 3.1: Mandatory <12.0ms Epic EHR round-trip latency guarantee across all 45 clinics (actual 1.5ms to 10.4ms RTD). "
                "15% MRC service credit per 1.0ms above 12.0ms. "
                "Section 3.3: Chronic latency termination right (>18.0ms for 3 consecutive days) with zero ETF. "
                "Section 5.2: Automated TWAMP/Y.1731 telemetry billing credit issuance without manual tickets. "
                "Section 6.4: $5,000,000 HIPAA BAA Cyber Super-Cap (expandable to $10,000,000). "
                "Section 7.1: 36-month Near-Net CAPEX amortization ($4,200 folded into $116.67/month preserving 42.4% Gross Margin) + 5-site portability."
            ),
        },
        {
            "id": "DOC-CASE-STUDY-PNW-2025",
            "title": "Past_Winning_Bid_Pacific_Northwest_Health_Network_2025.pdf",
            "uri": "gs://rf_response_agent/apex_health_demo_docs/Past_Winning_Bid_Pacific_Northwest_Health_Network_2025.pdf",
            "content": (
                "Past Winning Bid Case Study: Pacific Northwest Health Network (38 Sites, $4.62M TCV, 2025). "
                "Section 4.1: Phased 30-day healthcare rollout completing On-Net sites in 14-18 days and Near-Net lateral fiber extensions by Day 26. "
                "Section 4.2: Dedicated PMP Healthcare Program Director and 12 regional optical field engineers. "
                "Section 5.1: Dedicated 24x7x365 US-Based Healthcare NOC pod in Seattle and Denver (<60s answer, 15m P1 isolation). "
                "Section 5.3: Bi-directional ServiceNow Tokyo/Xanadu eBonding deployed within 10 business days."
            ),
        },
        {
            "id": "DOC-APEX-RFP-2026",
            "title": "Apex_Health_RFP_SDWAN_Cloud.pdf",
            "uri": "gs://rf_response_agent/apex_health_demo_docs/Apex_Health_RFP_SDWAN_Cloud.pdf",
            "content": (
                "Apex Health Regional Network RFP #AH-2026-SDWAN-094. "
                "45 clinic sites across WA, OR, ID, and CA requiring low-latency redundant SD-WAN and 10Gbps Optical Wavelengths. "
                "Direct cloud interconnects to Google Cloud (us-west1) and Quincy, WA Epic EHR hosting enclave. "
                "Stringent HIPAA compliance, 99.999% SLA, strict penalty clause on latency exceeding 12.0ms (15% MRC credit per 1ms, termination >18ms). "
                "Near-Net constraints at Site #28 (Wenatchee Valley Specialty Clinic) and Site #33 (Hood River Gorge Medical Center). "
                "200-question vendor security and architecture compliance matrix."
            ),
        },
    ]

    for chunk in grounding_chunks:
        doc = discoveryengine.Document(
            id=chunk["id"],
            json_data=json.dumps(
                {
                    "title": chunk["title"],
                    "uri": chunk["uri"],
                    "category": "Telco Enterprise RFx Grounding",
                }
            ),
            content=discoveryengine.Document.Content(
                mime_type="text/plain",
                raw_bytes=chunk["content"].encode("utf-8"),
            ),
        )
        doc_client.update_document(
            request=discoveryengine.UpdateDocumentRequest(
                document=discoveryengine.Document(
                    name=f"{branch_parent}/documents/{chunk['id']}",
                    json_data=doc.json_data,
                    content=doc.content,
                ),
                allow_missing=True,
            )
        )
    print(f"Upserted {len(grounding_chunks)} indexed grounding documents into {DATA_STORE_ID}.")


if __name__ == "__main__":
    t0 = time.time()
    provision_spanner()
    provision_bigquery()
    provision_vertex_ai_search()
    print(f"All GCP data stores provisioned and seeded in {time.time() - t0:.1f}s!")
