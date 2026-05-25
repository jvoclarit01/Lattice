import json
from pathlib import Path
from textual.app import ComposeResult
from textual.widgets import Static, ListView, ListItem, Input, Button, Select
from textual.containers import Horizontal, Vertical
from tui.parser import LatticeParser

class NodeListItem(ListItem):
    """Custom ListItem that stores the associated node ID for type safety."""
    def __init__(self, child, node_id: str):
        super().__init__(child)
        self.node_id = node_id

def find_path_bfs(adj_map, start_id, end_id):
    """Finds the shortest path using Breadth-First Search on the directed graph."""
    if start_id == end_id:
        return [start_id], []
        
    queue = [(start_id, [start_id], [])]
    visited = {start_id}
    
    while queue:
        curr, path_nodes, path_rels = queue.pop(0)
        if curr == end_id:
            return path_nodes, path_rels
            
        for neighbor, rel in adj_map.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path_nodes + [neighbor], path_rels + [rel]))
                
    return None, None

def find_path_dfs(adj_map, start_id, end_id):
    """Finds a path using iterative Depth-First Search on the directed graph to prevent recursion limits."""
    if start_id == end_id:
        return [start_id], []
        
    stack = [(start_id, [start_id], [])]
    visited = set()
    
    while stack:
        curr, path_nodes, path_rels = stack.pop()
        if curr == end_id:
            return path_nodes, path_rels
            
        if curr not in visited:
            visited.add(curr)
            # Push in reverse order so we pop them in definition order
            neighbors = adj_map.get(curr, [])
            for neighbor, rel in reversed(neighbors):
                if neighbor not in visited:
                    stack.append((neighbor, path_nodes + [neighbor], path_rels + [rel]))
                    
    return None, None

class GraphifyConsoleView(Static):
    """View to search, analyze and query the codebase's knowledge graph."""
    
    CSS = """
    GraphifyConsoleView {
        height: 100%;
    }
    #graph-console-layout {
        layout: horizontal;
        height: 100%;
    }
    .panel-col {
        height: 100%;
        padding: 1;
    }
    #panel-left {
        width: 30%;
        border-right: solid $accent;
    }
    #panel-middle {
        width: 40%;
        border-right: solid $accent;
    }
    #panel-right {
        width: 30%;
    }
    #nodes-sidebar {
        height: 1fr;
        border: solid $accent;
        margin-top: 1;
    }
    #stats-box {
        border: double $primary;
        padding: 1;
        margin-bottom: 1;
        background: $surface;
        height: auto;
    }
    #node-detail-panel {
        height: 100%;
        layout: vertical;
    }
    .detail-item {
        margin-bottom: 1;
    }
    .neighbor-header {
        margin-top: 1;
        text-style: bold;
    }
    #incoming-list, #outgoing-list {
        height: 6;
        border: solid $accent;
        margin-bottom: 1;
    }
    #path-finder-panel {
        height: 100%;
        layout: vertical;
    }
    .path-input {
        margin-bottom: 1;
    }
    #btn-find-path {
        margin-top: 1;
        width: 100%;
    }
    #path-results {
        margin-top: 1;
        border: solid $success;
        padding: 1;
        height: 1fr;
        background: $surface;
    }
    #graph-error {
        margin: 2;
        padding: 2;
        border: solid red;
    }
    """

    def __init__(self, parser: LatticeParser):
        super().__init__()
        self.parser = parser
        self.graph_file = self.parser.workspace / "graphify-out" / "graph.json"
        self.graph_loaded = False
        self.graph_data = {}
        self.all_nodes = []
        self.nodes_map = {}
        self.incoming_map = {}
        self.outgoing_map = {}
        self.adj_map = {}
        self.load_error = None
        self._pending_select_id = None
        
        self.load_graph()

    def load_graph(self) -> None:
        if not self.graph_file.exists():
            self.graph_loaded = False
            self.load_error = "File not found"
            return

        try:
            with open(self.graph_file, "r", encoding="utf-8") as f:
                self.graph_data = json.load(f)
            
            self.all_nodes = self.graph_data.get("nodes", [])
            self.nodes_map = {n["id"]: n for n in self.all_nodes if "id" in n}
            
            # Prebuild mappings to optimize queries
            self.incoming_map = {n_id: [] for n_id in self.nodes_map}
            self.outgoing_map = {n_id: [] for n_id in self.nodes_map}
            self.adj_map = {n_id: [] for n_id in self.nodes_map}
            
            for link in self.graph_data.get("links", []):
                src = link.get("source")
                tgt = link.get("target")
                rel = link.get("relation", "links")
                if src and tgt:
                    # In case of links pointing to non-existent nodes, initialize map keys
                    if src not in self.outgoing_map:
                        self.outgoing_map[src] = []
                    if src not in self.adj_map:
                        self.adj_map[src] = []
                    if src not in self.incoming_map:
                        self.incoming_map[src] = []
                    if tgt not in self.incoming_map:
                        self.incoming_map[tgt] = []
                    if tgt not in self.outgoing_map:
                        self.outgoing_map[tgt] = []
                    if tgt not in self.adj_map:
                        self.adj_map[tgt] = []

                    self.outgoing_map[src].append(tgt)
                    self.incoming_map[tgt].append(src)
                    self.adj_map[src].append((tgt, rel))
            
            self.graph_loaded = True
            self.load_error = None
        except json.JSONDecodeError as e:
            self.graph_loaded = False
            self.load_error = f"Invalid JSON format: {e}"
        except Exception as e:
            self.graph_loaded = False
            self.load_error = f"Error loading file: {e}"

    def get_node_label(self, node_id: str) -> str:
        node = self.nodes_map.get(node_id)
        if node and node.get("label"):
            return node.get("label")
        return node_id

    def compose(self) -> ComposeResult:
        if not self.graph_loaded:
            msg = (
                "[bold red]graphify-out/graph.json not found![/bold red]\nPlease run graphify first."
                if self.load_error == "File not found"
                else f"[bold red]{self.load_error}[/bold red]"
            )
            yield Static(msg, id="graph-error")
            return

        # Calculate stats
        nodes_count = len(self.all_nodes)
        links_count = len(self.graph_data.get("links", []))
        
        he_list = self.graph_data.get("hyperedges") or self.graph_data.get("graph", {}).get("hyperedges", [])
        hyperedges_count = len(he_list)
        
        communities = {n.get("community") for n in self.all_nodes if n.get("community") is not None}
        communities_count = len(communities)

        with Horizontal(id="graph-console-layout"):
            # Left Panel: Sidebar & Search
            with Vertical(id="panel-left", classes="panel-col"):
                # Stats Box
                with Vertical(id="stats-box"):
                    yield Static(f"[bold cyan]Total Nodes:[/bold cyan] [yellow]{nodes_count}[/yellow]", id="stats-nodes")
                    yield Static(f"[bold cyan]Total Links:[/bold cyan] [yellow]{links_count}[/yellow]", id="stats-links")
                    yield Static(f"[bold cyan]Total Hyperedges:[/bold cyan] [yellow]{hyperedges_count}[/yellow]", id="stats-hyperedges")
                    yield Static(f"[bold cyan]Communities:[/bold cyan] [yellow]{communities_count}[/yellow]", id="stats-communities")
                
                yield Input(placeholder="Search nodes...", id="node-search")
                
                # ListView sidebar
                sidebar_items = []
                for node in self.all_nodes:
                    item = NodeListItem(
                        Static(f"{node.get('label', '')} ({node.get('id', '')})"),
                        node.get("id", "")
                    )
                    sidebar_items.append(item)
                yield ListView(*sidebar_items, id="nodes-sidebar")

            # Middle Panel: Details
            with Vertical(id="panel-middle", classes="panel-col"):
                with Vertical(id="node-detail-panel"):
                    yield Static("[bold yellow]Node Details[/bold yellow]", id="detail-header", classes="detail-item")
                    yield Static("[bold yellow]Label:[/bold yellow] Select a node", id="detail-label", classes="detail-item")
                    yield Static("[bold cyan]ID:[/bold cyan] -", id="detail-id", classes="detail-item")
                    yield Static("[bold green]Type:[/bold green] -", id="detail-type", classes="detail-item")
                    yield Static("[bold magenta]Community ID:[/bold magenta] -", id="detail-community", classes="detail-item")
                    yield Static("[bold white]Source File:[/bold white] -", id="detail-source-file", classes="detail-item")
                    
                    yield Static("Incoming Neighbors:", classes="neighbor-header")
                    yield ListView(id="incoming-list")
                    
                    yield Static("Outgoing Neighbors:", classes="neighbor-header")
                    yield ListView(id="outgoing-list")

            # Right Panel: Path Finder Wizard
            with Vertical(id="panel-right", classes="panel-col"):
                with Vertical(id="path-finder-panel"):
                    yield Static("[bold yellow]Path Finder Wizard[/bold yellow]", classes="detail-item")
                    yield Static("Source Node ID:")
                    yield Input(placeholder="e.g. node1", id="path-source", classes="path-input")
                    yield Static("Target Node ID:")
                    yield Input(placeholder="e.g. node2", id="path-target", classes="path-input")
                    yield Static("Path Finding Method:")
                    yield Select(
                        options=[("BFS (Shortest Path)", "bfs"), ("DFS (Depth-First Path)", "dfs")],
                        id="path-method",
                        allow_blank=False
                    )
                    yield Button("Find Path", id="btn-find-path", variant="primary")
                    yield Static("Path results will appear here.", id="path-results")

    def on_mount(self) -> None:
        if self.graph_loaded:
            try:
                self.query_one("#path-method", Select).value = "bfs"
            except Exception:
                pass
            
            # Select first node if available and trigger details to prevent desynchronization
            sidebar = self.query_one("#nodes-sidebar", ListView)
            if sidebar.children:
                sidebar.index = 0
                first_item = sidebar.children[0]
                if hasattr(first_item, "node_id"):
                    self.show_node_details(first_item.node_id)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id == "nodes-sidebar":
            item = event.item
            if item and hasattr(item, "node_id"):
                self.show_node_details(item.node_id)
        elif event.list_view.id in ("incoming-list", "outgoing-list"):
            item = event.item
            if item and hasattr(item, "node_id"):
                self.select_node_by_id(item.node_id)

    def select_node_by_id(self, node_id: str) -> None:
        self._pending_select_id = node_id
        sidebar = self.query_one("#nodes-sidebar", ListView)
        
        # Check if the node is present in the current sidebar list
        for index, item in enumerate(sidebar.children):
            if getattr(item, "node_id", None) == node_id:
                sidebar.index = index
                self._pending_select_id = None
                break
        else:
            # Rebuild without filter to make sure it's found
            search_input = self.query_one("#node-search", Input)
            if search_input.value != "":
                search_input.value = ""
                # Clearing value triggers on_input_changed asynchronously.
                # Since self._pending_select_id is set, it will select it when rebuilds.
            else:
                # If input was already empty, rebuild sidebar directly
                self.rebuild_sidebar(selected_id=node_id)
                self._pending_select_id = None
        
        # Explicitly update details panel
        self.show_node_details(node_id)

    def rebuild_sidebar(self, filter_query: str = "", selected_id: str = None) -> None:
        sidebar = self.query_one("#nodes-sidebar", ListView)
        sidebar.clear()
        
        filtered_nodes = []
        for node in self.all_nodes:
            lbl = node.get("label", "")
            nid = node.get("id", "")
            if not filter_query or filter_query in lbl.lower() or filter_query in nid.lower():
                filtered_nodes.append(node)
                
        target_index = None
        for i, node in enumerate(filtered_nodes):
            item = NodeListItem(
                Static(f"{node.get('label', '')} ({node.get('id', '')})"),
                node.get("id", "")
            )
            sidebar.append(item)
            if selected_id and node.get("id") == selected_id:
                target_index = i
                
        if target_index is not None:
            sidebar.index = target_index
        elif filtered_nodes:
            sidebar.index = 0

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "node-search":
            selected_id = self._pending_select_id
            self.rebuild_sidebar(filter_query=event.value.lower(), selected_id=selected_id)
            self._pending_select_id = None

    def show_node_details(self, node_id: str) -> None:
        node = self.nodes_map.get(node_id)
        if not node:
            return
            
        self.query_one("#detail-label", Static).update(f"[bold yellow]Label:[/bold yellow] {node.get('label', '')}")
        self.query_one("#detail-id", Static).update(f"[bold cyan]ID:[/bold cyan] {node.get('id', '')}")
        self.query_one("#detail-type", Static).update(f"[bold green]Type:[/bold green] {node.get('file_type', '')}")
        
        comm = node.get('community')
        comm_str = str(comm) if comm is not None else "-"
        self.query_one("#detail-community", Static).update(f"[bold magenta]Community ID:[/bold magenta] {comm_str}")
        self.query_one("#detail-source-file", Static).update(f"[bold white]Source File:[/bold white] {node.get('source_file', '')}")
        
        # Read prebuilt incoming and outgoing maps
        incoming = self.incoming_map.get(node_id, [])
        outgoing = self.outgoing_map.get(node_id, [])
                
        # Populate incoming list
        incoming_list = self.query_one("#incoming-list", ListView)
        incoming_list.clear()
        for neighbor_id in sorted(set(incoming)):
            lbl = self.get_node_label(neighbor_id)
            item = NodeListItem(Static(f"{lbl} ({neighbor_id})"), neighbor_id)
            incoming_list.append(item)
            
        # Populate outgoing list
        outgoing_list = self.query_one("#outgoing-list", ListView)
        outgoing_list.clear()
        for neighbor_id in sorted(set(outgoing)):
            lbl = self.get_node_label(neighbor_id)
            item = NodeListItem(Static(f"{lbl} ({neighbor_id})"), neighbor_id)
            outgoing_list.append(item)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-find-path":
            self.calculate_and_display_path()

    def calculate_and_display_path(self) -> None:
        src = self.query_one("#path-source", Input).value.strip()
        tgt = self.query_one("#path-target", Input).value.strip()
        method = self.query_one("#path-method", Select).value
        
        if not src or not tgt:
            self.query_one("#path-results", Static).update("[bold red]Please specify both Source and Target IDs.[/bold red]")
            return
            
        if method == "dfs":
            path_nodes, path_rels = find_path_dfs(self.adj_map, src, tgt)
        else:
            path_nodes, path_rels = find_path_bfs(self.adj_map, src, tgt)
            
        results_widget = self.query_one("#path-results", Static)
        if path_nodes:
            parts = []
            for i in range(len(path_nodes)):
                parts.append(self.get_node_label(path_nodes[i]))
                if i < len(path_rels):
                    parts.append(f"--({path_rels[i]})-->")
            chain = " ".join(parts)
            results_widget.update(f"[bold green]Path Found:[/bold green]\n{chain}")
        else:
            results_widget.update(f"[bold red]No path found between {src} and {tgt}[/bold red]")
