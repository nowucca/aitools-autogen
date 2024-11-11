import asyncio
import os
from asyncio import sleep

import streamlit as st

import utils
from blueprint_generate_core_client import CoreClientTestBlueprint
from config import llm_config_openai as llm_config
from streamlit_file_browser import st_file_browser

st.set_page_config(
    page_title="Streamlit Using Agents",
    page_icon="🕵️‍♂️",
)

st.toast("Welcome to a test of Streamlit with Agents!", icon="🕵️‍♂️")

if st.session_state.get("blueprint", None) is None:
    st.session_state.blueprint = CoreClientTestBlueprint()


async def run_blueprint(seed: int = 42) -> str:
    await sleep(3)
    llm_config["seed"] = seed
    await st.session_state.blueprint.initiate_work(message=task)
    return st.session_state.blueprint.summary_result

if os.path.exists('aitools_autogen/coding'):
    st.markdown('# Generated Code')
    event = st_file_browser("aitools_autogen/coding", key='A')

blueprint_ctr, parameter_ctr = st.columns(2, gap="large")
with blueprint_ctr:
    st.markdown("# Run Blueprint")
    url = st.text_input("Enter a OpenAPI Schema URL to test:",
                        value="https://petstore3.swagger.io/api/v3/openapi.json")
    agents = st.button("Start the Agents!", type="primary")

with parameter_ctr:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Other Options")
    clear = st.button("Clear the autogen cache...&nbsp; ⚠️", type="secondary")
    seed = st.number_input("Enter a seed for the random number generator:", value=42)

results_ctr = st.empty()


if clear:
    with results_ctr:
        st.status("Clearing the agent cache...")
        utils.clear_working_dir(".cache", "*")
        st.status("Cache cleared!")

if agents:
    with results_ctr:
        st.status("Running the Blueprint...")

    task = f"""
            I want to retrieve the Open API specification from
            {url}
            """

    text = asyncio.run(run_blueprint(seed=seed))
    st.balloons()



    with results_ctr:
        st.markdown(text)
