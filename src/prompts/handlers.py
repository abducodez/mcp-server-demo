"""
Prompt definitions and implementations for the MCP server.

This module handles all prompt-related MCP protocol operations.
"""

import logging
from typing import Dict, List, Optional

import mcp.types as types
from mcp.server.lowlevel import Server

# Configure module logger
logger = logging.getLogger(__name__)

# Prompt templates for common interactions
AVAILABLE_PROMPTS = [
    types.Prompt(
        name="analyze-user-data",
        description="Analyze user data patterns and provide insights",
        arguments=[
            types.PromptArgument(
                name="focus_area",
                description="Specific aspect to analyze (activity, emails, etc.)",
                required=False
            )
        ]
    ),
    types.Prompt(
        name="generate-report",
        description="Generate a formatted report based on available data",
        arguments=[
            types.PromptArgument(
                name="report_type",
                description="Type of report to generate (summary, detailed, etc.)",
                required=True
            ),
            types.PromptArgument(
                name="include_metadata",
                description="Whether to include system metadata in the report",
                required=False
            )
        ]
    )
]

def setup_prompt_handlers(server: Server) -> None:
    """
    Set up prompt-related handlers on the provided server instance.
    
    Args:
        server: The MCP server instance
    """
    
    @server.list_prompts()
    async def list_prompts() -> List[types.Prompt]:
        """
        Return the list of available prompts.
        Prompts are user-controlled templates for common LLM interactions.
        
        Returns:
            List of available prompts
        """
        logger.info("Listing available prompts")
        return AVAILABLE_PROMPTS
    
    @server.get_prompt()
    async def get_prompt(
        name: str, arguments: Optional[Dict[str, str]] = None
    ) -> types.GetPromptResult:
        """
        Generate a specific prompt with the provided arguments.
        Prompts help standardize common interaction patterns.
        
        Args:
            name: The name of the prompt to get
            arguments: Optional arguments to customize the prompt
            
        Returns:
            Prompt result with messages
            
        Raises:
            ValueError: If the prompt name is unknown
        """
        logger.info(f"Getting prompt: {name} with arguments: {arguments}")
        
        if arguments is None:
            arguments = {}
        
        if name == "analyze-user-data":
            # Create a prompt for user data analysis
            focus_area = arguments.get("focus_area", "general patterns")
            
            return types.GetPromptResult(
                description="Prompt for analyzing user data patterns",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(
                            type="text",
                            text=f"Please analyze the user data with focus on: {focus_area}. "
                                f"Look for patterns, insights, and any notable trends. "
                                f"Consider user activity status, email domains, and user distribution."
                        )
                    )
                ]
            )
        
        elif name == "generate-report":
            # Create a prompt for report generation
            report_type = arguments.get("report_type", "summary")
            include_metadata = arguments.get("include_metadata", "false").lower() == "true"
            
            base_text = f"Generate a {report_type} report based on the available user data. "
            
            if include_metadata:
                base_text += "Include system metadata and technical details in your report. "
            
            base_text += "Make the report clear, well-structured, and actionable."
            
            return types.GetPromptResult(
                description="Prompt for generating data reports",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(
                            type="text",
                            text=base_text
                        )
                    )
                ]
            )
        
        else:
            raise ValueError(f"Unknown prompt: {name}")
