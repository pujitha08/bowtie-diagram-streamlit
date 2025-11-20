# Bowtie Diagram Application

## Team Information
**Team 2 Members:** Pujitha Attuluri, Dana Moua, Jessica Escutia Miranda, Camila Garcia, Venkata Keerthika Kottakota
**Choosen Approach:** Approach 1 – Build using ReactFlow

## Risk Story Summary

Our bow tie risk story focuses on a rideshare scenario where small failures during an Uber or Lyft trip can escalate into a major incident. Risks such as an intoxicated driver, distracted driving, slippery roads, and poor visibility each increase the chance of a dangerous situation—and when combined, they significantly amplify the hazard. The analysis shows how gaps in driver behavior, environmental conditions, and real-time decision-making can compound quickly in a high-traffic setting. By mapping threats, controls, and consequences, we highlight the importance of strong safety safeguards to prevent a routine rideshare trip from turning into a serious incident.

## Live Application

**Streamlit App:** https://bowtie-diagram-app-reactflow-team02.streamlit.app/

## Features

- Interactive node types (Hazard, Threat, Barriers, Consequences, Degradation factors)
- Add/delete nodes and branches
- Collapse/expand threat and consequence chains
- Toggle barrier failure states
- Auto-layout using ELK algorithm
- Inline node renaming
- **NEW**: Add degradation-only nodes without consequences

## How to Run/View

### Option 1: View Online
Visit the live Streamlit app link above

### Option 2: Run Locally

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure
```
bowtie-diagram-app/
├── app.py                      # Main entry point
├── components/                 # React components
│   ├── react_app.js           # Main app logic
│   ├── node_components.py     # Node designs
│   ├── initial_data.py        # Default data
│   └── html_template.py       # HTML builder
├── static/                     # Styles and colors
│   ├── css/styles.py
│   └── js/colors.py
└── utils/                      # Helper functions
    └── helpers.py
```

## Usage

1. Use toolbar buttons to add threats, barriers, or consequences
2. Click nodes to select them
3. Use the rename bar to edit node labels
4. Click +/− buttons on threats/consequences to collapse chains
5. Click the bowtie icon on barriers to toggle failure state

## Acknowledgement

This is a student project developed for DSBA 5122 in collaboration with Todus Advisors. Bowtie Symbols are proprietary of Todus Advisors.

## License

MIT License