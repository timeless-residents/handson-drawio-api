"""Example of generating a standalone HTML viewer for a Draw.io diagram."""

import sys
import os
import webbrowser

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.drawio_api.client import DrawioAPIClient


def create_sample_diagram():
    """Create a sample network diagram."""
    client = DrawioAPIClient()
    
    # Create a new diagram
    diagram = client.create_diagram(title="Network Diagram")
    
    # Add nodes for the network diagram with different styles
    diagram = client.add_node(
        diagram, 
        "Internet", 
        400, 
        40, 
        120, 
        60, 
        "ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;"
    )
    
    diagram = client.add_node(
        diagram, 
        "Firewall", 
        400, 
        160, 
        120, 
        60, 
        "rhombus;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
    )
    
    diagram = client.add_node(
        diagram, 
        "Router", 
        400, 
        280, 
        120, 
        60, 
        "triangle;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    )
    
    diagram = client.add_node(
        diagram, 
        "Switch", 
        400, 
        400, 
        120, 
        60, 
        "shape=process;whiteSpace=wrap;html=1;backgroundOutline=1;fillColor=#d5e8d4;strokeColor=#82b366;"
    )
    
    # Add servers
    diagram = client.add_node(
        diagram, 
        "Web Server", 
        200, 
        520, 
        120, 
        60, 
        "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    diagram = client.add_node(
        diagram, 
        "Database", 
        400, 
        520, 
        120, 
        60, 
        "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    diagram = client.add_node(
        diagram, 
        "File Server", 
        600, 
        520, 
        120, 
        60, 
        "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;"
    )
    
    # Find node IDs
    internet_id = diagram["cells"][0]["id"]
    firewall_id = diagram["cells"][1]["id"]
    router_id = diagram["cells"][2]["id"]
    switch_id = diagram["cells"][3]["id"]
    web_server_id = diagram["cells"][4]["id"]
    database_id = diagram["cells"][5]["id"]
    file_server_id = diagram["cells"][6]["id"]
    
    # Add edges
    edge_style = "endArrow=classic;startArrow=classic;html=1;rounded=0;strokeWidth=2;"
    
    diagram = client.add_edge(diagram, internet_id, firewall_id, style=edge_style)
    diagram = client.add_edge(diagram, firewall_id, router_id, style=edge_style)
    diagram = client.add_edge(diagram, router_id, switch_id, style=edge_style)
    diagram = client.add_edge(diagram, switch_id, web_server_id, style=edge_style)
    diagram = client.add_edge(diagram, switch_id, database_id, style=edge_style)
    diagram = client.add_edge(diagram, switch_id, file_server_id, style=edge_style)
    
    return diagram


def main():
    """Generate a diagram and create an HTML viewer for it."""
    client = DrawioAPIClient()
    
    # Create a sample network diagram
    diagram = create_sample_diagram()
    
    # Export to XML format
    xml_data = client.export_diagram(diagram, format="xml")
    
    # Save XML to file for reference
    with open("network_diagram.xml", "w") as f:
        f.write(xml_data)
    
    # Generate a preview URL
    preview_url = client.get_preview_url(xml_data, title=diagram["title"])
    
    # Read the HTML template
    template_path = os.path.join(os.path.dirname(__file__), "html_viewer_template.html")
    with open(template_path, "r") as f:
        html_template = f.read()
    
    # Replace the placeholder with the actual diagram URL
    html_content = html_template.replace("DIAGRAM_URL", preview_url)
    
    # Save the HTML file
    output_path = "network_diagram_viewer.html"
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"Diagram created: {diagram['title']}")
    print(f"XML exported to: network_diagram.xml")
    print(f"HTML viewer created: {output_path}")
    
    # Open the HTML viewer in the default web browser
    print("\nOpening HTML viewer in browser...")
    webbrowser.open('file://' + os.path.abspath(output_path))


if __name__ == "__main__":
    main()