"""
CSS styles for the Bowtie Diagram application
"""

CSS_STYLES = """
html, body, #root { height:100%; margin:0; }
.wrap  { height:72vh; border:1px solid #eee; border-radius:12px; }
.tools { display:flex; gap:8px; align-items:center; margin:8px 0 12px; flex-wrap:wrap; }
.btn   { padding:6px 10px; border:1px solid #ddd; border-radius:8px;
         background:#fafafa; cursor:pointer; font-size:13px; }
.btn:hover { background:#f0f0f0; }
.card  { color:#000; }

.legend {
  display:flex;
  flex-wrap:wrap;
  gap:12px;
  align-items:center;
  margin:6px 0;
  font-size:13px;
  color:#444;
}
.legend-item { display:flex; align-items:center; gap:4px; }
.legend-swatch {
  width:14px; height:14px; border-radius:2px;
  border:1px solid rgba(0,0,0,0.2);
}

.rename-bar {
  display:flex; align-items:center; gap:8px;
  margin:6px 0;
  font-size:14px;
}
.rename-bar input {
  padding:4px 6px; border-radius:6px;
  border:1px solid #ccc; min-width:260px;
  font-size:13px;
}
"""