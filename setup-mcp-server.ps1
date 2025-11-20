# Setup script for the updated MCP Atlassian Server
# This script will build and run the new MCP server with Jira API v3 support

Write-Host "=== MCP Atlassian Server Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
$envFile = "mcp-atlassian-updated\.env"
if (-not (Test-Path $envFile)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please provide your Jira credentials:" -ForegroundColor Green
    Write-Host ""
    
    # Get Jira site name
    $siteName = Read-Host "Jira Site Name (e.g., rehrig.atlassian.net)"
    
    # Get user email
    $userEmail = Read-Host "Jira User Email (e.g., nmodlin@rehrig.com)"
    
    # Get API token (masked input)
    Write-Host "Jira API Token (input will be hidden):" -NoNewline
    $apiToken = Read-Host -AsSecureString
    $apiTokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiToken))
    
    # Create .env file
    @"
# Atlassian Configuration
ATLASSIAN_SITE_NAME=$siteName
ATLASSIAN_USER_EMAIL=$userEmail
ATLASSIAN_API_TOKEN=$apiTokenPlain

# MCP Configuration
MCP_SERVER_NAME=mcp-atlassian-integration
MCP_SERVER_VERSION=2.1.1

# Logging Configuration
LOG_LEVEL=info
"@ | Out-File -FilePath $envFile -Encoding UTF8
    
    Write-Host ""
    Write-Host "✓ .env file created successfully!" -ForegroundColor Green
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Yellow
Set-Location mcp-atlassian-updated
docker build -t mcp-atlassian-server:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Docker build failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Write-Host ""
Write-Host "✓ Docker image built successfully!" -ForegroundColor Green

Write-Host ""
Write-Host "Starting MCP server container..." -ForegroundColor Yellow

# Stop and remove old container if it exists
docker stop friendly_goldberg 2>$null
docker rm friendly_goldberg 2>$null

# Run the new container with the same name for compatibility
docker run -d `
    --name friendly_goldberg `
    --env-file .env `
    -i `
    mcp-atlassian-server:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start container!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Set-Location ..

Write-Host ""
Write-Host "✓ MCP server container started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Container name: friendly_goldberg" -ForegroundColor Cyan
Write-Host "Image: mcp-atlassian-server:latest (with Jira API v3 support)" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now test the agent server!" -ForegroundColor Green
Write-Host "Run: python agent-server/debug_agent.py" -ForegroundColor Yellow

