import os
from .base import *  # noqa # pylint: disable=unused-wildcard-import


DEBUG = True

ALLOWED_HOSTS = ['*','127.0.0.1', '0.0.0.0', os.getenv('ALLOWED_LOCAL_HOST', '')]
