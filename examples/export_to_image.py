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
    
    # Export to SVG format (most reliable)
    output_path = "flowchart.svg"
    image_path = client.export_to_image(diagram, output_path, format="svg")
    print(f"Exported diagram to {output_path}")
    
    # Try other formats (note: these may fail if the API is unavailable)
    print("\nAttempting to export to other formats (these may fail if the API is unavailable):")
    try:
        # Export to PNG
        image_path = client.export_to_image(diagram, "flowchart.png", format="png")
        print("✓ Successfully exported diagram to flowchart.png")
        
        # Export with transparent background
        image_path = client.export_to_image(
            diagram, 
            "flowchart_transparent.png", 
            format="png", 
            transparent=True
        )
        print("✓ Successfully exported diagram with transparent background")
        
        # Export with custom scale
        image_path = client.export_to_image(
            diagram, 
            "flowchart_large.png", 
            format="png", 
            scale=2.0
        )
        print("✓ Successfully exported diagram with 2x scale")
        
        # Export with custom background color
        image_path = client.export_to_image(
            diagram, 
            "flowchart_yellow_bg.png", 
            format="png", 
            bg="#FFFFCC"
        )
        print("✓ Successfully exported diagram with custom background")
    except Exception as e:
        print(f"Note: Some export formats failed - SVG should still work. Error: {str(e)}")


if __name__ == "__main__":
    main()