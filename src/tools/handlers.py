"""
Tool definitions and implementations for the MCP server.

This module handles all tool-related MCP protocol operations.
"""

import json
import logging
from datetime import datetime
from typing import Any, List

import mcp.types as types
from mcp.server.lowlevel import Server


# Configure module logger
logger = logging.getLogger(__name__)


# Sample data for demonstration purposes
SAMPLE_DATA = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "active": True},
        {"id": 2, "name": "Bob", "email": "bob@example.com", "active": False},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com", "active": True}
    ],
    "system_info": {
        "server_name": "example-mcp-server",
        "version": "1.0.0",
        "started_at": datetime.now().isoformat()
    }
}


def calculate_user_statistics() -> dict:
    """
    Calculate statistics about the users.
    
    Returns:
        dict: Dictionary of user statistics
    """
    active_users = sum(1 for user in SAMPLE_DATA["users"] if user["active"])
    total_users = len(SAMPLE_DATA["users"])
    inactive_users = total_users - active_users
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "activity_rate": f"{(active_users / total_users * 100):.1f}%" if total_users > 0 else "0.0%"
    }

def update_user_status(user_id: int, active: bool) -> tuple[bool, str]:
    """
    Update a user's active status.
    
    Args:
        user_id: The ID of the user to update
        active: New active status for the user
        
    Returns:
        tuple[bool, str]: Success status and message
    """
    for user in SAMPLE_DATA["users"]:
        if user["id"] == user_id:
            old_status = user["active"]
            user["active"] = active
            return True, f"Updated user {user_id} status from {old_status} to {active}"
    
    return False, f"User with ID {user_id} not found"

def setup_tool_handlers(server: Server) -> None:
    """
    Set up tool-related handlers on the provided server instance.
    
    Args:
        server: The MCP server instance
    """
    
    @server.list_tools()
    async def list_tools() -> List[types.Tool]:
        """
        Return the list of available tools.
        This enables tool discovery by clients and models.
        
        Returns:
            List of available tools
        """
        return [
            types.Tool(
                name="calculate_user_stats",
                description="Calculate statistics about users in the database",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            types.Tool(
                name="update_user_status", 
                description="Update the active status of a specific user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user to update"
                        },
                        "active": {
                            "type": "boolean", 
                            "description": "New active status for the user",
                            "default": True
                        }
                    },
                    "required": ["user_id"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> List[types.Content]:
        """
        Handle tool calls from the client.
        Tools are model-controlled and allow the AI to perform actions.
        
        Args:
            name: The name of the tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            List of content items as a result of the tool call
            
        Raises:
            ValueError: If the tool name is unknown
        """
        logger.info(f"Tool called: {name} with arguments: {arguments}")
        
        if name == "calculate_user_stats":
            # Calculate user statistics using the data module
            stats = calculate_user_statistics()
            
            return [
                types.TextContent(
                    type="text",
                    text=f"User Statistics Analysis:\n{json.dumps(stats, indent=2)}"
                )
            ]
        
        elif name == "update_user_status":
            # Update user status using the data module
            user_id = arguments.get("user_id")
            new_status = arguments.get("active", True)
            
            _, message = update_user_status(user_id, new_status)
            
            return [
                types.TextContent(
                    type="text",
                    text=message
                )
            ]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    