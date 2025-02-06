import os
from typing import Optional

class Config:
    """Configuration settings for the parrot server."""
    def __init__(self):
        # Server settings
        self.host: str = os.environ.get('HOST', '')
        self.port: int = int(os.environ.get('PORT', '8080'))
        
        # Logging settings
        self.log_level: str = os.environ.get('LOG_LEVEL', 'INFO')
        self.log_format: str = os.environ.get('LOG_FORMAT', 'pretty')  # 'pretty' or 'json'

# Global config instance
config = Config()
