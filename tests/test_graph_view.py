import json
import pytest
from pathlib import Path
from tui.app import LatticeApp
from textual.widgets import ListView, Static, Input, Button, Select

SAMPLE_GRAPH_DATA = {
    "directed": False,
    "multigraph": False,
    "graph": {
        "hyperedges": [
            {
                "id": "he1",
                "label": "Hyperedge 1",
                "nodes": ["node1", "node2"],
                "relation": "relate",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
                "source_file": "file1.py"
            }
        ]
    },
    "nodes": [
        {
            "id": "node1",
            "label": "Node One",
            "file_type": "code",
            "source_file": "file1.py",
            "community": 1
        },
        {
            "id": "node2",
            "label": "Node Two",
            "file_type": "document",
            "source_file": "file2.md",
            "community": 2
        },
        {
            "id": "node3",
            "label": "Node Three",
            "file_type": "rationale",
            "source_file": "file3.md",
            "community": 1
        }
    ],
    "links": [
        {
            "source": "node1",
            "target": "node2",
            "relation": "calls"
        },
        {
            "source": "node2",
            "target": "node3",
            "relation": "references"
        }
    ]
}

@pytest.mark.asyncio
async def test_graphify_console_missing_file(tmp_path):
    # Ensure graphify-out/graph.json does not exist
    app = LatticeApp(str(tmp_path))
    async with app.run_test() as pilot:
        try:
            await pilot.click("#tab-graphify")
        except Exception:
            await pilot.click("#--content-tab-graphify")
        
        # Verify the error message is shown (it has "graphify-out/graph.json not found!")
        error_widget = app.query_one("#graph-error", Static)
        assert error_widget is not None
        assert "graphify-out/graph.json not found!" in str(error_widget.render())

@pytest.mark.asyncio
async def test_graphify_console_stats_and_nodes(tmp_path):
    # Create graphify-out/graph.json
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    graph_json = graphify_out / "graph.json"
    graph_json.write_text(json.dumps(SAMPLE_GRAPH_DATA), encoding="utf-8")
    
    app = LatticeApp(str(tmp_path))
    async with app.run_test() as pilot:
        try:
            await pilot.click("#tab-graphify")
        except Exception:
            await pilot.click("#--content-tab-graphify")
        
        # Check stats
        stats_nodes = app.query_one("#stats-nodes", Static)
        stats_links = app.query_one("#stats-links", Static)
        stats_hyperedges = app.query_one("#stats-hyperedges", Static)
        stats_communities = app.query_one("#stats-communities", Static)
        
        assert "3" in str(stats_nodes.render())
        assert "2" in str(stats_links.render())
        assert "1" in str(stats_hyperedges.render())
        assert "2" in str(stats_communities.render())
        
        # Check node list in sidebar
        sidebar_list = app.query_one("#nodes-sidebar", ListView)
        assert len(sidebar_list.children) == 3

@pytest.mark.asyncio
async def test_graphify_console_search_filter(tmp_path):
    # Create graphify-out/graph.json
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    graph_json = graphify_out / "graph.json"
    graph_json.write_text(json.dumps(SAMPLE_GRAPH_DATA), encoding="utf-8")
    
    app = LatticeApp(str(tmp_path))
    async with app.run_test() as pilot:
        try:
            await pilot.click("#tab-graphify")
        except Exception:
            await pilot.click("#--content-tab-graphify")
        
        # Filter nodes search
        search_input = app.query_one("#node-search", Input)
        search_input.value = "Three"
        
        # Verify the list gets filtered
        sidebar_list = app.query_one("#nodes-sidebar", ListView)
        # Wait a moment for UI update
        await pilot.pause()
        assert len(sidebar_list.children) == 1
        
        # Reset search
        search_input.value = ""
        await pilot.pause()
        assert len(sidebar_list.children) == 3

@pytest.mark.asyncio
async def test_graphify_console_selection_and_navigation(tmp_path):
    # Create graphify-out/graph.json
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    graph_json = graphify_out / "graph.json"
    graph_json.write_text(json.dumps(SAMPLE_GRAPH_DATA), encoding="utf-8")
    
    app = LatticeApp(str(tmp_path))
    async with app.run_test() as pilot:
        try:
            await pilot.click("#tab-graphify")
        except Exception:
            await pilot.click("#--content-tab-graphify")
        
        sidebar_list = app.query_one("#nodes-sidebar", ListView)
        
        # Select "Node Two" (index 1)
        sidebar_list.index = 1
        sidebar_list.post_message(ListView.Selected(sidebar_list, sidebar_list.children[1], 1))
        await pilot.pause()
        
        # Verify details panel updates
        detail_label = app.query_one("#detail-label", Static)
        detail_id = app.query_one("#detail-id", Static)
        detail_type = app.query_one("#detail-type", Static)
        detail_community = app.query_one("#detail-community", Static)
        detail_source = app.query_one("#detail-source-file", Static)
        
        assert "Node Two" in str(detail_label.render())
        assert "node2" in str(detail_id.render())
        assert "document" in str(detail_type.render())
        assert "2" in str(detail_community.render())
        assert "file2.md" in str(detail_source.render())
        
        # Verify incoming/outgoing neighbors
        incoming_list = app.query_one("#incoming-list", ListView)
        outgoing_list = app.query_one("#outgoing-list", ListView)
        
        assert len(incoming_list.children) == 1  # node1
        assert len(outgoing_list.children) == 1  # node3
        
        # Click the outgoing neighbor to navigate
        outgoing_list = app.query_one("#outgoing-list", ListView)
        outgoing_list.post_message(ListView.Selected(outgoing_list, outgoing_list.children[0], 0))
        await pilot.pause()
        
        # Verify details now show Node Three
        assert "Node Three" in str(detail_label.render())
        assert "node3" in str(detail_id.render())

@pytest.mark.asyncio
async def test_graphify_console_pathfinding(tmp_path):
    # Create graphify-out/graph.json
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    graph_json = graphify_out / "graph.json"
    graph_json.write_text(json.dumps(SAMPLE_GRAPH_DATA), encoding="utf-8")
    
    app = LatticeApp(str(tmp_path))
    async with app.run_test() as pilot:
        try:
            await pilot.click("#tab-graphify")
        except Exception:
            await pilot.click("#--content-tab-graphify")
            
        # Enter pathfinding values
        src_input = app.query_one("#path-source", Input)
        tgt_input = app.query_one("#path-target", Input)
        method_select = app.query_one("#path-method", Select)
        
        src_input.value = "node1"
        tgt_input.value = "node3"
        method_select.value = "bfs"
        
        app.query_one("#btn-find-path", Button).press()
        await pilot.pause()
        
        results_widget = app.query_one("#path-results", Static)
        expected_chain = "Node One --(calls)--> Node Two --(references)--> Node Three"
        assert expected_chain in str(results_widget.render())
        
        # Test BFS with unreachable nodes
        src_input.value = "node3"
        tgt_input.value = "node1"
        app.query_one("#btn-find-path", Button).press()
        await pilot.pause()
        assert "No path found between node3 and node1" in str(results_widget.render())
        
        # Test DFS
        src_input.value = "node1"
        tgt_input.value = "node3"
        method_select.value = "dfs"
        app.query_one("#btn-find-path", Button).press()
        await pilot.pause()
        assert expected_chain in str(results_widget.render())

@pytest.mark.asyncio
async def test_graphify_console_invalid_json(tmp_path):
    # Create invalid JSON file
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    graph_json = graphify_out / "graph.json"
    graph_json.write_text("{invalid json", encoding="utf-8")
    
    app = LatticeApp(str(tmp_path))
    async with app.run_test() as pilot:
        try:
            await pilot.click("#tab-graphify")
        except Exception:
            await pilot.click("#--content-tab-graphify")
            
        error_widget = app.query_one("#graph-error", Static)
        assert error_widget is not None
        assert "Invalid JSON format" in str(error_widget.render())

@pytest.mark.asyncio
async def test_graphify_console_mount_deserialization(tmp_path):
    # Create graphify-out/graph.json
    graphify_out = tmp_path / "graphify-out"
    graphify_out.mkdir(parents=True, exist_ok=True)
    graph_json = graphify_out / "graph.json"
    graph_json.write_text(json.dumps(SAMPLE_GRAPH_DATA), encoding="utf-8")
    
    app = LatticeApp(str(tmp_path))
    async with app.run_test() as pilot:
        try:
            await pilot.click("#tab-graphify")
        except Exception:
            await pilot.click("#--content-tab-graphify")
            
        # Verify first item (Node One) is selected on mount and details populated
        detail_label = app.query_one("#detail-label", Static)
        detail_id = app.query_one("#detail-id", Static)
        assert "Node One" in str(detail_label.render())
        assert "node1" in str(detail_id.render())

