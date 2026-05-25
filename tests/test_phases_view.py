import pytest
from tui.app import LatticeApp
from textual.widgets import OptionList

@pytest.mark.asyncio
async def test_phases_tab_loaded(tmp_path):
    plan_file = tmp_path / ".lattice-plan.md"
    plan_file.write_text("## Phase 01: Setup\n- [ ] Task A\n", encoding="utf-8")
    
    app = LatticeApp(str(tmp_path))
    async with app.run_test() as pilot:
        # Switch tab (handle both old and new Textual tab id conventions)
        try:
            await pilot.click("#tab-phases")
        except Exception:
            await pilot.click("#--content-tab-phases")
            
        option_list = app.query_one(OptionList)
        assert option_list is not None
        assert option_list.option_count == 1
