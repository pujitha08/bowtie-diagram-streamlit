"""
Initial data configuration for the Bowtie Diagram
Contains the default nodes and edges
"""

INITIAL_DATA_JS = """
const initialNodes = [
  {
    id:"hazard",
    type:"hazardNode",
    position:{x:620,y:400},
    data:{label:"Driving a commercial vehicle on a highway", type:"hazard"}
  },
  {
    id:"topevent",
    type:"topEventNode",
    position:{x:650,y:500},
    data:{label:"Loss of control over the vehicle at 70 mph", type:"topevent"}
  },
  // Threat 1: Intoxicated driving - WITH 4 BARRIERS
  {
    id:"t1",
    type:"threatNode",
    position:{x:50,y:50},
    data:{label:"Intoxicated driving", type:"threat", collapsed:false, onToggleCollapse:null}
  },
  {
    id:"pb1-1",
    type:"barrierNode",
    position:{x:220,y:50},
    data:{label:"Driver reports himself unwell or impaired and supervisor assigns a replacement (a designated driver)", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t1"}
  },
  {
    id:"pb1-2",
    type:"barrierNode",
    position:{x:420,y:50},
    data:{label:"Dispatcher or supervisor detect the driver is unwell or impaired and pull the driver from duty and assign a replacement", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t1"}
  },
  {
    id:"pb1-3",
    type:"barrierNode",
    position:{x:620,y:50},
    data:{label:"Ignition interlock devices prevents driver for starting the engine", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t1"}
  },
  {
    id:"pb1-4",
    type:"barrierNode",
    position:{x:820,y:50},
    data:{label:"Driver detects alerts triggered from the lane departure warning system and prevents lane drift", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t1"}
  },
  // Threat 2: Distractive driving
  {
    id:"t2",
    type:"threatNode",
    position:{x:50,y:250},
    data:{label:"Distractive driving", type:"threat", collapsed:false, onToggleCollapse:null}
  },
  {
    id:"pb2-1",
    type:"barrierNode",
    position:{x:220,y:250},
    data:{label:"Voice-activated Dispatch System reduces manual input and screen activation while driving", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t2"}
  },
  {
    id:"pb2-2",
    type:"barrierNode",
    position:{x:420,y:250},
    data:{label:"Driver detects alerts triggered from the lane departure warning system and prevents lane drift", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t2"}
  },
  // Threat 3: Driving on slippery road
  {
    id:"t3",
    type:"threatNode",
    position:{x:50,y:450},
    data:{label:"Driving on slippery road", type:"threat", collapsed:false, onToggleCollapse:null}
  },
  {
    id:"pb3-1",
    type:"barrierNode",
    position:{x:220,y:450},
    data:{label:"Driver listens to weather report and adjusts driving schedule to avoid rain", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t3"}
  },
  {
    id:"pb3-2",
    type:"barrierNode",
    position:{x:420,y:450},
    data:{label:"Defensive driving", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t3"}
  },
  {
    id:"pb3-3",
    type:"barrierNode",
    position:{x:620,y:450},
    data:{label:"Anti-lock Braking System (ABS) maintains steering control", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t3"}
  },
  // Threat 4: Driving with poor visibility
  {
    id:"t4",
    type:"threatNode",
    position:{x:50,y:650},
    data:{label:"Driving with poor visibility", type:"threat", collapsed:false, onToggleCollapse:null}
  },
  {
    id:"pb4-1",
    type:"barrierNode",
    position:{x:220,y:650},
    data:{label:"Driver listens to weather report and adjusts driving schedule to avoid rain", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t4"}
  },
  {
    id:"pb4-2",
    type:"barrierNode",
    position:{x:420,y:650},
    data:{label:"Defensive driving", type:"barrier-prevent", failed:false, onToggleFail:null, threatId:"t4"}
  },
  // Consequence 1: Crash into a fixed object
  {
    id:"c1",
    type:"consequenceNode",
    position:{x:1200,y:100},
    data:{label:"Crash into a fixed object", type:"consequence", collapsed:false, onToggleCollapse:null}
  },
  {
    id:"mb1-1",
    type:"barrierNode",
    position:{x:880,y:100},
    data:{label:"Forward Collision Warning System and Defensive Driving", type:"barrier-mitigate", failed:false, onToggleFail:null, consequenceId:"c1"}
  },
  {
    id:"mb1-2",
    type:"barrierNode",
    position:{x:1040,y:100},
    data:{label:"Crumble Zone", type:"barrier-mitigate", failed:false, onToggleFail:null, consequenceId:"c1"}
  },
  // Consequence 2: Driver impacts internals of the vehicle
  {
    id:"c2",
    type:"consequenceNode",
    position:{x:1200,y:350},
    data:{label:"Driver impacts internals of the vehicle", type:"consequence", collapsed:false, onToggleCollapse:null}
  },
  {
    id:"mb2-1",
    type:"barrierNode",
    position:{x:880,y:350},
    data:{label:"Seatbelt prevent driver from colliding with the internals", type:"barrier-mitigate", failed:false, onToggleFail:null, consequenceId:"c2"}
  },
  {
    id:"mb2-2",
    type:"barrierNode",
    position:{x:1040,y:350},
    data:{label:"Airbag", type:"barrier-mitigate", failed:false, onToggleFail:null, consequenceId:"c2"}
  },
  // Consequence 3: Vehicle roll-over
  {
    id:"c3",
    type:"consequenceNode",
    position:{x:1200,y:600},
    data:{label:"Vehicle roll-over", type:"consequence", collapsed:false, onToggleCollapse:null}
  },
  {
    id:"mb3-1",
    type:"barrierNode",
    position:{x:880,y:600},
    data:{label:"Rollover protection (e.g. reinforced structure)", type:"barrier-mitigate", failed:false, onToggleFail:null, consequenceId:"c3"}
  }
];

const initialEdges = [
  // Hazard to Top Event
  {
    id:"e-hz-te",
    source:"hazard",
    target:"topevent",
    sourceHandle:"bottom",
    targetHandle:"top",
    type:"straight",
    markerEnd:{type:RF.MarkerType.ArrowClosed},
    style:{stroke:"#777", strokeWidth:1.6},
    hidden:false
  },
  // Threat 1 chain - WITH 4 BARRIERS
  {id:"e-t1-pb1-1", source:"t1", target:"pb1-1", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb1-1-pb1-2", source:"pb1-1", target:"pb1-2", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb1-2-pb1-3", source:"pb1-2", target:"pb1-3", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb1-3-pb1-4", source:"pb1-3", target:"pb1-4", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb1-4-te", source:"pb1-4", target:"topevent", targetHandle:"left", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  // Threat 2 chain
  {id:"e-t2-pb2-1", source:"t2", target:"pb2-1", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb2-1-pb2-2", source:"pb2-1", target:"pb2-2", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb2-2-te", source:"pb2-2", target:"topevent", targetHandle:"left", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  // Threat 3 chain
  {id:"e-t3-pb3-1", source:"t3", target:"pb3-1", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb3-1-pb3-2", source:"pb3-1", target:"pb3-2", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb3-2-pb3-3", source:"pb3-2", target:"pb3-3", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb3-3-te", source:"pb3-3", target:"topevent", targetHandle:"left", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  // Threat 4 chain
  {id:"e-t4-pb4-1", source:"t4", target:"pb4-1", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb4-1-pb4-2", source:"pb4-1", target:"pb4-2", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-pb4-2-te", source:"pb4-2", target:"topevent", targetHandle:"left", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  // Consequence 1 chain
  {id:"e-te-mb1-1", source:"topevent", sourceHandle:"sR", target:"mb1-1", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-mb1-1-mb1-2", source:"mb1-1", target:"mb1-2", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-mb1-2-c1", source:"mb1-2", target:"c1", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  // Consequence 2 chain
  {id:"e-te-mb2-1", source:"topevent", sourceHandle:"sR", target:"mb2-1", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-mb2-1-mb2-2", source:"mb2-1", target:"mb2-2", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-mb2-2-c2", source:"mb2-2", target:"c2", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  // Consequence 3 chain
  {id:"e-te-mb3-1", source:"topevent", sourceHandle:"sR", target:"mb3-1", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false},
  {id:"e-mb3-1-c3", source:"mb3-1", target:"c3", type:"smoothstep", markerEnd:{type:RF.MarkerType.ArrowClosed}, style:{stroke:"#777", strokeWidth:1.6}, hidden:false}
];
"""