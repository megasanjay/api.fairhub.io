"""Configuration for the application."""

import os
from dotenv import dotenv_values

FAIRHUB_DATABASE_URL = os.environ.get("FAIRHUB_DATABASE_URL")

# take environment variables from .env
envcfg = dotenv_values(".env")

if "FAIRHUB_DATABASE_URL" in envcfg:
    FAIRHUB_DATABASE_URL = envcfg["FAIRHUB_DATABASE_URL"]