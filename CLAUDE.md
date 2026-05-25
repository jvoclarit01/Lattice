# Lattice TUI Project Guidelines

## Command Guide

### Run TUI
```bash
python lattice-tui.py
```

### Run Tests
```bash
# Run all tests
python -m pytest -v

# Run specific test file
python -m pytest -v tests/test_graph_view.py
```

## Architectural Conventions

### Textual Widgets & Layout
- Maintain clean separation of concerns. Keep graph parsing, calculations, and search algorithms (e.g. BFS/DFS) in separate parser modules or as pure functions outside UI classes.
- Use native Textual layout constraints and containers (`Horizontal`, `Vertical`, `TabbedContent`, `TabPane`) with theme colors (`$accent`, `$primary`, `$surface`, `$success`).
- Avoid coordinate-based pilot clicks in tests. Instead, trigger selections programmatically (`ListView.post_message` with `ListView.Selected`) or call `.press()` on buttons.
- Subclass standard Textual widgets like `ListItem` when keeping track of custom attributes (e.g., `NodeListItem` for storing `node_id`).

### Data & File Handling
- Resolve all paths dynamically relative to the parsed workspace root (`self.parser.workspace`).
- Always use `encoding="utf-8"` explicitly when reading or writing markdown plans, skill documents, or knowledge graphs (`graphify` outputs).
- Gracefully handle file missing and format corruption states by showing stylized error views (e.g., `Static` with `id="graph-error"`) instead of raising application crashes.
