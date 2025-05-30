"""
Core configuration and utilities for the Gugugu API
"""
import os
from openai import OpenAI


def get_ai_client() -> OpenAI:
    """
    Initialize and return OpenAI client with environment configuration
    
    Returns:
        OpenAI: Configured OpenAI client instance
        
    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set
    """
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    return OpenAI(api_key=api_key, base_url=base_url)


def get_ai_model() -> str:
    """
    Get the AI model name from environment variables
    
    Returns:
        str: AI model name, defaults to "deepseek-ai/DeepSeek-V3"
    """
    return os.getenv("AI_MODEL", "deepseek-ai/DeepSeek-V3")


def get_debug_mode() -> bool:
    """
    Get debug mode setting from environment variables
    
    Returns:
        bool: True if debug mode is enabled, False otherwise
    """
    return os.getenv("DEBUG", "False").lower() == "true"
