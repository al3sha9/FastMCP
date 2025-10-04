#!/bin/bash

echo "Setting up FastMCP for Choose Your Own Adventure Game..."

# Install FastMCP and dependencies
echo "Installing FastMCP dependencies..."
pip3 install -r mcp_requirements.txt

# Make the MCP server executable
chmod +x mcp_server.py

echo "Setup complete!"
echo ""
echo "To use with Gemini CLI:"
echo "1. Make sure your backend server is running on http://localhost:8000"
echo "2. Configure your Gemini CLI to use the MCP server:"
echo "   - Server path: $(pwd)/mcp_server.py"
echo "   - Or use the config file: $(pwd)/mcp_config.json"
echo ""
echo "Available MCP tools:"
echo "  - create_story(theme): Create a new story"
echo "  - check_job_status(): Check story generation progress"  
echo "  - get_story(): Load and start playing a story"
echo "  - make_choice(choice_text): Make a choice in the story"
echo "  - get_current_status(): See current game state"
echo "  - list_available_options(): See available choices"
echo ""
echo "Example usage with Gemini CLI:"
echo '  "Create a space adventure story"'
echo '  "Check if my story is ready"'  
echo '  "Load my story and start playing"'
echo '  "I want to explore the mysterious cave"'
