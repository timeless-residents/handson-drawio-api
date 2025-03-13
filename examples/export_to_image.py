"""Example of exporting a diagram to an image file."""

import sys
import os
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.drawio_api.client import DrawioAPIClient


def main():
    """Create a flowchart diagram and export it as an image."""
    client = DrawioAPIClient()
    
    # Create a new diagram
    diagram = client.create_diagram(title="Flowchart for Image Export")
    
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
    
    # Add edges with improved styling
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
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;fontStyle=1;fontColor=#990000;"
    )
    
    # Calculate the bounds of the diagram
    bounds = client.calculate_diagram_size(diagram)
    print(f"Diagram bounds: {bounds}")
    
    # Export to SVG format
    output_path = "flowchart.svg"
    image_path = client.export_to_image(diagram, output_path, format="svg")
    print(f"Exported diagram to {output_path}")
    print("✓ The SVG file was created successfully.")
    print("  You can open it in any web browser or SVG editor.")
    
    # Create a simple HTML file to display the SVG
    with open("flowchart_viewer.html", "w") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Flowchart Viewer</title>
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
        <object data="{output_path}" type="image/svg+xml" width="100%">
            Your browser does not support SVG
        </object>
    </div>
    <p><i>This diagram was generated programmatically using the Draw.io API.</i></p>
</body>
</html>""")
    
    print(f"✓ Created HTML viewer: flowchart_viewer.html")
    
    # Create helper HTML files for other formats
    print("\nCreating HTML helper files for other formats:")
    
    # PNG format helper
    image_path = client.export_to_image(diagram, "flowchart.png", format="png")
    print("✓ Created PNG helper files")
    
    # Try SVG with some custom styling
    image_path = client.export_to_image(
        diagram, 
        "flowchart_custom.svg", 
        format="svg"
    )
    print("✓ Created custom SVG file")
    
    print("\nUsage Instructions:")
    print("1. Open flowchart_viewer.html to view the SVG diagram")
    print("2. SVG files can also be opened directly in any browser")
    print("3. For PNG/JPG, open the .html file in a browser and use save-as")
    print("   Example: open flowchart.png.html in your browser")


if __name__ == "__main__":
    main()