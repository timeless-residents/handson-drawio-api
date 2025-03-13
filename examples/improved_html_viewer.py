"""Example of creating a diagram and generating an improved HTML viewer."""

import sys
import os
import webbrowser

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.drawio_api.client import DrawioAPIClient


def create_sample_diagram():
    """Create a simple class diagram."""
    client = DrawioAPIClient()
    
    # Create a new diagram
    diagram = client.create_diagram(title="クラス図サンプル")
    
    # スタイル定義
    class_style = "shape=ext;jettySize=10;html=1;whiteSpace=wrap;fontSize=11;align=center;strokeColor=#000000;fillColor=#E1F5FE;"
    interface_style = "shape=ext;jettySize=10;html=1;whiteSpace=wrap;fontSize=11;dashed=1;align=center;strokeColor=#000000;fillColor=#FFF8E1;"
    arrow_style = "endArrow=block;html=1;rounded=0;endFill=0;edgeStyle=elbowEdgeStyle;endSize=12;exitX=0.5;exitY=0;entryX=0.5;entryY=1;"
    association_style = "endArrow=open;html=1;rounded=0;endFill=0;edgeStyle=elbowEdgeStyle;endSize=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
    
    # クラスとインターフェース
    diagram = client.add_node(
        diagram,
        "<<interface>>\nAnimal\n+ makeSound(): void",
        400, 
        80, 
        200, 
        80,
        interface_style
    )
    
    diagram = client.add_node(
        diagram,
        "Dog\n- name: String\n+ makeSound(): void\n+ fetch(): void",
        200, 
        240, 
        200, 
        100,
        class_style
    )
    
    diagram = client.add_node(
        diagram,
        "Cat\n- name: String\n+ makeSound(): void\n+ purr(): void",
        600, 
        240, 
        200, 
        100,
        class_style
    )
    
    diagram = client.add_node(
        diagram,
        "AnimalFactory\n+ createAnimal(type: String): Animal",
        400, 
        440, 
        200, 
        80,
        class_style
    )
    
    # Find node IDs
    interface_id = diagram["cells"][0]["id"]
    dog_id = diagram["cells"][1]["id"]
    cat_id = diagram["cells"][2]["id"]
    factory_id = diagram["cells"][3]["id"]
    
    # Add relationships
    diagram = client.add_edge(diagram, dog_id, interface_id, style=arrow_style)
    diagram = client.add_edge(diagram, cat_id, interface_id, style=arrow_style)
    diagram = client.add_edge(diagram, factory_id, dog_id, style=association_style)
    diagram = client.add_edge(diagram, factory_id, cat_id, style=association_style)
    
    return diagram


def main():
    """Generate a diagram and create an improved HTML viewer for it."""
    client = DrawioAPIClient()
    
    # Create a sample class diagram
    diagram = create_sample_diagram()
    
    # Export to XML format
    xml_data = client.export_diagram(diagram, format="xml")
    
    # Save to file using the new helper function
    output_path = "class_diagram_viewer.html"
    html_file_path = client.save_diagram_for_web(xml_data, output_path, title=diagram["title"])
    
    print(f"Diagram created: {diagram['title']}")
    print(f"HTML viewer created: {output_path}")
    
    # Open the HTML viewer in the default web browser
    print("\nOpening HTML viewer in browser...")
    webbrowser.open('file://' + html_file_path)


if __name__ == "__main__":
    main()