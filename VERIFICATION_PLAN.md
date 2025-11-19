# HD Assistant Verification Plan

## Objective
Verify that the `AgentJira` has been successfully transformed into the `HD Support Assistant` and that all new help desk capabilities are functional.

## Prerequisites
- [ ] Environment variables are set (checked via `.env` existence)
- [ ] Python virtual environment is active
- [ ] Docker container for MCP server is running (`friendly_goldberg`)

## Verification Steps

### 1. Server Startup
- [ ] Restart `jira-tool-server` (Port 5001)
- [ ] Restart `agent-server` (Port 5002)
- [ ] Verify both servers are responding to health checks (or simple curl requests)

### 2. Functional Testing (via API/CLI)
We will use the `agent-server/debug_mcp.py` or a new test script to simulate user interactions.

#### Test Case A: Agent Persona & Triage
- **Input**: "Show me unassigned tickets"
- **Expected Output**:
    - Agent identifies as HD Assistant.
    - Calls `get_unassigned_queue`.
    - Returns a list of tickets from project HD with `assignee IS EMPTY`.

#### Test Case B: Workload Management
- **Input**: "What is on my plate?" (Simulating a specific user, e.g., "Nate Modlin")
- **Expected Output**:
    - Calls `get_tasks_for_user` with the user's name.
    - Returns list of assigned tickets.

#### Test Case C: Action - Assignment
- **Input**: "Assign HD-123 to me" (Replace HD-123 with a real ticket key found in Test Case A)
- **Expected Output**:
    - Calls `assign_ticket_to_user`.
    - Confirms assignment.

#### Test Case D: Action - Commenting
- **Input**: "Add a comment to HD-123 saying 'Investigating now'"
- **Expected Output**:
    - Calls `add_ticket_comment`.
    - Confirms comment addition.

### 3. Frontend Verification (Manual)
- [ ] Launch Frontend (`npm start` in `frontend/`)
- [ ] Verify Welcome Message: "Hi! I'm your Help Desk Assistant for project HD."
- [ ] Verify Suggested Queries match the new list.

## Automated Test Script
I will create a script `verify_hd_assistant.py` to automate the API-level tests (Step 2).
