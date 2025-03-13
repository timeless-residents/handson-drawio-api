"""Example of exporting a diagram to Draw.io format (.drawio)."""

import sys
import os
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.drawio_api.client import DrawioAPIClient


def main():
    """Create a flowchart diagram and export it as a .drawio file."""
    client = DrawioAPIClient()
    
    # Create a new diagram
    diagram = client.create_diagram(title="Flowchart for Draw.io Export")
    
    # Add nodes
    diagram = client.add_node(
        diagram, 
        "Start", 
        100, 
        40, 
        120, 
        40, 
        "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    diagram = client.add_node(
        diagram, 
        "Process Data", 
        100, 
        160, 
        120, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    diagram = client.add_node(
        diagram, 
        "Decision", 
        100, 
        300, 
        120, 
        60,
        "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    diagram = client.add_node(
        diagram, 
        "End Success", 
        240, 
        420, 
        120, 
        40,
        "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    diagram = client.add_node(
        diagram, 
        "End Failure", 
        -40, 
        420, 
        120, 
        40,
        "ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
    )
    
    # Find node IDs
    start_id = diagram["cells"][0]["id"]
    process_id = diagram["cells"][1]["id"]
    decision_id = diagram["cells"][2]["id"]
    success_id = diagram["cells"][3]["id"]
    failure_id = diagram["cells"][4]["id"]
    
    # Add edges
    diagram = client.add_edge(
        diagram, 
        start_id, 
        process_id,
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    diagram = client.add_edge(
        diagram, 
        process_id, 
        decision_id,
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    diagram = client.add_edge(
        diagram, 
        decision_id, 
        success_id, 
        "Yes",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;fontStyle=1;fontColor=#009900;"
    )
    diagram = client.add_edge(
        diagram, 
        decision_id, 
        failure_id, 
        "No",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;fontStyle=1;fontColor=#990000;exitX=0;exitY=0.5;"
    )
    
    # Export to different formats
    
    # 1. JSON format (original internal format)
    json_data = client.export_diagram(diagram, format="json")
    with open("flowchart.json", "w") as f:
        f.write(json_data)
    print("Exported diagram to flowchart.json")
    
    # 2. XML format (Draw.io compatible XML)
    xml_data = client.export_diagram(diagram, format="xml")
    with open("flowchart.xml", "w") as f:
        f.write(xml_data)
    print("Exported diagram to flowchart.xml")
    
    # 3. Draw.io format (.drawio file)
    drawio_data = client.export_diagram(diagram, format="drawio")
    with open("flowchart.drawio", "w") as f:
        f.write(drawio_data)
    print("Exported diagram to flowchart.drawio")
    
    # Create an informational HTML file
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Draw.io Export Guide</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        h1, h2 {{ color: #333; }}
        .file-box {{ 
            border: 1px solid #ddd; 
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
            background-color: #f9f9f9;
        }}
        .instructions {{ margin: 20px 0; }}
        pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; }}
        .highlight {{ color: #2c7cb0; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Draw.io Export Files</h1>
    <p>The following files have been created:</p>
    
    <div class="file-box">
        <h2>flowchart.drawio</h2>
        <p>This is a native Draw.io file that can be opened directly in Draw.io.</p>
        <div class="instructions">
            <p><strong>How to open:</strong></p>
            <ol>
                <li>Go to <a href="https://app.diagrams.net/" target="_blank">https://app.diagrams.net/</a></li>
                <li>Click "Open Existing Diagram"</li>
                <li>Select "Open from Device" and choose the flowchart.drawio file</li>
            </ol>
        </div>
    </div>
    
    <div class="file-box">
        <h2>flowchart.xml</h2>
        <p>This is the raw XML format used by Draw.io. It can also be imported.</p>
        <div class="instructions">
            <p><strong>How to open:</strong></p>
            <ol>
                <li>Go to <a href="https://app.diagrams.net/" target="_blank">https://app.diagrams.net/</a></li>
                <li>Click "Open Existing Diagram"</li>
                <li>Select "Open from Device" and choose the flowchart.xml file</li>
            </ol>
        </div>
    </div>
    
    <div class="file-box">
        <h2>flowchart.json</h2>
        <p>This is the internal JSON representation used by our API.</p>
        <p>This is useful for debugging or for further processing with other tools.</p>
    </div>
    
    <p class="highlight">Note: The .drawio format is the preferred format for sharing diagrams, as it contains all necessary information for Draw.io to open and edit the diagram.</p>
</body>
</html>"""
    
    with open("drawio_export_guide.html", "w") as f:
        f.write(html_content)
    
    print("Created export guide: drawio_export_guide.html")
    print("\nYou can now open flowchart.drawio directly in Draw.io!")


if __name__ == "__main__":
    main()