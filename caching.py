from flask_caching import Cache
from config import config

cache = Cache(
    config={
        key.replace("FAIRHUB_", ""): value
        for key, value in config.items()
        if "CACHE" in key
    }
)
