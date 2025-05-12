"""
Environment variable validation module.
This module provides functions for validating required environment variables on application startup.
"""
import logging
from typing import List
import os
from .settings import get_settings

logger = logging.getLogger(__name__)

def validate_required_env_vars() -> bool:
    """
    Validate that all required environment variables are set.
    Returns True if all required variables are present, False otherwise.
    """
    settings = get_settings()
    
    # Define groups of required environment variables
    required_groups = {
        "Supabase": ["SUPABASE_URL", "SUPABASE_KEY", "SUPABASE_JWT_SECRET"],
        "Pinecone": ["PINECONE_API_KEY", "PINECONE_ENVIRONMENT", "PINECONE_INDEX_NAME"],
        "OpenAI": ["OPENAI_API_KEY"],
        "Database": ["DATABASE_URL"]
    }
    
    all_valid = True
    
    for group_name, vars_list in required_groups.items():
        group_valid = True
        missing_vars = []
        
        for var_name in vars_list:
            # Get the value from settings using getattr
            var_value = getattr(settings, var_name, None)
            if not var_value:
                missing_vars.append(var_name)
                group_valid = False
        
        if not group_valid:
            logger.error(f"Missing required {group_name} environment variables: {', '.join(missing_vars)}")
            all_valid = False
    
    return all_valid

def validate_on_startup() -> None:
    """
    Run validation on application startup and log warnings for missing variables.
    """
    if not validate_required_env_vars():
        logger.warning(
            "Application started with missing environment variables. "
            "Some features may not work correctly. "
            "Please check the logs above for details."
        )
    else:
        logger.info("All required environment variables are set correctly.") 