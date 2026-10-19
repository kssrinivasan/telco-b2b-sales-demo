/* Agentic Deal Cockpit — Frontend Controller */

let cockpitState = {
  rfp_metadata: {},
  google_maps_api_key: "",
  pops: [],
  backbone_links: [],
  sites: [],
  splice_closures: [],
  questions: [],
  economics: {},
  grounding_documents: [],
  signoff_state: {},
  telemetry_log: [],
};

let gMap = null;
let gInfoWindow = null;
let clinicMarkers = [];
let popMarkers = [];
let spliceMarkers = [];
let mapPolylines = [];

let currentStatusFilter = "all";
let currentCategoryFilter = "ALL";
let searchDebounceTimer = null;

document.addEventListener("DOMContentLoaded", async () => {
  await loadBootstrapState();
});

async function loadBootstrapState() {
  try {
    const res = await fetch("/api/bootstrap");
    const data = await res.json();
    cockpitState = { ...cockpitState, ...data };

    renderGroundingDocuments(data.grounding_documents || []);
    renderSitesTable(data.sites || []);
    renderPricingTable(data.economics?.pricing_line_items || []);
    renderEconomicsMetrics(data.economics || {});
    renderSignoffCard(data.signoff_state || {}, data.economics || {});
    renderTelemetryLog(data.telemetry_log || []);

    // Pre-populate Site #28 in the Spanner Inspector Drawer
    if (data.sites && data.sites.length > 0) {
      inspectClinicSite("SITE-028", false);
    }

    // Load Google Maps JS API dynamically
    if (data.google_maps_api_key && !window.google?.maps) {
      const script = document.createElement("script");
      script.src = `https://maps.googleapis.com/maps/api/js?key=${data.google_maps_api_key}&callback=initCockpitMap`;
      script.async = true;
      script.defer = true;
      document.head.appendChild(script);
    } else if (window.google?.maps) {
      initCockpitMap();
    }

    // Load initial 200 compliance questions
    await filterComplianceQuestions("all", "ALL");
  } catch (err) {
    console.error("Bootstrap error:", err);
  }
}

/* Tab Switching */
function switchTab(tabId) {
  const tabs = ["brief", "map", "compliance", "commercial", "telemetry"];
  tabs.forEach((t) => {
    document.getElementById(`tab-btn-${t}`)?.classList.toggle("active", t === tabId);
    document.getElementById(`tab-pane-${t}`)?.classList.toggle("active", t === tabId);
  });
  if (tabId === "map" && gMap) {
    setTimeout(() => {
      google.maps.event.trigger(gMap, "resize");
    }, 80);
  }
}

/* 4-Step Workflow Execution */
async function triggerWorkflowStep(stepNum) {
  for (let i = 1; i <= 4; i++) {
    document.getElementById(`step-card-${i}`)?.classList.toggle("active", i === stepNum);
  }

  const timerLabel = document.getElementById("step-timer-label");
  if (timerLabel) timerLabel.textContent = `Running Step ${stepNum}...`;

  const tabForStep = {
    1: "brief",
    2: "compliance",
    3: "map",
    4: "commercial",
  };
  switchTab(tabForStep[stepNum] || "brief");

  try {
    const res = await fetch(`/api/step/${stepNum}`, { method: "POST" });
    const data = await res.json();

    if (timerLabel) {
      timerLabel.textContent = `Step ${stepNum} (${data.execution_time_ms}ms)`;
    }
    if (data.telemetry_log) {
      renderTelemetryLog(data.telemetry_log);
    }

    // Append concise agent update in Copilot Chat
    appendChatBubble(
      "agent",
      `<strong>[Step ${stepNum} · ${data.agent_name}]</strong> (${data.execution_time_ms}ms)<br/>${data.headline}`
    );

    if (stepNum === 2) {
      await filterComplianceQuestions("review", "ALL");
    } else if (stepNum === 3) {
      setTimeout(() => focusNearNetSite("SITE-028"), 200);
    }
  } catch (err) {
    console.error(`Error executing step ${stepNum}:`, err);
  }
}

async function runFullDemoFlow() {
  const btn = document.getElementById("btn-run-all-steps");
  if (btn) {
    btn.disabled = true;
    btn.textContent = "Running 4-Step Agentic Demo...";
  }
  for (let s = 1; s <= 4; s++) {
    await triggerWorkflowStep(s);
    await new Promise((r) => setTimeout(r, 1100));
  }
  if (btn) {
    btn.disabled = false;
    btn.innerHTML = "&#9654; Run Guided 4-Step Sales Demo";
  }
}

/* Google Maps Initialization & Rendering */
window.initCockpitMap = function () {
  const mapEl = document.getElementById("google-map-canvas");
  if (!mapEl || !window.google?.maps) return;

  gMap = new google.maps.Map(mapEl, {
    center: { lat: 45.85, lng: -120.65 },
    zoom: 6,
    mapTypeId: "roadmap",
    mapTypeControl: true,
    streetViewControl: true,
    fullscreenControl: true,
    styles: [
      { featureType: "poi.business", stylers: [{ visibility: "off" }] },
      { featureType: "water", stylers: [{ color: "#cfe2f3" }] },
    ],
  });

  gInfoWindow = new google.maps.InfoWindow();
  drawNetworkTopologyOnMap();
};

function drawNetworkTopologyOnMap() {
  if (!gMap) return;

  // Clear existing overlays
  clinicMarkers.forEach((m) => m.setMap(null));
  popMarkers.forEach((m) => m.setMap(null));
  spliceMarkers.forEach((m) => m.setMap(null));
  mapPolylines.forEach((l) => l.setMap(null));
  clinicMarkers = [];
  popMarkers = [];
  spliceMarkers = [];
  mapPolylines = [];

  const popById = {};
  (cockpitState.pops || []).forEach((p) => {
    popById[p.pop_id] = p;
  });

  // 1. Draw DWDM Backbone Ring Links between the 9 Regional PoPs
  (cockpitState.backbone_links || []).forEach((link) => {
    const p1 = popById[link.from_pop];
    const p2 = popById[link.to_pop];
    if (!p1 || !p2) return;
    const trunkLine = new google.maps.Polyline({
      path: [
        { lat: p1.lat, lng: p1.lng },
        { lat: p2.lat, lng: p2.lng },
      ],
      geodesic: true,
      strokeColor: "#1d4ed8",
      strokeOpacity: 0.65,
      strokeWeight: 3.5,
      map: gMap,
    });
    mapPolylines.push(trunkLine);
  });

  // 2. Draw 9 Regional Optical PoPs & Cloud Interconnects
  (cockpitState.pops || []).forEach((pop) => {
    const marker = new google.maps.Marker({
      position: { lat: pop.lat, lng: pop.lng },
      map: gMap,
      title: `${pop.pop_id}: ${pop.pop_name}`,
      zIndex: 100,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 9,
        fillColor: "#1d4ed8",
        fillOpacity: 1.0,
        strokeColor: "#ffffff",
        strokeWeight: 2.5,
      },
    });
    marker.addListener("click", () => {
      gInfoWindow.setContent(`
        <div style="font-family: sans-serif; max-width: 280px; padding: 4px;">
          <div style="font-size: 11px; font-weight: 700; color: #1d4ed8;">${pop.pop_id} · ${pop.pop_tier}</div>
          <div style="font-size: 13.5px; font-weight: 800; margin: 2px 0 4px;">${pop.pop_name}</div>
          <div style="font-size: 12px; color: #334155;">
            <strong>Address:</strong> ${pop.address}<br/>
            <strong>Platform:</strong> ${pop.router_platform}<br/>
            <strong>Available Ports:</strong> ${pop.available_10g_ports}x 10G / ${pop.available_100g_ports}x 100G<br/>
            <strong>Cloud On-Ramp:</strong> ${pop.cloud_onramp}<br/>
            <strong>Base EHR Latency:</strong> ${pop.base_ehr_latency_ms}ms
          </div>
        </div>
      `);
      gInfoWindow.open(gMap, marker);
    });
    popMarkers.push(marker);
  });

  // 3. Draw 45 Clinic Sites + Splice Closures + Optical Feed Polylines
  (cockpitState.sites || []).forEach((site) => {
    const isNearNet = site.network_status === "Near-Net";
    const pop = popById[site.pop_id];

    // Feed line from serving PoP to Splice Closure
    if (pop) {
      const feedLine = new google.maps.Polyline({
        path: [
          { lat: pop.lat, lng: pop.lng },
          { lat: site.splice_lat, lng: site.splice_lng },
        ],
        geodesic: true,
        strokeColor: isNearNet ? "#d97706" : "#10b981",
        strokeOpacity: isNearNet ? 0.65 : 0.28,
        strokeWeight: isNearNet ? 2.2 : 1.3,
        map: gMap,
      });
      mapPolylines.push(feedLine);
    }

    // For Near-Net sites (#28 & #33), draw the Splice Closure Vault marker and Lateral Extension Polyline
    if (isNearNet) {
      const spliceMarker = new google.maps.Marker({
        position: { lat: site.splice_lat, lng: site.splice_lng },
        map: gMap,
        title: `Splice Closure ${site.splice_closure_id} (${site.distance_to_splice_m}m to ${site.site_id})`,
        zIndex: 150,
        icon: {
          path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
          scale: 5,
          fillColor: "#dc2626",
          fillOpacity: 1.0,
          strokeColor: "#ffffff",
          strokeWeight: 1.5,
        },
      });
      spliceMarker.addListener("click", () => {
        gInfoWindow.setContent(`
          <div style="font-family: sans-serif; max-width: 260px; padding: 4px;">
            <div style="font-size: 11px; font-weight: 700; color: #dc2626;">SPLICE CLOSURE VAULT · ${site.splice_closure_id}</div>
            <div style="font-size: 12.5px; font-weight: 700; margin: 3px 0;">Serves ${site.site_id} (${site.city}, ${site.state})</div>
            <div style="font-size: 12px; color: #334155;">
              <strong>Lateral Extension Run:</strong> ${site.distance_to_splice_m} meters (&lt;150m Near-Net)<br/>
              <strong>Method:</strong> ${site.construction_method}<br/>
              <strong>Build CAPEX:</strong> $${site.build_capex_usd.toLocaleString()} (Waived via 36m Amortization)
            </div>
          </div>
        `);
        gInfoWindow.open(gMap, spliceMarker);
      });
      spliceMarkers.push(spliceMarker);

      const lateralLine = new google.maps.Polyline({
        path: [
          { lat: site.splice_lat, lng: site.splice_lng },
          { lat: site.lat, lng: site.lng },
        ],
        geodesic: true,
        strokeColor: "#dc2626",
        strokeOpacity: 0.95,
        strokeWeight: 4,
        map: gMap,
      });
      mapPolylines.push(lateralLine);
    }

    const marker = new google.maps.Marker({
      position: { lat: site.lat, lng: site.lng },
      map: gMap,
      title: `${site.site_id}: ${site.site_name} (${site.network_status})`,
      zIndex: isNearNet ? 200 : 80,
      label: isNearNet
        ? {
            text: `#${site.site_num}`,
            color: "#ffffff",
            fontSize: "10px",
            fontWeight: "bold",
          }
        : null,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: isNearNet ? 11 : 6.5,
        fillColor: isNearNet ? "#f59e0b" : "#10b981",
        fillOpacity: 0.95,
        strokeColor: "#ffffff",
        strokeWeight: isNearNet ? 2.5 : 1.5,
      },
    });

    marker.siteData = site;
    marker.addListener("click", () => {
      inspectClinicSite(site.site_id, true);
    });

    clinicMarkers.push(marker);
  });
}

function resetMapView() {
  if (!gMap) return;
  clinicMarkers.forEach((m) => m.setVisible(true));
  gMap.setCenter({ lat: 45.85, lng: -120.65 });
  gMap.setZoom(6);
}

function toggleMapFilter(mode) {
  clinicMarkers.forEach((m) => {
    const isNear = m.siteData.network_status === "Near-Net";
    if (mode === "nearnet") {
      m.setVisible(isNear);
    } else if (mode === "onnet") {
      m.setVisible(!isNear);
    } else {
      m.setVisible(true);
    }
  });
}

function focusNearNetSite(siteId) {
  switchTab("map");
  inspectClinicSite(siteId, true);
}

/* Live Cloud Spanner Point Inspection */
async function inspectClinicSite(siteId, panMap = true) {
  try {
    const res = await fetch(`/api/sites/${siteId}`);
    const data = await res.json();
    const s = data.site;
    const p = data.pop || {};
    const c = data.splice_closure || {};

    if (data.telemetry_log) {
      renderTelemetryLog(data.telemetry_log);
    }

    const badge = document.getElementById("inspector-latency-badge");
    if (badge) {
      badge.textContent = `${data.spanner_query_latency_ms}ms Spanner SQL`;
    }

    const body = document.getElementById("site-inspector-body");
    if (body && s) {
      const isNear = s.network_status === "Near-Net";
      body.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <span class="mono" style="font-weight: 800; font-size: 13px;">${s.site_id} · ${s.clinic_type}</span>
          <span class="status-pill ${isNear ? "nearnet" : "onnet"}">${s.network_status} (${s.distance_to_splice_m}m)</span>
        </div>
        <div style="font-weight: 800; font-size: 15px; margin-bottom: 4px;">${s.site_name}</div>
        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 12px;">
          ${s.address} <span class="mono">(${s.lat.toFixed(4)}, ${s.lng.toFixed(4)})</span>
        </div>

        <div class="grid-2" style="gap: 8px; margin-bottom: 12px;">
          <div style="background: var(--bg-subtle); padding: 8px 10px; border-radius: 6px;">
            <div style="font-size: 10.5px; color: var(--text-secondary); font-weight: 700;">OPTICAL EHR LATENCY</div>
            <div class="mono" style="font-size: 16px; font-weight: 800; color: var(--status-onnet);">${s.estimated_ehr_latency_ms}ms</div>
            <div style="font-size: 10.5px; color: var(--text-muted);">Legacy WAN: ${s.legacy_wan_latency_ms}ms | SLA &lt;12ms</div>
          </div>
          <div style="background: var(--bg-subtle); padding: 8px 10px; border-radius: 6px;">
            <div style="font-size: 10.5px; color: var(--text-secondary); font-weight: 700;">LATERAL BUILD CAPEX</div>
            <div class="mono" style="font-size: 16px; font-weight: 800; color: ${isNear ? "var(--status-nearnet)" : "var(--status-onnet)"};">$${s.build_capex_usd.toLocaleString()}</div>
            <div style="font-size: 10.5px; color: var(--text-muted);">${isNear ? "Waived via 36m Amortization" : "Zero Build (Lit On-Net)"}</div>
          </div>
        </div>

        <div style="font-size: 12px; line-height: 1.6; border-top: 1px solid var(--border-light); padding-top: 8px;">
          <div><strong>Serving Optical PoP:</strong> <span class="mono">${s.pop_id}</span> (${p.city || ""}, ${p.state || ""} — ${data.fiber_route_km_to_pop} km optical route)</div>
          <div><strong>Nearest Splice Closure:</strong> <span class="mono">${s.splice_closure_id}</span> (${s.distance_to_splice_m}m · ${c.available_dark_strands || 24} dark strands free)</div>
          <div><strong>Port Reservation:</strong> ${s.port_readiness}</div>
          <div><strong>Construction Method:</strong> ${s.construction_method}</div>
          <div><strong>Optical Loss Budget:</strong> <span class="mono">${s.optical_loss_budget_db} dB</span> (ITU-T G.652.D SMF)</div>
          <div><strong>Monthly Recurring (MRC):</strong> <span class="mono">$${s.monthly_mrc_usd.toLocaleString()}/mo</span></div>
        </div>

        <div class="sql-block">${data.sql_executed}</div>
      `;
    }

    if (panMap && gMap && s) {
      gMap.panTo({ lat: s.lat, lng: s.lng });
      gMap.setZoom(s.network_status === "Near-Net" ? 16 : 12);
      const targetMarker = clinicMarkers.find((m) => m.siteData.site_id === siteId);
      if (targetMarker && gInfoWindow) {
        const isNear = s.network_status === "Near-Net";
        gInfoWindow.setContent(`
          <div style="font-family: sans-serif; max-width: 280px; padding: 4px;">
            <div style="font-size: 11px; font-weight: 700; color: ${isNear ? "#d97706" : "#059669"};">
              ${s.site_id} · ${s.network_status.toUpperCase()} (${s.distance_to_splice_m}m from ${s.splice_closure_id})
            </div>
            <div style="font-size: 13.5px; font-weight: 800; margin: 2px 0 4px;">${s.site_name}</div>
            <div style="font-size: 12px; color: #334155;">
              <strong>Address:</strong> ${s.address}<br/>
              <strong>EHR Latency:</strong> <strong>${s.estimated_ehr_latency_ms}ms</strong> (Legacy: ${s.legacy_wan_latency_ms}ms · SLA &lt;12ms)<br/>
              <strong>Port / Build:</strong> ${s.construction_method}<br/>
              <strong>Build CAPEX:</strong> $${s.build_capex_usd.toLocaleString()} ${isNear ? "(36m Amortized)" : "(Lit On-Net)"}
            </div>
          </div>
        `);
        gInfoWindow.open(gMap, targetMarker);
      }
    }
  } catch (err) {
    console.error("Failed to inspect site:", err);
  }
}

/* Render 45-Site Schedule Table */
function renderSitesTable(sites) {
  const tbody = document.getElementById("sites-table-body");
  if (!tbody) return;
  tbody.innerHTML = sites
    .map((s) => {
      const isNear = s.network_status === "Near-Net";
      return `
        <tr class="${isNear ? "row-nearnet" : ""}" onclick="inspectClinicSite('${s.site_id}', true)">
          <td class="mono"><strong>${s.site_id}</strong></td>
          <td>
            <strong>${s.site_name}</strong>
            <div style="font-size: 11px; color: var(--text-secondary);">${s.address}</div>
          </td>
          <td><span class="status-pill ${isNear ? "nearnet" : "onnet"}">${s.network_status}</span></td>
          <td class="mono">${s.pop_id}</td>
          <td class="mono">${s.splice_closure_id}</td>
          <td class="mono"><strong>${s.distance_to_splice_m}m</strong></td>
          <td class="mono" style="color: var(--status-onnet); font-weight: 700;">${s.estimated_ehr_latency_ms}ms</td>
          <td class="mono" style="color: ${s.legacy_wan_latency_ms > 12 ? "var(--status-critical)" : "var(--text-muted)"};">${s.legacy_wan_latency_ms}ms</td>
          <td style="font-size: 12px;">${s.construction_method}</td>
          <td class="mono"><strong>$${s.build_capex_usd.toLocaleString()}</strong></td>
        </tr>
      `;
    })
    .join("");
}

/* Render Grounding Documents Grid */
function renderGroundingDocuments(docs) {
  const container = document.getElementById("grounding-doc-grid");
  if (!container) return;
  container.innerHTML = docs
    .map(
      (d) => `
      <div class="doc-card">
        <div>
          <div style="font-size: 11px; font-weight: 700; color: var(--brand-primary); text-transform: uppercase;">${d.doc_type} · ${d.pages} Pages</div>
          <div style="font-weight: 700; font-size: 13px; margin: 4px 0;">${d.title}</div>
          <div style="font-size: 12px; color: var(--text-secondary);">${d.summary}</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 8px; border-top: 1px solid var(--border-light);">
          <span class="mono" style="font-size: 11px; color: var(--text-muted);">${d.filename}</span>
          <a class="btn btn-outline" style="padding: 4px 10px; font-size: 11.5px;" href="/api/docs/${d.filename}" target="_blank">Open PDF &#8599;</a>
        </div>
      </div>
    `
    )
    .join("");
}

/* 200-Question Compliance Matrix */
async function filterComplianceQuestions(status, category) {
  currentStatusFilter = status;
  currentCategoryFilter = category;
  const searchVal = document.getElementById("question-search-input")?.value || "";

  document.getElementById("filter-q-all")?.classList.toggle("btn-primary", status === "all");
  document.getElementById("filter-q-all")?.classList.toggle("btn-outline", status !== "all");
  document.getElementById("filter-q-auto")?.classList.toggle("btn-primary", status === "auto");
  document.getElementById("filter-q-auto")?.classList.toggle("btn-outline", status !== "auto");

  const params = new URLSearchParams({
    status: status,
    category: category,
    search: searchVal,
  });

  try {
    const res = await fetch(`/api/questions?${params.toString()}`);
    const data = await res.json();
    renderQuestionsTable(data.questions || [], data.counts || {});
  } catch (err) {
    console.error("Failed to load questions:", err);
  }
}

function debouncedQuestionSearch() {
  clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => {
    filterComplianceQuestions(currentStatusFilter, currentCategoryFilter);
  }, 200);
}

function renderQuestionsTable(questions, counts) {
  const tbody = document.getElementById("questions-table-body");
  if (!tbody) return;

  if (counts.all) {
    const tabCount = document.getElementById("tab-count-compliance");
    if (tabCount) {
      tabCount.textContent = `${counts.auto + counts.review_approved}/${counts.all} Ready`;
    }
  }

  tbody.innerHTML = questions
    .map((q) => {
      const isAuto = q.status === "Auto-Answered";
      const isApproved = q.sme_approved;
      return `
        <tr class="${!isAuto && !isApproved ? "row-nearnet" : ""}">
          <td class="mono">
            <strong>${q.question_id}</strong><br/>
            <span class="status-pill ${isAuto ? "onnet" : "nearnet"}" style="margin-top: 4px;">${q.category}</span>
          </td>
          <td>
            <div style="font-weight: 700; font-size: 12px; color: var(--text-secondary); margin-bottom: 2px;">${q.domain}</div>
            <div style="font-size: 12.5px;">${q.question_text}</div>
            ${
              !isAuto
                ? `<div style="margin-top: 6px; font-size: 11.5px; color: var(--status-nearnet);"><strong>SME Flag (${q.risk_level} Risk):</strong> ${q.review_reason}</div>`
                : ""
            }
          </td>
          <td>
            <div id="ans-view-${q.question_id}" style="font-size: 12.5px; line-height: 1.45;">${q.answer_text}</div>
          </td>
          <td>
            <a href="/api/docs/${q.source_doc}" target="_blank" style="font-weight: 700; font-size: 12px; color: var(--brand-primary); text-decoration: none;">
              &#128196; ${q.source_doc} &#8599;
            </a>
            <div class="mono" style="font-size: 11px; color: var(--text-secondary); margin-top: 3px;">${q.source_citation}</div>
          </td>
          <td>
            ${
              isAuto
                ? `<span class="status-pill onnet">&#10003; Auto (100% Conf.)</span>`
                : isApproved
                ? `<span class="status-pill onnet">&#10003; SME Approved</span>`
                : `
                  <div style="display: flex; flex-direction: column; gap: 6px;">
                    <span class="status-pill nearnet">Review (${q.confidence_pct}% Conf.)</span>
                    <button class="btn btn-emerald" style="padding: 4px 8px; font-size: 11.5px;" onclick="approveSingleQuestion('${q.question_id}')">
                      &#10003; Approve Answer
                    </button>
                  </div>
                `
            }
          </td>
        </tr>
      `;
    })
    .join("");
}

async function approveSingleQuestion(questionId) {
  try {
    const res = await fetch(`/api/questions/${questionId}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ approved: true }),
    });
    const data = await res.json();
    if (data.telemetry_log) renderTelemetryLog(data.telemetry_log);
    await filterComplianceQuestions(currentStatusFilter, currentCategoryFilter);
  } catch (err) {
    console.error("Failed to approve question:", err);
  }
}

async function approveAllFlaggedQuestions() {
  try {
    const res = await fetch("/api/questions/approve-all-flagged", { method: "POST" });
    const data = await res.json();
    if (data.telemetry_log) renderTelemetryLog(data.telemetry_log);
    await filterComplianceQuestions(currentStatusFilter, currentCategoryFilter);
    appendChatBubble(
      "agent",
      `<strong>[SME Compliance Governance]</strong> All 15 flagged human-review questions (including <code>Q-052 Custom BGP routing</code> and <code>Q-139 &lt;12ms SLA credits</code>) have been approved and persisted to BigQuery.`
    );
  } catch (err) {
    console.error("Failed to approve all flagged questions:", err);
  }
}

/* Deal Economics Simulator & Pricing Table */
async function runEconomicsSimulation() {
  const amortMonths = parseInt(document.getElementById("sim-amort-months")?.value || "36", 10);
  const discountPct = parseFloat(document.getElementById("sim-discount-slider")?.value || "0");
  const discountLabel = document.getElementById("sim-discount-label");
  if (discountLabel) discountLabel.textContent = `${discountPct.toFixed(1)}%`;

  try {
    const res = await fetch("/api/simulate-economics", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        amortization_months: amortMonths,
        discount_pct: discountPct,
        include_near_net_sites: true,
      }),
    });
    const econ = await res.json();
    renderEconomicsMetrics(econ);
    if (econ.telemetry_log) renderTelemetryLog(econ.telemetry_log);
  } catch (err) {
    console.error("Failed to simulate economics:", err);
  }
}

function renderEconomicsMetrics(econ) {
  if (!econ || !econ.monthly_recurring_revenue_usd) return;
  const mrrEl = document.getElementById("sim-mrr");
  const tcvEl = document.getElementById("sim-tcv");
  const marginEl = document.getElementById("sim-margin");
  const winEl = document.getElementById("sim-winprob");
  const nreNoteEl = document.getElementById("sim-nre-note");
  const guardrailEl = document.getElementById("sim-guardrail-pill");

  if (mrrEl) mrrEl.textContent = `$${econ.monthly_recurring_revenue_usd.toLocaleString()}`;
  if (tcvEl) {
    const term = econ.amortization_months || 36;
    tcvEl.textContent = `TCV: $${econ.total_contract_value_usd.toLocaleString()} (${term}m)`;
  }
  if (marginEl) marginEl.textContent = `${econ.gross_margin_pct}%`;
  if (winEl) winEl.textContent = `${econ.estimated_win_probability_pct}%`;
  if (nreNoteEl) {
    nreNoteEl.textContent =
      econ.upfront_nre_charged_usd === 0
        ? `$0 Upfront NRE ($${econ.monthly_amortized_capex_usd}/mo amort.)`
        : `$${econ.upfront_nre_charged_usd.toLocaleString()} Upfront NRE Billed`;
  }
  if (guardrailEl) {
    guardrailEl.className = `status-pill ${econ.meets_margin_guardrail ? "onnet" : "critical"}`;
    guardrailEl.textContent = econ.meets_margin_guardrail
      ? `Margin Guardrail: PASS (${econ.gross_margin_pct}% >= 40%)`
      : `Margin Guardrail: BELOW 40% FLOOR (${econ.gross_margin_pct}%)`;
  }

  // Update top banner KPI as well
  const topMargin = document.getElementById("kpi-margin");
  if (topMargin) {
    topMargin.textContent = `${econ.gross_margin_pct}% ($${(econ.total_contract_value_usd / 1e6).toFixed(2)}M TCV)`;
  }
  const tabMargin = document.getElementById("tab-count-margin");
  if (tabMargin) {
    tabMargin.textContent = `${econ.gross_margin_pct}% Margin`;
  }
}

function renderPricingTable(items) {
  const tbody = document.getElementById("pricing-table-body");
  if (!tbody) return;
  tbody.innerHTML = items
    .map(
      (item) => `
      <tr>
        <td class="mono"><strong>${item.sku_id}</strong></td>
        <td><strong>${item.product_name}</strong></td>
        <td>${item.category}</td>
        <td class="mono">${item.quantity}</td>
        <td class="mono">$${item.unit_list_mrc_usd.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
        <td class="mono"><strong>$${item.unit_proposed_mrc_usd.toLocaleString(undefined, { minimumFractionDigits: 2 })}</strong></td>
        <td class="mono" style="color: var(--brand-primary); font-weight: 700;">$${item.total_monthly_mrc_usd.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
        <td style="font-size: 12px;">${item.sla_tier}</td>
      </tr>
    `
    )
    .join("");
}

/* 1-Click Commercial VP Sign-Off */
async function submitVpSignoff() {
  const amortMonths = parseInt(document.getElementById("sim-amort-months")?.value || "36", 10);
  const discountPct = parseFloat(document.getElementById("sim-discount-slider")?.value || "0");
  try {
    const res = await fetch("/api/signoff", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        approver_name: "Elena Rostova, SVP Commercial & Enterprise Markets",
        amortization_months: amortMonths,
        discount_override_pct: discountPct,
        comments: "Approved 36-month Near-Net CAPEX amortization ($4,200); 42.4% Gross Margin verified.",
      }),
    });
    const data = await res.json();
    renderSignoffCard(data.signoff_state, data.economics);
    if (data.telemetry_log) renderTelemetryLog(data.telemetry_log);
    appendChatBubble(
      "agent",
      `<strong>[Executive Sign-Off Complete]</strong> Proposal <code>PROP-APEX-2026-1012</code> digitally approved by <strong>${data.signoff_state.approver_name}</strong> at ${data.signoff_state.approved_at}. Ready for submission to Apex Health.`
    );
  } catch (err) {
    console.error("VP sign-off error:", err);
  }
}

function renderSignoffCard(state, econ) {
  if (!state) return;
  const badge = document.getElementById("signoff-status-badge");
  const btn = document.getElementById("btn-vp-signoff");
  const ts = document.getElementById("vp-signoff-timestamp");
  const pipeStatus = document.getElementById("pipeline-vp-status");

  if (state.signed_off) {
    if (badge) {
      badge.textContent = `SIGNED OFF (${state.approved_at})`;
      badge.style.background = "rgba(16,185,129,0.3)";
    }
    if (btn) {
      btn.textContent = "✓ Approved & Digitally Signed by Commercial VP";
      btn.disabled = true;
    }
    if (ts) {
      ts.innerHTML = `<strong style="color: var(--status-onnet);">APPROVED AT ${state.approved_at}:</strong> ${state.comments}`;
    }
    if (pipeStatus) {
      pipeStatus.className = "status-pill onnet";
      pipeStatus.textContent = "VP APPROVED & SIGNED";
    }
  }
}

/* Copilot Chat */
async function handleChatSubmit(event) {
  event.preventDefault();
  const input = document.getElementById("chat-input");
  if (!input || !input.value.trim()) return;
  const msg = input.value.trim();
  input.value = "";
  await sendQuickPrompt(msg);
}

async function sendQuickPrompt(message) {
  appendChatBubble("user", message);
  appendChatBubble("agent", `<em id="pending-chat-indicator">Querying Cloud Spanner, BigQuery &amp; Vertex AI Search...</em>`);

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    const pending = document.getElementById("pending-chat-indicator");
    if (pending && pending.parentElement) {
      pending.parentElement.innerHTML = formatMarkdownSimple(data.reply) +
        `<div class="mono" style="margin-top: 6px; font-size: 10.5px; color: var(--text-muted);">Grounded in ${data.latency_ms}ms · Spanner + BigQuery + Vertex Search</div>`;
    }
    if (data.telemetry_log) renderTelemetryLog(data.telemetry_log);
  } catch (err) {
    console.error("Chat error:", err);
  }
}

function appendChatBubble(role, htmlContent) {
  const container = document.getElementById("chat-messages");
  if (!container) return;
  const div = document.createElement("div");
  div.className = `chat-bubble ${role}`;
  div.innerHTML = htmlContent;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function formatMarkdownSimple(text) {
  if (!text) return "";
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/`(.*?)`/g, "<code class='mono'>$1</code>")
    .replace(/\n- /g, "<br/>• ")
    .replace(/\n\* /g, "<br/>• ")
    .replace(/\n/g, "<br/>");
}

/* Telemetry Log Rendering */
function renderTelemetryLog(logs) {
  const container = document.getElementById("telemetry-log-container");
  if (!container) return;
  const countEl = document.getElementById("tab-count-telemetry");
  if (countEl) countEl.textContent = `${logs.length} Queries`;

  container.innerHTML = logs
    .map(
      (entry) => `
      <div style="border: 1px solid var(--border-light); border-radius: 6px; padding: 10px 12px; margin-bottom: 10px; background: var(--bg-surface);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <span class="status-pill onnet">${entry.source}</span>
            <strong style="margin-left: 8px; font-size: 13px;">${entry.operation}</strong>
          </div>
          <div class="mono" style="font-size: 12px; color: var(--brand-primary); font-weight: 700;">
            ${entry.latency_ms}ms · ${entry.rows_returned} rows · ${entry.timestamp}
          </div>
        </div>
        <div class="sql-block">${entry.query}</div>
      </div>
    `
    )
    .join("");
}

async function refreshLiveGcpDatabases() {
  try {
    const res = await fetch("/api/refresh-live-db", { method: "POST" });
    const data = await res.json();
    if (data.telemetry_log) renderTelemetryLog(data.telemetry_log);
  } catch (err) {
    console.error("Failed live DB refresh:", err);
  }
}
