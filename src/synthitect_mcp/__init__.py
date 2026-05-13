"""Synthitect Protocol MCP Server.

A Model Context Protocol server implementing the Contract-First Agentic Workflow (CFAW).
Provides tools that generate Sub-Agent Briefings — structured prompts that the
Orchestrator hands off to specialized sub-agents. These tools DO NOT execute
sub-agents; they return text briefings for the Orchestrator to delegate.

Usage:
    from synthitect_mcp import server
    # Run with: python -m synthitect_mcp

Architecture:
    - server.py: Core MCP server with three briefing-generation tools
    - file_manager.py: File I/O utility for plan artifacts

Tools (all return text briefings; Orchestrator must spawn sub-agents):
    1. generate_plan_briefing(ticket_id, raw_idea) -> str
    2. generate_tdd_red_briefing(ticket_id) -> str
    3. generate_implementation_briefing(ticket_id) -> str
"""

__version__ = "1.0.0"
__description__ = "Synthitect Protocol MCP Server - CFAW Implementation"
