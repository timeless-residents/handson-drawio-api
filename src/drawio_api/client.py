"""Draw.io API client implementation."""

import json
import base64
import os
import time
import urllib.parse
import xml.etree.ElementTree as ET
import xml.dom.minidom
import requests
import tempfile
from typing import Dict, Any, Optional, List, Union, Tuple

# Optional imports - will be used if available
try:
    import cairosvg
    CAIROSVG_AVAILABLE = True
except ImportError:
    CAIROSVG_AVAILABLE = False

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


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
            format: The export format (json, xml, drawio)
            
        Returns:
            The exported diagram data
        """
        # Create a copy of the diagram to avoid modifying the original
        diagram_copy = diagram.copy()
        
        if format.lower() == "json":
            return json.dumps(diagram_copy)
        elif format.lower() == "xml":
            return self._convert_to_xml(diagram_copy)
        elif format.lower() == "drawio":
            # Mark this diagram for drawio format
            diagram_copy["_format"] = "drawio"
            # .drawio format is XML wrapped in a specific way for Draw.io
            xml_content = self._convert_to_xml(diagram_copy)
            return self._create_drawio_file(xml_content, diagram_copy.get("title", "Diagram"))
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _create_drawio_file(self, xml_content: str, title: str) -> str:
        """Create a .drawio file format from XML content.
        
        Args:
            xml_content: The diagram content in XML format
            title: The diagram title
            
        Returns:
            The diagram in .drawio format
        """
        # Strip XML declaration as it will be included in the mxfile
        xml_content = xml_content.replace('<?xml version="1.0" encoding="UTF-8"?>\n', '')
        
        # In Draw.io format, the diagram content is stored as uncompressed XML
        # (No URL-safe Base64 encoding as originally implemented)
        
        # Create the mxfile structure used by Draw.io
        drawio_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="{int(time.time())}" agent="Draw.io API Client" version="21.1.2" type="device">
  <diagram id="diagram-id" name="{title}">
    <mxGraphModel dx="1326" dy="798" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100">
      {xml_content.strip()}
    </mxGraphModel>
  </diagram>
</mxfile>"""
        
        return drawio_content
    
    def _convert_to_xml(self, diagram: Dict[str, Any]) -> str:
        """Convert a diagram from JSON to XML format compatible with Draw.io."""
        # For the drawio format, we'll just create the inner cells part
        # as the mxGraphModel wrapper will be added by _create_drawio_file
        
        # Create the root cell
        root = ET.Element("root")
        
        # Create the parent cell (cell 0)
        cell0 = ET.SubElement(root, "mxCell")
        cell0.set("id", "0")
        
        # Create the layer cell (cell 1)
        cell1 = ET.SubElement(root, "mxCell")
        cell1.set("id", "1")
        cell1.set("parent", "0")
        
        # Add the cells from the diagram
        for cell in diagram["cells"]:
            if cell["type"] == "node":
                mx_cell = ET.SubElement(root, "mxCell")
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
                mx_cell = ET.SubElement(root, "mxCell")
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
        
        # Convert to string with XML declaration for standard XML format
        rough_string = ET.tostring(root, encoding="utf-8")
        reparsed = xml.dom.minidom.parseString(rough_string)
        
        # For non-drawio format (just XML), we'll wrap it in mxGraphModel
        if diagram.get("_format", "") != "drawio":
            # Wrap in mxGraphModel for standard XML output
            full_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
            full_xml += '<mxGraphModel dx="1326" dy="798" grid="1" gridSize="10" guides="1" '
            full_xml += 'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            full_xml += 'pageWidth="850" pageHeight="1100">\n'
            full_xml += reparsed.toprettyxml(indent="  ").replace('<?xml version="1.0" ?>\n', '')
            full_xml += '</mxGraphModel>'
            return full_xml
        
        # For drawio format, just return the inner XML
        return reparsed.toprettyxml(indent="  ").replace('<?xml version="1.0" ?>\n', '')
    
    def export_to_image(self, diagram: Dict[str, Any], 
                      output_path: str, 
                      format: str = "png", 
                      transparent: bool = False,
                      scale: float = 1.0,
                      bg: str = "") -> str:
        """Export the diagram to an image file.
        
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
        # For SVG format, we'll use our own implementation
        if format.lower() == 'svg':
            return self._create_svg_from_diagram(diagram, output_path)
            
        # For PNG, JPG and PDF formats, we'll use CairoSVG if available
        if format.lower() in ['png', 'jpg', 'jpeg', 'pdf'] and CAIROSVG_AVAILABLE:
            # First create an SVG file
            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp_svg:
                svg_path = temp_svg.name
            
            # Generate SVG file
            self._create_svg_from_diagram(diagram, svg_path)
            
            # Convert to the target format using CairoSVG
            try:
                if format.lower() == 'png':
                    # Handle transparency
                    if transparent:
                        cairosvg.svg2png(url=svg_path, write_to=output_path, 
                                        scale=scale, background_color="transparent")
                    else:
                        background_color = bg if bg else "#ffffff"
                        cairosvg.svg2png(url=svg_path, write_to=output_path, 
                                        scale=scale, background_color=background_color)
                elif format.lower() in ['jpg', 'jpeg']:
                    # JPEG doesn't support transparency
                    background_color = bg if bg else "#ffffff"
                    cairosvg.svg2png(url=svg_path, write_to=output_path + ".png", 
                                    scale=scale, background_color=background_color)
                    
                    # Convert PNG to JPEG using Pillow
                    if PILLOW_AVAILABLE:
                        with Image.open(output_path + ".png") as img:
                            # Save as JPEG with white background
                            rgb_img = img.convert('RGB')
                            rgb_img.save(output_path, quality=95)
                        # Remove temporary PNG
                        os.remove(output_path + ".png")
                    else:
                        # If Pillow is not available, just keep the PNG
                        os.rename(output_path + ".png", output_path)
                        print("Warning: Pillow not available. Saved as PNG instead of JPEG.")
                        
                elif format.lower() == 'pdf':
                    cairosvg.svg2pdf(url=svg_path, write_to=output_path, scale=scale)
                
                # Clean up temporary SVG file
                os.remove(svg_path)
                
                print(f"Successfully exported diagram to {os.path.basename(output_path)}")
                return os.path.abspath(output_path)
                
            except Exception as e:
                print(f"Error converting SVG to {format.upper()}: {str(e)}")
                print("Falling back to HTML export helper method...")
                # If conversion fails, fall back to the original method
                os.remove(svg_path)
        
        # If we get here, either:
        # 1. The format is not supported for direct conversion
        # 2. CairoSVG is not available
        # 3. The conversion failed
        
        # First convert the diagram to XML
        xml_data = self._convert_to_xml(diagram)
        bounds = self.calculate_diagram_size(diagram)
        encoded_xml = urllib.parse.quote(xml_data)
        
        # Create a basic HTML file with embed URL to export the image
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Diagram Export</title>
    <style>
        body {{ margin: 0; overflow: hidden; }}
        iframe {{ border: none; width: 100%; height: 100vh; }}
    </style>
</head>
<body>
    <p>Export this diagram using right-click → "Save image as..." option:</p>
    <img src="{self.base_url}?embed=1&proto=json&spin=1" alt="Diagram" id="diagram" />
    
    <script>
        // The diagram data
        const diagramXML = decodeURIComponent("{encoded_xml}");
        
        // A function to save the SVG as a file
        function exportImage() {{
            const img = document.getElementById('diagram');
            img.src = "{self.base_url}?embed=1&proto=json&spin=1";
            
            // We'd update the image source with our XML data
            // but this doesn't work without browser automation
            console.log("Please manually export the image");
        }}
        
        // Try to export automatically
        window.onload = exportImage;
    </script>
</body>
</html>"""

        # Generate a simple HTML file that can be opened in a browser
        html_path = f"{output_path}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        library_advice = ""
        if not CAIROSVG_AVAILABLE:
            library_advice = f"""
NOTE: For automatic {format.upper()} generation, install CairoSVG and Pillow:
    pip install cairosvg Pillow
"""
        
        # Save a dummy image file
        dummy_image_content = f"""
This is a dummy {format.upper()} file. The API to automatically generate {format.upper()} files requires additional libraries or a web browser.
{library_advice}
INSTRUCTIONS:
1. Open the accompanying HTML file ({os.path.basename(html_path)}) in a web browser
2. Right-click on the diagram and select "Save image as..."
3. Save the image as {os.path.basename(output_path)}

ALTERNATIVE:
Use the SVG format instead, which can be generated directly:
    client.export_to_image(diagram, "diagram.svg", format="svg")
"""
        
        with open(output_path, 'w') as f:
            f.write(dummy_image_content)
            
        print(f"Created HTML export helper: {html_path}")
        print(f"Note: Open this HTML file in a browser and use 'Save image as...' to export the diagram")
            
        return os.path.abspath(output_path)
        
    def _create_svg_from_diagram(self, diagram: Dict[str, Any], output_path: str) -> str:
        """Create an SVG file from a diagram.
        
        Args:
            diagram: The diagram to convert to SVG
            output_path: Where to save the SVG file
            
        Returns:
            Absolute path to the saved SVG file
        """
        # Calculate diagram bounds
        bounds = self.calculate_diagram_size(diagram)
        min_x, min_y, max_x, max_y = bounds
        width = max_x - min_x
        height = max_y - min_y
        
        # Start SVG file with the right size and arrow marker definition - simplified modern format
        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" height="{height}" 
     viewBox="{min_x} {min_y} {width} {height}">
     
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="#000"/>
        </marker>
    </defs>
    
    <!-- White background -->
    <rect x="{min_x}" y="{min_y}" width="{width}" height="{height}" fill="white"/>
"""
        
        # For each node in the diagram, create an SVG element
        for cell in diagram["cells"]:
            if cell["type"] == "node":
                x, y = cell["x"], cell["y"]
                w, h = cell["width"], cell["height"]
                label = cell["label"]
                
                # Parse the style to get fill, stroke, etc.
                style = cell["style"]
                fill_color = "#dae8fc"  # Default blue fill
                stroke_color = "#6c8ebf"  # Default blue stroke
                
                # Extract style properties
                style_props = dict(prop.split("=") for prop in style.split(";") if "=" in prop)
                
                if "fillColor" in style_props:
                    fill_color = style_props["fillColor"]
                if "strokeColor" in style_props:
                    stroke_color = style_props["strokeColor"]
                
                # Determine shape type from style
                shape_type = "rect"
                rx = 6  # Default rounded corners
                if "rounded=0" in style:
                    rx = 0
                if "rhombus" in style:
                    shape_type = "polygon"
                    points = f"{x},{y+h/2} {x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h}"
                elif "ellipse" in style:
                    shape_type = "ellipse"
                    cx, cy = x + w/2, y + h/2
                    rx, ry = w/2, h/2
                elif "cylinder" in style:
                    shape_type = "cylinder"
                    cylinder_height = min(h * 0.3, 20)  # Height of the cylinder top part (proportional to height)
                    
                # Create the shape element
                if shape_type == "rect":
                    svg_content += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1"/>\n'
                elif shape_type == "ellipse":
                    svg_content += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1"/>\n'
                elif shape_type == "polygon":
                    svg_content += f'<polygon points="{points}" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1"/>\n'
                elif shape_type == "cylinder":
                    # Draw the cylinder (database) shape using a group for better organization
                    ellipse_rx = w / 2
                    ellipse_ry = cylinder_height / 2
                    
                    # Create a simpler but more reliable cylinder representation
                    svg_content += f'<g class="database-cylinder">\n'
                    
                    # Body of the cylinder
                    svg_content += f'  <rect x="{x}" y="{y + ellipse_ry}" width="{w}" height="{h - 2*ellipse_ry}" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1"/>\n'
                    
                    # Top ellipse (cap) of cylinder
                    svg_content += f'  <ellipse cx="{x + ellipse_rx}" cy="{y + ellipse_ry}" rx="{ellipse_rx}" ry="{ellipse_ry}" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1"/>\n'
                    
                    # Bottom visible part - just the visible arc, no complete ellipse
                    # This is the front-facing half of the bottom ellipse
                    svg_content += f'  <path d="M {x} {y + h - ellipse_ry} Q {x + w/2} {y + h + ellipse_ry}, {x + w} {y + h - ellipse_ry}" fill="none" stroke="{stroke_color}" stroke-width="1"/>\n'
                    
                    # Sides of the cylinder - vertical lines connecting ellipses
                    svg_content += f'  <line x1="{x}" y1="{y + ellipse_ry}" x2="{x}" y2="{y + h - ellipse_ry}" stroke="{stroke_color}" stroke-width="1"/>\n'
                    svg_content += f'  <line x1="{x + w}" y1="{y + ellipse_ry}" x2="{x + w}" y2="{y + h - ellipse_ry}" stroke="{stroke_color}" stroke-width="1"/>\n'
                    
                    # Close the group
                    svg_content += f'</g>\n'
                
                # Add text label
                if "\n" in label:
                    lines = label.split("\n")
                    line_height = 16
                    y_offset = y + (h - (len(lines) * line_height)) / 2
                    
                    for i, line in enumerate(lines):
                        text_y = y_offset + (i + 0.7) * line_height
                        svg_content += f'<text x="{x + w/2}" y="{text_y}" text-anchor="middle" font-family="Arial" font-size="12">{line}</text>\n'
                else:
                    svg_content += f'<text x="{x + w/2}" y="{y + h/2 + 5}" text-anchor="middle" font-family="Arial" font-size="12">{label}</text>\n'
        
        # For each edge
        for cell in diagram["cells"]:
            if cell["type"] == "edge":
                # Find source and target nodes
                source_id = cell["source"]
                target_id = cell["target"]
                
                source_node = None
                target_node = None
                
                for node in diagram["cells"]:
                    if node["type"] == "node":
                        if node["id"] == source_id:
                            source_node = node
                        elif node["id"] == target_id:
                            target_node = node
                
                if source_node and target_node:
                    # Calculate start and end points
                    source_x = source_node["x"] + source_node["width"] / 2
                    source_y = source_node["y"] + source_node["height"]
                    
                    target_x = target_node["x"] + target_node["width"] / 2
                    target_y = target_node["y"]
                    
                    # For orthogonal edges with bends
                    if "edgeStyle=orthogonalEdgeStyle" in cell.get("style", ""):
                        # Draw orthogonal line with intermediate point
                        mid_y = (source_y + target_y) / 2
                        
                        # Path for orthogonal line
                        path = f"M {source_x} {source_y} L {source_x} {mid_y} L {target_x} {mid_y} L {target_x} {target_y}"
                        
                        # Determine arrow style
                        arrow_end = "url(#arrow)"  # Always use arrow by default
                        
                        stroke_color = "#000000"  # Default black
                        style_props = dict(prop.split("=") for prop in cell.get("style", "").split(";") if "=" in prop)
                        if "strokeColor" in style_props:
                            stroke_color = style_props["strokeColor"]
                            
                        # Draw the path
                        svg_content += f'<path d="{path}" fill="none" stroke="{stroke_color}" stroke-width="1" marker-end="{arrow_end}"/>\n'
                        
                        # Add label if present
                        if cell.get("label"):
                            # Position label at middle segment
                            label_x = (source_x + target_x) / 2
                            label_y = mid_y - 10
                            
                            # Determine text color
                            text_color = "#000000"  # Default black
                            if "fontColor" in style_props:
                                text_color = style_props["fontColor"]
                                
                            svg_content += f'<text x="{label_x}" y="{label_y}" text-anchor="middle" font-family="Arial" font-size="12" fill="{text_color}">{cell["label"]}</text>\n'
                            
                    else:
                        # Draw a straight line with an arrow
                        svg_content += f'<line x1="{source_x}" y1="{source_y}" x2="{target_x}" y2="{target_y}" stroke="black" stroke-width="1" marker-end="url(#arrow)"/>\n'
                        
                        # Add label if present
                        if cell.get("label"):
                            # Position label along the line
                            label_x = (source_x + target_x) / 2
                            label_y = (source_y + target_y) / 2 - 10
                            svg_content += f'<text x="{label_x}" y="{label_y}" text-anchor="middle" font-family="Arial" font-size="12">{cell["label"]}</text>\n'
        
        # Close the SVG
        svg_content += "</svg>"
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
            
        return os.path.abspath(output_path)
            
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
        min_x = min_x - padding  # Allow negative coordinates
        min_y = min_y - padding
        max_x = max_x + padding
        max_y = max_y + padding
        
        # Ensure we have a reasonable minimum viewing area
        if max_x - min_x < 500:
            center_x = (max_x + min_x) / 2
            min_x = center_x - 250
            max_x = center_x + 250
            
        if max_y - min_y < 500:
            center_y = (max_y + min_y) / 2
            min_y = center_y - 250
            max_y = center_y + 250
        
        return (min_x, min_y, max_x, max_y)