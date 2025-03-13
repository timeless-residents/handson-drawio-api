"""Generate a flowchart of main.py program flow and export it to .drawio format."""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.drawio_api.client import DrawioAPIClient


def main():
    """Create a flowchart of main.py and export as .drawio."""
    client = DrawioAPIClient()
    
    # Create a new diagram
    diagram = client.create_diagram(title="main.py Program Flow")
    
    # Add nodes
    # Starting node
    diagram = client.add_node(
        diagram, 
        "Start", 
        300, 
        40, 
        120, 
        40, 
        "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    
    # Import statements
    diagram = client.add_node(
        diagram, 
        "Import modules and examples", 
        300, 
        120, 
        180, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # Check command line
    diagram = client.add_node(
        diagram, 
        "Check if command line\narguments provided", 
        300, 
        220, 
        180, 
        60,
        "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    # Get example name
    diagram = client.add_node(
        diagram, 
        "Get example name\nfrom sys.argv[1]", 
        600, 
        220, 
        160, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # Check for "simple"
    diagram = client.add_node(
        diagram, 
        "example == 'simple'?", 
        600, 
        320, 
        160, 
        60,
        "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    # Run simple example
    diagram = client.add_node(
        diagram, 
        "Run\ncreate_simple_diagram()", 
        800, 
        320, 
        160, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # Check for "image"
    diagram = client.add_node(
        diagram, 
        "example == 'image'?", 
        600, 
        420, 
        160, 
        60,
        "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    # Run image example
    diagram = client.add_node(
        diagram, 
        "Run\nexport_to_image()", 
        800, 
        420, 
        160, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # Check for "datastore"
    diagram = client.add_node(
        diagram, 
        "example == 'datastore'?", 
        600, 
        520, 
        160, 
        60,
        "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    # Run datastore example
    diagram = client.add_node(
        diagram, 
        "Run\ncreate_datastore_diagram()", 
        800, 
        520, 
        160, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # Check for "drawio"
    diagram = client.add_node(
        diagram, 
        "example == 'drawio'?", 
        600, 
        620, 
        160, 
        60,
        "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    # Run drawio example
    diagram = client.add_node(
        diagram, 
        "Run\nexport_to_drawio()", 
        800, 
        620, 
        160, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # Unknown example
    diagram = client.add_node(
        diagram, 
        "Print error and\navailable examples", 
        600, 
        720, 
        160, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
    )
    
    # Default case (no arguments)
    diagram = client.add_node(
        diagram, 
        "Run\ncreate_datastore_diagram()\n(default)", 
        300, 
        320, 
        180, 
        60,
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # End node
    diagram = client.add_node(
        diagram, 
        "End", 
        450, 
        820, 
        120, 
        40,
        "ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    
    # Find node IDs
    start_id = diagram["cells"][0]["id"]
    imports_id = diagram["cells"][1]["id"]
    check_args_id = diagram["cells"][2]["id"]
    get_example_id = diagram["cells"][3]["id"]
    simple_check_id = diagram["cells"][4]["id"]
    simple_run_id = diagram["cells"][5]["id"]
    image_check_id = diagram["cells"][6]["id"]
    image_run_id = diagram["cells"][7]["id"]
    datastore_check_id = diagram["cells"][8]["id"]
    datastore_run_id = diagram["cells"][9]["id"]
    drawio_check_id = diagram["cells"][10]["id"]
    drawio_run_id = diagram["cells"][11]["id"]
    error_id = diagram["cells"][12]["id"]
    default_id = diagram["cells"][13]["id"]
    end_id = diagram["cells"][14]["id"]
    
    # Add edges
    # Main flow
    diagram = client.add_edge(diagram, start_id, imports_id, style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;")
    diagram = client.add_edge(diagram, imports_id, check_args_id, style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;")
    
    # Command line argument branch
    diagram = client.add_edge(
        diagram, check_args_id, get_example_id, "Yes",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # No command line args branch
    diagram = client.add_edge(
        diagram, check_args_id, default_id, "No",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # Connect example name to first check
    diagram = client.add_edge(
        diagram, get_example_id, simple_check_id,
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    # Connect simple check to run
    diagram = client.add_edge(
        diagram, simple_check_id, simple_run_id, "Yes",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # Connect simple check to next check
    diagram = client.add_edge(
        diagram, simple_check_id, image_check_id, "No",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # Connect image check to run
    diagram = client.add_edge(
        diagram, image_check_id, image_run_id, "Yes",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # Connect image check to next check
    diagram = client.add_edge(
        diagram, image_check_id, datastore_check_id, "No",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # Connect datastore check to run
    diagram = client.add_edge(
        diagram, datastore_check_id, datastore_run_id, "Yes",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # Connect datastore check to next check
    diagram = client.add_edge(
        diagram, datastore_check_id, drawio_check_id, "No",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # Connect drawio check to run
    diagram = client.add_edge(
        diagram, drawio_check_id, drawio_run_id, "Yes",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # Connect drawio check to error
    diagram = client.add_edge(
        diagram, drawio_check_id, error_id, "No",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;align=center;verticalAlign=middle;"
    )
    
    # Connect all outcomes to end
    diagram = client.add_edge(
        diagram, simple_run_id, end_id,
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, image_run_id, end_id,
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, datastore_run_id, end_id,
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, drawio_run_id, end_id,
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, error_id, end_id,
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, default_id, end_id,
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    # Export to different formats
    # 1. Draw.io format
    drawio_data = client.export_diagram(diagram, format="drawio")
    with open("main_program_flow.drawio", "w") as f:
        f.write(drawio_data)
    print("Exported main.py flowchart to main_program_flow.drawio")
    
    # 2. PNG image
    client.export_to_image(diagram, "main_program_flow.png", format="png")
    print("Exported main.py flowchart to main_program_flow.png")
    
    # 3. SVG image
    client.export_to_image(diagram, "main_program_flow.svg", format="svg")
    print("Exported main.py flowchart to main_program_flow.svg")
    
    print("\nYou can now open main_program_flow.drawio directly in Draw.io!")


if __name__ == "__main__":
    main()