
config_list = [
    {
        'model': 'gpt-4',
        'api_key': 'aitools',
        'api_base': 'http://aitools.cs.vt.edu:7860/openai/v1'
    }
]

llm_config = {
    "request_timeout": 300,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0.1,
    "allow_format_str_template": True
}



