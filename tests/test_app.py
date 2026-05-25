import pytest
from tui.app import LatticeApp

@pytest.mark.asyncio
async def test_app_loading():
    app = LatticeApp(workspace_path=".")
    async with app.run_test() as pilot:
        assert app.title == "Lattice Terminal UI"
