"""Canonical realistic dataset for the Telco B2B AI Sales Agent Demo (Apex Health RFP).

Used to seed Cloud Spanner, BigQuery, and Vertex AI Search PDFs, and as a fast
fallback/validation reference.
"""

from typing import Any

RFP_METADATA: dict[str, Any] = {
    "rfp_id": "RFP-AH-2026-SDWAN-094",
    "customer_name": "Apex Health Regional Network",
    "customer_hq": "1201 Third Ave, Suite 2800, Seattle, WA 98101",
    "title": "Enterprise Managed Dual-Transport SD-WAN, 10G Optical Wavelength & Multi-Cloud Interconnect",
    "issue_date": "October 10, 2026",
    "submission_deadline": "October 24, 2026",
    "contract_term_months": 36,
    "total_sites": 45,
    "on_net_sites": 43,
    "near_net_sites": 2,
    "total_questions": 200,
    "auto_answered_questions": 185,
    "human_review_questions": 15,
    "deal_score": 92,
    "deal_fit_label": "High Fit (Tier-1 Strategic Healthcare Pursuit)",
    "sla_availability_target": "99.999%",
    "max_ehr_latency_ms": 12.0,
    "near_net_capex_total_usd": 4200,
    "monthly_recurring_revenue_usd": 148500,
    "total_contract_value_usd": 5346000,
    "protected_gross_margin_pct": 42.4,
    "unamortized_upfront_margin_pct": 42.3,
    "estimated_win_probability_pct": 89.0,
    "traditional_turnaround_days": 21,
    "agentic_turnaround_minutes": 11,
}

# 9 Regional Optical PoPs & Cloud Interconnect Hubs
FIBER_POPS: list[dict[str, Any]] = [
    {
        "pop_id": "POP-SEA-01",
        "pop_name": "Seattle Westin Core & Google Cloud Interconnect",
        "city": "Seattle",
        "state": "WA",
        "address": "2001 Sixth Ave, Seattle, WA 98121",
        "lat": 47.6148,
        "lng": -122.3385,
        "pop_tier": "Tier-1 Core / Cloud Interconnect",
        "router_platform": "Nokia 7750 SR-14s / Ciena 6500",
        "total_10g_ports": 256,
        "available_10g_ports": 68,
        "total_100g_ports": 64,
        "available_100g_ports": 18,
        "cloud_onramp": "Google Cloud Dedicated Interconnect (us-west1 / Seattle Edge)",
        "current_utilization_pct": 61.4,
        "base_ehr_latency_ms": 1.8,
    },
    {
        "pop_id": "POP-QCY-01",
        "pop_name": "Quincy Epic EHR Primary Data Center Gateway",
        "city": "Quincy",
        "state": "WA",
        "address": "525 D St NW, Quincy, WA 98848",
        "lat": 47.2343,
        "lng": -119.8525,
        "pop_tier": "Tier-1 Healthcare EHR Enclave Hub",
        "router_platform": "Cisco ASR 9910 / Ciena Waveserver 5",
        "total_10g_ports": 192,
        "available_10g_ports": 54,
        "total_100g_ports": 48,
        "available_100g_ports": 16,
        "cloud_onramp": "Epic EHR Primary Hosting Enclave + Azure ExpressRoute",
        "current_utilization_pct": 57.2,
        "base_ehr_latency_ms": 0.4,
    },
    {
        "pop_id": "POP-BEL-01",
        "pop_name": "Bellevue Eastside Metro Optical Hub",
        "city": "Bellevue",
        "state": "WA",
        "address": "10900 NE 8th St, Bellevue, WA 98004",
        "lat": 47.6175,
        "lng": -122.1950,
        "pop_tier": "Tier-2 Metro Aggregation",
        "router_platform": "Nokia 7750 SR-7s",
        "total_10g_ports": 128,
        "available_10g_ports": 41,
        "total_100g_ports": 32,
        "available_100g_ports": 11,
        "cloud_onramp": "Eastside Metro DWDM Ring to POP-SEA-01",
        "current_utilization_pct": 63.8,
        "base_ehr_latency_ms": 2.3,
    },
    {
        "pop_id": "POP-TAC-01",
        "pop_name": "Tacoma South Sound Regional PoP",
        "city": "Tacoma",
        "state": "WA",
        "address": "1102 A St, Tacoma, WA 98402",
        "lat": 47.2529,
        "lng": -122.4443,
        "pop_tier": "Tier-2 Metro Aggregation",
        "router_platform": "Nokia 7750 SR-7s",
        "total_10g_ports": 128,
        "available_10g_ports": 39,
        "total_100g_ports": 32,
        "available_100g_ports": 12,
        "cloud_onramp": "I-5 Corridor DWDM Express to POP-SEA-01",
        "current_utilization_pct": 59.0,
        "base_ehr_latency_ms": 3.1,
    },
    {
        "pop_id": "POP-SPO-01",
        "pop_name": "Spokane Inland Northwest Core PoP",
        "city": "Spokane",
        "state": "WA",
        "address": "501 W Second Ave, Spokane, WA 99201",
        "lat": 47.6572,
        "lng": -117.4198,
        "pop_tier": "Tier-2 Regional Core",
        "router_platform": "Cisco ASR 9906 / Ciena 6500",
        "total_10g_ports": 144,
        "available_10g_ports": 46,
        "total_100g_ports": 32,
        "available_100g_ports": 14,
        "cloud_onramp": "I-90 Low-Latency Optical Wave to POP-QCY-01",
        "current_utilization_pct": 52.5,
        "base_ehr_latency_ms": 3.4,
    },
    {
        "pop_id": "POP-PDX-01",
        "pop_name": "Portland Pittock Core & Cloud Interconnect",
        "city": "Portland",
        "state": "OR",
        "address": "921 SW Washington St, Portland, OR 97205",
        "lat": 45.5222,
        "lng": -122.6811,
        "pop_tier": "Tier-1 Core / Cloud Interconnect",
        "router_platform": "Nokia 7750 SR-14s / Ciena 6500",
        "total_10g_ports": 256,
        "available_10g_ports": 74,
        "total_100g_ports": 64,
        "available_100g_ports": 22,
        "cloud_onramp": "Google Cloud Dedicated Interconnect (us-west1 The Dalles)",
        "current_utilization_pct": 64.1,
        "base_ehr_latency_ms": 4.5,
    },
    {
        "pop_id": "POP-EUG-01",
        "pop_name": "Eugene Willamette Valley Optical PoP",
        "city": "Eugene",
        "state": "OR",
        "address": "100 E Broadway, Eugene, OR 97401",
        "lat": 44.0505,
        "lng": -123.0911,
        "pop_tier": "Tier-2 Regional Aggregation",
        "router_platform": "Nokia 7750 SR-7s",
        "total_10g_ports": 96,
        "available_10g_ports": 34,
        "total_100g_ports": 24,
        "available_100g_ports": 9,
        "cloud_onramp": "Willamette Express DWDM Ring to POP-PDX-01",
        "current_utilization_pct": 49.8,
        "base_ehr_latency_ms": 6.4,
    },
    {
        "pop_id": "POP-BOI-01",
        "pop_name": "Boise Treasure Valley Regional PoP",
        "city": "Boise",
        "state": "ID",
        "address": "350 N 9th St, Boise, ID 83702",
        "lat": 43.6188,
        "lng": -116.2054,
        "pop_tier": "Tier-2 Regional Core",
        "router_platform": "Cisco ASR 9906 / Ciena 6500",
        "total_10g_ports": 96,
        "available_10g_ports": 31,
        "total_100g_ports": 24,
        "available_100g_ports": 10,
        "cloud_onramp": "I-84 Direct Optical Express to The Dalles & Quincy",
        "current_utilization_pct": 51.3,
        "base_ehr_latency_ms": 7.6,
    },
    {
        "pop_id": "POP-SAC-01",
        "pop_name": "Sacramento Northern California Optical Hub",
        "city": "Sacramento",
        "state": "CA",
        "address": "620 12th St, Sacramento, CA 95814",
        "lat": 38.5835,
        "lng": -121.4882,
        "pop_tier": "Tier-2 Regional Core",
        "router_platform": "Nokia 7750 SR-12 / Ciena 6500",
        "total_10g_ports": 128,
        "available_10g_ports": 44,
        "total_100g_ports": 32,
        "available_100g_ports": 13,
        "cloud_onramp": "I-5 Long-Haul Ultra-Low-Loss SMF to POP-EUG-01 & POP-PDX-01",
        "current_utilization_pct": 55.9,
        "base_ehr_latency_ms": 9.8,
    },
]

# Backbone DWDM optical trunks connecting the 9 PoPs
FIBER_BACKBONE_LINKS: list[dict[str, Any]] = [
    {"from_pop": "POP-SEA-01", "to_pop": "POP-BEL-01", "capacity_gbps": 800, "rtd_ms": 0.5, "route_name": "I-90 Lake Washington DWDM Ring"},
    {"from_pop": "POP-BEL-01", "to_pop": "POP-QCY-01", "capacity_gbps": 800, "rtd_ms": 1.9, "route_name": "Cascades Ultra-Low-Latency Express"},
    {"from_pop": "POP-SEA-01", "to_pop": "POP-TAC-01", "capacity_gbps": 800, "rtd_ms": 0.8, "route_name": "Puget Sound West Optical Trunk"},
    {"from_pop": "POP-TAC-01", "to_pop": "POP-PDX-01", "capacity_gbps": 1600, "rtd_ms": 2.4, "route_name": "I-5 Pacific Northwest Core Express"},
    {"from_pop": "POP-QCY-01", "to_pop": "POP-SPO-01", "capacity_gbps": 800, "rtd_ms": 2.2, "route_name": "Columbia Basin East DWDM Trunk"},
    {"from_pop": "POP-QCY-01", "to_pop": "POP-PDX-01", "capacity_gbps": 1200, "rtd_ms": 3.1, "route_name": "Columbia River Gorge Optical Express"},
    {"from_pop": "POP-PDX-01", "to_pop": "POP-EUG-01", "capacity_gbps": 800, "rtd_ms": 1.9, "route_name": "Willamette Valley Optical Ring"},
    {"from_pop": "POP-PDX-01", "to_pop": "POP-BOI-01", "capacity_gbps": 800, "rtd_ms": 4.2, "route_name": "Blue Mountains Long-Haul Express"},
    {"from_pop": "POP-SPO-01", "to_pop": "POP-BOI-01", "capacity_gbps": 400, "rtd_ms": 4.6, "route_name": "Inland Empire Diverse Path"},
    {"from_pop": "POP-EUG-01", "to_pop": "POP-SAC-01", "capacity_gbps": 800, "rtd_ms": 3.9, "route_name": "Shasta Cascade Ultra-Low-Loss SMF"},
]

# Raw definitions for the 45 Apex Health clinic sites
_RAW_SITES: list[tuple[int, str, str, str, str, float, float, str, str, int, float, float]] = [
    # (site_num, name, address, city, state, lat, lng, pop_id, clinic_type, dist_m, latency_ms, legacy_latency_ms)
    (1, "Apex Health First Hill Flagship Medical Center", "747 Broadway, Seattle, WA 98122", "Seattle", "WA", 47.6088, -122.3215, "POP-SEA-01", "Tertiary Hospital & Trauma Center", 0, 2.1, 8.4),
    (2, "Apex Health South Lake Union Genomics & Oncology Clinic", "820 Yale Ave N, Seattle, WA 98109", "Seattle", "WA", 47.6269, -122.3303, "POP-SEA-01", "Specialty Oncology Center", 4, 2.2, 9.1),
    (3, "Apex Health Ballard Primary & Urgent Care", "1801 NW Market St, Seattle, WA 98107", "Seattle", "WA", 47.6685, -122.3802, "POP-SEA-01", "Urgent & Primary Care", 8, 2.5, 11.2),
    (4, "Apex Health Northgate Diagnostic Imaging Center", "10330 Meridian Ave N, Seattle, WA 98133", "Seattle", "WA", 47.7042, -122.3336, "POP-SEA-01", "Diagnostic Imaging & Radiology", 6, 2.6, 12.8),
    (5, "Apex Health West Seattle Family Medicine", "4744 Alaska Ave SW, Seattle, WA 98116", "Seattle", "WA", 47.5608, -122.3867, "POP-SEA-01", "Outpatient Clinic", 9, 2.7, 11.5),
    (6, "Apex Health Renton Valley Regional Hospital", "400 S 43rd St, Renton, WA 98055", "Renton", "WA", 47.4418, -122.2121, "POP-SEA-01", "Regional Medical Center", 5, 2.9, 10.6),
    (7, "Apex Health Bellevue Overlake Heart & Vascular Institute", "1135 116th Ave NE, Bellevue, WA 98004", "Bellevue", "WA", 47.6203, -122.1868, "POP-BEL-01", "Cardiovascular Specialty", 3, 2.6, 9.4),
    (8, "Apex Health Redmond Technology Campus Clinic", "16315 NE 74th St, Redmond, WA 98052", "Redmond", "WA", 47.6708, -122.1225, "POP-BEL-01", "Outpatient & Telehealth Hub", 7, 2.8, 10.9),
    (9, "Apex Health Kirkland Totem Lake Medical Pavilion", "12039 NE 128th St, Kirkland, WA 98034", "Kirkland", "WA", 47.7145, -122.1802, "POP-BEL-01", "Multi-Specialty Pavilion", 11, 2.9, 11.8),
    (10, "Apex Health Issaquah Highlands Surgical Center", "751 NE Blakely Dr, Issaquah, WA 98029", "Issaquah", "WA", 47.5416, -122.0189, "POP-BEL-01", "Ambulatory Surgery Center", 9, 2.5, 11.1),
    (11, "Apex Health Everett Providence Corridor Clinic", "1321 Colby Ave, Everett, WA 98201", "Everett", "WA", 47.9975, -122.2044, "POP-SEA-01", "Regional Specialty Clinic", 12, 3.4, 13.5),
    (12, "Apex Health Lynnwood Alderwood Pediatrics & Primary Care", "3500 188th St SW, Lynnwood, WA 98037", "Lynnwood", "WA", 47.8279, -122.2816, "POP-SEA-01", "Pediatrics & Family Care", 10, 3.1, 11.9),
    (13, "Apex Health Tacoma Commencement Bay Medical Center", "1608 S J St, Tacoma, WA 98405", "Tacoma", "WA", 47.2464, -122.4521, "POP-TAC-01", "Regional Hospital", 4, 3.4, 10.8),
    (14, "Apex Health Federal Way Commons Clinic", "34500 11th Ave S, Federal Way, WA 98003", "Federal Way", "WA", 47.2921, -122.3192, "POP-TAC-01", "Outpatient Clinic", 8, 3.5, 12.1),
    (15, "Apex Health Puyallup South Hill Specialty Center", "1515 3rd St SE, Puyallup, WA 98372", "Puyallup", "WA", 47.1764, -122.2901, "POP-TAC-01", "Multi-Specialty Clinic", 11, 3.7, 13.0),
    (16, "Apex Health Olympia Capitol Medical Pavilion", "3900 Capital Mall Dr SW, Olympia, WA 98502", "Olympia", "WA", 47.0419, -122.9428, "POP-TAC-01", "Regional Medical Pavilion", 14, 4.1, 14.2),
    (17, "Apex Health Bremerton Kitsap Peninsula Clinic", "2525 Cherry Ave, Bremerton, WA 98310", "Bremerton", "WA", 47.5835, -122.6288, "POP-SEA-01", "Outpatient & Imaging Clinic", 15, 3.8, 14.9),
    (18, "Apex Health Bellingham Mount Baker Medical Center", "2901 Squalicum Pkwy, Bellingham, WA 98225", "Bellingham", "WA", 48.7768, -122.4632, "POP-SEA-01", "Regional Medical Center", 12, 4.6, 15.6),
    (19, "Apex Health Mount Vernon Skagit Valley Clinic", "1415 E Kincaid St, Mount Vernon, WA 98274", "Mount Vernon", "WA", 48.4162, -122.3245, "POP-SEA-01", "Primary & Urgent Care", 9, 4.1, 13.9),
    (20, "Apex Health Vancouver Columbia River Medical Campus", "400 NE Mother Joseph Pl, Vancouver, WA 98664", "Vancouver", "WA", 45.6227, -122.6134, "POP-PDX-01", "Regional Hospital", 6, 4.8, 11.7),
    (21, "Apex Health Spokane Sacred Heart Corridor Clinic", "101 W 8th Ave, Spokane, WA 99204", "Spokane", "WA", 47.6486, -117.4132, "POP-SPO-01", "Regional Medical Center", 3, 3.7, 11.4),
    (22, "Apex Health Spokane Valley Veradale Specialty Center", "12410 E Sinto Ave, Spokane Valley, WA 99216", "Spokane Valley", "WA", 47.6648, -117.2384, "POP-SPO-01", "Specialty & Surgical Clinic", 9, 3.9, 12.6),
    (23, "Apex Health Coeur d'Alene Lake City Clinic", "2003 Kootenai Health Way, Coeur d'Alene, ID 83814", "Coeur d'Alene", "ID", 47.6968, -116.7982, "POP-SPO-01", "Regional Outpatient Center", 14, 4.4, 14.8),
    (24, "Apex Health Richland Tri-Cities Oncology & Imaging", "1100 Goethals Dr, Richland, WA 99352", "Richland", "WA", 46.2804, -119.2842, "POP-QCY-01", "Oncology & Radiology", 11, 2.9, 13.2),
    (25, "Apex Health Kennewick Columbia Center Clinic", "7201 W Grandridge Blvd, Kennewick, WA 99336", "Kennewick", "WA", 46.2185, -119.2218, "POP-QCY-01", "Outpatient & Urgent Care", 8, 3.1, 13.7),
    (26, "Apex Health Yakima Valley Memorial Clinic", "2811 Tieton Dr, Yakima, WA 98902", "Yakima", "WA", 46.5924, -120.5478, "POP-QCY-01", "Regional Specialty Clinic", 13, 2.6, 12.9),
    (27, "Apex Health Moses Lake Basin Family Medicine", "801 E Wheeler Rd, Moses Lake, WA 98837", "Moses Lake", "WA", 47.1258, -119.2614, "POP-QCY-01", "Primary Care & Telehealth", 7, 1.5, 11.0),
    # SITE #28: NEAR-NET (<150m from splice closure SC-QCY-028, 82m lateral extension required)
    (28, "Apex Health Wenatchee Valley Specialty Clinic", "820 N Chelan Ave, Wenatchee, WA 98801", "Wenatchee", "WA", 47.4352, -120.3204, "POP-QCY-01", "Rural Specialty & Tele-ICU Hub", 82, 4.6, 19.4),
    (29, "Apex Health Walla Walla Blue Mountain Clinic", "401 W Poplar St, Walla Walla, WA 99362", "Walla Walla", "WA", 46.0646, -118.3430, "POP-QCY-01", "Outpatient Clinic", 14, 3.8, 14.5),
    (30, "Apex Health Portland Pearl District Medical Tower", "1130 NW 22nd Ave, Portland, OR 97210", "Portland", "OR", 45.5311, -122.6965, "POP-PDX-01", "Tertiary Specialty Tower", 4, 4.7, 10.2),
    (31, "Apex Health Portland South Waterfront Genomics Center", "3303 SW Bond Ave, Portland, OR 97239", "Portland", "OR", 45.4989, -122.6712, "POP-PDX-01", "Genomics & Clinical Trials", 6, 4.8, 10.5),
    (32, "Apex Health Beaverton Sunset Corridor Clinic", "15950 SW Millikan Way, Beaverton, OR 97006", "Beaverton", "OR", 45.4975, -122.8412, "POP-PDX-01", "Multi-Specialty Clinic", 10, 5.1, 11.8),
    # SITE #33: NEAR-NET (<150m from splice closure SC-PDX-033, 118m lateral extension required)
    (33, "Apex Health Hood River Gorge Medical Center", "1125 May St, Hood River, OR 97031", "Hood River", "OR", 45.7068, -121.5241, "POP-PDX-01", "Regional Rural Medical Center", 118, 6.8, 22.1),
    (34, "Apex Health Hillsboro Silicon Forest Medical Pavilion", "10670 NE Cornell Rd, Hillsboro, OR 97124", "Hillsboro", "OR", 45.5339, -122.8758, "POP-PDX-01", "Ambulatory Surgery & Imaging", 9, 5.2, 12.0),
    (35, "Apex Health Gresham Mount Hood Regional Clinic", "24800 SE Stark St, Gresham, OR 97030", "Gresham", "OR", 45.5182, -122.4084, "POP-PDX-01", "Regional Medical Clinic", 11, 5.0, 12.3),
    (36, "Apex Health Salem Capitol Heart & Orthopedic Center", "890 Oak St SE, Salem, OR 97301", "Salem", "OR", 44.9332, -123.0289, "POP-PDX-01", "Cardiology & Orthopedics", 12, 5.7, 13.4),
    (37, "Apex Health Corvallis Willamette Research Clinic", "3600 NW Samaritan Dr, Corvallis, OR 97330", "Corvallis", "OR", 44.6024, -123.2535, "POP-EUG-01", "Clinical Research & Primary Care", 13, 6.9, 14.7),
    (38, "Apex Health Eugene RiverBend Specialty Pavilion", "3333 RiverBend Dr, Springfield, OR 97477", "Eugene", "OR", 44.0811, -123.0275, "POP-EUG-01", "Regional Specialty Center", 5, 6.7, 13.8),
    (39, "Apex Health Bend Cascade High Desert Medical Center", "2500 NE Neff Rd, Bend, OR 97701", "Bend", "OR", 44.0672, -121.2665, "POP-EUG-01", "Regional Medical Center", 15, 7.9, 16.4),
    (40, "Apex Health Medford Rogue Valley Oncology & Surgery", "2825 E Barnett Rd, Medford, OR 97504", "Medford", "OR", 42.3168, -122.8312, "POP-EUG-01", "Oncology & Surgery Center", 16, 8.8, 17.9),
    (41, "Apex Health Boise St. Luke's Plaza Specialty Clinic", "190 E Bannock St, Boise, ID 83712", "Boise", "ID", 43.6121, -116.1932, "POP-BOI-01", "Regional Specialty Center", 6, 7.9, 15.2),
    (42, "Apex Health Meridian Treasure Valley Medical Campus", "520 S Eagle Rd, Meridian, ID 83642", "Meridian", "ID", 43.6008, -116.3541, "POP-BOI-01", "Multi-Specialty Campus", 11, 8.2, 16.0),
    (43, "Apex Health Nampa Canyon County Family Clinic", "1510 12th Ave Rd, Nampa, ID 83686", "Nampa", "ID", 43.5592, -116.5598, "POP-BOI-01", "Primary & Urgent Care", 14, 8.5, 16.8),
    (44, "Apex Health Redding Shasta Regional Clinic", "1100 Butte St, Redding, CA 96001", "Redding", "CA", 40.5842, -122.3914, "POP-SAC-01", "Regional Outpatient Center", 12, 9.6, 17.5),
    (45, "Apex Health Sacramento Sutter Corridor Medical Center", "2801 L St, Sacramento, CA 95816", "Sacramento", "CA", 38.5724, -121.4702, "POP-SAC-01", "Regional Medical Center", 5, 10.4, 18.2),
]

CLINIC_SITES: list[dict[str, Any]] = []
SPLICE_CLOSURES: list[dict[str, Any]] = []

for (
    site_num,
    site_name,
    address,
    city,
    state,
    lat,
    lng,
    pop_id,
    clinic_type,
    dist_m,
    latency_ms,
    legacy_latency_ms,
) in _RAW_SITES:
    site_id = f"SITE-{site_num:03d}"
    pop_short = pop_id.split("-")[1]
    splice_id = f"SC-{pop_short}-{site_num:03d}"
    is_near_net = site_num in (28, 33)

    # Calculate realistic splice closure lat/lng offset
    if site_num == 28:
        splice_lat = round(lat - 0.00062, 6)
        splice_lng = round(lng + 0.00055, 6)
        build_capex_usd = 1820
        construction_type = "82m Directional Micro-Trenching & 48-Strand SMF Lateral Pull"
        permit_authority = "City of Wenatchee Public Works ROW Utility Permit (Fast-Track 10 Days)"
        nid_status = "Ciena 5170 NID Staged at POP-QCY-01 Depot"
        mrc_usd = 3450
    elif site_num == 33:
        splice_lat = round(lat - 0.00088, 6)
        splice_lng = round(lng + 0.00078, 6)
        build_capex_usd = 2380
        construction_type = "118m Existing Conduit Pull + Vault Splice Termination"
        permit_authority = "City of Hood River & ODOT Utility Vault Access Permit (12 Days)"
        nid_status = "Nokia 7210 SAS-S NID Staged at POP-PDX-01 Depot"
        mrc_usd = 3550
    else:
        splice_lat = round(lat - 0.00008, 6)
        splice_lng = round(lng + 0.00008, 6)
        build_capex_usd = 0
        construction_type = "In-Building MDF Riser Patch Only (On-Net Lit Building)"
        permit_authority = "None Required (Existing Lit Building Entry)"
        nid_status = "Dual-Homed 10G SFP+ Ports Reserved & Pre-Cabled"
        mrc_usd = 3100 if "Hospital" not in clinic_type and "Tower" not in clinic_type else 3600

    status = "Near-Net" if is_near_net else "On-Net"
    bandwidth_tier = "10Gbps Active/Active Wave + Dual SD-WAN" if ("Hospital" in clinic_type or "Tower" in clinic_type or is_near_net) else "10Gbps Primary Wave + 2Gbps Diverse SD-WAN"

    CLINIC_SITES.append(
        {
            "site_num": site_num,
            "site_id": site_id,
            "site_name": site_name,
            "address": address,
            "city": city,
            "state": state,
            "lat": lat,
            "lng": lng,
            "pop_id": pop_id,
            "splice_closure_id": splice_id,
            "splice_lat": splice_lat,
            "splice_lng": splice_lng,
            "clinic_type": clinic_type,
            "network_status": status,
            "distance_to_splice_m": dist_m,
            "bandwidth_tier": bandwidth_tier,
            "port_readiness": "Lateral Fiber Extension Required (<150m)" if is_near_net else "10Gbps SFP+ Port Reserved (Immediate Provision)",
            "estimated_ehr_latency_ms": latency_ms,
            "legacy_wan_latency_ms": legacy_latency_ms,
            "sla_compliant": latency_ms < 12.0,
            "build_capex_usd": build_capex_usd,
            "construction_method": construction_type,
            "permit_requirement": permit_authority,
            "cpe_nid_status": nid_status,
            "monthly_mrc_usd": mrc_usd,
            "optical_loss_budget_db": round(2.4 + (dist_m * 0.012), 2),
        }
    )

    SPLICE_CLOSURES.append(
        {
            "splice_closure_id": splice_id,
            "pop_id": pop_id,
            "served_site_id": site_id,
            "lat": splice_lat,
            "lng": splice_lng,
            "fiber_cable_id": f"FBR-{pop_short}-RING-{(site_num % 4) + 1:02d}",
            "total_strands": 144,
            "available_dark_strands": 36 if not is_near_net else 24,
            "enclosure_type": "Corning SCF-6C Butt-Splice Vault Closure",
            "splice_loss_db": 0.08,
        }
    )

# BigQuery Table 1: fiber_build_cost_models
FIBER_BUILD_COST_MODELS: list[dict[str, Any]] = [
    {
        "model_id": "COST-NEARNET-WENATCHEE-028",
        "site_id": "SITE-028",
        "site_name": "Apex Health Wenatchee Valley Specialty Clinic",
        "region": "Central Washington (Wenatchee / Chelan County)",
        "distance_m": 82,
        "construction_method": "Directional Micro-Trenching + 48-Strand SMF Pull",
        "civil_trenching_cost_per_m_usd": 14.50,
        "fiber_cable_and_splice_cost_usd": 381.00,
        "row_permit_and_traffic_control_usd": 250.00,
        "total_estimated_capex_usd": 1820.00,
        "estimated_construction_days": 9,
        "amortized_36m_monthly_usd": 50.56,
    },
    {
        "model_id": "COST-NEARNET-HOODRIVER-033",
        "site_id": "SITE-033",
        "site_name": "Apex Health Hood River Gorge Medical Center",
        "region": "Columbia River Gorge (Hood River County, OR)",
        "distance_m": 118,
        "construction_method": "Existing Municipal Conduit Pull + Vault Splice Termination",
        "civil_trenching_cost_per_m_usd": 13.80,
        "fiber_cable_and_splice_cost_usd": 451.60,
        "row_permit_and_traffic_control_usd": 300.00,
        "total_estimated_capex_usd": 2380.00,
        "estimated_construction_days": 11,
        "amortized_36m_monthly_usd": 66.11,
    },
    {
        "model_id": "COST-ONNET-LIT-STD",
        "site_id": "ALL-43-ONNET-SITES",
        "site_name": "43 On-Net Lit Building Clinic Sites (0m - 16m MDF Riser)",
        "region": "Pacific Northwest Footprint (WA / OR / ID / CA)",
        "distance_m": 8,
        "construction_method": "Zero Civil Build - Existing In-Building Single-Mode Fiber Riser",
        "civil_trenching_cost_per_m_usd": 0.0,
        "fiber_cable_and_splice_cost_usd": 0.0,
        "row_permit_and_traffic_control_usd": 0.0,
        "total_estimated_capex_usd": 0.0,
        "estimated_construction_days": 2,
        "amortized_36m_monthly_usd": 0.0,
    },
]

# BigQuery Table 2: product_pricing_catalog
PRODUCT_PRICING_CATALOG: list[dict[str, Any]] = [
    {
        "sku_id": "TEL-SDWAN-10G-HOSP",
        "product_name": "10Gbps Active/Active Optical Wave + Managed Dual-CPE SD-WAN (Hospital & Near-Net Tier)",
        "category": "Access & SD-WAN",
        "quantity": 10,
        "unit_list_mrc_usd": 4200.00,
        "unit_proposed_mrc_usd": 3570.00,
        "unit_direct_cost_mrc_usd": 1980.00,
        "total_monthly_mrc_usd": 35700.00,
        "total_monthly_cost_usd": 19800.00,
        "sla_tier": "99.999% Five-Nines + <12ms EHR Latency Guarantee",
    },
    {
        "sku_id": "TEL-SDWAN-10G-CLINIC",
        "product_name": "10Gbps Primary Wave + 2Gbps Diverse SD-WAN (Outpatient & Specialty Clinic Tier)",
        "category": "Access & SD-WAN",
        "quantity": 35,
        "unit_list_mrc_usd": 3250.00,
        "unit_proposed_mrc_usd": 2720.00,
        "unit_direct_cost_mrc_usd": 1560.00,
        "total_monthly_mrc_usd": 95200.00,
        "total_monthly_cost_usd": 54600.00,
        "sla_tier": "99.999% Five-Nines + <12ms EHR Latency Guarantee",
    },
    {
        "sku_id": "TEL-CLD-100G-INTX",
        "product_name": "100Gbps Redundant Google Cloud Dedicated Interconnect & Quincy Epic EHR Direct Wave",
        "category": "Cloud Interconnect",
        "quantity": 2,
        "unit_list_mrc_usd": 6500.00,
        "unit_proposed_mrc_usd": 5400.00,
        "unit_direct_cost_mrc_usd": 3150.00,
        "total_monthly_mrc_usd": 10800.00,
        "total_monthly_cost_usd": 6300.00,
        "sla_tier": "99.999% Optical Diversity + MACsec Line-Rate Encryption",
    },
    {
        "sku_id": "TEL-SEC-HIPAA-SASE",
        "product_name": "HIPAA/HITRUST Zero-Trust SASE, AES-256-GCM IPsec & 24x7 Healthcare NOC eBonding",
        "category": "Managed Security & Compliance",
        "quantity": 45,
        "unit_list_mrc_usd": 190.00,
        "unit_proposed_mrc_usd": 151.11,
        "unit_direct_cost_mrc_usd": 104.81,
        "total_monthly_mrc_usd": 6800.00,
        "total_monthly_cost_usd": 4716.67,
        "sla_tier": "HIPAA BAA + 15-Minute P1 Incident Response SLA",
    },
    {
        "sku_id": "TEL-CAPEX-AMORT-36M",
        "product_name": "Near-Net Lateral Fiber Construction CAPEX (Sites #28 & #33 - $4,200 Amortized over 36 Mos)",
        "category": "Infrastructure Build Amortization",
        "quantity": 2,
        "unit_list_mrc_usd": 58.33,
        "unit_proposed_mrc_usd": 0.00,
        "unit_direct_cost_mrc_usd": 58.33,
        "total_monthly_mrc_usd": 0.00,
        "total_monthly_cost_usd": 116.67,
        "sla_tier": "100% Upfront NRE Waived (Absorbed in 36-Month Deal Margin)",
    },
]

# BigQuery Table 3: historical_bid_analytics
HISTORICAL_BID_ANALYTICS: list[dict[str, Any]] = [
    {
        "bid_id": "BID-2025-PNW-881",
        "customer_segment": "Regional Healthcare Network (38 Sites)",
        "deal_tcv_usd": 4620000,
        "on_net_ratio_pct": 92.1,
        "upfront_nre_charged_usd": 0,
        "amortized_capex_usd": 6800,
        "gross_margin_pct": 41.8,
        "response_time_hours": 18,
        "outcome": "WON",
        "win_driver": "Zero upfront construction NRE + guaranteed <12ms Epic EHR latency SLA",
    },
    {
        "bid_id": "BID-2025-CASCADE-412",
        "customer_segment": "Multi-State Clinic Group (52 Sites)",
        "deal_tcv_usd": 5890000,
        "on_net_ratio_pct": 94.2,
        "upfront_nre_charged_usd": 0,
        "amortized_capex_usd": 4900,
        "gross_margin_pct": 43.1,
        "response_time_hours": 14,
        "outcome": "WON",
        "win_driver": "36-month CAPEX amortization + 100% HIPAA BAA & HITRUST compliance matrix",
    },
    {
        "bid_id": "BID-2024-VALLEY-309",
        "customer_segment": "Regional Hospital System (41 Sites)",
        "deal_tcv_usd": 4950000,
        "on_net_ratio_pct": 87.8,
        "upfront_nre_charged_usd": 14500,
        "amortized_capex_usd": 0,
        "gross_margin_pct": 44.0,
        "response_time_hours": 480,
        "outcome": "LOST",
        "win_driver": "Lost due to 3-week manual quote turnaround and separate upfront NRE line item",
    },
    {
        "bid_id": "BID-2026-APEX-MODEL",
        "customer_segment": "Apex Health Regional Network (45 Sites - Current Deal)",
        "deal_tcv_usd": 5346000,
        "on_net_ratio_pct": 95.6,
        "upfront_nre_charged_usd": 0,
        "amortized_capex_usd": 4200,
        "gross_margin_pct": 42.4,
        "response_time_hours": 1,
        "outcome": "PROJECTED_WIN_89PCT",
        "win_driver": "43/45 On-Net + $4,200 Near-Net CAPEX folded into 36-month schedule preserving 42.4% Gross Margin",
    },
]


def _build_200_compliance_questions() -> list[dict[str, Any]]:
    """Generates all 200 realistic compliance matrix questions (185 Auto-Answered + 15 Human Review)."""
    questions: list[dict[str, Any]] = []

    # 15 specific questions flagged for human review with rich context
    human_review_specs: dict[int, dict[str, str]] = {
        14: {
            "category": "SEC",
            "domain": "HIPAA & Zero-Trust Encryption",
            "question_text": "Does the provider allow Apex Health's internal SOC to hold exclusive customer-managed HSM root keys (BYOK/HYOK) for SD-WAN control-plane IPsec re-keying on a 15-minute rotation interval?",
            "suggested_answer": "Conditional Support: Standard enterprise profile uses FIPS 140-3 Level 3 Cloud HSM with 60-minute Ikev2 re-keying and customer-held KEK. A 15-minute re-key timer is supported via custom SD-WAN controller policy profile but requires joint CPU benchmark sign-off.",
            "source_doc": "Telco_HIPAA_ISO27001_Security_Compliance_Attestation_v4.2.pdf",
            "source_citation": "Section 4.3 (FIPS 140-3 Key Management & BYOK), Page 5",
            "review_reason": "Custom 15-minute IKEv2 re-key interval deviates from standard 60-minute enterprise policy; requires Security Architect sign-off.",
            "risk_level": "Low",
        },
        31: {
            "category": "SEC",
            "domain": "HIPAA & Zero-Trust Encryption",
            "question_text": "Will the vendor accept unlimited third-party penetration testing against live production CPE management interfaces without a 7-day advance maintenance window notice?",
            "suggested_answer": "Exception Proposed: We welcome annual and ad-hoc gray-box/black-box penetration testing by Apex Health's red team against dedicated customer VRF and CPE enclaves with a 24-hour electronic notification to our Healthcare SOC to prevent automated DDoS scrubbing false-positives.",
            "source_doc": "Telco_HIPAA_ISO27001_Security_Compliance_Attestation_v4.2.pdf",
            "source_citation": "Section 7.2 (Customer Red-Team & Vulnerability Testing Protocol), Page 8",
            "risk_level": "Medium",
            "review_reason": "Unannounced testing on shared PoP Peering edges requires 24-hour SOC safelisting notice.",
        },
        52: {
            "category": "NET",
            "domain": "SD-WAN & Dynamic Routing",
            "question_text": "Custom BGP routing requirement: Support dynamic BGP community string tagging (65001:100 through 65001:450) with sub-second BFD timers (3x 15ms = 45ms detection) and custom AS-path prepending directly into customer-managed Epic EHR VRFs across all 45 clinics.",
            "suggested_answer": "Supported with Engineering Validation: Nokia 7750 SR PoPs and Prisma/Versa SD-WAN edge appliances natively support 15ms hardware-assisted BFD echo timers and pass-through BGP extended community strings (65001:100–450). Requires Principal Network Architect validation of route-map damper thresholds to avoid micro-flap propagation.",
            "source_doc": "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf",
            "source_citation": "Section 3.4 (Hardware-Assisted BFD & Custom BGP Community Tagging), Page 6",
            "risk_level": "Medium",
            "review_reason": "Custom BGP routing requirement with 15ms BFD timers requires Principal Network Architect sign-off.",
        },
        68: {
            "category": "NET",
            "domain": "Optical Access & Near-Net Build",
            "question_text": "Confirm that 100% of the 45 clinic sites are currently lit On-Net with zero outside-plant lateral construction required prior to turn-up.",
            "suggested_answer": "Clarification & Commercial Mitigation: 43 of 45 sites (95.6%) are 100% On-Net lit buildings with 10Gbps SFP+ ports reserved today. Only 2 sites—Site #28 (Wenatchee, 82m) and Site #33 (Hood River, 118m)—are Near-Net (<150m from active splice closures SC-QCY-028 and SC-PDX-033). Both lateral builds will complete within 11 business days, and 100% of the $4,200 CAPEX is waived upfront via 36-month amortization.",
            "source_doc": "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf",
            "source_citation": "Section 2.2 (On-Net vs. Near-Net Fast-Track Lateral Construction), Page 4",
            "risk_level": "Low",
            "review_reason": "2 of 45 sites (#28 and #33) are Near-Net (<150m) requiring short lateral fiber run extensions; confirm commercial CAPEX waiver language.",
        },
        79: {
            "category": "NET",
            "domain": "SD-WAN & Dynamic Routing",
            "question_text": "Can the SD-WAN edge appliance host a third-party containerized clinical IoT packet broker (Docker/KVM 4 vCPU, 16GB RAM) directly on the branch uCPE hardware at all 45 clinics?",
            "suggested_answer": "Supported via uCPE Upgrade Option: Our standard branch CPE includes 2 spare vCPUs/8GB RAM for service chaining. Hosting a 4 vCPU/16GB RAM clinical IoT container across all 45 clinics is supported on our uCPE-Pro blade at zero additional MRC when bundled in a 36-month term.",
            "source_doc": "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf",
            "source_citation": "Section 5.1 (uCPE Virtual Network Function Hosting Specifications), Page 9",
            "risk_level": "Low",
            "review_reason": "Verify uCPE-Pro memory allocation for customer container image at branch clinics.",
        },
        91: {
            "category": "NET",
            "domain": "Optical Access & Near-Net Build",
            "question_text": "For rural clinics in Central Washington (Site #28 Wenatchee) and Columbia Gorge (Site #33 Hood River), guarantee physically diverse dual building entries separated by at least 25 meters.",
            "suggested_answer": "Engineering Design Attached: Site #28 utilizes North Chelan Ave utility vault entry (north riser) + diverse 5G Standalone/LEO enterprise backup during Phase 1, with secondary south alley conduit available. Site #33 uses May St east vault and 12th St west riser separated by 31 meters.",
            "source_doc": "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf",
            "source_citation": "Section 2.4 (Dual-Entry & Diverse Last-Mile Engineering), Page 5",
            "risk_level": "Medium",
            "review_reason": "OSP Engineering review of Site #28 secondary alley conduit easement.",
        },
        108: {
            "category": "CLD",
            "domain": "Google Cloud & Epic EHR Interconnect",
            "question_text": "Support jumbo frames of 9,216 bytes end-to-end across both the 10Gbps clinic wavelengths and the 100Gbps Google Cloud Dedicated Interconnect attachments.",
            "suggested_answer": "Partial Technical Qualification: Our 10Gbps Optical Wavelengths and Quincy Epic EHR Direct Waves natively support 9,216-byte Jumbo Frames end-to-end. Google Cloud Dedicated Interconnect VLAN attachments support a maximum MTU of 8,896 bytes per GCP specification; our border routers automatically clamp TCP MSS or segment at 8,896 bytes on the GCP leg.",
            "source_doc": "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf",
            "source_citation": "Section 4.2 (Cloud Interconnect MTU & Jumbo Frame Alignment), Page 7",
            "risk_level": "Low",
            "review_reason": "Clarify GCP Dedicated Interconnect 8,896-byte hardware MTU ceiling vs. 9,216-byte optical wave MTU.",
        },
        121: {
            "category": "CLD",
            "domain": "Google Cloud & Epic EHR Interconnect",
            "question_text": "Provide automated BGP graceful-restart and sub-2-second failover between Quincy Primary Epic EHR enclave and Google Cloud us-west1 DR enclave triggered by synthetic Epic Hyperspace transaction probes.",
            "suggested_answer": "Supported via Custom IPSLA + SD-WAN App-Probe Policy: Synthetic HTTPS/Citrix ICA probes to Epic Hyperspace execute every 250ms; three consecutive probe failures (<750ms) trigger automated SD-WAN tunnel steering and BGP local-preference flip to Google Cloud us-west1 DR.",
            "source_doc": "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf",
            "source_citation": "Section 4.4 (Epic EHR Synthetic Transaction Steering), Page 8",
            "risk_level": "Low",
            "review_reason": "Cloud Solutions Architect to confirm synthetic probe URI endpoints with Apex Health Epic team.",
        },
        139: {
            "category": "SLA",
            "domain": "99.999% Availability & <12ms Latency SLA",
            "question_text": "Confirm acceptance of a 15% Monthly Recurring Charge (MRC) service credit for every 1.0ms of round-trip latency exceeding 12.0ms (5-minute 95th percentile) between any clinic and the Primary Epic EHR Data Center.",
            "suggested_answer": "Accepted with On-Net Optical Guarantee: All 45 clinics (including Near-Net Sites #28 at 4.6ms and #33 at 6.8ms once lateral fiber extensions are lit) operate between 1.5ms and 10.4ms RTD—providing a minimum 1.6ms safety margin below the 12.0ms ceiling. We accept the 15% MRC credit per 1.0ms exceedance up to 100% of site MRC.",
            "source_doc": "Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf",
            "source_citation": "Section 3.1 (Healthcare <12ms Latency Guarantee & Credit Schedule), Page 4",
            "risk_level": "Medium",
            "review_reason": "Commercial VP sign-off required for custom 15% per 1ms latency penalty tier (standard tier is 10% per 1ms).",
        },
        142: {
            "category": "SLA",
            "domain": "99.999% Availability & <12ms Latency SLA",
            "question_text": "Confirm that chronic latency exceeding 18.0ms for three consecutive calendar days grants Apex Health immediate termination-for-cause rights for the affected clinic without early termination liability.",
            "suggested_answer": "Accepted with Standard Excused Outage Carve-Out: We accept the chronic latency termination right (>18.0ms for 3 consecutive days) with zero Early Termination Fee (ETF), excluding customer-induced LAN congestion or municipal civil force-majeure fiber cuts where secondary diverse transport remains below 15.0ms.",
            "source_doc": "Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf",
            "source_citation": "Section 3.3 (Chronic SLA Remedies & ETF Waiver Terms), Page 5",
            "risk_level": "Medium",
            "review_reason": "Legal & Commercial review of force-majeure carve-out wording on chronic latency clause.",
        },
        154: {
            "category": "SLA",
            "domain": "99.999% Availability & <12ms Latency SLA",
            "question_text": "Will the provider issue SLA service credits automatically on the following month's invoice via telemetry smart-contract without requiring Apex Health to submit a manual credit claim ticket?",
            "suggested_answer": "Supported & Enabled: Our TWAMP/Y.1731 telemetry engine streams real-time 1-second SLA metrics into BigQuery and automatically applies earned SLA credits to the monthly billing run without requiring a customer claim ticket.",
            "source_doc": "Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf",
            "source_citation": "Section 5.2 (Zero-Touch Automated SLA Credit Issuance), Page 7",
            "risk_level": "Low",
            "review_reason": "Billing Ops verification of automated credit feed into Apex Health EDI 810 invoice profile.",
        },
        166: {
            "category": "SLA",
            "domain": "99.999% Availability & <12ms Latency SLA",
            "question_text": "Accept uncapped consequential damages up to $10,000,000 for HIPAA ePHI data breaches caused by provider-managed SD-WAN firmware vulnerabilities.",
            "suggested_answer": "Mutual Super-Cap Proposed: Per our Healthcare BAA Schedule, we provide a dedicated $5,000,000 Cyber & HIPAA Regulatory Super-Cap (3x standard enterprise cap). Raising the super-cap to $10,000,000 is available subject to Executive Risk Committee sign-off.",
            "source_doc": "Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf",
            "source_citation": "Section 6.4 (HIPAA BAA Cyber Liability Super-Cap), Page 8",
            "risk_level": "High",
            "review_reason": "Legal counsel review required for $10M HIPAA liability super-cap request vs. $5M standard healthcare BAA cap.",
        },
        178: {
            "category": "OPS",
            "domain": "24x7 NOC, ServiceNow eBonding & Deployment",
            "question_text": "Complete full production cutover of all 45 clinics—including Near-Net Sites #28 and #33—within 30 calendar days of contract signature.",
            "suggested_answer": "Committed with Phased Wave Schedule: All 43 On-Net clinics and both 100G Cloud Interconnects will turn up within 14–18 calendar days. Near-Net Sites #28 (Wenatchee, 82m build) and #33 (Hood River, 118m build) are scheduled for civil completion by Day 21 and full optical cutover by Day 26—meeting the 30-day deadline with 4 days of buffer.",
            "source_doc": "Past_Winning_Bid_Pacific_Northwest_Health_Network_2025.pdf",
            "source_citation": "Section 4.1 (Accelerated 30-Day Healthcare Rollout Methodology), Page 5",
            "risk_level": "Low",
            "review_reason": "OSP Construction PM confirmation of Wenatchee and Hood River permit fast-track queue.",
        },
        189: {
            "category": "OPS",
            "domain": "24x7 NOC, ServiceNow eBonding & Deployment",
            "question_text": "Provide bi-directional ServiceNow Tokyo/Xanadu eBonding with custom HL7/Epic impact severity mapping within 10 business days of contract award.",
            "suggested_answer": "Supported via Pre-Built ServiceNow Healthcare Connector: Our REST/GraphQL ServiceNow eBonding adapter includes pre-mapped Epic EHR clinic criticality tiers and can be deployed into Apex Health's UAT instance within 5 business days and production within 10 business days.",
            "source_doc": "Past_Winning_Bid_Pacific_Northwest_Health_Network_2025.pdf",
            "source_citation": "Section 5.3 (ServiceNow Bi-Directional eBonding Integration), Page 7",
            "risk_level": "Low",
            "review_reason": "ITSM Integration Engineer to verify custom Epic severity field names with Apex Health ServiceNow admin.",
        },
        197: {
            "category": "OPS",
            "domain": "24x7 NOC, ServiceNow eBonding & Deployment",
            "question_text": "Include a 180-day penalty-free 'Right-to-Downsize' clause allowing Apex Health to relocate or decommission up to 5 clinic circuits without construction clawback or ETF.",
            "suggested_answer": "Accepted for Portable MRC: We grant 100% portability and zero-ETF decommissioning for up to 5 On-Net clinics after Day 180, provided aggregate monthly revenue remains above 90% of baseline commitment.",
            "source_doc": "Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf",
            "source_citation": "Section 7.1 (Healthcare Clinic Portability & Flex-Down Clause), Page 9",
            "risk_level": "Low",
            "review_reason": "Commercial Deal Desk confirmation of 5-site portability flex clause.",
        },
    }

    # Templates for the remaining 185 Auto-Answered (100% confidence) questions
    sec_templates = [
        ("Encryption in Transit for ePHI", "Confirm that all ePHI traffic traversing SD-WAN overlays and optical wavelengths uses FIPS 140-3 validated AES-256-GCM encryption at line rate.", "Compliant (100% Supported): All 45 clinic SD-WAN appliances enforce FIPS 140-3 Level 3 validated AES-256-GCM IPsec tunnels with SHA-512 HMAC, complemented by IEEE 802.1AE MACsec Layer-2 optical encryption across all 10G/100G wavelengths.", "Section 2.1 (FIPS 140-3 Line-Rate Encryption), Page 2"),
        ("HIPAA Business Associate Agreement (BAA)", "Confirm readiness to execute the standard Apex Health HIPAA/HITECH Business Associate Agreement without material redlines.", "Compliant (100% Supported): We execute the HIPAA/HITECH Omnibus Rule Business Associate Agreement (BAA) and maintain annual third-party HIPAA Security Rule & HITECH Subtitle D audit attestations across all transport, PoP, and NOC operations.", "Section 1.2 (HIPAA & HITECH BAA Execution), Page 1"),
        ("HITRUST CSF v11 & ISO/IEC 27001 Certification", "Provide current HITRUST CSF v11 r2 and ISO/IEC 27001:2022 certification scope covering all Pacific Northwest PoPs and NOC centers.", "Compliant (100% Supported): All 9 regional PoPs (Seattle, Quincy, Bellevue, Tacoma, Spokane, Portland, Eugene, Boise, Sacramento) and our 24x7 US-based Healthcare NOC hold active HITRUST CSF v11 r2 and ISO/IEC 27001:2022 certifications.", "Section 1.4 (HITRUST CSF v11 & ISO 27001 Scope), Page 2"),
        ("Zero-Trust Micro-Segmentation for Clinical VLANs", "Verify support for VRF-aware zone-based firewalls isolating Epic EHR workstations, PACS medical imaging, guest Wi-Fi, and infusion-pump IoT VLANs.", "Compliant (100% Supported): Each clinic uCPE enforces 8 isolated VRF security zones with stateful Layer-7 medical device fingerprinting (DICOM, HL7, Epic Hyperspace) and strict east-west micro-segmentation.", "Section 3.2 (Clinical VRF Micro-Segmentation), Page 4"),
        ("SOC 2 Type II Continuous Compliance", "Confirm AICPA SOC 2 Type II attestation across all 5 Trust Services Criteria with zero open high-severity exceptions.", "Compliant (100% Supported): Our latest 12-month SOC 2 Type II report (audited by Deloitte) covers Security, Availability, Processing Integrity, Confidentiality, and Privacy with zero exceptions.", "Section 1.5 (SOC 2 Type II Attestation), Page 3"),
    ]

    net_templates = [
        ("Dual-Transport Active/Active SD-WAN Architecture", "Verify that every clinic site terminates two physically independent transports with automatic sub-second packet-by-packet failover.", "Compliant (100% Supported): Every Apex Health clinic is engineered with a Primary 10Gbps Dedicated Optical Wavelength plus a Secondary Diverse Fiber/Carrier-Ethernet transport managed by active/active SD-WAN forward error correction (FEC).", "Section 1.1 (Dual-Transport Active/Active SD-WAN), Page 1"),
        ("Optical Wavelength ITU-T G.652.D Performance", "Confirm that all 10Gbps access circuits utilize dedicated OTN/DWDM wavelengths rather than oversubscribed GPON/best-effort broadband.", "Compliant (100% Supported): All 45 clinics receive dedicated, non-oversubscribed 10Gbps MEF 3.0 Certified Optical Carrier Ethernet / OTN circuits terminated on Ciena 5170 or Nokia 7210 SAS NIDs with hardware Y.1731 OAM probes.", "Section 2.1 (Dedicated 10G Optical Transport), Page 3"),
        ("QoS Priority Queuing for Epic EHR & Tele-ICU", "Describe hardware QoS markings and strict-priority scheduling for Epic Hyperspace, VoIP, and real-time Tele-ICU video streams.", "Compliant (100% Supported): Hardware hierarchical QoS (H-QoS) guarantees 40% strict low-latency queuing (EF/CS5) for Epic EHR and Tele-ICU video, 35% assured forwarding (AF41) for PACS/DICOM imaging, and scavenger policing for bulk updates.", "Section 3.1 (Healthcare H-QoS Traffic Engineering), Page 5"),
        ("High-Availability Dual-CPE Branch Redundancy", "Confirm that flagship hospitals and regional medical centers include dual redundant SD-WAN appliances in VRRP/HA state sync.", "Compliant (100% Supported): All regional hospitals, tertiary towers, and Near-Net hubs include dual HA SD-WAN appliances with stateful session synchronization, dual redundant power supplies, and 8-hour lithium battery backup.", "Section 3.3 (High-Availability Branch CPE Design), Page 6"),
        ("IPv6 Dual-Stack & Segment Routing (SR-MPLS)", "Verify full native IPv4/IPv6 dual-stack routing and Traffic-Engineered Segment Routing (SR-MPLS TI-LFA) across the regional core.", "Compliant (100% Supported): Our Pacific Northwest core runs SR-MPLS with Topology-Independent Loop-Free Alternates (TI-LFA), guaranteeing <50ms core optical protection switching and native IPv4/IPv6 dual-stack transport.", "Section 2.3 (SR-MPLS TI-LFA Core Protection), Page 4"),
    ]

    cld_templates = [
        ("100Gbps Google Cloud Dedicated Interconnect", "Confirm redundant 100Gbps Google Cloud Dedicated Interconnect capacity in us-west1 with 99.99% GCP SLA alignment.", "Compliant (100% Supported): We provision redundant 100Gbps Google Cloud Dedicated Interconnects across POP-SEA-01 (Seattle Westin) and POP-PDX-01 (Portland Pittock) feeding GCP us-west1 across physically diverse dark-fiber routes.", "Section 4.1 (Google Cloud 100G Dedicated Interconnect), Page 7"),
        ("Direct Optical Peering to Quincy Epic EHR Data Center", "Verify direct sub-5ms optical wave connectivity into the Quincy, WA Epic EHR primary hosting enclave.", "Compliant (100% Supported): POP-QCY-01 is co-located within 400 meters of the Quincy Epic EHR enclave with dual dark-fiber cross-connects delivering 0.4ms intra-campus latency and <4.8ms regional Washington clinic RTD.", "Section 4.3 (Quincy Epic EHR Direct Optical Enclave), Page 8"),
        ("Multi-Cloud Hairpin Avoidance & Direct Cloud On-Ramp", "Confirm that clinic-to-cloud traffic routes directly to the nearest Cloud Interconnect PoP without trombone backhauling.", "Compliant (100% Supported): Regional clinics in WA, OR, ID, and CA egress via local regional PoPs directly onto our 800G/1600G DWDM express trunks into Seattle, Quincy, and Portland cloud gateways with zero hairpinning.", "Section 4.2 (Direct Multi-Cloud Routing Topology), Page 7"),
        ("Automated Cloud BGP Route Filtering & RPKI", "Verify RPKI route origin validation and automated BGP prefix-list guardrails on all cloud interconnect sessions.", "Compliant (100% Supported): All Cloud Router BGP sessions enforce strict RPKI validation, MD5/TCP-AO session authentication, and automated prefix-limit filters preventing route leaks between cloud and clinical VRFs.", "Section 4.5 (Cloud Routing Security & RPKI), Page 8"),
    ]

    sla_templates = [
        ("99.999% Five-Nines Core & Access Availability SLA", "Confirm contractual commitment to 99.999% monthly availability (<26 seconds downtime/month) across all dual-homed clinic sites.", "Compliant (100% Supported): Our Master Service Agreement guarantees 99.999% end-to-end site availability across all 45 dual-transport clinics, backed by 0.0% packet loss and <2ms jitter SLAs.", "Section 2.1 (99.999% Five-Nines Availability Commitment), Page 2"),
        ("<12.0ms Round-Trip Latency SLA to Epic EHR", "Verify that every proposed clinic site meets the mandatory <12.0ms RTD latency threshold to the Epic EHR hosting enclave.", "Compliant (100% Supported): Live Cloud Spanner topology modeling confirms all 45 clinics achieve between 1.5ms and 10.4ms RTD to the Epic EHR hub (mean: 4.8ms), strictly below the 12.0ms SLA threshold.", "Section 3.1 (Healthcare <12ms Latency Guarantee), Page 4"),
        ("Mean Time to Repair (MTTR) & Optical Restoral", "State the guaranteed Core Optical Switching time and Physical Fiber Cut Mean Time to Repair (MTTR).", "Compliant (100% Supported): Automated DWDM optical ring protection restores traffic in <50ms. For physical last-mile events, our regional field engineering depots guarantee <2-hour on-site dispatch and <4-hour physical fiber restoral.", "Section 4.1 (Optical Protection & 4-Hour MTTR SLA), Page 6"),
        ("Packet Loss (<0.01%) and Jitter (<1.5ms) Commitments", "Confirm real-time SLA thresholds for packet delivery ratio and inter-packet jitter on clinical voice/video classes.", "Compliant (100% Supported): We contractually guarantee >=99.99% packet delivery (<0.01% loss) and <=1.5ms inter-packet jitter across EF and AF41 clinical traffic classes, measured continuously at 1-second intervals.", "Section 3.2 (Jitter & Packet Loss SLA Thresholds), Page 5"),
    ]

    ops_templates = [
        ("24x7x365 US-Based Healthcare NOC Support", "Confirm that all Tier-1 through Tier-3 NOC engineers supporting Apex Health are US-based, HIPAA-trained personnel.", "Compliant (100% Supported): Apex Health is assigned to our dedicated US-based Healthcare NOC pod (Seattle, WA & Denver, CO) staffed 24x7x365 by HIPAA-badged network engineers with a <60-second live answer SLA.", "Section 5.1 (Dedicated 24x7 Healthcare NOC Pod), Page 6"),
        ("Real-Time Telemetry Streaming & BigQuery Portal", "Verify that Apex Health receives real-time streaming access to per-clinic latency, optical power (dBm), and SD-WAN utilization telemetry.", "Compliant (100% Supported): Our Agentic Telemetry Portal provides live sub-second streaming of optical Rx/Tx dBm power, TWAMP latency, BGP state, and top application flows via dashboard and REST API.", "Section 5.2 (Real-Time Telemetry & Portal Access), Page 7"),
        ("Zero-Downtime Maintenance Window Governance", "Confirm that all planned network maintenance occurs strictly within Tuesday/Thursday 01:00–04:00 PT windows with 14-day advance notice.", "Compliant (100% Supported): All non-emergency maintenance is restricted to 01:00–04:00 PT maintenance windows with 14 calendar days advance ServiceNow change-request notification and hitless in-service software upgrades (ISSU).", "Section 5.4 (Hitless ISSU & Change Governance), Page 8"),
        ("Dedicated Program Director & Field Turn-Up Team", "Confirm assignment of a PMP-certified Healthcare Program Director and regional field installation engineers for the 45-site rollout.", "Compliant (100% Supported): We assign a dedicated PMP-certified Healthcare Program Director, two Lead Solutions Architects, and 12 regional PNW field technicians who delivered our 38-site Pacific Northwest Health Network deployment ahead of schedule.", "Section 4.2 (Dedicated Healthcare Rollout Team), Page 5"),
    ]

    for q_num in range(1, 201):
        q_id = f"Q-{q_num:03d}"
        if q_num in human_review_specs:
            spec = human_review_specs[q_num]
            questions.append(
                {
                    "question_id": q_id,
                    "question_num": q_num,
                    "category": spec["category"],
                    "domain": spec["domain"],
                    "question_text": spec["question_text"],
                    "status": "Flagged for Human Review",
                    "confidence_pct": 84,
                    "answer_text": spec["suggested_answer"],
                    "source_doc": spec["source_doc"],
                    "source_citation": spec["source_citation"],
                    "review_reason": spec["review_reason"],
                    "risk_level": spec["risk_level"],
                    "sme_approved": False,
                }
            )
            continue

        # Assign category by question number range
        if q_num <= 45:
            cat = "SEC"
            domain = "HIPAA & Zero-Trust Encryption"
            tpl = sec_templates[(q_num - 1) % len(sec_templates)]
            doc = "Telco_HIPAA_ISO27001_Security_Compliance_Attestation_v4.2.pdf"
        elif q_num <= 95:
            cat = "NET"
            domain = "SD-WAN & Optical Architecture"
            tpl = net_templates[(q_num - 46) % len(net_templates)]
            doc = "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf"
        elif q_num <= 135:
            cat = "CLD"
            domain = "Google Cloud & Epic EHR Interconnect"
            tpl = cld_templates[(q_num - 96) % len(cld_templates)]
            doc = "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf"
        elif q_num <= 170:
            cat = "SLA"
            domain = "99.999% Availability & <12ms Latency SLA"
            tpl = sla_templates[(q_num - 136) % len(sla_templates)]
            doc = "Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf"
        else:
            cat = "OPS"
            domain = "24x7 NOC, ServiceNow eBonding & Deployment"
            tpl = ops_templates[(q_num - 171) % len(ops_templates)]
            doc = "Past_Winning_Bid_Pacific_Northwest_Health_Network_2025.pdf"

        topic, base_q, base_a, citation = tpl
        # Add realistic variation referencing specific RFP clause numbers or regional sites
        site_ref = CLINIC_SITES[(q_num * 3) % len(CLINIC_SITES)]
        clause_id = f"RFP-{cat}-{q_num:03d}"
        question_text = f"[{clause_id} - {topic}] {base_q} (Applicable across all 45 sites including {site_ref['site_name']} in {site_ref['city']}, {site_ref['state']})."

        questions.append(
            {
                "question_id": q_id,
                "question_num": q_num,
                "category": cat,
                "domain": domain,
                "question_text": question_text,
                "status": "Auto-Answered",
                "confidence_pct": 100,
                "answer_text": base_a,
                "source_doc": doc,
                "source_citation": citation,
                "review_reason": "Exact match verified in Vertex AI Search & BigQuery compliance repository.",
                "risk_level": "None",
                "sme_approved": True,
            }
        )

    return questions


COMPLIANCE_QUESTIONS: list[dict[str, Any]] = _build_200_compliance_questions()

# Grounding Reference Documents Metadata (for Vertex AI Search & PDF Viewer)
GROUNDING_DOCUMENTS: list[dict[str, Any]] = [
    {
        "filename": "Apex_Health_RFP_SDWAN_Cloud.pdf",
        "title": "Apex Health Regional Network RFP #AH-2026-SDWAN-094",
        "doc_type": "Customer RFP Document",
        "pages": 12,
        "summary": "Customer-issued RFP for 45 regional clinics across WA, OR, ID, and CA requiring 10Gbps Optical Wavelengths, Dual-Transport Managed SD-WAN, 100Gbps Google Cloud & Epic EHR Interconnects, 99.999% SLA, <12ms EHR latency penalty clause, and 200-question compliance matrix.",
    },
    {
        "filename": "Telco_HIPAA_ISO27001_Security_Compliance_Attestation_v4.2.pdf",
        "title": "Telco Enterprise HIPAA, HITRUST CSF v11 & ISO 27001 Security Attestation v4.2",
        "doc_type": "Regulatory & Security Attestation",
        "pages": 9,
        "summary": "Official security compliance manual covering HIPAA/HITECH BAA execution, FIPS 140-3 Level 3 AES-256-GCM encryption, IEEE 802.1AE MACsec optical encryption, VRF clinical micro-segmentation, and SOC 2 Type II controls.",
    },
    {
        "filename": "Enterprise_SDWAN_Cloud_Interconnect_Reference_Architecture_2026.pdf",
        "title": "Enterprise Dual-Transport SD-WAN, 10G Wavelength & Multi-Cloud Reference Architecture (2026)",
        "doc_type": "Technical Reference Architecture",
        "pages": 10,
        "summary": "Engineering specification for Nokia 7750 SR / Ciena 6500 optical core, 15ms hardware BFD, custom BGP community tagging, 100Gbps Google Cloud Dedicated Interconnect, Quincy Epic EHR direct wave peering, and Near-Net lateral fiber splicing.",
    },
    {
        "filename": "Master_Service_Agreement_SLA_99999_Schedule_and_Penalties.pdf",
        "title": "Master Service Agreement (MSA) — Healthcare 99.999% Five-Nines SLA & <12ms Latency Schedule",
        "doc_type": "Legal & Commercial SLA Schedule",
        "pages": 9,
        "summary": "Contractual SLA schedule defining 99.999% site availability, <12.0ms Epic EHR round-trip latency guarantee, 15% MRC service credit tiers, chronic outage termination rights, automated telemetry credit issuance, and 36-month CAPEX amortization policies.",
    },
    {
        "filename": "Past_Winning_Bid_Pacific_Northwest_Health_Network_2025.pdf",
        "title": "Past Winning Bid Reference: Pacific Northwest Health Network (38 Sites, $4.62M TCV, 2025)",
        "doc_type": "Historical Winning Proposal & Case Study",
        "pages": 8,
        "summary": "Benchmark winning healthcare proposal demonstrating 30-day multi-site deployment, ServiceNow eBonding integration, 24x7 US Healthcare NOC operations, and 36-month Near-Net CAPEX amortization strategy.",
    },
]
