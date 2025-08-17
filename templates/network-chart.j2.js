var authors = [
  {% for each in network_nodes %}
  {id: '{{ each.id }}', name: '{{ each.id }}'}{% if not loop.last %},{% endif %}
  {% endfor %}
];

var pairs = [
  {% for each in network_edges %}
  {source: '{{ each.source }}', target: '{{ each.target }}', count: {{ each.weight }}}{% if not loop.last %},{% endif %}
  {% endfor %}
];

// ====== 轉成 cytoscape elements ======
var nodeMap = {};
authors.forEach(function(a){ nodeMap[a.id] = { id: String(a.id), name: a.name }; });

var nodeWeight = {}, ewMin = Infinity, ewMax = -Infinity;
Object.keys(nodeMap).forEach(function(id){ nodeWeight[id] = 0; });

pairs.forEach(function(e){
  var s = String(e.source), t = String(e.target), w = Number(e.count)||0;
  if (s === t) return;
  nodeWeight[s] += w; nodeWeight[t] += w;
  if (w < ewMin) ewMin = w; if (w > ewMax) ewMax = w;
});
if (!isFinite(ewMin)) { ewMin = 0; ewMax = 1; }
if (ewMin === ewMax) { ewMin -= 1; ewMax += 1; }

var elements = { nodes: [], edges: [] };
Object.keys(nodeMap).forEach(function(id){
  elements.nodes.push({ data: { id: id, name: nodeMap[id].name, nweight: nodeWeight[id] } });
});

pairs.forEach(function(e, i){
  var s = String(e.source), t = String(e.target);
  if (s === t) return;
  elements.edges.push({ data: { id: 'e'+i, source: s, target: t, weight: Number(e.count)||0 } });
});

var nwVals = Object.keys(nodeWeight).map(function(k){ return nodeWeight[k]; });
var nwMin = Math.min.apply(Math, nwVals.length? nwVals : [0]);
var nwMax = Math.max.apply(Math, nwVals.length? nwVals : [1]);
if (nwMin === nwMax) { nwMin -= 1; nwMax += 1; }

// ====== 初始化 cytoscape ======
var cy = window.cy = cytoscape({
  container: document.getElementById('cy'),
  elements: elements,
  layout: { name: 'cose', animate: true },
  style: [
    {
      selector: 'node',
      style: {
        'content': 'data(name)',
        'text-valign': 'center',
        'text-halign': 'center',
        'font-size': 12,
        // 顏色根據 nweight 深淺漸變（從淺藍到深藍）
        'background-color': 'mapData(nweight, ' + nwMin + ', ' + nwMax + ', #c6dbef, #08306b)',
        'width': 'mapData(nweight, ' + nwMin + ', ' + nwMax + ', 24, 64)',
        'height': 'mapData(nweight, ' + nwMin + ', ' + nwMax + ', 24, 64)',
        'color': '#222',
        'border-width': 2,
        'border-color': '#fff',
        'text-outline-color': '#fff',
        'text-outline-width': 1
      }
    },
    {
      selector: 'edge',
      style: {
        'curve-style': 'bezier',
        'line-color': '#999',
        'opacity': 0.85,
        'width': 'mapData(weight, ' + ewMin + ', ' + ewMax + ', 1, 10)',
        'label': 'data(weight)',
        'font-size': 10,
        'text-rotation': 'autorotate'
      }
    },
    // 互動高亮樣式
    { selector: '.faded', style: { 'opacity': 0.15, 'text-opacity': 0.15 } },
    { selector: 'node.highlighted', style: { 'border-color': '#111', 'border-width': 3 } },
    { selector: 'edge.highlighted', style: { 'line-color': '#666', 'opacity': 1, 'width': 6 } }
  ],
  wheelSensitivity: 0.2
});

// ====== 互動高亮：點擊節點 -> 高亮鄰居；點背景 -> 還原 ======
cy.on('tap', 'node', function(evt){
  var node = evt.target;
  var neighborhood = node.closedNeighborhood();
  cy.elements().removeClass('highlighted').addClass('faded');
  neighborhood.removeClass('faded');
  node.addClass('highlighted');
  node.connectedEdges().addClass('highlighted');
  cy.fit(neighborhood, 50);
});

cy.on('tap', function(evt){
  if (evt.target === cy) {
    cy.elements().removeClass('faded highlighted');
    cy.fit(cy.elements(), 50);
  }
});

// ====== 可選：滑過節點時預覽高亮（移出還原，不覆蓋點擊狀態） ======
cy.on('mouseover', 'node', function(evt){
  if (cy.$('.highlighted').length) return; // 若已有點擊高亮則不處理 hover
  var node = evt.target;
  var neighborhood = node.closedNeighborhood();
  cy.elements().addClass('faded');
  neighborhood.removeClass('faded');
});

cy.on('mouseout', 'node', function(){
  if (cy.$('.highlighted').length) return; // 保留點擊狀態
  cy.elements().removeClass('faded');
});

// ====== 布局切換功能 ======
function switchLayout(name){
  var opts = { name: name, animate: true };
  if (name === 'concentric') {
    opts.minNodeSpacing = 20;
    opts.concentric = function(n){ return n.data('nweight') || 0; };
    opts.levelWidth = function(){ return (nwMax - nwMin) / 4 || 1; };
  }
  cy.layout(opts).run();
}


// ====== 邊權重過濾（提供給 HTML 的滑桿呼叫） ======
var __edgeThreshold = 0;
function setEdgeThreshold(thr){
  __edgeThreshold = Number(thr) || 0;
  // 顯示/隱藏邊
  cy.edges().forEach(function(e){
    var pass = (e.data('weight') || 0) >= __edgeThreshold;
    e.style('display', pass ? 'element' : 'none');
  });
  // 隱藏孤立節點（沒有可見邊相連）
  cy.nodes().forEach(function(n){
    var visibleDegree = n.connectedEdges().filter(function(e){ return e.style('display') !== 'none'; }).length;
    n.style('display', visibleDegree > 0 || __edgeThreshold <= 0 ? 'element' : 'none');
  });
  // 自動調整視圖
  var visible = cy.elements().filter(function(ele){ return ele.style('display') !== 'none'; });
  if (visible.length) cy.fit(visible, 50);
}
