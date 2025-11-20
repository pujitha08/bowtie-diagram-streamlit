/* ------------------ ELK Layout ------------------ */
async function elkLayout(nodes, edges) {
  if (window.ELK) {
    try {
      const elk = new window.ELK();
      const graph = {
        id:'root',
        layoutOptions:{
          'elk.algorithm':'layered',
          'elk.direction':'RIGHT'
        },
        children:nodes.map(n=>({id:n.id, width:200, height:80})),
        edges:edges.map(e=>({id:e.id, sources:[e.source], targets:[e.target]}))
      };
      const res = await elk.layout(graph);

      const pos = Object.fromEntries(
        (res.children||[]).map(c=>[c.id,{x:c.x,y:c.y}])
      );

      return nodes.map(n=>({...n, position:pos[n.id] || n.position}));
    } catch(e) {
      console.warn("ELK failed, using fallback.", e);
    }
  }

  const colX = {
    threat:100,
    'barrier-prevent':260,
    hazard:420,
    topevent:620,
    'barrier-mitigate':820,
    consequence:1020,
    degradation:620
  };

  return nodes.map((n,i)=>({
    ...n,
    position:{
      x: colX[n.data.type] || 420,
      y: 120 + i*80
    }
  }));
}

/* ------------------ Main App ------------------ */
function App() {

  const [nodes, setNodes] = React.useState(initialNodes);
  const [edges, setEdges] = React.useState(initialEdges);
  const [selectedNodeId, setSelectedNodeId] = React.useState(null);

  const onNodesChange = React.useCallback(
    (changes)=>setNodes(nds=>RF.applyNodeChanges(changes, nds)), []
  );
  const onEdgesChange = React.useCallback(
    (changes)=>setEdges(eds=>RF.applyEdgeChanges(changes, eds)), []
  );

  const onNodeClick = (e,node)=> setSelectedNodeId(node.id);

  const toggleBarrierFail = React.useCallback((id)=>{
    let newFail = false;

    setNodes(ns =>
      ns.map(n => {
        if (n.id !== id) return n;
        const prev = !!n.data.failed;
        newFail = !prev;
        return {...n, data:{...n.data, failed:newFail}};
      })
    );

    setEdges(es =>
      es.map(e => {
        if (e.source===id || e.target===id) {
          return {
            ...e,
            style:{
              stroke:newFail ? "#B00020" : "#777",
              strokeWidth:newFail ? 2.0 : 1.6
            }
          };
        }
        return e;
      })
    );
  },[]);

  const toggleThreatCollapse = React.useCallback((threatId)=>{
    setNodes(prevNodes => 
      prevNodes.map(n => 
        n.id === threatId 
          ? {...n, data: {...n.data, collapsed: !n.data.collapsed}}
          : n
      )
    );
  },[]);

  const toggleConsequenceCollapse = React.useCallback((consequenceId)=>{
    setNodes(prevNodes => 
      prevNodes.map(n => 
        n.id === consequenceId 
          ? {...n, data: {...n.data, collapsed: !n.data.collapsed}}
          : n
      )
    );
  },[]);
  
  React.useEffect(() => {
    const collapsedThreats = nodes.filter(n => n.type === 'threatNode' && n.data.collapsed);
    const collapsedConsequences = nodes.filter(n => n.type === 'consequenceNode' && n.data.collapsed);
    
    if (collapsedThreats.length === 0 && collapsedConsequences.length === 0) {
      setNodes(ns => ns.map(n => ({...n, hidden: false})));
      setEdges(es => es.filter(e => !e.id.startsWith('collapse-')).map(e => ({...e, hidden: false})));
      return;
    }
    
    const barriersToHide = new Set();
    const edgesToHide = new Set();
    
    collapsedThreats.forEach(threat => {
      nodes.forEach(n => {
        if (n.type === 'barrierNode' && n.data.threatId === threat.id) {
          barriersToHide.add(n.id);
        }
      });
      
      edges.forEach(e => {
        if (e.source === threat.id || barriersToHide.has(e.source) || barriersToHide.has(e.target)) {
          edgesToHide.add(e.id);
        }
      });
    });
    
    collapsedConsequences.forEach(consequence => {
      nodes.forEach(n => {
        if (n.type === 'barrierNode' && n.data.consequenceId === consequence.id) {
          barriersToHide.add(n.id);
        }
      });
      
      edges.forEach(e => {
        if (e.target === consequence.id || barriersToHide.has(e.source) || barriersToHide.has(e.target)) {
          edgesToHide.add(e.id);
        }
      });
    });
    
    setNodes(ns => ns.map(n => {
      if (n.type === 'barrierNode' && barriersToHide.has(n.id)) {
        return {...n, hidden: true};
      }
      return {...n, hidden: false};
    }));
    
    setEdges(es => {
      let updatedEdges = es.filter(e => !e.id.startsWith('collapse-'));
      
      updatedEdges = updatedEdges.map(e => {
        if (edgesToHide.has(e.id)) {
          return {...e, hidden: true};
        }
        return {...e, hidden: false};
      });
      
      collapsedThreats.forEach(threat => {
        updatedEdges.push({
          id: `collapse-threat-${threat.id}`,
          source: threat.id,
          target: 'topevent',
          targetHandle: 'left',
          type: 'smoothstep',
          markerEnd: {type: RF.MarkerType.ArrowClosed},
          style: {stroke: '#777', strokeWidth: 1.6},
          hidden: false
        });
      });
      
      collapsedConsequences.forEach(consequence => {
        updatedEdges.push({
          id: `collapse-consequence-${consequence.id}`,
          source: 'topevent',
          sourceHandle: 'sR',
          target: consequence.id,
          type: 'smoothstep',
          markerEnd: {type: RF.MarkerType.ArrowClosed},
          style: {stroke: '#777', strokeWidth: 1.6},
          hidden: false
        });
      });
      
      return updatedEdges;
    });
  }, [
    nodes.filter(n => n.type === 'threatNode' || n.type === 'consequenceNode').map(n => `${n.id}:${n.data.collapsed}`).join(','), 
    edges.length
  ]);

  // Update node callbacks when they're created
  React.useEffect(() => {
    setNodes(ns => ns.map(n => {
      if (n.type === 'barrierNode') {
        return {...n, data: {...n.data, onToggleFail: toggleBarrierFail}};
      }
      if (n.type === 'threatNode') {
        return {...n, data: {...n.data, onToggleCollapse: toggleThreatCollapse}};
      }
      if (n.type === 'consequenceNode') {
        return {...n, data: {...n.data, onToggleCollapse: toggleConsequenceCollapse}};
      }
      return n;
    }));
  }, [toggleBarrierFail, toggleThreatCollapse, toggleConsequenceCollapse]);

  const addThreatBranch = ()=>{
    const th = uid("th");
    const pb = uid("pb");

    setNodes(ns => ns.concat(
      {
        id:th,
        type:"threatNode",
        position:{x:100,y:100 + (ns.filter(n=>n.type==='threatNode').length * 120)},
        data:{
          label:"THREAT",
          type:"threat",
          collapsed:false,
          onToggleCollapse:toggleThreatCollapse
        }
      },
      {
        id:pb,
        type:"barrierNode",
        position:{x:260,y:120 + (ns.filter(n=>n.type==='threatNode').length * 120)},
        data:{
          label:"BARRIER",
          type:"barrier-prevent",
          failed:false,
          onToggleFail:toggleBarrierFail,
          threatId:th
        }
      }
    ));

    setEdges(es => es.concat(
      {
        id:uid("e"),
        source:th,
        target:pb,
        type:"smoothstep",
        markerEnd:{type:RF.MarkerType.ArrowClosed},
        style:{stroke:"#777", strokeWidth:1.6},
        hidden:false
      },
      {
        id:uid("e"),
        source:pb,
        target:"topevent",
        targetHandle:"sL",
        type:"smoothstep",
        markerEnd:{type:RF.MarkerType.ArrowClosed},
        style:{stroke:"#777", strokeWidth:1.6},
        hidden:false
      }
    ));
  };

  const addMitigationBranch = ()=>{
    const mb = uid("mb");
    const cs = uid("cs");

    setNodes(ns => ns.concat(
      {
        id:mb,
        type:"barrierNode",
        position:{x:780,y:200 + (ns.filter(n=>n.type==='barrierNode' && n.data.type==='barrier-mitigate').length * 120)},
        data:{
          label:"BARRIER",
          type:"barrier-mitigate",
          failed:false,
          onToggleFail:toggleBarrierFail,
          consequenceId:cs
        }
      },
      {
        id:cs,
        type:"consequenceNode",
        position:{x:1000,y:220 + (ns.filter(n=>n.type==='consequenceNode').length * 120)},
        data:{
          label:"CONSEQUENCE",
          type:"consequence",
          collapsed:false,
          onToggleCollapse:toggleConsequenceCollapse
        }
      }
    ));

    setEdges(eds => eds.concat(
      {
        id:uid("e"),
        source:"topevent",
        sourceHandle:"sR",
        target:mb,
        type:"smoothstep",
        markerEnd:{type:RF.MarkerType.ArrowClosed},
        style:{stroke:"#777", strokeWidth:1.6},
        hidden:false
      },
      {
        id:uid("e"),
        source:mb,
        target:cs,
        type:"smoothstep",
        markerEnd:{type:RF.MarkerType.ArrowClosed},
        style:{stroke:"#777", strokeWidth:1.6},
        hidden:false
      }
    ));
  };

  const addDegradationBranch = ()=>{
    const id = selectedNodeId;
    if (!id) return;
    const barrier = nodes.find(n => n.id === id && n.type === "barrierNode");
    if (!barrier) return;

    const df = uid("df");
    const esc = uid("esc");

    const baseX = (barrier.position && barrier.position.x) || 600;
    const baseY = (barrier.position && barrier.position.y) || 220;

    setNodes(ns => ns.concat(
      {
        id:df,
        type:"degrNode",
        position:{x:baseX, y:baseY+150},
        data:{label:"DEGRADATION FACTOR", type:"degradation"}
      },
      {
        id:esc,
        type:"consequenceNode",
        position:{x:baseX+220, y:baseY+150},
        data:{
          label:"CONSEQUENCE",
          type:"consequence",
          collapsed:false,
          onToggleCollapse:toggleConsequenceCollapse
        }
      }
    ));

    setEdges(es => es.concat(
      {
        id:uid("e"),
        source:id,
        target:df,
        type:"smoothstep",
        markerEnd:{type:RF.MarkerType.ArrowClosed},
        style:{stroke:"#777", strokeWidth:1.6},
        hidden:false
      },
      {
        id:uid("e"),
        source:df,
        target:esc,
        type:"smoothstep",
        markerEnd:{type:RF.MarkerType.ArrowClosed},
        style:{stroke:"#777", strokeWidth:1.6},
        hidden:false
      }
    ));
  };

  const addDegradationOnly = ()=>{
    const id = selectedNodeId;
    if (!id) {
      alert('Please select a barrier first');
      return;
    }
    const barrier = nodes.find(n => n.id === id && n.type === "barrierNode");
    if (!barrier) {
      alert('Please select a barrier node to add a degradation factor');
      return;
    }

    const df = uid("df");

    const baseX = (barrier.position && barrier.position.x) || 600;
    const baseY = (barrier.position && barrier.position.y) || 220;

    setNodes(ns => ns.concat(
      {
        id:df,
        type:"degrNode",
        position:{x:baseX, y:baseY+150},
        data:{label:"DEGRADATION FACTOR", type:"degradation"}
      }
    ));

    setEdges(es => es.concat(
      {
        id:uid("e"),
        source:id,
        target:df,
        type:"smoothstep",
        markerEnd:{type:RF.MarkerType.ArrowClosed},
        style:{stroke:"#777", strokeWidth:1.6},
        hidden:false
      }
    ));
  };

  const addBarrierToThreat = ()=>{
    const id = selectedNodeId;
    if (!id) return;
    const threat = nodes.find(n => n.id === id && n.type === "threatNode");
    if (!threat) return;

    const newBarrier = uid("pb");
    
    let lastBarrier = null;
    let lastBarrierId = null;
    
    edges.forEach(e => {
      if (e.target === "topevent") {
        const sourceNode = nodes.find(n => n.id === e.source);
        if (sourceNode && sourceNode.type === 'barrierNode' && sourceNode.data.threatId === id) {
          lastBarrier = sourceNode;
          lastBarrierId = e.source;
        }
      }
    });

    if (!lastBarrier) {
      edges.forEach(e => {
        if (e.source === id) {
          const targetNode = nodes.find(n => n.id === e.target);
          if (targetNode && targetNode.type === 'barrierNode') {
            lastBarrier = targetNode;
            lastBarrierId = e.target;
          }
        }
      });
    }

    if (!lastBarrier) return;

    const baseX = (lastBarrier.position && lastBarrier.position.x) || 400;
    const baseY = (lastBarrier.position && lastBarrier.position.y) || 200;

    setNodes(ns => ns.concat({
      id: newBarrier,
      type: "barrierNode",
      position: {x: baseX + 200, y: baseY},
      data: {
        label: "BARRIER",
        type: "barrier-prevent",
        failed: false,
        onToggleFail: toggleBarrierFail,
        threatId: id
      }
    }));

    setEdges(es => {
      const newEdges = es.filter(e => !(e.source === lastBarrierId && e.target === "topevent"));
      return newEdges.concat(
        {
          id: uid("e"),
          source: lastBarrierId,
          target: newBarrier,
          type: "smoothstep",
          markerEnd: {type: RF.MarkerType.ArrowClosed},
          style: {stroke: "#777", strokeWidth: 1.6},
          hidden: false
        },
        {
          id: uid("e"),
          source: newBarrier,
          target: "topevent",
          targetHandle: "left",
          type: "smoothstep",
          markerEnd: {type: RF.MarkerType.ArrowClosed},
          style: {stroke: "#777", strokeWidth: 1.6},
          hidden: false
        }
      );
    });
  };

  const addBarrierToMitigation = ()=>{
    const id = selectedNodeId;
    if (!id) {
      alert('Please select a consequence first');
      return;
    }
    
    const selectedNode = nodes.find(n => n.id === id);
    
    if (!selectedNode || selectedNode.type !== "consequenceNode") {
      alert('Please select a consequence node to add mitigation barriers');
      return;
    }
    
    const consequenceId = id;
    
    let lastBarrierId = null;
    edges.forEach(e => {
      if (e.target === consequenceId && !e.hidden) {
        const sourceNode = nodes.find(n => n.id === e.source);
        if (sourceNode && sourceNode.type === 'barrierNode' && sourceNode.data.type === 'barrier-mitigate') {
          lastBarrierId = e.source;
        }
      }
    });
    
    if (!lastBarrierId) {
      alert('Could not find a mitigation barrier connected to this consequence');
      return;
    }
    
    const lastBarrier = nodes.find(n => n.id === lastBarrierId);
    const newBarrier = uid("mb");
    
    const baseX = (lastBarrier.position && lastBarrier.position.x) || 800;
    const baseY = (lastBarrier.position && lastBarrier.position.y) || 200;

    setNodes(ns => ns.concat({
      id: newBarrier,
      type: "barrierNode",
      position: {x: baseX + 200, y: baseY},
      data: {
        label: "BARRIER",
        type: "barrier-mitigate",
        failed: false,
        onToggleFail: toggleBarrierFail,
        consequenceId: consequenceId
      }
    }));

    setEdges(es => {
      const newEdges = es.filter(e => !(e.source === lastBarrierId && e.target === consequenceId));
      
      return newEdges.concat(
        {
          id: uid("e"),
          source: lastBarrierId,
          target: newBarrier,
          type: "smoothstep",
          markerEnd: {type: RF.MarkerType.ArrowClosed},
          style: {stroke: "#777", strokeWidth: 1.6},
          hidden: false
        },
        {
          id: uid("e"),
          source: newBarrier,
          target: consequenceId,
          type: "smoothstep",
          markerEnd: {type: RF.MarkerType.ArrowClosed},
          style: {stroke: "#777", strokeWidth: 1.6},
          hidden: false
        }
      );
    });
  };

  const deleteSelectedNode = ()=>{
    const id = selectedNodeId;
    if (!id) {
      alert('Please select a node to delete');
      return;
    }
    
    const nodeToDelete = nodes.find(n => n.id === id);
    if (!nodeToDelete) return;
    
    // Don't allow deleting hazard or top event
    if (nodeToDelete.type === 'hazardNode' || nodeToDelete.type === 'topEventNode') {
      alert('Cannot delete the Hazard or Top Event nodes');
      return;
    }
    
    // If deleting a threat, delete all its barriers
    if (nodeToDelete.type === 'threatNode') {
      const barriersToDelete = nodes.filter(n => 
        n.type === 'barrierNode' && n.data.threatId === id
      ).map(n => n.id);
      
      setNodes(ns => ns.filter(n => 
        n.id !== id && !barriersToDelete.includes(n.id)
      ));
      setEdges(es => es.filter(e => 
        e.source !== id && e.target !== id && 
        !barriersToDelete.includes(e.source) && 
        !barriersToDelete.includes(e.target)
      ));
    }
    // If deleting a consequence, delete all its barriers
    else if (nodeToDelete.type === 'consequenceNode') {
      const barriersToDelete = nodes.filter(n => 
        n.type === 'barrierNode' && n.data.consequenceId === id
      ).map(n => n.id);
      
      setNodes(ns => ns.filter(n => 
        n.id !== id && !barriersToDelete.includes(n.id)
      ));
      setEdges(es => es.filter(e => 
        e.source !== id && e.target !== id && 
        !barriersToDelete.includes(e.source) && 
        !barriersToDelete.includes(e.target)
      ));
    }
    // For barriers and degradation factors, just delete the node
    else {
      setNodes(ns => ns.filter(n => n.id !== id));
      setEdges(es => es.filter(e => e.source !== id && e.target !== id));
    }
    
    setSelectedNodeId(null);
  };

  const startOver = ()=>{
    if (confirm('Are you sure you want to start over? This will reset the diagram to the full example.')) {
      setNodes(initialNodes);
      setEdges(initialEdges);
      setSelectedNodeId(null);
    }
  };

  const relayout = async ()=>{
    const laid = await elkLayout(nodes,edges);
    setNodes(laid);
  };

  const selectedNode = nodes.find(n=>n.id===selectedNodeId) || null;

  const renameBar = selectedNode ? React.createElement(
    "div",
    {className:"rename-bar"},
    [
      "Label:",
      React.createElement("input", {
        key:"in",
        value:selectedNode.data.label,
        onChange:(e)=>{
          const val = e.target.value;
          setNodes(ns =>
            ns.map(n =>
              n.id===selectedNodeId ? {...n, data:{...n.data, label:val}} : n
            )
          );
        }
      }),
      React.createElement("button",{
        className:"btn", onClick:()=>setSelectedNodeId(null)
      },"Close")
    ]
  ) : null;

  return React.createElement(
    React.Fragment,
    null,

    React.createElement("div",{className:"legend"},
      [
        ["Hazard","hazard"],
        ["Threat","threat"],
        ["Prevention Barrier","barrier-prevent"],
        ["Mitigation Barrier","barrier-mitigate"],
        ["Consequence","consequence"],
        ["Degradation Factor","degradation"]
      ].map(([txt,key]) =>
        React.createElement("div",{key,className:"legend-item"},[
          React.createElement("span",{className:"legend-swatch",
            style:{background: key==="hazard" ? COLORS.stripeYellow
                    : key==="threat" ? '#4A90E2'
                    : key==="consequence" ? '#E53935'
                    : key==="degradation" ? '#F4B183'
                    : "#ccc"}}),
          React.createElement("span",null,txt)
        ])
      )
    ),

    renameBar,

    React.createElement("div",{className:"tools"},[
      React.createElement("button",{className:"btn",onClick:addThreatBranch},
        "+ Threat branch"),
      React.createElement("button",{className:"btn",onClick:addBarrierToThreat},
        "+ Barrier (to selected threat)"),
      React.createElement("button",{className:"btn",onClick:addMitigationBranch},
        "+ Mitigation branch"),
      React.createElement("button",{className:"btn",onClick:addBarrierToMitigation},
        "+ Barrier (to selected consequence)"),
      React.createElement("button",{className:"btn",onClick:addDegradationOnly},
        "+ Degradation only (from selected barrier)"),
      React.createElement("button",{className:"btn",onClick:addDegradationBranch},
        "+ Degradation + Consequence (from selected barrier)"),
      React.createElement("button",{
        className:"btn",
        onClick:deleteSelectedNode,
        style:{background: selectedNodeId ? '#ffebee' : '#fafafa', borderColor: selectedNodeId ? '#e57373' : '#ddd'}
      },"Delete selected"),
      React.createElement("button",{className:"btn",onClick:relayout},
        "Auto-layout (ELK)"),
      React.createElement("button",{
        className:"btn",
        onClick:startOver,
        style:{background:'#fff3e0', borderColor:'#ff9800', marginLeft:'auto'}
      },"Start Over")
    ]),

    React.createElement("div",{className:"wrap"},
      React.createElement(RF.ReactFlow,{
        nodes, edges,
        onNodesChange, onEdgesChange,
        onNodeClick,
        fitView:true,
        proOptions:{hideAttribution:true},
        nodeTypes:nodeTypes
      },
        React.createElement(RF.Background,{gap:16}),
        React.createElement(RF.MiniMap,{zoomable:true, pannable:true}),
        React.createElement(RF.Controls,null)
      )
    )
  );
}