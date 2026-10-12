/**
 * Main Workbench Application Controller.
 * Handles state, tabs, REST calls, UI rendering, review queue actions, and export.
 */

const API_BASE = ''; // Same origin
let appState = {
  dashboard: null,
  sources: [],
  entities: [],
  ambiguities: [],
  timeline: [],
  graph: null,
  signals: [],
  contradictions: [],
  circularReporting: [],
  reviewQueue: [],
  auditLog: [],
  report: null,
  piiRedacted: false
};

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  loadAllData();
  setupEventListeners();
});

function initTabs() {
  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-tab');
      switchTab(target);
    });
  });
}

function switchTab(tabId) {
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

  const activeTab = document.querySelector(`.nav-tab[data-tab="${tabId}"]`);
  const activePanel = document.getElementById(`panel-${tabId}`);

  if (activeTab && activePanel) {
    activeTab.classList.add('active');
    activePanel.classList.add('active');

    // Resize graph if switching to knowledge graph
    if (tabId === 'graph' && typeof cy !== 'undefined' && cy) {
      setTimeout(() => {
        cy.resize();
        cy.fit(null, 40);
      }, 100);
    }
  }
}

async function loadAllData() {
  try {
    showLoading();
    const [dashRes, srcRes, entRes, timeRes, graphRes, sigRes, contraRes, revRes, auditRes] = await Promise.all([
      fetch(`${API_BASE}/api/dashboard`).then(r => r.json()),
      fetch(`${API_BASE}/api/sources`).then(r => r.json()),
      fetch(`${API_BASE}/api/entities`).then(r => r.json()),
      fetch(`${API_BASE}/api/timeline`).then(r => r.json()),
      fetch(`${API_BASE}/api/graph/cytoscape`).then(r => r.json()),
      fetch(`${API_BASE}/api/weak-signals`).then(r => r.json()),
      fetch(`${API_BASE}/api/contradictions`).then(r => r.json()),
      fetch(`${API_BASE}/api/review-queue`).then(r => r.json()),
      fetch(`${API_BASE}/api/audit-log`).then(r => r.json())
    ]);

    appState.dashboard = dashRes;
    appState.sources = srcRes;
    appState.entities = entRes.entities;
    appState.ambiguities = entRes.unresolved_ambiguities;
    appState.timeline = timeRes;
    appState.graph = graphRes;
    appState.signals = sigRes;
    appState.contradictions = contraRes.contradictions;
    appState.circularReporting = contraRes.circular_reporting;
    appState.reviewQueue = revRes;
    appState.auditLog = auditRes;

    renderDashboard();
    renderSources();
    renderEntities();
    renderTimeline();
    renderGraph();
    renderWeakSignals();
    renderContradictions();
    renderReviewQueue();
    renderAuditLog();
    loadReport();

    hideLoading();
  } catch (err) {
    console.error('Failed to load workbench data:', err);
    hideLoading();
  }
}

function renderDashboard() {
  const d = appState.dashboard;
  if (!d) return;

  document.getElementById('stat-sources').textContent = d.total_sources;
  document.getElementById('stat-entities').textContent = d.total_entities;
  document.getElementById('stat-events').textContent = d.total_events;
  document.getElementById('stat-signals').textContent = d.total_weak_signals;
  document.getElementById('stat-contradictions').textContent = d.contradictions_count;
  document.getElementById('stat-review-pending').textContent = d.review_queue_pending;

  // Update nav badges
  const revBadge = document.getElementById('badge-review-count');
  if (revBadge) revBadge.textContent = d.review_queue_pending;
  const contraBadge = document.getElementById('badge-contra-count');
  if (contraBadge) contraBadge.textContent = d.contradictions_count;

  // Audio disclosure notice
  const audioBox = document.getElementById('audio-capability-notice');
  if (audioBox && d.audio_capabilities) {
    const aud = d.audio_capabilities;
    audioBox.innerHTML = `
      <div class="alert-box alert-warning">
        <div class="alert-icon">🎙️</div>
        <div class="alert-content">
          <h4>Audio & Speech Capability Disclosure</h4>
          <p>${aud.status_message}</p>
          <ul style="margin-top: 0.5rem; font-size: 0.8rem; color: var(--text-muted); padding-left: 1.25rem;">
            ${aud.next_practical_steps.map(s => `<li>${s}</li>`).join('')}
          </ul>
        </div>
      </div>
    `;
  }
}

function renderSources() {
  const container = document.getElementById('sources-list-container');
  if (!container) return;

  container.innerHTML = appState.sources.map(s => {
    let audioHtml = '';
    if (s.audio_timestamps && s.audio_timestamps.length) {
      audioHtml = `
        <div class="audio-timeline-box">
          <div style="font-size: 0.8rem; font-weight: 600; color: var(--accent-indigo); margin-bottom: 0.5rem;">
            📻 Authorized Radio Recording Transcript Segments & Timecodes:
          </div>
          ${s.audio_timestamps.map(t => `
            <div style="display: flex; gap: 0.75rem; font-size: 0.78rem; margin-bottom: 0.35rem;">
              <span style="font-family: var(--font-mono); color: var(--accent-cyan); font-weight: 600;">[${t.time}]</span>
              <span style="color: #cbd5e1;">${t.speaker}: ${t.content}</span>
            </div>
          `).join('')}
        </div>
      `;
    }

    return `
      <div class="source-card">
        <div class="source-card-header">
          <div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <span class="badge" style="background: rgba(6, 182, 212, 0.15); color: #38bdf8; font-family: var(--font-mono);">${s.id}</span>
              <h4 class="source-card-title">${s.title}</h4>
            </div>
            <div class="source-card-meta">
              <span><strong>Publisher:</strong> ${s.source_org}</span>
              <span><strong>Type:</strong> ${s.source_type}</span>
              <span><strong>Language:</strong> ${s.original_language_name}</span>
              <span><strong>Date:</strong> ${s.publication_date || 'N/A'}</span>
              <span><strong>Reliability:</strong> ${(s.source_reliability_score * 100).toFixed(0)}%</span>
            </div>
          </div>
          <div style="display: flex; gap: 0.4rem;">
            ${s.is_primary_source ? `<span class="badge badge-lawful">Primary Source</span>` : `<span class="badge badge-classified">Secondary / Derivative</span>`}
            ${s.possible_duplicate_flag ? `<span class="badge" style="background: rgba(244,63,94,0.2); color: #fda4af;">Duplicate Risk</span>` : ''}
          </div>
        </div>

        <div class="text-compare-split">
          <div class="script-box">
            <div class="script-box-label">
              <span>Original Script & Text (${s.original_language_name})</span>
              <span>${s.is_mixed_language ? 'Code-Mixed' : 'Monolingual'}</span>
            </div>
            <p style="white-space: pre-wrap;">${applyPiiRedaction(s.original_text)}</p>
          </div>

          <div class="script-box" style="border-left: 2px solid var(--accent-indigo);">
            <div class="script-box-label" style="color: var(--accent-indigo);">
              <span>English Translation & Cross-Lingual Alignment</span>
              <span>${s.translation_status}</span>
            </div>
            <p style="white-space: pre-wrap;">${applyPiiRedaction(s.english_translation || 'N/A')}</p>
          </div>
        </div>

        ${audioHtml}
      </div>
    `;
  }).join('');
}

function renderEntities() {
  const container = document.getElementById('entities-table-container');
  if (!container) return;

  const ambiguityNotice = document.getElementById('entity-ambiguity-notice');
  if (ambiguityNotice && appState.ambiguities.length) {
    ambiguityNotice.innerHTML = `
      <div class="alert-box alert-warning">
        <div class="alert-icon">⚖️</div>
        <div class="alert-content">
          <h4>Conservative Entity Resolution Alert</h4>
          <p>The resolver identified potential name collisions but conservatively isolated them:</p>
          <ul style="margin-top: 0.5rem; font-size: 0.85rem; color: #fde68a;">
            ${appState.ambiguities.map(a => `<li><strong>${a.entity_1_name}</strong> vs <strong>${a.entity_2_name}</strong>: ${a.justification}</li>`).join('')}
          </ul>
        </div>
      </div>
    `;
  }

  container.innerHTML = `
    <table class="report-paper" style="width: 100%; margin: 0;">
      <thead>
        <tr>
          <th>ID</th>
          <th>Canonical Name</th>
          <th>Class</th>
          <th>Scripts / Indic Names</th>
          <th>Transliteration Aliases</th>
          <th>Involvement Status</th>
          <th>Resolution Status</th>
          <th>Sources</th>
        </tr>
      </thead>
      <tbody>
        ${appState.entities.map(e => `
          <tr>
            <td><code>${e.id}</code></td>
            <td><strong>${e.canonical_name}</strong></td>
            <td><span class="badge" style="background: rgba(255,255,255,0.08);">${e.entity_type}</span></td>
            <td>
              ${Object.entries(e.original_script_names || {}).map(([k, v]) => `<div><small style="color: var(--accent-cyan);">${k.toUpperCase()}:</small> ${v}</div>`).join('')}
            </td>
            <td><small>${(e.alternative_spellings || []).join(', ')}</small></td>
            <td>
              ${e.verified_involvement 
                ? `<span class="badge badge-lawful">Verified Actor</span>` 
                : `<span class="badge" style="background: rgba(148,163,184,0.15); color: #94a3b8;">Mentioned Only</span>`}
            </td>
            <td><code>${e.resolution_status}</code></td>
            <td>${e.source_ids.map(s => `<code>${s}</code>`).join(' ')}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

function renderTimeline() {
  const container = document.getElementById('timeline-container');
  if (!container) return;

  container.innerHTML = `
    <div class="timeline-list">
      ${appState.timeline.map(ev => {
        const isContra = ev.verification_status === 'contradicted';
        return `
          <div class="timeline-item ${isContra ? 'contradicted' : ''}">
            <div class="timeline-header">
              <span class="timeline-date">🗓️ ${ev.event_date || 'Unconfirmed'} ${ev.date_end ? '➔ ' + ev.date_end : ''}</span>
              <div>
                <span class="badge ${isContra ? 'badge-classified' : 'badge-lawful'}">${ev.verification_status.toUpperCase()}</span>
                <span class="badge" style="background: rgba(255,255,255,0.08);">${ev.temporal_status}</span>
              </div>
            </div>
            <h4 style="font-size: 1.05rem; font-weight: 600; margin-bottom: 0.35rem; color: #fff;">${ev.title}</h4>
            <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 0.75rem;">${ev.description}</p>
            <div style="font-size: 0.8rem; color: var(--text-dim); display: flex; gap: 1rem; flex-wrap: wrap;">
              <span>📍 <strong>Location:</strong> ${ev.location_name} (<em>${ev.location_precision}</em>)</span>
              <span>📰 <strong>Sources:</strong> ${ev.source_ids.map(s => `<code>${s}</code>`).join(', ')}</span>
            </div>
            ${ev.date_uncertainty ? `
              <div style="margin-top: 0.5rem; font-size: 0.78rem; color: #fde68a;">
                ⏳ <strong>Temporal Uncertainty:</strong> ${ev.date_uncertainty}
              </div>
            ` : ''}
            ${ev.contradictory_accounts && ev.contradictory_accounts.length ? `
              <div style="margin-top: 0.5rem; padding: 0.5rem; background: rgba(244,63,94,0.1); border-left: 3px solid var(--accent-rose); border-radius: 4px; font-size: 0.78rem; color: #fda4af;">
                ${ev.contradictory_accounts.join('<br>')}
              </div>
            ` : ''}
          </div>
        `;
      }).join('')}
    </div>
  `;
}

function renderGraph() {
  if (appState.graph && appState.graph.elements) {
    initGraphViewer(appState.graph.elements);
  }
}

function renderWeakSignals() {
  const container = document.getElementById('signals-container');
  if (!container) return;

  container.innerHTML = appState.signals.map(sig => `
    <div class="signal-card">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
        <div>
          <span class="badge" style="background: rgba(168,85,247,0.2); color: #c084fc; font-family: var(--font-mono);">${sig.id}</span>
          <h4 style="font-size: 1.15rem; font-weight: 600; color: #fff; margin-top: 0.3rem;">${sig.title}</h4>
        </div>
        <div class="signal-badges">
          <span class="badge badge-score">Strength: ${sig.signal_strength}</span>
          <span class="badge" style="background: rgba(6,182,212,0.15); color: #38bdf8;">Evidence Conf: ${sig.evidence_confidence}</span>
          ${sig.confidence_breakdown ? `<span class="badge" style="background: rgba(16,185,129,0.15); color: #34d399;">Score: ${sig.confidence_breakdown.composite_heuristic_score}</span>` : ''}
        </div>
      </div>

      <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 0.85rem;">${sig.description}</p>

      <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 1rem; font-size: 0.85rem; line-height: 1.6; margin-bottom: 0.85rem;">
        <p><strong>Operational Significance:</strong> ${sig.significance_rationale}</p>
        <div style="margin-top: 0.5rem;">
          <strong style="color: #fde68a;">Alternative Explanations & Counterevidence:</strong>
          <ul style="padding-left: 1.25rem; color: var(--text-muted);">
            ${sig.alternative_explanations.map(a => `<li>${a}</li>`).join('')}
            ${sig.counterevidence.map(c => `<li><em>Counterevidence:</em> ${c}</li>`).join('')}
          </ul>
        </div>
        <div style="margin-top: 0.5rem;">
          <strong style="color: #6ee7b7;">Targeted Verification Step:</strong>
          <ul style="padding-left: 1.25rem; color: var(--text-muted);">
            ${sig.recommended_verification_steps.map(v => `<li>${v}</li>`).join('')}
          </ul>
        </div>
      </div>

      <div style="display: flex; gap: 0.5rem; font-size: 0.75rem; color: var(--text-dim);">
        <span>Sources: ${sig.supporting_source_ids.map(s => `<code>${s}</code>`).join(' ')}</span>
        <span>•</span>
        <span>Entities: ${sig.supporting_entity_ids.map(e => `<code>${e}</code>`).join(' ')}</span>
      </div>
    </div>
  `).join('');
}

function renderContradictions() {
  const container = document.getElementById('contradictions-container');
  if (!container) return;

  let circHtml = '';
  if (appState.circularReporting && appState.circularReporting.length) {
    circHtml = `
      <div style="margin-bottom: 1.5rem;">
        ${appState.circularReporting.map(c => `
          <div class="alert-box alert-danger">
            <div class="alert-icon">🔄</div>
            <div class="alert-content">
              <h4>${c.id}: Circular Reporting Loop Detected</h4>
              <p><strong>Primary Source:</strong> <code>${c.primary_or_prior_source_id}</code> (${c.primary_or_prior_title})</p>
              <p><strong>Secondary Aggregator:</strong> <code>${c.derivative_source_id}</code> (${c.derivative_title})</p>
              <p style="margin-top: 0.35rem; color: #fca5a5;">${c.similarity_rationale}</p>
              <p style="margin-top: 0.35rem; font-weight: 600; color: #fff;">${c.analytical_impact}</p>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  let contraHtml = appState.contradictions.map(con => `
    <div class="panel-card">
      <div class="panel-header">
        <h3>⚡ [${con.id}] Discrepancy: ${con.dimension}</h3>
        <span class="badge badge-classified">UNRESOLVED FACTUAL CONFLICT</span>
      </div>
      <div class="grid-2">
        <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 1rem; border-left: 3px solid var(--accent-cyan);">
          <div style="font-size: 0.75rem; color: var(--accent-cyan); font-weight: 600; text-transform: uppercase;">
            Account A (${con.claim_a.source_ids.join(', ')})
          </div>
          <div style="font-size: 1.1rem; font-weight: 700; color: #fff; margin: 0.4rem 0;">
            ${con.claim_a.value}
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted);">${con.claim_a.provenance}</p>
          <small style="color: var(--text-dim);">${con.claim_a.authority_level}</small>
        </div>

        <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 1rem; border-left: 3px solid var(--accent-rose);">
          <div style="font-size: 0.75rem; color: var(--accent-rose); font-weight: 600; text-transform: uppercase;">
            Account B (${con.claim_b.source_ids.join(', ')})
          </div>
          <div style="font-size: 1.1rem; font-weight: 700; color: #fff; margin: 0.4rem 0;">
            ${con.claim_b.value}
          </div>
          <p style="font-size: 0.8rem; color: var(--text-muted);">${con.claim_b.provenance}</p>
          <small style="color: var(--text-dim);">${con.claim_b.authority_level}</small>
        </div>
      </div>
      <div style="margin-top: 1rem; padding: 0.85rem; background: rgba(99,102,241,0.08); border-radius: 6px; font-size: 0.85rem;">
        <p><strong>Analytical Assessment:</strong> ${con.analytical_assessment}</p>
        <p style="margin-top: 0.35rem; color: var(--accent-cyan);"><strong>Recommended Resolution:</strong> ${con.recommended_verification}</p>
      </div>
    </div>
  `).join('');

  container.innerHTML = circHtml + contraHtml;
}

function renderReviewQueue() {
  const container = document.getElementById('review-queue-container');
  if (!container) return;

  container.innerHTML = appState.reviewQueue.map(item => {
    const isApproved = item.current_status === 'analyst_approved';
    const isRejected = item.current_status === 'rejected';
    const statusClass = isApproved ? 'approved' : (isRejected ? 'rejected' : 'pending');

    return `
      <div class="review-item ${statusClass}" id="queue-item-${item.id}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
          <div>
            <span class="badge" style="background: rgba(255,255,255,0.08); font-family: var(--font-mono);">${item.id}</span>
            <span class="badge" style="background: rgba(99,102,241,0.15); color: #a5b4fc;">${item.item_type}</span>
            <h4 style="font-size: 1.05rem; font-weight: 600; color: #fff; margin-top: 0.25rem;">${item.title}</h4>
          </div>
          <span class="badge ${isApproved ? 'badge-lawful' : (isRejected ? 'badge-classified' : 'badge-classified')}">
            ${item.current_status.toUpperCase()}
          </span>
        </div>

        <p style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 0.75rem;">${item.description}</p>

        <div style="background: rgba(0,0,0,0.3); border-radius: 6px; padding: 0.75rem; font-size: 0.82rem; margin-bottom: 0.75rem;">
          <p><strong>Machine Hypothesis:</strong> <code>${item.machine_hypothesis}</code> (Confidence: ${item.machine_confidence})</p>
          ${item.supporting_excerpts && item.supporting_excerpts.length ? `
            <div style="margin-top: 0.35rem; color: var(--text-muted);">
              ${item.supporting_excerpts.map(e => `<blockquote>"${e}"</blockquote>`).join('')}
            </div>
          ` : ''}
        </div>

        ${item.analyst_rationale ? `
          <div style="padding: 0.5rem 0.75rem; background: rgba(16,185,129,0.1); border-left: 3px solid var(--accent-emerald); border-radius: 4px; font-size: 0.8rem; color: #a7f3d0; margin-bottom: 0.75rem;">
            <strong>Analyst (${item.analyst_id || 'analyst'}):</strong> ${item.analyst_rationale}
          </div>
        ` : ''}

        <div class="review-actions">
          <button class="btn-action" onclick="openReviewDecisionModal('${item.id}', 'approve')">
            ✅ Approve Match
          </button>
          <button class="btn-action" onclick="openReviewDecisionModal('${item.id}', 'reject')">
            ❌ Reject / Separate
          </button>
          <button class="btn-action" onclick="openReviewDecisionModal('${item.id}', 'mark_needs_verification')">
            🔍 Flag for Field Check
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function renderAuditLog() {
  const container = document.getElementById('audit-log-container');
  if (!container) return;

  container.innerHTML = `
    <table class="report-paper" style="width: 100%; margin: 0; font-size: 0.8rem;">
      <thead>
        <tr>
          <th>Log ID</th>
          <th>Timestamp</th>
          <th>Analyst</th>
          <th>Action</th>
          <th>Target ID</th>
          <th>Rationale</th>
        </tr>
      </thead>
      <tbody>
        ${appState.auditLog.map(l => `
          <tr>
            <td><code>${l.id}</code></td>
            <td><small>${l.timestamp}</small></td>
            <td><code>${l.analyst_id}</code></td>
            <td><span class="badge" style="background: rgba(255,255,255,0.08);">${l.action}</span></td>
            <td><code>${l.target_id}</code></td>
            <td>${l.rationale}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

async function loadReport() {
  const container = document.getElementById('report-container');
  if (!container) return;

  try {
    const md = await fetch(`${API_BASE}/api/report/markdown`).then(r => r.text());
    container.innerHTML = `
      <div style="display: flex; gap: 0.75rem; justify-content: flex-end; margin-bottom: 1rem;">
        <button class="btn-action" onclick="downloadReportMd()">⬇️ Download Markdown (.md)</button>
        <button class="btn-action" onclick="downloadReportJson()">⬇️ Download JSON</button>
        <button class="btn-action btn-primary" onclick="window.print()">🖨️ Print / Save PDF</button>
      </div>
      <div class="report-paper">
        <pre style="white-space: pre-wrap; font-family: var(--font-body); font-size: 0.9rem; line-height: 1.6;">${applyPiiRedaction(md)}</pre>
      </div>
    `;
  } catch (err) {
    container.innerHTML = `<p>Error loading intelligence report.</p>`;
  }
}

// Review Decision Modal Handlers
let activeReviewId = null;
let activeDecisionType = null;

function openReviewDecisionModal(itemId, decisionType) {
  activeReviewId = itemId;
  activeDecisionType = decisionType;
  const modal = document.getElementById('review-decision-modal');
  const title = document.getElementById('modal-review-title');
  const actName = decisionType.replace('_', ' ').toUpperCase();
  title.textContent = `Record Analyst Decision: ${actName} [${itemId}]`;
  document.getElementById('modal-rationale-input').value = '';
  modal.classList.add('active');
}

function closeReviewModal() {
  const modal = document.getElementById('review-decision-modal');
  modal.classList.remove('active');
}

async function submitReviewDecision() {
  const rationale = document.getElementById('modal-rationale-input').value.trim();
  if (!rationale) {
    alert('Analyst rationale note is required for auditability.');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/review-queue/${activeReviewId}/action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        decision: activeDecisionType,
        rationale: rationale
      })
    });
    if (res.ok) {
      closeReviewModal();
      await loadAllData();
    } else {
      alert('Error updating review item.');
    }
  } catch (err) {
    console.error('Failed to submit review:', err);
  }
}

// Ingestion Form Handler
async function handleSourceIngestion(e) {
  e.preventDefault();
  const title = document.getElementById('ingest-title').value;
  const org = document.getElementById('ingest-org').value;
  const type = document.getElementById('ingest-type').value;
  const text = document.getElementById('ingest-text').value;

  if (!title || !text) {
    alert('Please provide title and text content.');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/sources`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: title,
        source_org: org,
        source_type: type,
        text: text
      })
    });
    if (res.ok) {
      alert('Document successfully ingested and analyzed!');
      document.getElementById('ingest-form').reset();
      await loadAllData();
      switchTab('sources');
    }
  } catch (err) {
    alert('Error ingesting document.');
  }
}

// PII Redaction toggle
function togglePiiRedaction() {
  appState.piiRedacted = !appState.piiRedacted;
  const btn = document.getElementById('btn-toggle-pii');
  if (btn) {
    btn.textContent = appState.piiRedacted ? '🛡️ PII Redaction: ACTIVE' : '🛡️ PII Redaction: OFF';
    btn.style.color = appState.piiRedacted ? '#34d399' : '#fff';
  }
  renderSources();
  loadReport();
}

function applyPiiRedaction(text) {
  if (!appState.piiRedacted || !text) return text;
  // Redact phone patterns and residential door numbers
  let out = text.replace(/(\+?91[\-\s]?)?[6-9]\d{9}/g, '[REDACTED_PHONE]');
  out = out.replace(/\bAge\s*\d{2}\b/gi, 'Age [REDACTED]');
  return out;
}

// Reset Benchmark Corpus
async function resetBenchmark() {
  if (confirm('Reset workbench state to default multilingual benchmark corpus?')) {
    await fetch(`${API_BASE}/api/reset-corpus`, { method: 'POST' });
    await loadAllData();
  }
}

// Download handlers
function downloadReportMd() {
  window.open(`${API_BASE}/api/report/markdown`, '_blank');
}
function downloadReportJson() {
  window.open(`${API_BASE}/api/report`, '_blank');
}

function setupEventListeners() {
  const form = document.getElementById('ingest-form');
  if (form) form.addEventListener('submit', handleSourceIngestion);

  const resetBtn = document.getElementById('btn-reset-benchmark');
  if (resetBtn) resetBtn.addEventListener('click', resetBenchmark);

  const piiBtn = document.getElementById('btn-toggle-pii');
  if (piiBtn) piiBtn.addEventListener('click', togglePiiRedaction);
}

function showLoading() {}
function hideLoading() {}
