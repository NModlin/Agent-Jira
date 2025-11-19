#!/bin/bash

# AI-Powered Jira Dashboard Setup Script
# This script helps you set up all three components of the system

set -e

echo "🚀 AI-Powered Jira Dashboard Setup"
echo "===================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python and Node.js are installed${NC}"
echo ""

# Setup Jira Tool Server
echo "📦 Setting up Jira Tool Server..."
cd jira-tool-server

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Created .env file. Please edit jira-tool-server/.env with your Jira credentials.${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Installing dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt
deactivate

echo -e "${GREEN}✓ Jira Tool Server setup complete${NC}"
echo ""

# Setup Agent Server
echo "🤖 Setting up Agent Server..."
cd ../agent-server

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Created .env file. Please edit agent-server/.env with your API keys.${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Installing dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt
deactivate

echo -e "${GREEN}✓ Agent Server setup complete${NC}"
echo ""

# Setup Frontend
echo "🎨 Setting up Frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"
echo ""

# Final instructions
echo "===================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your environment variables:"
echo "   - Edit jira-tool-server/.env with your Jira credentials"
echo "   - Edit agent-server/.env with your LangSmith and Gemini API keys"
echo ""
echo "2. Update Jira project key:"
echo "   - Edit jira-tool-server/jira_client.py"
echo "   - Replace 'YOUR_PROJECT' with your actual Jira project key"
echo ""
echo "3. Start the servers (in separate terminals):"
echo ""
echo "   Terminal 1 - Jira Tool Server:"
echo "   $ cd jira-tool-server"
echo "   $ source venv/bin/activate"
echo "   $ python app.py"
echo ""
echo "   Terminal 2 - Agent Server:"
echo "   $ cd agent-server"
echo "   $ source venv/bin/activate"
echo "   $ python app.py"
echo ""
echo "   Terminal 3 - Frontend:"
echo "   $ cd frontend"
echo "   $ npm run dev"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "For detailed setup instructions, see:"
echo "  - README.md (main documentation)"
echo "  - LANGSMITH_SETUP.md (LangSmith configuration)"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"

