"""Draw.io API client implementation."""

import json
import os
import base64
import requests
import urllib.parse
import xml.etree.ElementTree as ET
import xml.dom.minidom
from typing import Dict, Any, Optional, List, Union


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

    def add_node(
        self,
        diagram: Dict[str, Any],
        label: str,
        x: float,
        y: float,
        width: float = 120,
        height: float = 60,
        style: Optional[str] = None,
    ) -> Dict[str, Any]:
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
            "style": style or "rounded=1;whiteSpace=wrap;html=1;",
        }

        diagram["cells"].append(node)
        diagram["modified"] = True

        return diagram

    def add_edge(
        self,
        diagram: Dict[str, Any],
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        style: Optional[str] = None,
    ) -> Dict[str, Any]:
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
            "style": style or "endArrow=classic;html=1;rounded=0;",
        }

        diagram["cells"].append(edge)
        diagram["modified"] = True

        return diagram

    def export_diagram(self, diagram: Dict[str, Any], format: str = "xml") -> str:
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
        """Convert a diagram from JSON to XML format compatible with Draw.io.

        Args:
            diagram: The diagram in JSON format

        Returns:
            The diagram in XML format
        """
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

    def get_preview_url(self, xml_data: str, title: str = "Diagram") -> str:
        """Generate a URL to preview the diagram in Draw.io.

        Args:
            xml_data: The diagram data in XML format
            title: The title of the diagram

        Returns:
            A URL that can be used to view the diagram in Draw.io
        """
        # Encode the XML data
        encoded_data = base64.b64encode(xml_data.encode("utf-8")).decode("utf-8")
        url_encoded = urllib.parse.quote(encoded_data)

        # Construct the URL
        preview_url = f"{self.base_url}?lightbox=1&edit=_blank&layers=1&nav=1&title={urllib.parse.quote(title)}&xml={url_encoded}"

        return preview_url
        
    def generate_html_viewer(self, xml_data: str, title: str = "Diagram") -> str:
        """Generate a standalone HTML page that displays the diagram.
        
        Args:
            xml_data: The diagram data in XML format
            title: The title of the diagram
            
        Returns:
            HTML content that can be saved to a file and opened in a browser
        """
        # Create a self-contained HTML file with the XML data embedded
        encoded_data = base64.b64encode(xml_data.encode('utf-8')).decode('utf-8')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Draw.io Viewer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
        }}
        .iframe-container {{
            width: 100%;
            height: 600px;
            border: 1px solid #ddd;
            margin-top: 20px;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        .info {{
            margin-top: 20px;
            padding: 15px;
            background-color: #e8f4f8;
            border-radius: 4px;
        }}
        #diagram-container {{
            width: 100%;
            height: 600px;
            border: 1px solid #ddd;
            overflow: auto;
            margin-top: 20px;
        }}
        pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 12px;
            padding: 10px;
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-top: 20px;
            height: 200px;
            overflow: auto;
            display: none;
        }}
        .button-container {{
            margin-top: 10px;
        }}
        button {{
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
        }}
        button:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        
        <div class="button-container">
            <button onclick="openInDrawIo()">Open in Draw.io</button>
            <button onclick="toggleXmlView()">Toggle XML View</button>
        </div>
        
        <div id="diagram-container">
            <iframe id="diagram-iframe" src="{self.base_url}?embed=1&ui=atlas&spin=1&proto=json&hideScrollbars=1" frameborder="0" allowfullscreen></iframe>
        </div>
        
        <pre id="xml-view">{xml_data}</pre>
        
        <div class="info">
            <h3>使い方</h3>
            <p>このダイアグラムは Draw.io API を使用してプログラムで作成されています。</p>
            <p>「Open in Draw.io」ボタンをクリックすると、Draw.io で直接開いて編集できます。</p>
            <p>「Toggle XML View」ボタンをクリックすると、XML データを表示/非表示できます。</p>
        </div>
    </div>
    
    <script>
        // ダイアグラムデータ (Base64エンコード)
        const diagramData = "{encoded_data}";
        
        // Draw.ioでダイアグラムを開く
        function openInDrawIo() {{
            const url = '{self.base_url}?lightbox=1&edit=_blank&layers=1&nav=1&title={urllib.parse.quote(title)}&xml=' + encodeURIComponent(diagramData);
            window.open(url, '_blank');
        }}
        
        // XMLビューの表示/非表示を切り替える
        function toggleXmlView() {{
            const xmlView = document.getElementById('xml-view');
            xmlView.style.display = xmlView.style.display === 'none' ? 'block' : 'none';
        }}
        
        // ページ読み込み時にダイアグラムを設定
        window.onload = function() {{
            // iframe内のDrawioクライアントがロードされたらダイアグラムを設定
            const iframe = document.getElementById('diagram-iframe');
            iframe.addEventListener('load', function() {{
                // 少し待ってからダイアグラムデータを送信（Draw.ioの初期化を待つ）
                setTimeout(function() {{
                    try {{
                        // Base64デコードしてXMLを取得
                        const xmlData = atob(diagramData);
                        
                        // iframeにメッセージを送信
                        iframe.contentWindow.postMessage(JSON.stringify({{
                            action: 'load',
                            xml: xmlData
                        }}), '*');
                    }} catch (error) {{
                        console.error('Failed to load diagram:', error);
                    }}
                }}, 1000);
            }});
        }};
    </script>
</body>
</html>
"""
        return html
        
    def save_diagram_for_web(self, xml_data: str, output_path: str, title: str = "Diagram") -> str:
        """Save the diagram as an HTML file that can be opened in a browser.
        
        Args:
            xml_data: The diagram data in XML format
            output_path: The path to save the HTML file to
            title: The title of the diagram
            
        Returns:
            The absolute path to the saved HTML file
        """
        html_content = self.generate_html_viewer(xml_data, title)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        return os.path.abspath(output_path)
