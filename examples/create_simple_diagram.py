"""Example of creating a simple diagram using the Draw.io API client."""

import sys
import os
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.drawio_api.client import DrawioAPIClient


def main():
    """Create a simple flowchart diagram."""
    client = DrawioAPIClient()
    
    # Create a new diagram
    diagram = client.create_diagram(title="Simple Flowchart")
    
    # Add nodes
    diagram = client.add_node(diagram, "Start", 100, 40, 120, 40)
    diagram = client.add_node(diagram, "Process Data", 100, 160, 120, 60)
    diagram = client.add_node(diagram, "Decision", 100, 300, 120, 60)
    diagram = client.add_node(diagram, "End Success", 240, 420, 120, 40)
    diagram = client.add_node(diagram, "End Failure", -40, 420, 120, 40)
    
    # Find node IDs
    start_id = diagram["cells"][0]["id"]
    process_id = diagram["cells"][1]["id"]
    decision_id = diagram["cells"][2]["id"]
    success_id = diagram["cells"][3]["id"]
    failure_id = diagram["cells"][4]["id"]
    
    # Add edges
    diagram = client.add_edge(diagram, start_id, process_id)
    diagram = client.add_edge(diagram, process_id, decision_id)
    diagram = client.add_edge(diagram, decision_id, success_id, "Yes")
    diagram = client.add_edge(diagram, decision_id, failure_id, "No")
    
    # Export and print the diagram
    export_data = client.export_diagram(diagram)
    print(f"Diagram created successfully: {diagram['title']}")
    
    # Save to file for inspection
    with open("simple_flowchart.json", "w") as f:
        f.write(export_data)
    
    print(f"Diagram exported to simple_flowchart.json")


if __name__ == "__main__":
    main()