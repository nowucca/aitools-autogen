import os
import sys

config_list_openai = [
    {
        'base_url': 'http://aitools.cs.vt.edu:7860/openai/v1',
        'api_key': 'aitools',
        'model': 'gpt-4-turbo-preview',
    },
    {
        'base_url': 'http://aitools.cs.vt.edu:7860/openai/v1',
        'api_key': 'aitools',
        'model': 'gpt-3.5-turbo',
    }

]

llm_config_openai = {
    "timeout": 300,
    "seed": 42,
    "config_list": config_list_openai,
    "temperature": 0.1,
    "allow_format_str_template": True
}


DEFAULT_MODEL = "gpt-4-turbo-preview"
FAST_MODEL = "gpt-3.5-turbo"
# Regular expression for finding a code block
CODE_BLOCK_PATTERN = r"(.*?)```(\w*)\n(.*?)\n```"
WORKING_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "coding")
UNKNOWN = "unknown"
TIMEOUT_MSG = "Timeout"
DEFAULT_TIMEOUT = 600
WIN32 = sys.platform == "win32"
PATH_SEPARATOR = WIN32 and "\\" or "/"
