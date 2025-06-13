"""
Configuration settings for the UR agent.
"""

import os
from ..utils.utils import get_env_var

# Google Cloud Project Settings
PROJECT_ID = get_env_var("GOOGLE_CLOUD_PROJECT")
LOCATION = get_env_var("GOOGLE_CLOUD_LOCATION")

# GCS Storage Settings
GCS_DEFAULT_STORAGE_CLASS = "STANDARD"
GCS_DEFAULT_LOCATION = "US"
GCS_LIST_BUCKETS_MAX_RESULTS = 50
GCS_LIST_BLOBS_MAX_RESULTS = 100
GCS_DEFAULT_CONTENT_TYPE = "application/pdf"

# Agent Settings
AGENT_NAME = "ur_agent"
AGENT_MODEL = "gemini-2.5-pro-preview-05-06"
AGENT_OUTPUT_KEY = "last_response"

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
