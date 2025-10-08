"""
AI Insights Module

This module provides AI-powered financial insights, predictions, and recommendations
based on the user's transaction data.
"""

from . import models, schemas, service, endpoints

# This makes the module importable and initializes the models
__all__ = ["models", "schemas", "service", "endpoints"]

# Initialize any module-level components here
def init_module():
    """Initialize the AI insights module"""
    # Any initialization code can go here
    pass
