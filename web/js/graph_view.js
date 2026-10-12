/**
 * Knowledge Graph visualization controller using Cytoscape.js.
 */

let cy = null;

const NODE_COLORS = {
  'PERSON': '#f43f5e',
  'ORGANIZATION': '#6366f1',
  'LOCATION': '#06b6d4',
  'EVENT': '#f59e0b',
  'SOURCE': '#3b82f6',
  'INFRASTRUCTURE': '#10b981',
  'OBJECT_CONSIGNMENT': '#8b5cf6'
};

function initGraphViewer(elementsData) {
  const container = document.getElementById('cytoscape-container');
  if (!container) return;

  if (typeof cytoscape === 'undefined') {
    container.innerHTML = `
      <div style="padding: 2rem; text-align: center; color: var(--text-muted);">
        <p>⚠️ Cytoscape library loading. If offline, the structured node and edge tables remain fully functional below.</p>
      </div>`;
    return;
  }

  // Cytoscape stylesheet
  const cyStyle = [
    {
      selector: 'node',
      style: {
        'label': 'data(label)',
        'color': '#f3f4f6',
        'font-size': '11px',
        'font-family': 'Inter, sans-serif',
        'text-valign': 'bottom',
        'text-margin-y': 6,
        'background-color': function(ele) {
          return NODE_COLORS[ele.data('type')] || '#64748b';
        },
        'width': function(ele) {
          return ele.data('type') === 'EVENT' ? 38 : (ele.data('type') === 'SOURCE' ? 32 : 36);
        },
        'height': function(ele) {
          return ele.data('type') === 'EVENT' ? 38 : (ele.data('type') === 'SOURCE' ? 32 : 36);
        },
        'border-width': 2,
        'border-color': '#ffffff',
        'border-opacity': 0.25,
        'overlay-opacity': 0,
        'transition-property': 'background-color, line-color, target-arrow-color',
        'transition-duration': '0.2s'
      }
    },
    {
      selector: 'node:selected',
      style: {
        'border-width': 4,
        'border-color': '#38bdf8',
        'border-opacity': 1,
        'shadow-blur': 15,
        'shadow-color': '#38bdf8',
        'shadow-opacity': 0.8
      }
    },
    {
      selector: 'edge',
      style: {
        'label': 'data(label)',
        'font-size': '9px',
        'font-family': 'JetBrains Mono, monospace',
        'color': '#94a3b8',
        'text-rotation': 'autorotate',
        'text-margin-y': -8,
        'curve-style': 'bezier',
        'width': 2,
        'line-color': '#475569',
        'target-arrow-shape': 'triangle',
        'target-arrow-color': '#475569',
        'arrow-scale': 1.1,
        'opacity': 0.85
      }
    },
    {
      selector: 'edge[!direct]',
      style: {
        'line-style': 'dashed',
        'line-dash-pattern': [6, 3],
        'line-color': '#a855f7',
        'target-arrow-color': '#a855f7'
      }
    },
    {
      selector: 'edge[status = "contradicted"]',
      style: {
        'line-style': 'dashed',
        'line-dash-pattern': [4, 4],
        'line-color': '#f43f5e',
        'target-arrow-color': '#f43f5e',
        'color': '#fca5a5'
      }
    },
    {
      selector: 'edge:selected',
      style: {
        'width': 4,
        'line-color': '#38bdf8',
        'target-arrow-color': '#38bdf8',
        'color': '#38bdf8'
      }
    }
  ];

  try {
    cy = cytoscape({
      container: container,
      elements: elementsData,
      style: cyStyle,
      layout: {
        name: 'cose',
        idealEdgeLength: 130,
        nodeOverlap: 20,
        refresh: 20,
        fit: true,
        padding: 40,
        randomize: false,
        componentSpacing: 100,
        nodeRepulsion: 400000,
        edgeElasticity: 100,
        nestingFactor: 5,
        gravity: 80,
        numIter: 1000,
        initialTemp: 200,
        coolingFactor: 0.95,
        minTemp: 1.0
      }
    });

    // Node click inspector
    cy.on('tap', 'node', function(evt) {
      const node = evt.target;
      displayNodeInspector(node.data());
    });

    // Edge click inspector
    cy.on('tap', 'edge', function(evt) {
      const edge = evt.target;
      displayEdgeInspector(edge.data());
    });

    // Background click resets inspector
    cy.on('tap', function(evt) {
      if (evt.target === cy) {
        clearInspector();
      }
    });
  } catch (err) {
    console.error("Cytoscape initialization error:", err);
  }
}

function displayNodeInspector(data) {
  const panel = document.getElementById('graph-inspector-panel');
  if (!panel) return;
  panel.innerHTML = `
    <div class="panel-card" style="margin-bottom: 0;">
      <div class="panel-header">
        <h3>🔍 Node Inspector</h3>
        <span class="badge" style="background: ${NODE_COLORS[data.type] || '#6366f1'}33; color: ${NODE_COLORS[data.type] || '#818cf8'}">
          ${data.type}
        </span>
      </div>
      <div style="margin-bottom: 0.75rem;">
        <h4 style="font-size: 1.1rem; color: #fff;">${data.label}</h4>
        <p style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono);">ID: ${data.id}</p>
      </div>
      <div style="font-size: 0.85rem; line-height: 1.6;">
        <p><strong>Confidence:</strong> <span class="badge" style="background: rgba(255,255,255,0.1);">${data.confidence}</span></p>
        <p><strong>Verification:</strong> <span class="badge badge-classified">${data.status}</span></p>
        ${data.properties ? `<div style="margin-top: 0.5rem; background: rgba(0,0,0,0.3); padding: 0.65rem; border-radius: 6px; font-size: 0.75rem; font-family: var(--font-mono);">
          <pre>${JSON.stringify(data.properties, null, 2)}</pre>
        </div>` : ''}
      </div>
    </div>
  `;
}

function displayEdgeInspector(data) {
  const panel = document.getElementById('graph-inspector-panel');
  if (!panel) return;
  panel.innerHTML = `
    <div class="panel-card" style="margin-bottom: 0;">
      <div class="panel-header">
        <h3>🔗 Relationship Inspector</h3>
        <span class="badge badge-classified">${data.status}</span>
      </div>
      <div style="margin-bottom: 0.75rem;">
        <h4 style="font-size: 1rem; color: #fff;">${data.label}</h4>
        <p style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono);">
          ${data.source} ➔ ${data.target}
        </p>
      </div>
      <div style="font-size: 0.85rem; line-height: 1.6;">
        <p><strong>Type:</strong> <code>${data.rel_type}</code></p>
        <p><strong>Direct Evidence:</strong> ${data.direct ? '✅ Direct Primary' : '⚠️ Inferred Link'}</p>
        <p><strong>Confidence:</strong> ${data.confidence}</p>
        ${data.flags && data.flags.length ? `
          <div style="margin-top: 0.5rem; color: #fda4af; font-size: 0.78rem;">
            ${data.flags.map(f => `⚠️ ${f}`).join('<br>')}
          </div>
        ` : ''}
      </div>
    </div>
  `;
}

function clearInspector() {
  const panel = document.getElementById('graph-inspector-panel');
  if (!panel) return;
  panel.innerHTML = `
    <div class="panel-card" style="margin-bottom: 0; text-align: center; color: var(--text-dim); padding: 2rem 1rem;">
      <p>Click any node or relationship edge in the graph canvas to inspect provenance, quotes, and audit status.</p>
    </div>
  `;
}

function filterGraphByType(type) {
  if (!cy) return;
  if (type === 'ALL') {
    cy.elements().show();
  } else {
    cy.elements().hide();
    const matchingNodes = cy.nodes(`[type = "${type}"]`);
    matchingNodes.show();
    matchingNodes.connectedEdges().show();
    matchingNodes.neighborhood().show();
  }
}

function zoomGraphIn() {
  if (cy) cy.zoom(cy.zoom() * 1.25);
}

function zoomGraphOut() {
  if (cy) cy.zoom(cy.zoom() * 0.8);
}

function fitGraphView() {
  if (cy) cy.fit(null, 40);
}
