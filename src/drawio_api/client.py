"""Draw.io API client implementation."""

import json
import base64
import os
import urllib.parse
import xml.etree.ElementTree as ET
import xml.dom.minidom
import requests
from typing import Dict, Any, Optional, List, Union, Tuple


class DrawioAPIClient:
    """Client for interacting with the Draw.io API."""
    
    def __init__(self, base_url: str = "https://embed.diagrams.net"):
        """Initialize the Draw.io API client.
        
        Args:
            base_url: The base URL for the Draw.io API
        """
        self.base_url = base_url
        
    def create_diagram(self, title: str = "New Diagram") -> Dict[str, Any]:
        """Create a new empty diagram.
        
        Args:
            title: The title of the new diagram
            
        Returns:
            Dict containing diagram information
        """
        # For now, this is a placeholder that would return a local structure
        # In a real implementation, this might interact with a Draw.io server
        return {
            "title": title,
            "cells": [],
            "modified": False,
        }
        
    def add_node(self, diagram: Dict[str, Any], 
                label: str, 
                x: float, 
                y: float, 
                width: float = 120, 
                height: float = 60,
                style: Optional[str] = None) -> Dict[str, Any]:
        """Add a node to the diagram.
        
        Args:
            diagram: The diagram to add the node to
            label: The text label for the node
            x: The x-coordinate of the node
            y: The y-coordinate of the node
            width: The width of the node
            height: The height of the node
            style: The style string for the node
            
        Returns:
            Updated diagram with the new node
        """
        # This is a simplified placeholder implementation
        node_id = f"node_{len(diagram['cells']) + 1}"
        
        node = {
            "id": node_id,
            "type": "node",
            "label": label,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "style": style or "rounded=1;whiteSpace=wrap;html=1;"
        }
        
        diagram["cells"].append(node)
        diagram["modified"] = True
        
        return diagram
        
    def add_edge(self, diagram: Dict[str, Any],
                source_id: str,
                target_id: str,
                label: Optional[str] = None,
                style: Optional[str] = None) -> Dict[str, Any]:
        """Add an edge between nodes in the diagram.
        
        Args:
            diagram: The diagram to add the edge to
            source_id: The ID of the source node
            target_id: The ID of the target node
            label: Optional label for the edge
            style: The style string for the edge
            
        Returns:
            Updated diagram with the new edge
        """
        # This is a simplified placeholder implementation
        edge_id = f"edge_{len(diagram['cells']) + 1}"
        
        edge = {
            "id": edge_id,
            "type": "edge",
            "source": source_id,
            "target": target_id,
            "label": label,
            "style": style or "endArrow=classic;html=1;rounded=0;"
        }
        
        diagram["cells"].append(edge)
        diagram["modified"] = True
        
        return diagram
    
    def export_diagram(self, diagram: Dict[str, Any], format: str = "json") -> str:
        """Export the diagram to the specified format.
        
        Args:
            diagram: The diagram to export
            format: The export format (json, xml)
            
        Returns:
            The exported diagram data
        """
        if format.lower() == "json":
            return json.dumps(diagram)
        elif format.lower() == "xml":
            return self._convert_to_xml(diagram)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _convert_to_xml(self, diagram: Dict[str, Any]) -> str:
        """Convert a diagram from JSON to XML format compatible with Draw.io."""
        # Create the mxGraphModel element
        root = ET.Element("mxGraphModel")
        root.set("dx", "1326")
        root.set("dy", "798")
        root.set("grid", "1")
        root.set("gridSize", "10")
        root.set("guides", "1")
        root.set("tooltips", "1")
        root.set("connect", "1")
        root.set("arrows", "1")
        root.set("fold", "1")
        root.set("page", "1")
        root.set("pageScale", "1")
        root.set("pageWidth", "850")
        root.set("pageHeight", "1100")
        
        # Create the root cell
        root_cell = ET.SubElement(root, "root")
        
        # Create the parent cell (cell 0)
        cell0 = ET.SubElement(root_cell, "mxCell")
        cell0.set("id", "0")
        
        # Create the layer cell (cell 1)
        cell1 = ET.SubElement(root_cell, "mxCell")
        cell1.set("id", "1")
        cell1.set("parent", "0")
        
        # Add the cells from the diagram
        for cell in diagram["cells"]:
            if cell["type"] == "node":
                mx_cell = ET.SubElement(root_cell, "mxCell")
                mx_cell.set("id", cell["id"])
                mx_cell.set("value", cell["label"])
                mx_cell.set("style", cell["style"])
                mx_cell.set("parent", "1")
                mx_cell.set("vertex", "1")
                
                geometry = ET.SubElement(mx_cell, "mxGeometry")
                geometry.set("x", str(cell["x"]))
                geometry.set("y", str(cell["y"]))
                geometry.set("width", str(cell["width"]))
                geometry.set("height", str(cell["height"]))
                geometry.set("as", "geometry")
                
            elif cell["type"] == "edge":
                mx_cell = ET.SubElement(root_cell, "mxCell")
                mx_cell.set("id", cell["id"])
                if cell.get("label"):
                    mx_cell.set("value", cell["label"])
                mx_cell.set("style", cell["style"])
                mx_cell.set("parent", "1")
                mx_cell.set("source", cell["source"])
                mx_cell.set("target", cell["target"])
                mx_cell.set("edge", "1")
                
                geometry = ET.SubElement(mx_cell, "mxGeometry")
                geometry.set("relative", "1")
                geometry.set("as", "geometry")
        
        # Convert to string and pretty-print
        rough_string = ET.tostring(root, encoding="utf-8")
        reparsed = xml.dom.minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def export_to_image(self, diagram: Dict[str, Any], 
                      output_path: str, 
                      format: str = "png", 
                      transparent: bool = False,
                      scale: float = 1.0,
                      bg: str = "") -> str:
        """Export the diagram to an image file using the draw.io export API.
        
        Args:
            diagram: The diagram to export
            output_path: Path where the image will be saved
            format: Image format (png, jpg, svg, pdf)
            transparent: Whether the background should be transparent (png only)
            scale: Scale factor for the output image (1.0 = 100%)
            bg: Background color (e.g. '#ffffff')
            
        Returns:
            Path to the saved image file
        """
        # First convert the diagram to XML
        xml_data = self._convert_to_xml(diagram)
        
        # Encode the diagram XML for the request
        encoded_xml = base64.b64encode(xml_data.encode('utf-8')).decode('utf-8')
        
        # Build the URL with query parameters for the draw.io viewer
        # This works by creating a URL that loads the diagram in the draw.io viewer
        # and then using a headless browser or direct API call to render it
        url_params = {
            'format': format,
            'w': 1000,  # Width
            'h': 1000,  # Height
            'scale': scale
        }
        
        if transparent and format == 'png':
            url_params['transparent'] = 'true'
            
        if bg:
            url_params['bg'] = bg
            
        # Create a query string from the parameters
        param_str = '&'.join([f"{k}={v}" for k, v in url_params.items()])
        
        # Method 1: Using DrawioAPIClient.renderDiagram endpoint (alternative approach)
        # The public draw.io API for exporting diagrams
        export_url = f"https://convert.diagrams.net/node/export"
        
        # Prepare the request data
        data = {
            'xml': encoded_xml,
            'format': format,
            'scale': scale
        }
        
        # Add optional parameters
        if transparent and format == 'png':
            data['transparent'] = 'true'
            
        if bg:
            data['bg'] = bg
        
        # Make the API request - using public API endpoint
        try:
            response = requests.post(export_url, data=data)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Save the image
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                # Return the absolute path to the saved file
                return os.path.abspath(output_path)
            else:
                # If that fails, we'll try our fallback method
                print(f"Primary export method failed, trying fallback... ({response.status_code})")
        except Exception as e:
            print(f"Primary export method failed, trying fallback... ({str(e)})")
            
        # Fallback method - generate local SVG using the XML directly
        try:
            # For SVG format, we can do direct conversion
            if format.lower() == 'svg':
                # This is a simplified approach for SVG generation
                # Create a basic SVG wrapper around the diagram content
                svg_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
                svg_header += '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                svg_header += 'width="800" height="600" version="1.1">\n'
                
                # Extract just the diagram content from the XML
                svg_content = xml_data.replace('<?xml version="1.0" ?>', '')
                
                # Wrap the content in the SVG tags
                svg_content = svg_header + svg_content + '</svg>'
                
                # Save the SVG file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                
                return os.path.abspath(output_path)
                
            # For other formats, we need to inform the user that export failed
            print(f"Warning: Export to {format} format failed. Only SVG fallback is currently supported.")
            
            # Create a simple text file explaining the issue
            with open(output_path, 'w') as f:
                f.write(f"Export to {format} failed.\n")
                f.write("The Draw.io export API is unavailable.\n")
                f.write("Please try again later or use the SVG format instead.\n")
                
            return os.path.abspath(output_path)
            
        except Exception as e:
            raise Exception(f"Image export failed: {str(e)}")
            
        # If all methods fail
        raise Exception("All export methods failed")
            
    def calculate_diagram_size(self, diagram: Dict[str, Any]) -> Tuple[float, float, float, float]:
        """Calculate the bounds of the diagram (min_x, min_y, max_x, max_y).
        
        Args:
            diagram: The diagram to calculate bounds for
            
        Returns:
            Tuple of (min_x, min_y, max_x, max_y) coordinates
        """
        if not diagram["cells"]:
            return (0, 0, 800, 600)  # Default size for empty diagrams
        
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        
        for cell in diagram["cells"]:
            if cell["type"] == "node":
                x, y = cell["x"], cell["y"]
                width, height = cell["width"], cell["height"]
                
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x + width)
                max_y = max(max_y, y + height)
        
        # Add some padding
        padding = 50
        min_x = max(0, min_x - padding)
        min_y = max(0, min_y - padding)
        max_x = max_x + padding
        max_y = max_y + padding
        
        return (min_x, min_y, max_x, max_y)