"""Unit tests for MCP server tools."""

import shutil
import tempfile
from pathlib import Path

import pytest
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from synthitect_mcp.file_manager import FileManager
from synthitect_mcp.server import (
    generate_plan_briefing,
    generate_tdd_red_briefing,
    generate_implementation_briefing,
)


class TestServerTools:

    @pytest.fixture
    def temp_dir(self):
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp)

    @pytest.fixture
    def fm(self, temp_dir):
        return FileManager(str(temp_dir))

    @pytest.fixture
    def fm_with_plan(self, fm):
        """FileManager with completed plan phase artifacts."""
        ticket_id = "TEST-001"
        ticket_dir = fm.create_ticket_directory(ticket_id)
        (ticket_dir / "spec.md").write_text("# Spec\n\n## Objective\nTest feature.")
        (ticket_dir / "test_spec.md").write_text("# Test Spec\n\n## Happy Path\n...")
        fm.set_phase_state(ticket_id, "plan", completed=True)
        return fm, ticket_id

    @pytest.fixture
    def fm_with_tdd_red(self, fm_with_plan):
        """FileManager with tdd_red phase marked complete."""
        fm, ticket_id = fm_with_plan
        fm.set_phase_state(ticket_id, "tdd_red", completed=True)
        return fm, ticket_id

    # =========================================================================
    # generate_plan_briefing
    # =========================================================================

    @pytest.mark.asyncio
    async def test_plan_briefing_returns_text(self, fm):
        result = await generate_plan_briefing(fm, {
            "ticket_id": "PLAN-001",
            "raw_idea": "Add user authentication"
        })
        assert len(result) == 1
        assert result[0].type == "text"
        assert len(result[0].text) > 50

    @pytest.mark.asyncio
    async def test_plan_briefing_injects_variables(self, fm):
        result = await generate_plan_briefing(fm, {
            "ticket_id": "PLAN-002",
            "raw_idea": "Add offline sync"
        })
        text = result[0].text
        assert "PLAN-002" in text
        assert "Add offline sync" in text
        assert "{{ ticket_id }}" not in text
        assert "{{ raw_idea }}" not in text

    @pytest.mark.asyncio
    async def test_plan_briefing_creates_ticket_directory(self, fm):
        await generate_plan_briefing(fm, {
            "ticket_id": "PLAN-003",
            "raw_idea": "Test"
        })
        assert (fm.base_dir / "plans" / "PLAN-003").exists()

    @pytest.mark.asyncio
    async def test_plan_briefing_sets_phase_in_progress(self, fm):
        await generate_plan_briefing(fm, {
            "ticket_id": "PLAN-004",
            "raw_idea": "Test"
        })
        state = fm.get_phase_state("PLAN-004")
        assert state["current_phase"] == "plan"
        assert "plan" not in state["completed_phases"]

    # =========================================================================
    # generate_tdd_red_briefing
    # =========================================================================

    @pytest.mark.asyncio
    async def test_tdd_red_briefing_returns_text(self, fm_with_plan):
        fm, ticket_id = fm_with_plan
        result = await generate_tdd_red_briefing(fm, {"ticket_id": ticket_id})
        assert len(result) == 1
        assert result[0].type == "text"
        assert len(result[0].text) > 50

    @pytest.mark.asyncio
    async def test_tdd_red_briefing_injects_ticket_id(self, fm_with_plan):
        fm, ticket_id = fm_with_plan
        result = await generate_tdd_red_briefing(fm, {"ticket_id": ticket_id})
        assert ticket_id in result[0].text
        assert "{{ ticket_id }}" not in result[0].text

    @pytest.mark.asyncio
    async def test_tdd_red_briefing_requires_spec_files(self, fm):
        fm.create_ticket_directory("NO-SPEC")
        result = await generate_tdd_red_briefing(fm, {"ticket_id": "NO-SPEC"})
        assert "ERROR" in result[0].text

    @pytest.mark.asyncio
    async def test_tdd_red_briefing_writes_stub_file(self, fm_with_plan):
        fm, ticket_id = fm_with_plan
        await generate_tdd_red_briefing(fm, {"ticket_id": ticket_id})
        stub_path = fm.base_dir / "plans" / ticket_id / "stub_implementation.py"
        assert stub_path.exists()

    @pytest.mark.asyncio
    async def test_tdd_red_briefing_sets_phase_in_progress(self, fm_with_plan):
        fm, ticket_id = fm_with_plan
        await generate_tdd_red_briefing(fm, {"ticket_id": ticket_id})
        state = fm.get_phase_state(ticket_id)
        assert state["current_phase"] == "tdd_red"
        assert "tdd_red" not in state["completed_phases"]

    @pytest.mark.asyncio
    async def test_tdd_red_briefing_enables_implementation(self, fm_with_plan):
        fm, ticket_id = fm_with_plan
        await generate_tdd_red_briefing(fm, {"ticket_id": ticket_id})
        fm.set_phase_state(ticket_id, "tdd_red", completed=True)
        result = await generate_implementation_briefing(fm, {"ticket_id": ticket_id})
        assert "ERROR" not in result[0].text

    # =========================================================================
    # generate_implementation_briefing
    # =========================================================================

    @pytest.mark.asyncio
    async def test_implementation_briefing_returns_text(self, fm_with_tdd_red):
        fm, ticket_id = fm_with_tdd_red
        result = await generate_implementation_briefing(fm, {"ticket_id": ticket_id})
        assert len(result) == 1
        assert result[0].type == "text"
        assert len(result[0].text) > 50

    @pytest.mark.asyncio
    async def test_implementation_briefing_injects_ticket_id(self, fm_with_tdd_red):
        fm, ticket_id = fm_with_tdd_red
        result = await generate_implementation_briefing(fm, {"ticket_id": ticket_id})
        assert ticket_id in result[0].text
        assert "{{ ticket_id }}" not in result[0].text

    @pytest.mark.asyncio
    async def test_implementation_briefing_requires_tdd_red(self, fm):
        fm.create_ticket_directory("NO-TDD")
        result = await generate_implementation_briefing(fm, {"ticket_id": "NO-TDD"})
        assert "ERROR" in result[0].text

    @pytest.mark.asyncio
    async def test_implementation_briefing_sets_phase_in_progress(self, fm_with_tdd_red):
        fm, ticket_id = fm_with_tdd_red
        await generate_implementation_briefing(fm, {"ticket_id": ticket_id})
        state = fm.get_phase_state(ticket_id)
        assert state["current_phase"] == "implementation"
        assert "implementation" not in state["completed_phases"]

    # =========================================================================
    # Template content
    # =========================================================================

    @pytest.mark.asyncio
    async def test_plan_briefing_mentions_spec_and_test_spec(self, fm):
        result = await generate_plan_briefing(fm, {"ticket_id": "X", "raw_idea": "Y"})
        text = result[0].text
        assert "spec.md" in text
        assert "test_spec.md" in text

    @pytest.mark.asyncio
    async def test_tdd_red_briefing_mentions_escalation(self, fm_with_plan):
        fm, ticket_id = fm_with_plan
        result = await generate_tdd_red_briefing(fm, {"ticket_id": ticket_id})
        assert "ESCALATION" in result[0].text or "proceed" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_implementation_briefing_mentions_escalation(self, fm_with_tdd_red):
        fm, ticket_id = fm_with_tdd_red
        result = await generate_implementation_briefing(fm, {"ticket_id": ticket_id})
        assert "ESCALATION" in result[0].text


class TestToolDefinitions:

    def test_tools_list_has_three_tools(self):
        from synthitect_mcp.server import TOOLS
        assert len(TOOLS) == 3

    def test_tool_names(self):
        from synthitect_mcp.server import TOOLS
        names = {t.name for t in TOOLS}
        assert names == {"generate_plan_briefing", "generate_tdd_red_briefing", "generate_implementation_briefing"}

    def test_plan_briefing_required_fields(self):
        from synthitect_mcp.server import TOOLS
        tool = next(t for t in TOOLS if t.name == "generate_plan_briefing")
        assert "ticket_id" in tool.inputSchema["required"]
        assert "raw_idea" in tool.inputSchema["required"]

    def test_tdd_red_required_fields(self):
        from synthitect_mcp.server import TOOLS
        tool = next(t for t in TOOLS if t.name == "generate_tdd_red_briefing")
        assert "ticket_id" in tool.inputSchema["required"]

    def test_implementation_required_fields(self):
        from synthitect_mcp.server import TOOLS
        tool = next(t for t in TOOLS if t.name == "generate_implementation_briefing")
        assert "ticket_id" in tool.inputSchema["required"]
