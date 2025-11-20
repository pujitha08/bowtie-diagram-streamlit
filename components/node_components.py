"""
React component definitions for Bowtie Diagram nodes
"""

REACT_COMPONENTS = """
/* ---------- Helper: box with colored + black stripes ---------- */
function StripeBox({ label, width, height, barColor, secondBarColor }) {
  const w = width || 180;
  const h = height || 80;
  const barH = 10;
  const blackH = 5;
  const borderColor = COLORS.borderBlue;

  const lines = wrapText(label || '', 160);
  const fontSize = lines.length > 3 ? 10 : lines.length > 2 ? 11 : 12;
  const lineHeight = fontSize + 2;
  const totalHeight = lines.length * lineHeight;
  const startY = (h / 2) - (totalHeight / 2) + (lineHeight / 2) - 5;

  return React.createElement(
    'svg',
    {
      width:w,
      height:h,
      style:{ overflow:'visible' }
    },
    [
      React.createElement('rect', {
        key:'rect',
        x:0, y:0,
        width:w, height:h,
        fill:'#FFFFFF',
        stroke:borderColor,
        strokeWidth:1
      }),
      React.createElement('rect', {
        key:'bar1',
        x:0, y:h-barH-blackH,
        width:w, height:barH,
        fill:barColor
      }),
      React.createElement('rect', {
        key:'bar2',
        x:0, y:h-blackH,
        width:w, height:blackH,
        fill:secondBarColor
      })
    ].concat(
      lines.map((line, i) => 
        React.createElement('text', {
          key: `txt${i}`,
          x: w/2,
          y: startY + (i * lineHeight),
          fill: '#000',
          fontSize: fontSize,
          fontFamily: 'sans-serif',
          textAnchor: 'middle',
          dominantBaseline: 'middle'
        }, line)
      )
    )
  );
}

/* ------------------ Custom Node Types ------------------ */

function HazardNode({ data }) {
  const label = data.label || 'HAZARD';
  return React.createElement(
    React.Fragment,
    null,
    [
      React.createElement(RF.Handle, {
        key:'t',
        type:'target',
        position:RF.Position.Left,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(RF.Handle, {
        key:'sTop',
        type:'source',
        position:RF.Position.Top,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(RF.Handle, {
        key:'s',
        id:'bottom',
        type:'source',
        position:RF.Position.Bottom,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(
        'div',
        { key:'body', className:'card' },
        React.createElement(StripeBox, {
          label,
          barColor:COLORS.stripeYellow,
          secondBarColor:COLORS.stripeBlack
        })
      )
    ]
  );
}

/* ThreatNode with collapse/expand functionality */
function ThreatNode({ id, data }) {
  const label = data.label || 'THREAT';
  const collapsed = !!data.collapsed;
  const w = 180;
  const h = 80;
  const borderColor = COLORS.borderBlue;

  const lines = wrapText(label, 160);
  const fontSize = lines.length > 3 ? 10 : lines.length > 2 ? 11 : 12;
  const lineHeight = fontSize + 2;
  const totalHeight = lines.length * lineHeight;
  const startY = (h / 2) - (totalHeight / 2) + (lineHeight / 2) - 10;

  const toggleCollapse = (e) => {
    e.stopPropagation();
    if (data.onToggleCollapse) data.onToggleCollapse(id);
  };

  return React.createElement(
    React.Fragment,
    null,
    [
      React.createElement(RF.Handle, {
        key:'s',
        type:'source',
        position:RF.Position.Right,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(
        'div',
        {
          key: 'container',
          style: {
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 4
          }
        },
        [
          React.createElement(
            'svg',
            {
              key:'svg',
              width:w,
              height:h,
              style:{ overflow:'visible' }
            },
            [
              React.createElement('rect', {
                key:'rect',
                x:0, y:0,
                width:w, height:h,
                fill:'#FFFFFF',
                stroke:borderColor,
                strokeWidth:1
              }),
              React.createElement('rect', {
                key:'blue',
                x:0, y:h-20,
                width:w, height:20,
                fill:'#4A90E2'
              }),
              React.createElement('rect', {
                key:'yel',
                x:0, y:h-25,
                width:w, height:5,
                fill:COLORS.stripeYellow
              })
            ].concat(
              lines.map((line, i) => 
                React.createElement('text', {
                  key: `txt${i}`,
                  x: w/2,
                  y: startY + (i * lineHeight),
                  fill: '#000',
                  fontSize: fontSize,
                  fontFamily: 'sans-serif',
                  textAnchor: 'middle',
                  dominantBaseline: 'middle'
                }, line)
              )
            )
          ),
          React.createElement(
            'div',
            {
              key: 'collapse-btn',
              style: {
                marginTop: 2,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              },
              onClick: toggleCollapse
            },
            React.createElement(
              'div',
              {
                style: {
                  width: 18,
                  height: 18,
                  borderRadius: '50%',
                  border: '1px solid #666',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 12,
                  background: '#fff'
                }
              },
              collapsed ? '+' : '−'
            )
          )
        ]
      )
    ]
  );
}

function ConsequenceNode({ id, data }) {
  const label = data.label || 'CONSEQUENCE';
  const collapsed = !!data.collapsed;
  
  const toggleCollapse = (e) => {
    e.stopPropagation();
    if (data.onToggleCollapse) data.onToggleCollapse(id);
  };

  return React.createElement(
    React.Fragment,
    null,
    [
      React.createElement(RF.Handle, {
        key:'t',
        type:'target',
        position:RF.Position.Left,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(
        'div',
        {
          key: 'container',
          style: {
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 4
          }
        },
        [
          React.createElement(
            'div',
            { key:'body', className:'card' },
            React.createElement(StripeBox, {
              label,
              barColor:'#E53935',
              secondBarColor:COLORS.stripeBlack
            })
          ),
          React.createElement(
            'div',
            {
              key: 'collapse-btn',
              style: {
                marginTop: 2,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              },
              onClick: toggleCollapse
            },
            React.createElement(
              'div',
              {
                style: {
                  width: 18,
                  height: 18,
                  borderRadius: '50%',
                  border: '1px solid #666',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 12,
                  background: '#fff'
                }
              },
              collapsed ? '+' : '−'
            )
          )
        ]
      )
    ]
  );
}

function DegrNode({ data }) {
  const label = data.label || 'DEGRADATION FACTOR';
  return React.createElement(
    React.Fragment,
    null,
    [
      React.createElement(RF.Handle, {
        key:'t',
        type:'target',
        position:RF.Position.Left,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(RF.Handle, {
        key:'s',
        type:'source',
        position:RF.Position.Right,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(
        'div',
        { key:'body', className:'card' },
        React.createElement(StripeBox, {
          label,
          barColor:'#F4B183',
          secondBarColor:COLORS.stripeBlack
        })
      )
    ]
  );
}

function TopEventNode({ data }) {
  const label = data.label || 'TOP EVENT';
  const size = 110;
  const borderColor = COLORS.borderBlue;
  const red = COLORS.topevent;

  const lines = wrapText(label.toUpperCase(), 80);
  const fontSize = lines.length > 3 ? 9 : lines.length > 2 ? 10 : 11;
  const lineHeight = fontSize + 2;
  const totalHeight = lines.length * lineHeight;
  const startY = (size / 2) - (totalHeight / 2) + (lineHeight / 2);

  return React.createElement(
    React.Fragment,
    null,
    [
      React.createElement(RF.Handle, {
        key:'t',
        id:'top',
        type:'target',
        position:RF.Position.Top,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(RF.Handle, {
        key:'tL',
        id:'left',
        type:'target',
        position:RF.Position.Left,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(RF.Handle, {
        key:'sR',
        type:'source',
        position:RF.Position.Right,
        style:{ background:'#555', width:8, height:8, borderRadius:'50%' }
      }),
      React.createElement(
        'svg',
        {
          key:'svg',
          width:size,
          height:size,
          style:{ overflow:'visible' }
        },
        [
          React.createElement('rect', {
            key:'diamond',
            x:size/4,
            y:size/4,
            width:size/2,
            height:size/2,
            fill:red,
            stroke:borderColor,
            strokeWidth:1,
            transform:`rotate(45 ${size/2} ${size/2})`
          }),
          React.createElement('rect', {
            key:'inner',
            x:size/4,
            y:size/4,
            width:size/2,
            height:size/2,
            fill:'#FFFFFF'
          })
        ].concat(
          lines.map((line, i) => 
            React.createElement('text', {
              key: `txt${i}`,
              x: size/2,
              y: startY + (i * lineHeight),
              fill: '#000',
              fontSize: fontSize,
              fontFamily: 'sans-serif',
              textAnchor: 'middle',
              dominantBaseline: 'middle'
            }, line)
          )
        )
      )
    ]
  );
}

/* Barrier node with bowtie icon on top */
function BarrierNode({ id, data }) {
  const failed = !!data.failed;
  const borderColor = COLORS.borderBlue;
  const bandColor = "#000000";
  const label = data.label || "BARRIER";

  const toggleFail = (e) => {
    e.stopPropagation();
    if (data.onToggleFail) data.onToggleFail(id);
  };

  const iconStroke = failed ? "#B00020" : "#335C8A";
  const leftColor = failed ? "#B00020" : "#A8D5BA";
  const rightColor = failed ? "#B00020" : "#A8D5BA";

  const lines = wrapText(label.toUpperCase(), 140);
  const fontSize = lines.length > 3 ? 9 : lines.length > 2 ? 10 : 11;
  const lineHeight = fontSize + 2;
  const totalHeight = lines.length * lineHeight;
  const startY = 32 - totalHeight / 2 + lineHeight / 2;

  return React.createElement(
    React.Fragment,
    null,
    [
      React.createElement(RF.Handle, {
        key: "t",
        type: "target",
        position: RF.Position.Left,
        style: { background: "#555", width: 8, height: 8, borderRadius: "50%" }
      }),
      React.createElement(RF.Handle, {
        key: "s",
        type: "source",
        position: RF.Position.Right,
        style: { background: "#555", width: 8, height: 8, borderRadius: "50%" }
      }),

      React.createElement(
        "div",
        {
          key: "body",
          style: {
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 2,
            paddingTop: 2
          }
        },
        [
          /* bowtie icon header */
          React.createElement(
            "div",
            {
              key: "header",
              style: {
                display: "flex",
                alignItems: "center",
                gap: 6,
                cursor: "pointer",
                marginBottom: -5
              },
              onClick: toggleFail
            },
            [
              React.createElement(
                "svg",
                {
                  key: "icon",
                  width: 90,
                  height: 35,
                  viewBox: "0 0 90 35",
                  style: { overflow: "visible" }
                },
                [
                  /* Left bowtie triangle (pointing left) */
                  React.createElement("path", {
                    key: "left-tie",
                    d: "M 45,17 L 25,8 L 25,26 Z",
                    fill: leftColor,
                    stroke: iconStroke,
                    strokeWidth: 1.5
                  }),
                  /* Right bowtie triangle (pointing right) */
                  React.createElement("path", {
                    key: "right-tie",
                    d: "M 45,17 L 65,8 L 65,26 Z",
                    fill: rightColor,
                    stroke: iconStroke,
                    strokeWidth: 1.5
                  }),
                  /* Center circle/knot */
                  React.createElement("circle", {
                    key: "knot",
                    cx: 45,
                    cy: 17,
                    r: 3,
                    fill: iconStroke,
                    stroke: iconStroke,
                    strokeWidth: 1
                  })
                ]
              ),
              failed &&
                React.createElement(
                  "svg",
                  {
                    key: "warn",
                    width: 20,
                    height: 20,
                    viewBox: "0 0 20 20"
                  },
                  [
                    React.createElement("polygon", {
                      key: "tri",
                      points: "10,3 3,17 17,17",
                      fill: "#B00020"
                    }),
                    React.createElement("text", {
                      key: "ex",
                      x: 10,
                      y: 13,
                      textAnchor: "middle",
                      fill: "#FFFFFF",
                      fontSize: 11,
                      fontFamily: "sans-serif"
                    }, "!")
                  ]
                )
            ]
          ),

          /* barrier box */
          React.createElement(
            "svg",
            { key: "box", width: 150, height: 64 },
            [
              React.createElement("rect", {
                key: "rect",
                x: 0,
                y: 0,
                width: 150,
                height: 64,
                fill: "#FFFFFF",
                stroke: borderColor,
                strokeWidth: 1.5
              }),
              React.createElement("rect", {
                key: "band",
                x: 0,
                y: 56,
                width: 150,
                height: 8,
                fill: bandColor
              }),
              ...lines.map((line, i) => 
                React.createElement("text", {
                  key: `txt${i}`,
                  x: 75,
                  y: startY + (i * lineHeight),
                  fill: "#000",
                  fontSize: fontSize,
                  fontFamily: "sans-serif",
                  textAnchor: "middle",
                  dominantBaseline: "middle"
                }, line)
              )
            ]
          )
        ]
      )
    ]
  );
}

/* Node types mapping */
const nodeTypes = {
  hazardNode: HazardNode,
  topEventNode: TopEventNode,
  threatNode: ThreatNode,
  consequenceNode: ConsequenceNode,
  degrNode: DegrNode,
  barrierNode: BarrierNode
};
"""