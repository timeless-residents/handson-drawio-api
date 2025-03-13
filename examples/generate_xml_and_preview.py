"""Example of generating XML from JSON and creating a web preview link."""

import sys
import os
import webbrowser

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.drawio_api.client import DrawioAPIClient


def main():
    """Create a diagram, export to XML, and generate a preview URL."""
    client = DrawioAPIClient()
    
    # Create a new diagram - a simple organization chart
    diagram = client.create_diagram(title="Organization Chart")
    
    # Add nodes for the organization chart
    diagram = client.add_node(
        diagram, 
        "CEO", 
        400, 
        40, 
        120, 
        60, 
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    # Add VPs
    diagram = client.add_node(
        diagram, 
        "VP Engineering", 
        200, 
        160, 
        120, 
        60, 
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    
    diagram = client.add_node(
        diagram, 
        "VP Marketing", 
        400, 
        160, 
        120, 
        60, 
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    
    diagram = client.add_node(
        diagram, 
        "VP Sales", 
        600, 
        160, 
        120, 
        60, 
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    
    # Add managers
    diagram = client.add_node(
        diagram, 
        "Dev Manager", 
        100, 
        280, 
        120, 
        60, 
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    diagram = client.add_node(
        diagram, 
        "QA Manager", 
        300, 
        280, 
        120, 
        60, 
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    diagram = client.add_node(
        diagram, 
        "Marketing Manager", 
        400, 
        280, 
        120, 
        60, 
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    diagram = client.add_node(
        diagram, 
        "Sales Manager", 
        600, 
        280, 
        120, 
        60, 
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    # Find node IDs
    ceo_id = diagram["cells"][0]["id"]
    vp_eng_id = diagram["cells"][1]["id"]
    vp_marketing_id = diagram["cells"][2]["id"]
    vp_sales_id = diagram["cells"][3]["id"]
    dev_manager_id = diagram["cells"][4]["id"]
    qa_manager_id = diagram["cells"][5]["id"]
    marketing_manager_id = diagram["cells"][6]["id"]
    sales_manager_id = diagram["cells"][7]["id"]
    
    # Add edges
    diagram = client.add_edge(
        diagram, 
        ceo_id, 
        vp_eng_id, 
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, 
        ceo_id, 
        vp_marketing_id, 
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, 
        ceo_id, 
        vp_sales_id, 
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, 
        vp_eng_id, 
        dev_manager_id, 
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, 
        vp_eng_id, 
        qa_manager_id, 
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, 
        vp_marketing_id, 
        marketing_manager_id, 
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    diagram = client.add_edge(
        diagram, 
        vp_sales_id, 
        sales_manager_id, 
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    )
    
    # Export to JSON and print the diagram
    json_data = client.export_diagram(diagram, format="json")
    print(f"Diagram created successfully: {diagram['title']}")
    
    # Save JSON to file for inspection
    with open("organization_chart.json", "w") as f:
        f.write(json_data)
    
    print(f"Diagram exported to organization_chart.json")
    
    # Convert to XML format
    xml_data = client.export_diagram(diagram, format="xml")
    
    # Save XML to file for inspection
    with open("organization_chart.xml", "w") as f:
        f.write(xml_data)
        
    print(f"Diagram exported to organization_chart.xml")
    
    # Generate a preview URL
    preview_url = client.get_preview_url(xml_data, title=diagram["title"])
    
    print(f"\nPreview URL generated:")
    print(preview_url)
    
    print("\nOpening diagram in web browser...")
    webbrowser.open(preview_url)
    
    print("\nUsage Instructions:")
    print("1. The diagram should open in your default web browser")
    print("2. You can edit the diagram by clicking 'Edit' in the web interface")
    print("3. To save your changes, use File > Save As in the web interface")


if __name__ == "__main__":
    main()