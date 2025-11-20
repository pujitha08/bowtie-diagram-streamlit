"""
HTML Template builder for the Bowtie Diagram
Combines all components into a single HTML document
"""

import os
from static.css.styles import CSS_STYLES
from static.js.colors import COLORS_JS
from utils.helpers import UTILS_JS
from components.node_components import REACT_COMPONENTS
from components.initial_data import INITIAL_DATA_JS


def get_html_template():
    """
    Generates the complete HTML template with embedded JavaScript
    """
    
    # Read the React app logic from external file
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    react_app_path = os.path.join(current_dir, 'react_app.js')
    
    with open(react_app_path, 'r') as f:
        react_app_js = f.read()
    
    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />

  <!-- React & ReactDOM -->
  <script crossorigin src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></script>

  <!-- React Flow UMD + CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reactflow/dist/style.css" />
  <script src="https://cdn.jsdelivr.net/npm/reactflow/dist/umd/index.min.js"></script>

  <!-- ELK (auto-layout) -->
  <script src="https://cdn.jsdelivr.net/npm/elkjs/lib/elk.bundled.js"></script>

  <style>
    {CSS_STYLES}
  </style>
</head>
<body>
<div id="root"></div>

<script>
const React = window.React;
const ReactDOM = window.ReactDOM;
const RF = window.ReactFlow;

{COLORS_JS}

{UTILS_JS}

{REACT_COMPONENTS}

{INITIAL_DATA_JS}

{react_app_js}

ReactDOM.createRoot(document.getElementById('root')).render(
  React.createElement(RF.ReactFlowProvider, null,
    React.createElement(App, null)
  )
);
</script>
</body>
</html>
"""