# Installation

    `$ python -mvenv venv`

    `$ source venv/bin/activate`
    
    `(venv) $ pip install -r requirements.txt`

# Usage

To run the standalone python demonstration:
    `(venv) $ python aitools_autogen/python_app_with_agents.py`

To run the streamlit demonstration using blueprints:
    `(venv) $ streamlit run aitools_autogen/streamlit_app_with_agents.py` 

# Running Tests

    `(venv) $ export PYTHONPATH="${PYTHONPATH}:${PWD}" && pytest


# Overview

`aitools_autogen` is a repository of code for generating code from blueprints.

Blueprints are objects holding multiple agents and their relationships,
together with tools to assist in their cooperation.

Agents are objects that can be run, and can be connected to other agents.

Blueprint can be run in a variety of ways, including as a standalone python program,
and as a streamlit app.

# Code Walkabout

Blueprints are a simple aggregation of agents and their relationships.
The `init` method of a blueprint or the `initiate_work` 
method is where the agents are created and connected.
See the `aitools_autogen/blueprint*.py` files for more details.

Agents are Autogen agents.  Either the Autogen agent has an llm associated,
or it does not.  If it does, we can initialize the agent with a `system_message`.
See the `aitools_autogen/agents.py` file for more details.

Autogen configuration variables are in the `aitools_autogen/config.py` file,
and are used to configure the Autogen agents with defaults.  Some settings for 
tools are also located in the `aitools_autogen/__init__.py` file.

The utility functions in `aitools_autogen/utils.py` are used to help with
the creation of files on disk when code is generated from an LLM.
Effectively these are the code generation utilities akin to the code execution
utilities in `autogen` itself.

The `aitools_autogen/python_app_with_agents.py` file is a standalone python program
that runs a blueprint, generating example test code in the `.code/` folder.

The `aitools_autogen/streamlit_app_with_agents.py` file is a streamlit app that
runs a blueprint, generating example test code in the `.code/` folder.
The streamlit app offers facilities which can use different OpenAPI urls,
clear the `.cache/` folder from `autogen`, and use different seed values.

