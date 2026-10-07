import sqlite3
import json
import os
import webbrowser
from datetime import datetime

DB_PATH = 'memory/events.db'
JSONL_PATH = 'memory/events.jsonl'
HTML_PATH = 'memory/graph.html'

def sync_to_sqlite():
    os.makedirs('memory', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            schemaVersion INTEGER,
            timestampUtc TEXT,
            actor TEXT,
            kind TEXT,
            content TEXT,
            evidence TEXT,
            confidence TEXT,
            supersedes TEXT
        )
    ''')
    
    if os.path.exists(JSONL_PATH):
        with open(JSONL_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                data = json.loads(line)
                cursor.execute('''
                    INSERT OR IGNORE INTO events 
                    (id, schemaVersion, timestampUtc, actor, kind, content, evidence, confidence, supersedes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('id'), data.get('schemaVersion'), data.get('timestampUtc'),
                    data.get('actor'), data.get('kind'), data.get('content'),
                    data.get('evidence'), data.get('confidence'), data.get('supersedes')
                ))
    conn.commit()
    return conn

def generate_graph(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, actor, kind, supersedes, timestampUtc, content FROM events')
    rows = cursor.fetchall()
    
    nodes = []
    links = []
    
    prev_id = None
    for row in rows:
        event_id, actor, kind, supersedes, timestamp, content = row
        nodes.append({
            "id": event_id,
            "group": kind,
            "actor": actor,
            "title": f"[{kind}] {actor} ({timestamp})\n{content[:50]}..."
        })
        
        if supersedes:
            links.append({"source": supersedes, "target": event_id, "type": "supersedes"})
        elif prev_id:
            links.append({"source": prev_id, "target": event_id, "type": "sequence"})
            
        prev_id = event_id

    graph_data = {"nodes": nodes, "links": links}
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Memory Graph (Obsidian Style)</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{ margin: 0; background-color: #1e1e1e; color: #fff; font-family: sans-serif; overflow: hidden; }}
        #graph {{ width: 100vw; height: 100vh; }}
        .node circle {{ stroke: #333; stroke-width: 1.5px; }}
        .node text {{ font-size: 12px; fill: #aaa; pointer-events: none; }}
        .link {{ stroke: #555; stroke-opacity: 0.6; }}
        #tooltip {{
            position: absolute; text-align: left; padding: 8px; font-size: 12px;
            background: rgba(0,0,0,0.8); border: 1px solid #444; border-radius: 4px;
            pointer-events: none; opacity: 0; max-width: 300px;
            color: #fff;
        }}
    </style>
</head>
<body>
    <div id="tooltip"></div>
    <svg id="graph"></svg>
    <script>
        const data = {json.dumps(graph_data)};
        
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        const color = d3.scaleOrdinal(d3.schemeCategory10);
        
        const svg = d3.select("#graph")
            .attr("viewBox", [0, 0, width, height]);
            
        const g = svg.append("g");
        
        const zoom = d3.zoom().on("zoom", (e) => {{
            g.attr("transform", e.transform);
        }});
        svg.call(zoom);

        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = g.append("g")
            .attr("class", "link")
            .selectAll("line")
            .data(data.links)
            .join("line")
            .attr("stroke-width", 2);

        const node = g.append("g")
            .attr("class", "node")
            .selectAll("g")
            .data(data.nodes)
            .join("g")
            .call(drag(simulation));

        node.append("circle")
            .attr("r", 8)
            .attr("fill", d => color(d.group))
            .on("mouseover", (event, d) => {{
                const tooltip = d3.select("#tooltip");
                tooltip.transition().duration(200).style("opacity", 1);
                tooltip.html(d.title.replace(/\\n/g, '<br/>'))
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 28) + "px");
            }})
            .on("mouseout", () => {{
                d3.select("#tooltip").transition().duration(500).style("opacity", 0);
            }});

        node.append("text")
            .attr("x", 12)
            .attr("y", 4)
            .text(d => d.actor);

        simulation.on("tick", () => {{
            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});

        function drag(simulation) {{
            function dragstarted(event) {{
                if (!event.active) simulation.alphaTarget(0.3).restart();
                event.subject.fx = event.subject.x;
                event.subject.fy = event.subject.y;
            }}
            function dragged(event) {{
                event.subject.fx = event.x;
                event.subject.fy = event.y;
            }}
            function dragended(event) {{
                if (!event.active) simulation.alphaTarget(0);
                event.subject.fx = null;
                event.subject.fy = null;
            }}
            return d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
        }}
    </script>
</body>
</html>
"""
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    conn = sync_to_sqlite()
    generate_graph(conn)
    conn.close()
    print(f"Banco SQLite atualizado.")
    print(f"Gráfico gerado em {HTML_PATH}")
    webbrowser.open('file://' + os.path.abspath(HTML_PATH))
