import autogen
from aitools_autogen.config import llm_config_llama2, llm_config_openai

# Define an assistant coder using the LLM
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_openai,
    system_message="""
    You are a professional Python coder, known for your insightful and engaging solutions with explanations to coding problems.
    You produce Python code in response to coding problems.  You do not comment on feedback, you respond ONLY with code.
    You should improve the quality of the code based on the feedback from the user.
    When the user indicates your code is acceptable, send a TERMINATE message.
    """,
)

# Define the user proxy, the driver of the conversation who has ability to execute code.
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    max_consecutive_auto_reply=6, # stop infinite chat loops
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },
    llm_config=llm_config_llama2
)

# Example Task
task = f"""
Write a function in Python to sort an array of integers using quicksort.
"""

res = user_proxy.initiate_chat(recipient=coder, message=task, max_turns=2, summary_method="last_msg")
print(res)
print("---")
print(user_proxy.last_message(coder))
#%%
