import pytest
from aitools_autogen.agents import WebScraperAgent

@pytest.fixture
def web_scraper_agent():
    return WebScraperAgent()

def test_web_scraper_agent(web_scraper_agent):
    task = """
    I want to retrieve the content of the following web pages:
    https://httpbin.org/get
    """
    web_scraper_agent.receive(message=task, request_reply=True, sender=web_scraper_agent, silent=True)
    last_message = web_scraper_agent.last_message()
    assert last_message is not None
    assert "https://httpbin.org/get" in last_message["content"]
    assert "url" in last_message["content"]["https://httpbin.org/get"]