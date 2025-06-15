"""
Resource definitions and implementations for the MCP server.

This module handles all resource-related MCP protocol operations.
"""

import logging
import json
from typing import List

import mcp.types as types
from mcp.server.lowlevel import Server
from pydantic import AnyUrl

from src.tools.handlers import SAMPLE_DATA

# Configure module logger
logger = logging.getLogger(__name__)

# Available resources - these represent data that can be read by clients
AVAILABLE_RESOURCES = [
    types.Resource(
        uri=AnyUrl("memory://users"),
        name="User Database",
        description="In-memory user database with sample user records",
        mimeType="application/json"
    ),
    types.Resource(
        uri=AnyUrl("memory://system-info"),
        name="System Information", 
        description="Current system status and server metadata",
        mimeType="application/json"
    )
]

def get_user_data() -> str:
    """
    Get the user data as a JSON string.
    
    Returns:
        str: JSON string representation of user data
    """
    return json.dumps(SAMPLE_DATA["users"], indent=2)

def get_system_info() -> str:
    """
    Get the system information as a JSON string.
    
    Returns:
        str: JSON string representation of system information
    """
    return json.dumps(SAMPLE_DATA["system_info"], indent=2)

def setup_resource_handlers(server: Server) -> None:
    """
    Set up resource-related handlers on the provided server instance.
    
    Args:
        server: The MCP server instance
    """
    
    @server.list_resources()
    async def list_resources() -> List[types.Resource]:
        """
        Return the list of available resources.
        Resources provide data that can be used as context for LLM interactions.
        
        Returns:
            List of available resources
        """
        logger.info("Listing available resources")
        return AVAILABLE_RESOURCES
    
    @server.read_resource()
    async def read_resource(uri: AnyUrl) -> str:
        """
        Read and return the contents of a specific resource.
        Resources are application-controlled and provide contextual data.
        
        Args:
            uri: The URI of the resource to read
            
        Returns:
            String content of the resource
            
        Raises:
            ValueError: If the resource URI is unknown
        """
        logger.info(f"Reading resource: {uri}")
        
        uri_str = str(uri)
        
        if uri_str == "memory://users":
            # Return user data as JSON string
            return get_user_data()
        
        elif uri_str == "memory://system-info":
            # Return system information as JSON string
            return get_system_info()
        
        else:
            raise ValueError(f"Unknown resource: {uri}")
