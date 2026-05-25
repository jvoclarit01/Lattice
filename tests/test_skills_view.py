import pytest
from tui.app import LatticeApp
from textual.widgets import ListView, Markdown

@pytest.mark.asyncio
async def test_skills_tab_loaded(tmp_path):
    # Create sample skill in tmp_path
    domains_dir = tmp_path / "domains" / "webdev"
    domains_dir.mkdir(parents=True, exist_ok=True)
    (domains_dir / "skill-auth.md").write_text("# Authentication Skill\n- Iron Laws", encoding="utf-8")
    
    app = LatticeApp(str(tmp_path))
    async with app.run_test() as pilot:
        # Switch tab (handle both old and new Textual tab id conventions)
        try:
            await pilot.click("#tab-skills")
        except Exception:
            await pilot.click("#--content-tab-skills")
            
        list_view = app.query_one(ListView)
        assert list_view is not None
        
        # Select first skill item
        await pilot.click("ListItem")
        markdown_widget = app.query_one(Markdown)
        assert markdown_widget is not None
        assert "# Authentication Skill" in markdown_widget.source
