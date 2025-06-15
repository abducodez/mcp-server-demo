
#!/usr/bin/env python
"""
MCP Server Demo - Main Entry Point

This script starts an MCP (Model Control Protocol) server that demonstrates
providing resources, tools, and prompts to AI models through a standardized
protocol. The server uses stdio transport for communication.

Usage:
    python demo.py

The server provides:
- Resources: User database and system information
- Tools: Calculate user statistics and update user status
- Prompts: Templates for data analysis and report generation
"""

import logging
import anyio
from mcp.server.stdio import stdio_server

from src.server import create_server

# Configure logging for better debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """
    Main entry point for the MCP server.
    Sets up stdio transport and runs the server event loop.
    """
    # Create and configure the server
    server = create_server()
    
    logger.info("Starting MCP server...")
    
    # Use stdio transport for communication with the client
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Server connected via stdio transport")
        
        # Run the server with proper initialization options
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    # Run the server using anyio for cross-platform async support
    logger.info("Initializing MCP server application")
    anyio.run(main)
