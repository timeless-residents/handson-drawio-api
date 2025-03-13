"""Tests for the Draw.io API client."""

import pytest
from src.drawio_api.client import DrawioAPIClient


def test_create_diagram():
    """Test creating a new diagram."""
    client = DrawioAPIClient()
    diagram = client.create_diagram(title="Test Diagram")
    
    assert diagram["title"] == "Test Diagram"
    assert len(diagram["cells"]) == 0
    assert diagram["modified"] is False


def test_add_node():
    """Test adding a node to a diagram."""
    client = DrawioAPIClient()
    diagram = client.create_diagram()
    
    # Add a node
    updated_diagram = client.add_node(diagram, "Test Node", 100, 100)
    
    assert len(updated_diagram["cells"]) == 1
    assert updated_diagram["cells"][0]["label"] == "Test Node"
    assert updated_diagram["cells"][0]["x"] == 100
    assert updated_diagram["cells"][0]["y"] == 100
    assert updated_diagram["modified"] is True


def test_add_edge():
    """Test adding an edge between nodes."""
    client = DrawioAPIClient()
    diagram = client.create_diagram()
    
    # Add two nodes
    diagram = client.add_node(diagram, "Node 1", 0, 0)
    diagram = client.add_node(diagram, "Node 2", 200, 0)
    
    node1_id = diagram["cells"][0]["id"]
    node2_id = diagram["cells"][1]["id"]
    
    # Add an edge
    updated_diagram = client.add_edge(diagram, node1_id, node2_id, "Test Edge")
    
    assert len(updated_diagram["cells"]) == 3
    assert updated_diagram["cells"][2]["source"] == node1_id
    assert updated_diagram["cells"][2]["target"] == node2_id
    assert updated_diagram["cells"][2]["label"] == "Test Edge"