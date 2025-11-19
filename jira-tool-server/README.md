# Jira Tool Server

A secure, stateless API service that exposes read-only Jira query endpoints for the AI-Powered Jira Dashboard.

## Features

- **Secure**: Jira API credentials are stored server-side only
- **Read-only**: All endpoints only query data, no modifications
- **Stateless**: No session management, pure API endpoints
- **CORS-enabled**: Can be called from frontend applications

## Setup

### 1. Install Dependencies

```bash
cd jira-tool-server
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your Jira credentials:

```bash
cp .env.example .env
```

Edit `.env` with your Jira details:
- `JIRA_URL`: Your Jira instance URL (e.g., https://your-domain.atlassian.net)
- `JIRA_EMAIL`: Your Jira account email
- `JIRA_API_TOKEN`: Your Jira API token (generate at https://id.atlassian.com/manage-profile/security/api-tokens)

### 3. Update JQL Queries

Edit `jira_client.py` and replace `YOUR_PROJECT` with your actual Jira project key in the JQL queries.

### 4. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5001`

## API Endpoints

### Health Check
```
GET /health
```

### Get Bugs Summary
```
POST /api/jira/get_bugs_summary
```
Returns summary of all open bugs including counts by priority.

### Get Tasks for User
```
POST /api/jira/get_tasks_for_user
Content-Type: application/json

{
  "username": "Alice Smith"
}
```
Returns tasks and bugs assigned to the specified user.

### Get Overall Progress
```
POST /api/jira/get_overall_progress
```
Returns team progress metrics including completed tasks, in-progress items, and story points.

## Testing

You can test the endpoints using curl:

```bash
# Health check
curl http://localhost:5001/health

# Get bugs summary
curl -X POST http://localhost:5001/api/jira/get_bugs_summary

# Get tasks for user
curl -X POST http://localhost:5001/api/jira/get_tasks_for_user \
  -H "Content-Type: application/json" \
  -d '{"username": "Alice Smith"}'

# Get overall progress
curl -X POST http://localhost:5001/api/jira/get_overall_progress
```

## Security Notes

- Never commit the `.env` file to version control
- Keep your Jira API token secure
- This server should be deployed behind proper authentication in production
- Consider rate limiting for production deployments

