"""Synthitect Protocol MCP Server.

A Model Context Protocol server implementing the Contract-First Agentic Workflow (CFAW).

Three-phase workflow:
1. Plan — agent reads codebase, produces spec.md + test_spec.md. Human approves.
2. TDD Red — agent writes failing tests against skeleton stubs.
3. Implement — agent writes production code to make tests pass.

Each tool returns a text briefing for the Orchestrator to pass to a sub-agent.
This server does NOT execute sub-agents.
"""

import os
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .file_manager import FileManager


server = Server("synthitect-protocol")


def get_file_manager() -> FileManager:
    base_dir = os.environ.get("SYNTHITECT_BASE_DIR")
    return FileManager(base_dir)


TOOLS = [
    Tool(
        name="generate_plan_briefing",
        description="""Generates a Sub-Agent Briefing for the Plan Sub-Agent.

This tool does NOT execute the sub-agent. It:
1. Creates the plans/{ticket_id}/ directory
2. Returns a text briefing — the Orchestrator MUST spawn a Plan Sub-Agent
   and pass this briefing as instructions.

The Plan Sub-Agent reads the codebase, understands the feature request, and produces:
- spec.md: implementation plan (target files, data models, API contracts)
- test_spec.md: behavioral scenarios (Given/When/Then with concrete expected values)

INPUTS:
- ticket_id: Unique identifier for this feature (e.g., 'FEAT-offline-sync')
- raw_idea: The user's description of the feature to build

OUTPUT:
Returns a briefing. After the sub-agent completes, the Orchestrator presents
spec.md and test_spec.md to the user for approval.

HUMAN GATE: User must approve the plan before proceeding to TDD Red.""",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": "Ticket identifier (e.g., 'FEAT-123', 'TASK-offline-sync')"
                },
                "raw_idea": {
                    "type": "string",
                    "description": "The user's description of the feature or change to implement"
                }
            },
            "required": ["ticket_id", "raw_idea"]
        }
    ),
    Tool(
        name="generate_tdd_red_briefing",
        description="""Generates a Sub-Agent Briefing for the TDD Red Sub-Agent.

This tool does NOT execute the sub-agent. It:
1. Verifies spec.md and test_spec.md exist for the ticket
2. Writes plans/{ticket_id}/stub_implementation.py (empty stubs for tests to compile)
3. Returns a text briefing — the Orchestrator MUST spawn a TDD Red Sub-Agent
   and pass this briefing as instructions.

The TDD Red Sub-Agent writes failing tests based on the approved test_spec.md.

INPUTS:
- ticket_id: The ticket identifier (must have user-approved plan)

OUTPUT:
Returns a briefing. After tests are written, the Orchestrator proceeds
immediately to generate_implementation_briefing — no human gate required.""",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": "Ticket identifier (must have completed Plan phase)"
                }
            },
            "required": ["ticket_id"]
        }
    ),
    Tool(
        name="generate_implementation_briefing",
        description="""Generates a Sub-Agent Briefing for the Implementation Sub-Agent.

This tool does NOT execute the sub-agent. It:
1. Verifies tdd_red phase is completed
2. Returns a text briefing — the Orchestrator MUST spawn an Implementation
   Sub-Agent and pass this briefing as instructions.

The Implementation Sub-Agent writes production code to make all failing tests pass.

INPUTS:
- ticket_id: The ticket identifier (must have completed TDD Red phase)

OUTPUT:
Returns a briefing. After all tests are green, the feature is complete.""",
        inputSchema={
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": "Ticket identifier (must have completed TDD Red phase)"
                }
            },
            "required": ["ticket_id"]
        }
    ),
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    fm = get_file_manager()

    if name == "generate_plan_briefing":
        return await generate_plan_briefing(fm, arguments)
    elif name == "generate_tdd_red_briefing":
        return await generate_tdd_red_briefing(fm, arguments)
    elif name == "generate_implementation_briefing":
        return await generate_implementation_briefing(fm, arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def generate_plan_briefing(fm: FileManager, arguments: dict) -> list[TextContent]:
    ticket_id = arguments["ticket_id"]
    raw_idea = arguments["raw_idea"]

    fm.create_ticket_directory(ticket_id)
    fm.set_phase_state(ticket_id, "plan", completed=False)

    template = fm.read_template("plan-phase.md")
    briefing = fm.inject_variables(template, {"ticket_id": ticket_id, "raw_idea": raw_idea})

    return [TextContent(type="text", text=briefing)]


async def generate_tdd_red_briefing(fm: FileManager, arguments: dict) -> list[TextContent]:
    ticket_id = arguments["ticket_id"]

    if not fm.ensure_spec_exists(ticket_id):
        return [TextContent(
            type="text",
            text=f"ERROR: Plan phase not completed for ticket '{ticket_id}'. "
                 f"Run generate_plan_briefing and get user approval first."
        )]

    stub_content = f"""# Stub: {ticket_id}
# Replaced by Implementation Sub-Agent after TDD Red phase.

class StubClass:
    pass
"""
    fm.write_file(f"plans/{ticket_id}/stub_implementation.py", stub_content)
    fm.set_phase_state(ticket_id, "tdd_red", completed=False)

    template = fm.read_template("tdd-red-phase.md")
    briefing = fm.inject_variables(template, {"ticket_id": ticket_id})

    return [TextContent(type="text", text=briefing)]


async def generate_implementation_briefing(fm: FileManager, arguments: dict) -> list[TextContent]:
    ticket_id = arguments["ticket_id"]

    if not fm.check_phase_prerequisite(ticket_id, "tdd_red"):
        return [TextContent(
            type="text",
            text=f"ERROR: TDD Red phase not completed for ticket '{ticket_id}'. "
                 f"Run generate_tdd_red_briefing first."
        )]

    fm.set_phase_state(ticket_id, "implementation", completed=False)

    template = fm.read_template("implement-phase.md")
    briefing = fm.inject_variables(template, {"ticket_id": ticket_id})

    return [TextContent(type="text", text=briefing)]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def main_cli():
    import anyio
    anyio.run(main)


if __name__ == "__main__":
    main_cli()
