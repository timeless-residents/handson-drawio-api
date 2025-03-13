"""Example of creating a diagram with a data store component."""

import sys
import os
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.drawio_api.client import DrawioAPIClient


def main():
    """Create a flowchart diagram with a data store component."""
    client = DrawioAPIClient()
    
    # Create a new diagram
    diagram = client.create_diagram(title="Flowchart with Data Store")
    
    # Add nodes
    diagram = client.add_node(
        diagram, 
        "Start", 
        200, 
        40, 
        120, 
        40, 
        "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    
    diagram = client.add_node(
        diagram, 
        "Get Request", 
        200, 
        120, 
        120, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    diagram = client.add_node(
        diagram, 
        "Validate Input", 
        200, 
        220, 
        120, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # Add Database/Data Store
    diagram = client.add_node(
        diagram, 
        "Database", 
        400, 
        320, 
        120, 
        60,
        "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;"
    )
    
    # Add decision node
    diagram = client.add_node(
        diagram, 
        "Is Valid?", 
        200, 
        320, 
        120, 
        60,
        "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    # Add process nodes
    diagram = client.add_node(
        diagram, 
        "Process Request", 
        200, 
        430, 
        120, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # End nodes
    diagram = client.add_node(
        diagram, 
        "Return Response", 
        200, 
        530, 
        120, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    diagram = client.add_node(
        diagram, 
        "Return Error", 
        40, 
        430, 
        120, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
    )
    
    diagram = client.add_node(
        diagram, 
        "End", 
        200, 
        630, 
        120, 
        40,
        "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    
    # Find node IDs
    start_id = diagram["cells"][0]["id"]
    get_request_id = diagram["cells"][1]["id"]
    validate_input_id = diagram["cells"][2]["id"]
    database_id = diagram["cells"][3]["id"]
    is_valid_id = diagram["cells"][4]["id"]
    process_request_id = diagram["cells"][5]["id"]
    return_response_id = diagram["cells"][6]["id"]
    return_error_id = diagram["cells"][7]["id"]
    end_id = diagram["cells"][8]["id"]
    
    # Add edges
    # Main flow
    diagram = client.add_edge(
        diagram, 
        start_id, 
        get_request_id,
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, 
        get_request_id, 
        validate_input_id,
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, 
        validate_input_id, 
        is_valid_id,
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    # Connection to database
    diagram = client.add_edge(
        diagram, 
        validate_input_id, 
        database_id,
        "Query",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;entryX=0.5;entryY=0;dashed=1;"
    )
    
    diagram = client.add_edge(
        diagram, 
        database_id, 
        process_request_id,
        "Result",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;entryX=1;entryY=0.5;dashed=1;"
    )
    
    # Valid path
    diagram = client.add_edge(
        diagram, 
        is_valid_id, 
        process_request_id, 
        "Yes",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;fontStyle=1;fontColor=#009900;"
    )
    
    # Invalid path
    diagram = client.add_edge(
        diagram, 
        is_valid_id, 
        return_error_id, 
        "No",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;fontStyle=1;fontColor=#990000;exitX=0;exitY=0.5;"
    )
    
    # Continue the flow
    diagram = client.add_edge(
        diagram, 
        process_request_id, 
        return_response_id,
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    # End paths
    diagram = client.add_edge(
        diagram, 
        return_error_id, 
        end_id,
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;entryX=0;entryY=0.5;"
    )
    
    diagram = client.add_edge(
        diagram, 
        return_response_id, 
        end_id,
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    # Export the diagram in both JSON and SVG formats
    json_data = client.export_diagram(diagram, format="json")
    
    # Save to JSON file for inspection
    with open("datastore_flowchart.json", "w") as f:
        f.write(json_data)
    
    # Export to SVG
    svg_path = client.export_to_image(diagram, "datastore_flowchart.svg", format="svg")
    
    # Create an HTML viewer
    with open("datastore_flowchart_viewer.html", "w") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Flowchart with Data Store - Viewer</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .svg-container {{ 
            border: 1px solid #ddd; 
            border-radius: 5px;
            padding: 10px;
            margin-top: 20px;
            max-width: 800px;
            overflow: auto;
        }}
        svg {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <h1>{diagram["title"]}</h1>
    <div class="svg-container">
        <object data="datastore_flowchart.svg" type="image/svg+xml" width="100%">
            Your browser does not support SVG
        </object>
    </div>
    <p><i>This diagram was generated programmatically using the Draw.io API.</i></p>
</body>
</html>""")
    
    print(f"Diagram created successfully: {diagram['title']}")
    print(f"Diagram exported to datastore_flowchart.json")
    print(f"SVG exported to {svg_path}")
    print(f"HTML viewer created: datastore_flowchart_viewer.html")


if __name__ == "__main__":
    main()