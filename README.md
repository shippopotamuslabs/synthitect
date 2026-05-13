# Synthitect Protocol

An open-source Model Context Protocol (MCP) server implementing the **Contract-First Agentic Workflow (CFAW)** methodology for AI-assisted software engineering.

## Overview

The Synthitect Protocol enforces contract-first development by providing a structured, phased workflow that maintains architectural integrity across AI-assisted coding sessions. It solves the session statelessness problem inherent in AI development by externalizing decisions into versioned specifications.

## Architecture (Mixture-of-Agents)

```
synthitect-protocol/
├── prompts/                    # Sub-Agent system prompts
│   ├── plan-phase.md          # Plan Sub-Agent (spec + test spec)
│   ├── tdd-red-phase.md       # TDD Red Sub-Agent prompt
│   └── implement-phase.md     # Implementation Sub-Agent prompt
├── src/synthitect_mcp/
│   ├── __init__.py
│   ├── server.py             # MCP server with 3 tools
│   └── file_manager.py       # File I/O utility
├── SKILL.md                   # Orchestrator instructions (MoA Manager)
├── pyproject.toml
└── README.md
```

## Installation

```bash
# From source
pip install -e .

# Or install dependencies directly
pip install mcp>=1.0.0
```

## Usage

### Starting the MCP Server

```bash
# Using the CLI entry point
synthitect-mcp

# Or directly with Python
python -m synthitect_mcp
```

### MCP Tools (3 tools)

Each tool returns a **text briefing**. The Orchestrator MUST spawn a sub-agent and pass the briefing as instructions. The MCP server does NOT execute sub-agents.

| Tool | Description |
|------|-------------|
| `generate_plan_briefing(ticket_id, raw_idea)` | Plan phase: creates `plans/{ticket_id}/`, returns briefing to produce `spec.md` and `test_spec.md` (human approval before TDD Red) |
| `generate_tdd_red_briefing(ticket_id)` | TDD Red: verifies plan artifacts exist, returns briefing to write failing tests |
| `generate_implementation_briefing(ticket_id)` | Implementation: after TDD Red completes, returns briefing to make tests pass |

### Integration with Claude Code

Add to your Claude Code MCP configuration:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "synthitect": {
      "command": "synthitect-mcp",
      "cwd": "/path/to/your/project"
    }
  }
}
```

Or install as a user-level MCP server:

```bash
# Add to your Claude Code MCP settings (Settings > Developer > Edit Config)
{
  "mcpServers": {
    "synthitect": {
      "command": "python",
      "args": ["-m", "synthitect_mcp"],
      "cwd": "/path/to/synthitect-protocol"
    }
  }
}
```

### Integration with Claude CLI

```bash
# Start Claude CLI with the Synthitect Protocol MCP server
claude --mcp-config /path/to/mcp-config.json

# Or use environment variable
export MCP_SERVER_PATH=/path/to/synthitect-protocol
claude
```

### Integration with Other MCP Clients

The server communicates over stdio, making it compatible with any MCP client:

```bash
# Direct execution
cd /path/to/your/project && python -m synthitect_mcp

# With custom base directory
SYNTHITECT_BASE_DIR=/path/to/your/project python -m synthitect_mcp
```

---

## Usage Examples

### Example 1: Full CFAW lifecycle with Claude Code

```
User: /synthitect Add offline-first sync for user preferences

Step 1 — Plan

Orchestrator calls:
  generate_plan_briefing(
    ticket_id="FEAT-001",
    raw_idea="Add offline-first sync for user preferences"
  )
→ Pass briefing to Plan Sub-Agent; it writes plans/FEAT-001/spec.md and test_spec.md

HUMAN GATE: Present spec.md + test_spec.md for approval before TDD Red.

Step 2 — TDD Red

Orchestrator calls:
  generate_tdd_red_briefing(ticket_id="FEAT-001")
→ Pass briefing to TDD Red Sub-Agent; failing tests and stubs as needed

Step 3 — Implementation

Orchestrator calls:
  generate_implementation_briefing(ticket_id="FEAT-001")
→ Pass briefing to Implementation Sub-Agent until the suite is green
```

### Example 2: Single-phase invocation

```javascript
// In Claude Code, you can invoke individual phases:

// Start or refresh the plan for a ticket
generate_plan_briefing("FEAT-002", "Add payment processing")

// After spec.md + test_spec.md exist and are approved
generate_tdd_red_briefing("FEAT-002")

// After TDD Red is complete
generate_implementation_briefing("FEAT-002")
```

### Example 3: Checking artifacts

```bash
# Plan artifacts live under plans/{ticket_id}/
ls plans/FEAT-001/
# spec.md  test_spec.md  (and .phase_state.json once phases run)

# View the working spec
cat plans/FEAT-001/spec.md

# Check if the plan phase produced both contracts
test -f plans/FEAT-001/spec.md -a -f plans/FEAT-001/test_spec.md && echo "Plan complete" || echo "Plan not ready"
```

### Example 4: Using with Custom Constitution

```bash
# Set a custom Constitution file
export CONSTITUTION_PATH=/path/to/project/CONSTITUTION.md

# The Orchestrator will inject this Constitution into sub-agent briefings
python -m synthitect_mcp
```

## CFAW lifecycle (this MCP)

```
/synthitect [idea]
    │
    ▼
┌──────────────────────────────────────────────┐
│  Phase 1: Plan                               │
│  generate_plan_briefing(ticket_id, raw_idea) │
│  Output: plans/{id}/spec.md                 │
│          plans/{id}/test_spec.md             │
└──────────────────────────────────────────────┘
    │  HUMAN GATE: Approve plan artifacts      │
    ▼
┌──────────────────────────────────────────────┐
│  Phase 2: TDD Red                            │
│  generate_tdd_red_briefing(ticket_id)        │
│  Output: Briefing for TDD Red Sub-Agent      │
└──────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────┐
│  Phase 3: Implementation                     │
│  generate_implementation_briefing(ticket_id) │
│  Output: Briefing for Implementation Sub-Agent│
└──────────────────────────────────────────────┘
    │
    ▼
   MERGE (your review / CI as usual)
```

## Key Features

### Contract-First Development
- All decisions externalized to versioned specs
- No code written without approved specification
- Constitution as architectural law

### Self-Review Loops
- Actor-Critic Reflection in Spec and TDD phases
- Tautology detection for tests
- Hallucination detection for dependencies

### Human Gates
- User or Architect approval after Plan phase (`spec.md` + `test_spec.md`)
- TDD Red and Implementation proceed per your orchestration (see `SKILL.md`)

### Drift Detection
- File manifest tracking
- Hard flags for manifest/build changes
- Visibility mutation detection

## The CFAW Contract

1. Intelligence lives in specs, not chat history
2. Constitution is law. Violations are rejected.
3. No code without approved spec. No spec without Constitution audit.
4. Spec phase produces implementation plan AND test spec. Tests are red before implementation.
5. Implementation derives from spec. Tests are verifiers, not blueprints.
6. Drift is flagged proportionally. Minor is noted; Significant is reverted or amended.
7. Behavioral scenarios define done. Coverage numbers are a floor.
8. Ask of every test: What is the most broken implementation that still passes?

## Documentation

- [CFAW Specification](CFAW.md) - Full methodology specification
- [SKILL.md](SKILL.md) - Orchestrator instructions for AI agents

## License

0BSD
