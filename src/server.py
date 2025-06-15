"""
Server configuration and setup module for the MCP server.

This module handles initialization and configuration of the MCP server instance.
"""

import logging
from mcp.server.lowlevel import Server

from src.resources.handlers import setup_resource_handlers
from src.tools.handlers import setup_tool_handlers
from src.prompts.handlers import setup_prompt_handlers

# Configure module logger
logger = logging.getLogger(__name__)

def create_server() -> Server:
    """
    Create and configure an MCP server instance.
    
    Returns:
        Configured server instance
    """
    # Initialize the MCP server with descriptive metadata
    logger.info("Creating MCP server instance")
    server = Server("example-mcp-server")
    
    # Set up all the handlers
    setup_resource_handlers(server)
    setup_tool_handlers(server)
    setup_prompt_handlers(server)
    
    return server
