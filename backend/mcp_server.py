#!/usr/bin/env python3
"""
FastMCP server for Choose Your Own Adventure Game
Allows natural language interaction with the story generation API
"""

import asyncio
import requests
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from fastmcp import FastMCP

# Configuration
API_BASE_URL = "http://localhost:8000/api"

@dataclass
class GameState:
    """Tracks the current game state"""
    current_story_id: Optional[int] = None
    current_node_id: Optional[int] = None
    session_id: Optional[str] = None
    last_job_id: Optional[str] = None
    story_data: Optional[Dict] = None

# Global game state
game_state = GameState()

# Initialize FastMCP
app = mcp = FastMCP("Choose Your Own Adventure Game")

@mcp.tool()
def create_story(theme: str) -> Dict[str, Any]:
    """
    Create a new Choose Your Own Adventure story with the given theme.
    
    Args:
        theme: The theme for the story (e.g., "space adventure", "medieval fantasy", "detective mystery")
    
    Returns:
        Dictionary with job information to track story generation progress
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/stories/create",
            json={"theme": theme},
            timeout=30
        )
        
        if response.status_code == 200:
            job_data = response.json()
            game_state.last_job_id = job_data.get("job_id")
            game_state.session_id = job_data.get("session_id")
            
            return {
                "success": True,
                "message": f"Story creation started with theme: '{theme}'",
                "job_id": job_data.get("job_id"),
                "session_id": job_data.get("session_id"),
                "status": job_data.get("status", "pending")
            }
        else:
            return {
                "success": False,
                "error": f"Failed to create story: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error creating story: {str(e)}"
        }

@mcp.tool()
def check_job_status(job_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Check the status of a story generation job.
    
    Args:
        job_id: The job ID to check. If not provided, uses the last job ID from current session.
    
    Returns:
        Dictionary with job status information
    """
    if not job_id:
        job_id = game_state.last_job_id
    
    if not job_id:
        return {
            "success": False,
            "error": "No job ID provided and no active job found"
        }
    
    try:
        response = requests.get(f"{API_BASE_URL}/jobs/{job_id}", timeout=30)
        
        if response.status_code == 200:
            job_data = response.json()
            status = job_data.get("status")
            
            # If job is completed, update game state
            if status == "completed" and job_data.get("story_id"):
                game_state.current_story_id = job_data.get("story_id")
            
            return {
                "success": True,
                "job_id": job_data.get("job_id"),
                "status": status,
                "theme": job_data.get("theme"),
                "story_id": job_data.get("story_id"),
                "created_at": job_data.get("created_at"),
                "completed_at": job_data.get("completed_at"),
                "error": job_data.get("error")
            }
        else:
            return {
                "success": False,
                "error": f"Failed to get job status: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error checking job status: {str(e)}"
        }

@mcp.tool()
def get_story(story_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve a complete story and prepare it for interactive gameplay.
    
    Args:
        story_id: The story ID to retrieve. If not provided, uses the current story.
    
    Returns:
        Dictionary with complete story data and current position
    """
    if not story_id:
        story_id = game_state.current_story_id
    
    if not story_id:
        return {
            "success": False,
            "error": "No story ID provided and no current story found"
        }
    
    try:
        response = requests.get(f"{API_BASE_URL}/stories/{story_id}/complete", timeout=30)
        
        if response.status_code == 200:
            story_data = response.json()
            
            # Update game state
            game_state.current_story_id = story_id
            game_state.story_data = story_data
            game_state.current_node_id = story_data["root_node"]["id"]
            
            root_node = story_data["root_node"]
            
            return {
                "success": True,
                "story_id": story_data["id"],
                "title": story_data["title"],
                "created_at": story_data["created_at"],
                "current_content": root_node["content"],
                "is_ending": root_node["is_ending"],
                "options": root_node.get("options", []),
                "message": "Story loaded successfully. You can now make choices to progress."
            }
        else:
            return {
                "success": False,
                "error": f"Failed to get story: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting story: {str(e)}"
        }

@mcp.tool()
def make_choice(choice_text: str) -> Dict[str, Any]:
    """
    Make a choice in the current story by selecting an option.
    
    Args:
        choice_text: The text of the choice/option to select
    
    Returns:
        Dictionary with the result of the choice and next story content
    """
    if not game_state.story_data or not game_state.current_node_id:
        return {
            "success": False,
            "error": "No active story found. Please load a story first using get_story()."
        }
    
    try:
        current_node = game_state.story_data["all_nodes"].get(str(game_state.current_node_id))
        
        if not current_node:
            return {
                "success": False,
                "error": "Current story node not found"
            }
        
        if current_node.get("is_ending"):
            return {
                "success": False,
                "error": "Story has ended. Start a new story to continue playing."
            }
        
        options = current_node.get("options", [])
        if not options:
            return {
                "success": False,
                "error": "No options available at current story position"
            }
        
        # Find matching option (case insensitive partial match)
        selected_option = None
        choice_lower = choice_text.lower()
        
        for option in options:
            if choice_lower in option["text"].lower() or option["text"].lower() in choice_lower:
                selected_option = option
                break
        
        if not selected_option:
            available_options = [opt["text"] for opt in options]
            return {
                "success": False,
                "error": f"Choice not found. Available options: {available_options}"
            }
        
        # Move to next node
        next_node_id = selected_option["next_node_id"]
        next_node = game_state.story_data["all_nodes"].get(str(next_node_id))
        
        if not next_node:
            return {
                "success": False,
                "error": "Next story node not found"
            }
        
        # Update current position
        game_state.current_node_id = next_node_id
        
        result = {
            "success": True,
            "selected_choice": selected_option["text"],
            "current_content": next_node["content"],
            "is_ending": next_node.get("is_ending", False),
            "options": next_node.get("options", [])
        }
        
        if next_node.get("is_ending"):
            result["is_winning_ending"] = next_node.get("is_winning_ending", False)
            result["message"] = "Story completed!"
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error making choice: {str(e)}"
        }

@mcp.tool()
def get_current_status() -> Dict[str, Any]:
    """
    Get the current game status and position.
    
    Returns:
        Dictionary with current game state information
    """
    if not game_state.story_data or not game_state.current_node_id:
        return {
            "success": True,
            "has_active_story": False,
            "message": "No active story. Create a new story to start playing."
        }
    
    try:
        current_node = game_state.story_data["all_nodes"].get(str(game_state.current_node_id))
        
        return {
            "success": True,
            "has_active_story": True,
            "story_id": game_state.current_story_id,
            "story_title": game_state.story_data.get("title"),
            "current_content": current_node["content"],
            "is_ending": current_node.get("is_ending", False),
            "options": current_node.get("options", []),
            "session_id": game_state.session_id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting status: {str(e)}"
        }

@mcp.tool()
def list_available_options() -> Dict[str, Any]:
    """
    List all available choices at the current story position.
    
    Returns:
        Dictionary with available options and their details
    """
    if not game_state.story_data or not game_state.current_node_id:
        return {
            "success": False,
            "error": "No active story found."
        }
    
    try:
        current_node = game_state.story_data["all_nodes"].get(str(game_state.current_node_id))
        
        if current_node.get("is_ending"):
            return {
                "success": True,
                "options": [],
                "message": "Story has ended. No more choices available."
            }
        
        options = current_node.get("options", [])
        
        return {
            "success": True,
            "options": [{"number": i+1, "text": opt["text"]} for i, opt in enumerate(options)],
            "message": f"Available choices: {len(options)}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error listing options: {str(e)}"
        }


def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()


