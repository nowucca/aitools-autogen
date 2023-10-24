import re
from typing import Optional, List, Dict, Any, Union

import autogen
import requests
from autogen import Agent, ConversableAgent

# It was at one stage interesting to play with removing the default reply functions.
# However, it just led to infinite conversations more easily.
# I'm keeping this agent here as a reminder of how I implemented it.
class CustomReplyAgent(ConversableAgent):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name if name is not None else "Custom Reply Agent", **kwargs)
        self._reply_func_list = []


# This is a general agent with a specific name and a specific reply function.
# It's not very useful, but it's a good example of how to implement a custom agent.
class OpenAPIAgent(autogen.AssistantAgent):
    def __init__(self):
        super().__init__(name="OpenAPI Agent", llm_config=None,
                         max_consecutive_auto_reply=3)
        self.register_reply([Agent, None], self._reply_func)

    def _reply_func(self,
                    recipient: ConversableAgent,
                    messages: Optional[List[Dict]] = None,
                    sender: Optional[Agent] = None,
                    config: Optional[Any] = None,
                    ) -> Any | Union[str, Dict, None]:
        urls = self._extract_urls(messages[0]["content"])
        if (urls is None) or (len(urls) == 0):
            return False, None
        return True, self._get_openapi_spec(urls[0])

    # Write a function that given a str extracts a list of urls present in the string
    def _extract_urls(self, text):
        """
            Extracts a list of URLs from a given string.

            :param text: str, the text to search for URLs.
            :return: list, a list of URLs found in the string.
            """
        url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_regex, text)
        return urls

    def _get_openapi_spec(self, url) -> Optional[str]:
        response = requests.get(url)
        if response.status_code == 200:
            return str(response.text)
        else:
            return None


# openai_agent = OpenAPIAgent()
# task = """
# I want to retrieve the Open API specification for the OpenAI API.
# https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml
# """
# openai_agent.receive(message=task, request_reply=True, sender=openai_agent)
# agent_details.print_conversable_agent_state(openai_agent)


# This is a general agent with a specific name and a specific reply function.
# It scours a set of urls and gathers a dictionary of the content of each url.
# There's no cycle protection yet.
class WebScraperAgent(autogen.AssistantAgent):
    def __init__(self):
        super().__init__(name="WebScraper Agent", llm_config=None,
                         max_consecutive_auto_reply=3)
        self.register_reply([Agent, None], self._scraper_func)

    def _scraper_func(self,
                      recipient: ConversableAgent,
                      messages: Optional[List[Dict]] = None,
                      sender: Optional[Agent] = None,
                      config: Optional[Any] = None,
                      ) -> Any | Union[str, Dict, None]:
        urls = self._extract_urls(messages[0]["content"])
        if (urls is None) or (len(urls) == 0):
            return False, None
        return True, self._get_scraped_content(urls)

    # Write a function that given a str extracts a list of urls present in the string
    @staticmethod
    def _extract_urls(text):
        """
            Extracts a list of URLs from a given string.

            :param text: str, the text to search for URLs.
            :return: list, a list of URLs found in the string.
            """
        url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_regex, text)
        return urls

    @staticmethod
    def _get_scraped_content(urls: List[str]) -> Dict[str, Dict[str, str]]:
        result = {}
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                result[url] = str(response.text)
            else:
                result[url] = None
        return {"content": result}

# Sometimes you just want one web page and its content directly....
class WebPageScraperAgent(WebScraperAgent):
    def _scraper_func(self,
                      recipient: ConversableAgent,
                      messages: Optional[List[Dict]] = None,
                      sender: Optional[Agent] = None,
                      config: Optional[Any] = None,
                      ) -> Any | Union[str, Dict, None]:
        urls = self._extract_urls(messages[0]["content"])
        if (urls is None) or (len(urls) == 0):
            return False, None
        content = self._get_scraped_content(urls[0])
        if content is None:
            return False, None
        return True, content

    def _get_scraped_content(self, url: str) -> Optional[Dict[str, str]]:
        result: Optional[Dict[str, str]] = dict()
        response = requests.get(url)
        if response.status_code == 200:
            result['content'] = str(response.text)
        else:
            result = None
        return result
