"""Generates realistic multi-page PDF documents for the Apex Health RFP & Vertex AI Search Grounding Store."""

import os
from pathlib import Path
import sys

from fpdf import FPDF

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.dataset import (
    CLINIC_SITES,
    COMPLIANCE_QUESTIONS,
    FIBER_BUILD_COST_MODELS,
    FIBER_POPS,
    PRODUCT_PRICING_CATALOG,
    RFP_METADATA,
)

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"


def _clean_text(text: str) -> str:
    """Sanitize characters for standard Latin-1 PDF core fonts."""
    return (
        text.replace("—", " - ")
        .replace("–", "-")
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("‘", "'")
        .replace("≥", ">=")
        .replace("≤", "<=")
        .replace("•", "*")
    )


class EnterprisePDF(FPDF):
    def __init__(self, doc_title: str, doc_code: str, classification: str = "CONFIDENTIAL - ENTERPRISE PROCUREMENT"):
        super().__init__()
        self.doc_title = _clean_text(doc_title)
        self.doc_code = _clean_text(doc_code)
        self.classification = _clean_text(classification)
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(70, 85, 105)
        self.cell(0, 6, f"{self.doc_code}  |  {self.doc_title}", border=False, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 210, 225)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(200, 210, 225)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 110, 125)
        self.cell(130, 8, self.classification)
        self.cell(60, 8, f"Page {self.page_no()}", align="R")

    def chapter_title(self, title: str):
        self.ln(2)
        self.set_fill_color(15, 35, 66)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, f"  {_clean_text(title)}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        self.set_text_color(20, 25, 35)

    def section_heading(self, heading: str):
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(15, 65, 130)
        self.cell(0, 6, _clean_text(heading), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(25, 30, 40)

    def body_paragraph(self, text: str):
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(30, 35, 45)
        self.multi_cell(0, 5.2, _clean_text(text))
        self.ln(2)


def generate_apex_health_rfp() -> Path:
    pdf = EnterprisePDF(
        doc_title="Apex Health Regional Network - RFP #AH-2026-SDWAN-094",
        doc_code="RFP-AH-2026-SDWAN-094",
        classification="APEX HEALTH PROCUREMENT - MANDATORY VENDOR COMPLIANCE",
    )
    pdf.add_page()

    # Cover / Title Banner
    pdf.set_fill_color(12, 42, 78)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, "  APEX HEALTH REGIONAL NETWORK", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(
        0,
        9,
        "  REQUEST FOR PROPOSAL: ENTERPRISE DUAL-TRANSPORT SD-WAN & 10G OPTICAL WAVE",
        fill=True,
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(4)
    pdf.set_text_color(20, 25, 35)

    pdf.chapter_title("SECTION 1: EXECUTIVE SUMMARY & ARCHITECTURAL MANDATES")
    pdf.body_paragraph(
        "Apex Health Regional Network ('Apex Health'), headquartered at 1201 Third Ave, Seattle, WA, operates "
        "45 clinical, surgical, oncology, and hospital facilities across Washington, Oregon, Idaho, and Northern "
        "California. Apex Health is issuing RFP #AH-2026-SDWAN-094 to select a single Tier-1 Telecommunications "
        "and Managed Network Service Provider for a 36-month contract term."
    )
    pdf.body_paragraph(
        "CRITICAL CLINICAL DRIVER: Apex Health has consolidated all real-time Epic Hyperspace Electronic Health Record "
        "(EHR) transactions, PACS high-resolution DICOM medical imaging, and Tele-ICU robotics into our Primary Data "
        "Center Enclave in Quincy, WA and our Disaster Recovery Cloud Enclave in Google Cloud (us-west1). Legacy "
        "best-effort WAN circuits at rural clinics (specifically Site #28 in Wenatchee, WA and Site #33 in Hood River, OR) "
        "currently suffer 19ms-22ms round-trip latency and intermittent packet loss, degrading clinician workstation "
        "responsiveness."
    )

    pdf.section_heading("1.1 Mandatory Technical & Commercial Requirements Summary")
    bullets = [
        "1. 45-Site Optical & SD-WAN Footprint: Provision dedicated 10Gbps Optical Wavelength primary circuits plus diverse active/active Managed SD-WAN secondary transport across all 45 clinics listed in Schedule A.",
        "2. Multi-Cloud & Epic EHR Core Interconnects: Deliver 2x 100Gbps Redundant Google Cloud Dedicated Interconnects (Seattle & Portland) and direct optical wave peering into the Quincy, WA Epic EHR Primary Enclave.",
        "3. Strict <12.0ms Latency SLA & Penalty Clause: Round-Trip Delay (RTD) between ANY of the 45 clinics and the Primary Epic EHR Data Center MUST NOT exceed 12.0 milliseconds (95th percentile over 5-minute intervals). Exceedances trigger an automatic 15% Monthly Recurring Charge (MRC) credit per 1.0ms over 12.0ms, with immediate termination-for-cause rights above 18.0ms.",
        "4. Five-Nines (99.999%) Site Availability SLA: End-to-end site availability must achieve >=99.999% (<26 seconds unscheduled downtime per month) with <50ms core optical protection switching and <45ms BFD routing failover.",
        "5. Stringent Healthcare Security & HIPAA BAA: Full FIPS 140-3 Level 3 AES-256-GCM encryption, IEEE 802.1AE MACsec optical encryption, HITRUST CSF v11 r2 certification, and unconditional execution of the Apex Health HIPAA/HITECH Business Associate Agreement (BAA).",
        "6. Zero Upfront Construction NRE Preference: Bidders are strongly advised to absorb or amortize any last-mile lateral fiber construction CAPEX (such as Near-Net extensions at Site #28 Wenatchee and Site #33 Hood River) across the 36-month contract term.",
        "7. 200-Question Vendor Security & Architecture Compliance Matrix: Bidders must complete all 200 mandatory compliance items across Security (SEC), Network (NET), Cloud (CLD), SLA, and Operations (OPS).",
    ]
    for b in bullets:
        pdf.body_paragraph(b)

    pdf.chapter_title("SECTION 2: SLA PENALTY SCHEDULE & LIQUIDATED CREDITS")
    pdf.body_paragraph(
        "Section 2.1 - <12.0ms Epic EHR Latency Covenant: Because sub-12ms latency is mandatory for Citrix/Epic Hyperspace "
        "session stability and real-time surgical telemetry, Provider agrees to continuous 1-second TWAMP/Y.1731 synthetic "
        "monitoring from all 45 clinics to POP-QCY-01 (Quincy Epic EHR Gateway) and POP-SEA-01 (Seattle GCP Interconnect). "
        "For every 1.0ms above 12.0ms RTD, Apex Health shall receive a 15% MRC service credit for the affected clinic. "
        "If any clinic exceeds 18.0ms for three (3) consecutive calendar days, Apex Health may terminate the affected circuit "
        "without Early Termination Fees (ETF)."
    )
    pdf.body_paragraph(
        "Section 2.2 - Custom BGP & Sub-Second BFD Routing Requirement (See Question Q-052): Provider must support custom "
        "BGP extended community string tagging (65001:100 through 65001:450) with hardware-assisted BFD timers (3x 15ms = 45ms "
        "detection) and custom AS-path prepending directly into customer-managed Epic EHR VRFs."
    )

    pdf.add_page()
    pdf.chapter_title("SCHEDULE A: MANDATORY 45 CLINIC SITE LOCATIONS & LATENCY TARGETS")
    pdf.body_paragraph(
        "Bidders must validate physical fiber availability, nearest splice closure distance, and projected round-trip "
        "latency to the Epic EHR Enclave for each of the 45 Apex Health facilities below. Note that Site #28 (Wenatchee, WA) "
        "and Site #33 (Hood River, OR) currently lack in-building fiber risers and require lateral outside-plant (OSP) "
        "fiber extensions from nearby utility vaults."
    )

    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(225, 232, 242)
    pdf.cell(14, 6, "Site ID", border=1, fill=True)
    pdf.cell(66, 6, "Facility Name", border=1, fill=True)
    pdf.cell(58, 6, "Street Address, City, State", border=1, fill=True)
    pdf.cell(20, 6, "Nearest PoP", border=1, fill=True)
    pdf.cell(32, 6, "Max EHR Latency", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 7)
    for s in CLINIC_SITES:
        if pdf.get_y() > 265:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_fill_color(225, 232, 242)
            pdf.cell(14, 6, "Site ID", border=1, fill=True)
            pdf.cell(66, 6, "Facility Name", border=1, fill=True)
            pdf.cell(58, 6, "Street Address, City, State", border=1, fill=True)
            pdf.cell(20, 6, "Nearest PoP", border=1, fill=True)
            pdf.cell(32, 6, "Max EHR Latency", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 7)
        highlight = s["site_num"] in (28, 33)
        if highlight:
            pdf.set_fill_color(255, 243, 205)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(14, 5.5, s["site_id"], border=1, fill=True)
        pdf.cell(66, 5.5, _clean_text(s["site_name"][:38]), border=1, fill=True)
        pdf.cell(58, 5.5, _clean_text(s["address"][:34]), border=1, fill=True)
        pdf.cell(20, 5.5, s["pop_id"], border=1, fill=True)
        note = "<12.0ms (Near-Net)" if highlight else "<12.0ms Mandatory"
        pdf.cell(32, 5.5, note, border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.add_page()
    pdf.chapter_title("SCHEDULE B: 200-QUESTION COMPLIANCE MATRIX EXCERPT (KEY MANDATES)")
    pdf.body_paragraph(
        "The complete 200-question compliance matrix is structured across five functional domains: "
        "Security & HIPAA Compliance (Q-001 to Q-045), Network & SD-WAN Architecture (Q-046 to Q-095), "
        "Cloud & Epic EHR Interconnect (Q-096 to Q-135), Service Level Agreements & Penalties (Q-136 to Q-170), "
        "and 24x7 Healthcare NOC & Operations (Q-171 to Q-200). Selected high-priority questions include:"
    )
    for q in COMPLIANCE_QUESTIONS[:35]:
        pdf.section_heading(f"{q['question_id']} [{q['category']} - {q['domain']}]")
        pdf.body_paragraph(q["question_text"])

    out_path = DOCS_DIR / "Apex_Health_RFP_SDWAN_Cloud.pdf"
    pdf.output(str(out_path))
    return out_path


def generate_security_attestation_pdf() -> Path:
    pdf = EnterprisePDF(
        doc_title="Telco HIPAA, HITRUST CSF v11 & ISO/IEC 27001 Security Compliance Attestation v4.2",
        doc_code="SEC-ATTEST-HIPAA-2026-V4.2",
        classification="VERIFIED ENTERPRISE SECURITY & COMPLIANCE REPOSITORY",
    )
    pdf.add_page()
    pdf.chapter_title("SECTION 1: REGULATORY CERTIFICATIONS & HIPAA BAA GOVERNANCE")
    pdf.section_heading("Section 1.2 - HIPAA & HITECH Business Associate Agreement (BAA) Execution")
    pdf.body_paragraph(
        "We unconditionally execute the customer's standard HIPAA/HITECH Omnibus Rule Business Associate Agreement (BAA) "
        "and maintain annual independent third-party HIPAA Security Rule (45 CFR Part 164 Subpart C) and HITECH Subtitle D "
        "compliance audits across all optical transport, SD-WAN orchestration, Cloud Interconnect PoPs, and 24x7 US Healthcare NOC facilities."
    )
    pdf.section_heading("Section 1.4 - HITRUST CSF v11 r2 & ISO/IEC 27001:2022 Certification Scope")
    pdf.body_paragraph(
        "All 9 Pacific Northwest and Western US Regional PoPs (POP-SEA-01 Seattle, POP-QCY-01 Quincy, POP-BEL-01 Bellevue, "
        "POP-TAC-01 Tacoma, POP-SPO-01 Spokane, POP-PDX-01 Portland, POP-EUG-01 Eugene, POP-BOI-01 Boise, and POP-SAC-01 Sacramento) "
        "hold active HITRUST CSF v11 r2 Validated Certifications and ISO/IEC 27001:2022 certificates."
    )
    pdf.section_heading("Section 1.5 - AICPA SOC 2 Type II Continuous Compliance Attestation")
    pdf.body_paragraph(
        "Our latest 12-month AICPA SOC 2 Type II examination report (audited by Deloitte & Touche LLP) covers all five Trust "
        "Services Criteria (Security, Availability, Processing Integrity, Confidentiality, and Privacy) with zero high-severity exceptions."
    )

    pdf.chapter_title("SECTION 2: CRYPTOGRAPHIC STANDARDS & LINE-RATE ENCRYPTION")
    pdf.section_heading("Section 2.1 - FIPS 140-3 Level 3 Line-Rate Encryption (IPsec & Optical MACsec)")
    pdf.body_paragraph(
        "All managed SD-WAN appliances enforce FIPS 140-3 Level 3 validated AES-256-GCM IPsec data-plane encryption with "
        "SHA-512 HMAC authentication and Diffie-Hellman Group 21 (ECDH P-521) Perfect Forward Secrecy. Underlying 10Gbps and "
        "100Gbps optical wavelengths enforce hardware IEEE 802.1AE MACsec 256-bit encryption on Ciena 6500/Waveserver and Nokia 7750 SR interfaces."
    )

    pdf.chapter_title("SECTION 3: ZERO-TRUST CLINICAL VRF MICRO-SEGMENTATION")
    pdf.section_heading("Section 3.2 - Clinical VRF Micro-Segmentation & Medical IoT Isolation")
    pdf.body_paragraph(
        "Each clinic uCPE appliance enforces up to 16 isolated VRF routing instances and stateful Layer-7 zone-based firewalls "
        "that strictly segregate Epic EHR clinical workstations, PACS/DICOM radiology imaging, Tele-ICU robotics, infusion pumps, "
        "and guest Wi-Fi traffic."
    )

    pdf.chapter_title("SECTION 4: KEY MANAGEMENT (BYOK / HYOK) & PENETRATION TESTING")
    pdf.section_heading("Section 4.3 - FIPS 140-3 Key Management, Cloud HSM & Customer BYOK")
    pdf.body_paragraph(
        "Standard enterprise profiles utilize FIPS 140-3 Level 3 Cloud HSM key hierarchies with 60-minute automated IKEv2 "
        "re-keying and Customer-Held Key Encryption Keys (BYOK). Custom 15-minute IKEv2 re-key rotation intervals are supported "
        "via dedicated controller security profiles subject to joint branch CPE CPU benchmark validation."
    )
    pdf.section_heading("Section 7.2 - Customer Red-Team & Vulnerability Testing Protocol")
    pdf.body_paragraph(
        "Customers may conduct annual and ad-hoc gray-box or black-box penetration testing against dedicated customer VRFs and "
        "CPE management enclaves upon providing a 24-hour electronic notification to our Healthcare SOC so automated core DDoS "
        "mitigation scrubbers can safelist the authorized testing source prefixes."
    )

    out_path = DOCS_DIR / "Telco_HIPAA_ISO27001_Security_Compliance_Attestation_v4.2.pdf"
    pdf.output(str(out_path))
    return out_path


def generate_reference_architecture_pdf() -> Path:
    pdf = EnterprisePDF(
        doc_title="Enterprise Dual-Transport SD-WAN, 10G Wavelength & Multi-Cloud Reference Architecture (2026)",
        doc_code="ARCH-SDWAN-OPTICAL-2026",
        classification="VERIFIED NETWORK ENGINEERING REFERENCE ARCHITECTURE",
    )
    pdf.add_page()
    pdf.chapter_title("SECTION 1: DUAL-TRANSPORT ACTIVE/ACTIVE SD-WAN ARCHITECTURE")
    pdf.section_heading("Section 1.1 - Dual-Transport Active/Active SD-WAN with Sub-Second Failover")
    pdf.body_paragraph(
        "Every healthcare clinic is engineered with a Primary 10Gbps Dedicated Optical Wavelength plus a Secondary Diverse "
        "Carrier-Ethernet/Fiber transport terminated on dual-homed SD-WAN edge appliances. Per-packet Forward Error Correction (FEC) "
        "and sub-second synthetic health probes guarantee zero session drops for Citrix/Epic Hyperspace transactions."
    )

    pdf.chapter_title("SECTION 2: 10G OPTICAL WAVELENGTHS & NEAR-NET LATERAL CONSTRUCTION")
    pdf.section_heading("Section 2.1 - Dedicated 10Gbps MEF 3.0 Optical Transport & ITU-T G.652.D Fiber")
    pdf.body_paragraph(
        "All 45 clinics utilize non-oversubscribed 10Gbps MEF 3.0 Carrier Ethernet / OTN wavelengths terminated on Ciena 5170 "
        "or Nokia 7210 SAS-S NIDs with continuous hardware ITU-T Y.1731 / TWAMP-Light optical performance telemetry."
    )
    pdf.section_heading("Section 2.2 - On-Net vs. Near-Net Fast-Track Lateral Construction (<150m)")
    pdf.body_paragraph(
        "Across the 45 Apex Health clinics, 43 locations (95.6%) are lit On-Net buildings with existing single-mode fiber risers "
        "and reserved 10Gbps SFP+ ports. Only two locations require short Near-Net lateral fiber extensions (<150m): "
        "Site #28 (Wenatchee Valley Specialty Clinic, 82m directional micro-trenching from splice closure SC-QCY-028, CAPEX $1,820) "
        "and Site #33 (Hood River Gorge Medical Center, 118m conduit pull from splice closure SC-PDX-033, CAPEX $2,380). Total "
        "civil CAPEX of $4,200 is completed within 11 business days and amortized over 36 months."
    )
    pdf.section_heading("Section 2.3 - SR-MPLS TI-LFA Core Optical Protection (<50ms)")
    pdf.body_paragraph(
        "Our regional DWDM backbone connecting Seattle, Bellevue, Tacoma, Quincy, Spokane, Portland, Eugene, Boise, and Sacramento "
        "runs Segment Routing (SR-MPLS) with Topology-Independent Loop-Free Alternates (TI-LFA) and optical roadm protection switching under 50ms."
    )
    pdf.section_heading("Section 2.4 - Dual-Entry & Diverse Last-Mile Engineering")
    pdf.body_paragraph(
        "Regional medical centers utilize physically diverse north/south or east/west underground conduit building entries separated "
        "by >=25 meters. For Site #28 (Wenatchee) and Site #33 (Hood River), primary underground fiber entries are complemented by "
        "secondary alley vault entries and active 5G/LEO backup."
    )

    pdf.chapter_title("SECTION 3: HEALTHCARE QoS, BFD TIMERS & CUSTOM BGP ROUTING")
    pdf.section_heading("Section 3.1 - Healthcare Hierarchical QoS (H-QoS) Traffic Engineering")
    pdf.body_paragraph(
        "Hardware H-QoS allocates 40% strict low-latency priority queuing (DSCP EF/CS5) for Epic EHR and Tele-ICU real-time streams, "
        "35% assured forwarding (AF41) for PACS/DICOM medical imaging, and 25% for enterprise clinical applications."
    )
    pdf.section_heading("Section 3.3 - High-Availability Dual-CPE Branch Design")
    pdf.body_paragraph(
        "All hospitals, tertiary surgical centers, and Near-Net regional hubs include dual redundant SD-WAN appliances in active/active "
        "stateful HA with dual power supplies and 8-hour battery backup."
    )
    pdf.section_heading("Section 3.4 - Hardware-Assisted BFD (<45ms) & Custom BGP Community Tagging")
    pdf.body_paragraph(
        "Nokia 7750 SR PoP border routers and branch SD-WAN appliances natively support hardware-assisted BFD echo timers down to "
        "15ms intervals (3x 15ms = 45ms detection), custom AS-path prepending, and transparent pass-through of customer BGP extended "
        "community strings (65001:100 through 65001:450) directly into Epic EHR VRFs."
    )

    pdf.chapter_title("SECTION 4: GOOGLE CLOUD INTERCONNECT & QUINCY EPIC EHR PEERING")
    pdf.section_heading("Section 4.1 - Redundant 100Gbps Google Cloud Dedicated Interconnect (us-west1)")
    pdf.body_paragraph(
        "We provision 2x 100Gbps Google Cloud Dedicated Interconnect connections across POP-SEA-01 (Seattle Westin) and POP-PDX-01 "
        "(Portland Pittock) with physically diverse optical paths into Google Cloud us-west1, meeting GCP's 99.99% Interconnect SLA."
    )
    pdf.section_heading("Section 4.2 - Cloud Interconnect MTU (8,896 Bytes) & Direct Multi-Cloud Routing")
    pdf.body_paragraph(
        "All 10Gbps optical wavelengths support 9,216-byte Jumbo Frames end-to-end, while Google Cloud Dedicated Interconnect VLAN "
        "attachments operate at GCP's maximum 8,896-byte hardware MTU with automatic MSS clamping."
    )
    pdf.section_heading("Section 4.3 - Quincy Epic EHR Direct Optical Enclave (0.4ms Campus Latency)")
    pdf.body_paragraph(
        "POP-QCY-01 in Quincy, WA sits within 400 meters of the Primary Epic EHR hosting enclave, delivering 0.4ms intra-campus latency "
        "and enabling all 45 clinics across WA, OR, ID, and CA to achieve 1.5ms to 10.4ms RTD (well below the 12.0ms SLA mandate)."
    )
    pdf.section_heading("Section 4.4 & 4.5 - Synthetic Epic Hyperspace Probes & RPKI Route Security")
    pdf.body_paragraph(
        "Synthetic HTTPS/ICA probes execute every 250ms against Epic Hyperspace VIPs, triggering automatic BGP local-preference failover "
        "to Google Cloud us-west1 DR in <750ms. All BGP sessions enforce RPKI origin validation and TCP-AO authentication."
    )
    pdf.section_heading("Section 5.1 - uCPE Virtual Network Function (VNF) Hosting Specifications")
    pdf.body_paragraph(
        "Branch uCPE-Pro appliances include dedicated KVM/Docker compute blades (up to 8 vCPUs, 32GB ECC RAM, 512GB NVMe) capable of "
        "hosting customer-managed clinical IoT packet brokers (4 vCPU / 16GB RAM) at zero additional MRC on a 36-month term."
    )

    out_path = DOCS_DIR / "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf"
    pdf.output(str(out_path))
    return out_path


def generate_msa_sla_pdf() -> Path:
    pdf = EnterprisePDF(
        doc_title="Master Service Agreement (MSA) - Healthcare 99.999% SLA & <12ms Latency Schedule",
        doc_code="LEGAL-MSA-SLA-99999-2026",
        classification="COMMERCIAL & LEGAL SLA SCHEDULE",
    )
    pdf.add_page()
    pdf.chapter_title("SECTION 2: FIVE-NINES (99.999%) AVAILABILITY COMMITMENT")
    pdf.section_heading("Section 2.1 - 99.999% End-to-End Site Availability Guarantee")
    pdf.body_paragraph(
        "Provider contractually guarantees 99.999% monthly end-to-end availability (<26 seconds of unscheduled outage per calendar month) "
        "for all dual-transport SD-WAN + 10Gbps Optical Wavelength clinic locations."
    )

    pdf.chapter_title("SECTION 3: HEALTHCARE <12.0ms LATENCY GUARANTEE & PENALTY SCHEDULE")
    pdf.section_heading("Section 3.1 - Mandatory <12.0ms Epic EHR Round-Trip Latency SLA & 15% Credit Tier")
    pdf.body_paragraph(
        "Provider guarantees that 5-minute 95th-percentile round-trip latency from each of the 45 Apex Health clinics to the Primary "
        "Epic EHR Enclave (POP-QCY-01) shall remain strictly below 12.0ms. Based on Cloud Spanner live optical path telemetry, all 45 "
        "clinics operate between 1.5ms and 10.4ms (including Site #28 Wenatchee at 4.6ms and Site #33 Hood River at 6.8ms post-fiber build). "
        "For every 1.0ms above 12.0ms, Customer receives an automatic 15% MRC service credit for the affected site up to 100% of monthly charges."
    )
    pdf.section_heading("Section 3.2 - Jitter (<=1.5ms) and Packet Delivery (>=99.99%) Guarantees")
    pdf.body_paragraph(
        "Provider guarantees inter-packet jitter <=1.5ms and packet loss <0.01% across all EF and AF41 clinical traffic classes."
    )
    pdf.section_heading("Section 3.3 - Chronic Latency Termination Right (>18.0ms for 3 Consecutive Days)")
    pdf.body_paragraph(
        "If any clinic experiences round-trip latency exceeding 18.0ms for three (3) consecutive calendar days (excluding customer-induced "
        "LAN overload or municipal civil force-majeure cuts where diverse backup transport remains <15.0ms), Customer may terminate the "
        "affected site circuit for cause with zero Early Termination Fee (ETF)."
    )

    pdf.chapter_title("SECTION 4 & 5: OPTICAL MTTR & AUTOMATED TELEMETRY BILLING CREDITS")
    pdf.section_heading("Section 4.1 - <50ms Core Protection & 4-Hour Physical Fiber Cut MTTR")
    pdf.body_paragraph(
        "Core DWDM ring protection switches in <50ms. Physical last-mile fiber cuts carry a guaranteed <2-hour technician dispatch "
        "and <4-hour physical splice restoral SLA."
    )
    pdf.section_heading("Section 5.2 - Zero-Touch Automated SLA Credit Issuance")
    pdf.body_paragraph(
        "TWAMP/Y.1731 telemetry streams directly into our BigQuery SLA accounting engine and automatically posts earned service credits "
        "to the next monthly EDI 810 invoice without requiring Customer to open a manual credit claim ticket."
    )

    pdf.chapter_title("SECTION 6 & 7: CYBER SUPER-CAP, CAPEX AMORTIZATION & PORTABILITY")
    pdf.section_heading("Section 6.4 - HIPAA BAA Cyber & Regulatory Liability Super-Cap")
    pdf.body_paragraph(
        "Our standard Healthcare BAA includes a $5,000,000 Cyber & HIPAA Regulatory Super-Cap (3x standard enterprise cap), with "
        "executive underwriting available up to $10,000,000 for Tier-1 multi-hospital networks."
    )
    pdf.section_heading("Section 7.1 - 36-Month Near-Net CAPEX Amortization & 5-Site Portability Flex Clause")
    pdf.body_paragraph(
        "Near-Net lateral fiber construction CAPEX up to $15,000 (including the $4,200 total for Apex Health Sites #28 and #33) is "
        "100% waived upfront and folded into the 36-month contract amortization schedule ($116.67/month total), preserving a 42.4% "
        "deal gross margin. Furthermore, Customer may relocate or decommission up to 5 On-Net clinic circuits after Day 180 with zero ETF."
    )

    out_path = DOCS_DIR / "Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf"
    pdf.output(str(out_path))
    return out_path


def generate_past_winning_bid_pdf() -> Path:
    pdf = EnterprisePDF(
        doc_title="Past Winning Bid Case Study: Pacific Northwest Health Network (38 Sites, $4.62M TCV)",
        doc_code="CASE-STUDY-PNW-HEALTH-2025",
        classification="COMMERCIAL BENCHMARK & OPERATIONS PLAYBOOK",
    )
    pdf.add_page()
    pdf.chapter_title("SECTION 1-3: EXECUTIVE BENCHMARK - PACIFIC NORTHWEST HEALTH NETWORK (2025)")
    pdf.body_paragraph(
        "In Q3 2025, we won and deployed a 38-site Dual-Transport SD-WAN, 10Gbps Wavelength, and 100Gbps Google Cloud / Epic EHR "
        "Interconnect contract ($4.62M TCV) for Pacific Northwest Health Network across WA, OR, and ID. By waiving $6,800 in Near-Net "
        "lateral fiber CAPEX via a 36-month amortization schedule, we preserved a 41.8% gross margin and beat incumbent bidders who "
        "charged upfront construction NRE."
    )

    pdf.chapter_title("SECTION 4: ACCELERATED 30-DAY HEALTHCARE ROLLOUT METHODOLOGY")
    pdf.section_heading("Section 4.1 - Phased 30-Day Turn-Up Schedule (On-Net & Near-Net Parallel Execution)")
    pdf.body_paragraph(
        "Wave 1 (Days 1-14): Turn up 100Gbps Google Cloud Dedicated Interconnects, Quincy Epic EHR Direct Waves, and first 25 On-Net "
        "lit buildings. Wave 2 (Days 15-21): Turn up remaining 18 On-Net clinics and complete directional micro-trenching / conduit pulls "
        "for Near-Net clinics (Sites #28 Wenatchee and #33 Hood River). Wave 3 (Days 22-26): Complete optical splicing, burn-in testing, "
        "and hitless production cutover of Near-Net sites - finishing 4 days ahead of the 30-day customer mandate."
    )
    pdf.section_heading("Section 4.2 - Dedicated PMP Healthcare Program Director & Regional Field Teams")
    pdf.body_paragraph(
        "Every healthcare deployment is led by a dedicated PMP-certified Healthcare Program Director, two Principal Solutions Architects, "
        "and 12 regional field optical engineers staged in Seattle, Quincy, Spokane, Portland, Eugene, and Boise."
    )

    pdf.chapter_title("SECTION 5: 24x7 US HEALTHCARE NOC & SERVICENOW EBONDING")
    pdf.section_heading("Section 5.1 - Dedicated 24x7x365 US-Based Healthcare NOC Pod")
    pdf.body_paragraph(
        "All Tier-1 through Tier-3 operational support is delivered from our US-based Healthcare NOC pods in Seattle, WA and Denver, CO "
        "by HIPAA-certified engineers with <60-second live answer and 15-minute P1 automated root-cause isolation."
    )
    pdf.section_heading("Section 5.2 - Real-Time Telemetry Streaming & BigQuery Analytics Portal")
    pdf.body_paragraph(
        "Customers receive live streaming access to per-clinic TWAMP latency, jitter, packet loss, optical dBm power levels, and BGP "
        "route state via our Agentic Telemetry Portal and REST/GraphQL APIs."
    )
    pdf.section_heading("Section 5.3 - ServiceNow Bi-Directional eBonding Integration (10-Day Turn-Up)")
    pdf.body_paragraph(
        "Our pre-built ServiceNow Tokyo/Xanadu Healthcare Connector maps circuit alarms directly to Epic EHR clinical criticality tiers "
        "and deploys into Customer's ServiceNow production instance within 10 business days of contract award."
    )
    pdf.section_heading("Section 5.4 - Hitless ISSU & Maintenance Window Governance (01:00-04:00 PT)")
    pdf.body_paragraph(
        "All planned maintenance is restricted to Tuesday/Thursday 01:00-04:00 PT windows with 14-day advance ServiceNow change notices "
        "and hitless In-Service Software Upgrades (ISSU)."
    )

    out_path = DOCS_DIR / "Past_Winning_Bid_Pacific_Northwest_Health_Network_2025.pdf"
    pdf.output(str(out_path))
    return out_path


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    generated = [
        generate_apex_health_rfp(),
        generate_security_attestation_pdf(),
        generate_reference_architecture_pdf(),
        generate_msa_sla_pdf(),
        generate_past_winning_bid_pdf(),
    ]
    for path in generated:
        print(f"Generated PDF: {path.name} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
