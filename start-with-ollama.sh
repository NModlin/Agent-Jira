#!/bin/bash

# Quick start script for Jira Dashboard with Ollama
# This script helps you get started with Ollama quickly

set -e

echo "🦙 Jira Dashboard with Ollama - Quick Start"
echo "============================================"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo ""
    echo "Please install Ollama first:"
    echo "  Mac: brew install ollama"
    echo "  Linux: curl -fsSL https://ollama.com/install.sh | sh"
    echo "  Windows: Download from https://ollama.com/download/windows"
    echo ""
    exit 1
fi

echo "✅ Ollama is installed"

# Check if Ollama is running
if ! curl -s http://localhost:11434 > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running. Starting Ollama..."
    ollama serve &
    sleep 3
fi

echo "✅ Ollama is running"

# Check if llama3.1 model is available
if ! ollama list | grep -q "llama3.1"; then
    echo ""
    echo "📥 Downloading Llama 3.1 model (this may take a few minutes)..."
    ollama pull llama3.1
fi

echo "✅ Llama 3.1 model is ready"
echo ""

# Update .env file if it exists
if [ -f "agent-server/.env" ]; then
    echo "📝 Updating agent-server/.env for Ollama..."
    
    # Check if LLM_PROVIDER exists, if not add it
    if ! grep -q "LLM_PROVIDER" agent-server/.env; then
        echo "" >> agent-server/.env
        echo "# LLM Provider Configuration" >> agent-server/.env
        echo "LLM_PROVIDER=ollama" >> agent-server/.env
        echo "OLLAMA_BASE_URL=http://localhost:11434" >> agent-server/.env
        echo "OLLAMA_MODEL=llama3.1" >> agent-server/.env
    else
        # Update existing values
        sed -i.bak 's/^LLM_PROVIDER=.*/LLM_PROVIDER=ollama/' agent-server/.env
        sed -i.bak 's/^OLLAMA_MODEL=.*/OLLAMA_MODEL=llama3.1/' agent-server/.env
        rm agent-server/.env.bak 2>/dev/null || true
    fi
    
    echo "✅ Configuration updated"
else
    echo "⚠️  agent-server/.env not found. Creating from template..."
    cp agent-server/.env.example agent-server/.env
    echo "✅ Created agent-server/.env"
    echo ""
    echo "⚠️  Please edit agent-server/.env and add your:"
    echo "   - LANGCHAIN_API_KEY (from LangSmith)"
    echo ""
fi

echo ""
echo "============================================"
echo "✅ Ollama Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Make sure you have configured:"
echo "   - jira-tool-server/.env (Jira credentials)"
echo "   - agent-server/.env (LangSmith API key)"
echo ""
echo "2. Start the servers (in 3 separate terminals):"
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
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For detailed setup, see OLLAMA_SETUP.md"
echo ""

