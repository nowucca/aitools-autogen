from typing import Optional

from autogen import ConversableAgent

import aitools_autogen
import utils
from agents import WebPageScraperAgent
from blueprint import Blueprint
from config import llm_config, config_list


class CoreClientTestBlueprint(Blueprint):

    def __init__(self, work_dir: Optional[str] = aitools_autogen.WORKING_DIR):
        super().__init__([], config_list=config_list, llm_config=llm_config)
        self._work_dir = work_dir or "code"
        self._summary_result: Optional[str] = None

    @property
    def summary_result(self) -> str | None:
        """The getter for the 'summary_result' attribute."""
        return self._summary_result

    @property
    def work_dir(self) -> str:
        """The getter for the 'work_dir' attribute."""
        return self._work_dir

    async def initiate_work(self, message: str):
        utils.clear_working_dir(self._work_dir)
        agent0 = ConversableAgent("a0",
                                  max_consecutive_auto_reply=0,
                                  llm_config=False,
                                  human_input_mode="NEVER")

        scraper_agent = WebPageScraperAgent()

        summary_agent = ConversableAgent("summary_agent",
                                         max_consecutive_auto_reply=6,
                                         llm_config=llm_config,
                                         human_input_mode="NEVER",
                                         code_execution_config=False,
                                         function_map=None,
                                         system_message="""You are a helpful AI assistant.
        You can summarize OpenAPI specifications.  When given an OpenAPI specification, 
        output a summary in bullet point form for each endpoint.
        Let's make it concise in markdown format.
        It should include short descriptions of parameters,
        and list expected possible response status codes.
        Return `None` if the OpenAPI specification is not valid or cannot be summarized.
            """)

        aiohttp_client_agent = ConversableAgent("aiohttp_client_agent",
                                                max_consecutive_auto_reply=6,
                                                llm_config=llm_config,
                                                human_input_mode="NEVER",
                                                code_execution_config=False,
                                                function_map=None,
                                                system_message="""
        You are a QA developer expert in Python, using the pytest framework.
        You're writing an http client layer for tests for an API.

        When you receive a message, you should expect that message to describe endpoints of an API.

        Let's use aiohttp for our core http client layer.
        All files must be generated in the api/client directory.

        Write a complete implementation covering all described endpoints.
        Use multiple classes in separate file names in a directory structure that makes sense.
        Use aiohttp.ClientSession for the http client.
        Use aiohttp.ClientResponse for the http response.

        Create the aiohttp session inside a `with` block so that it is closed automatically.
        The code using this generated code should not require aiohttp.

        You must indicate the script type in the code block. 
        Do not suggest incomplete code which requires users to modify. 
        Always put `# filename: api/client/<filename>` as the first line of each code block.

        Feel free to include multiple code blocks in one response. Do not ask users to copy and paste the result. 
        """)

        agent0.initiate_chat(scraper_agent, True, True, message=message)

        message = agent0.last_message(scraper_agent)

        agent0.initiate_chat(summary_agent, True, True, message=message)

        api_description_message = agent0.last_message(summary_agent)

        # api_description = api_description_message["content"]
        # print(api_description)

        agent0.initiate_chat(aiohttp_client_agent, True, True, message=api_description_message)

        llm_message = agent0.last_message(aiohttp_client_agent)["content"]
        utils.save_code_files(llm_message, self.work_dir)

        self._summary_result = utils.summarize_files(self.work_dir)
