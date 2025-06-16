from typing import Annotated
import autogen
import random

# --- Configuration and Agent Initialization (from Slide 8) ---
# config_list_phi3=[
#     {
#         'base_url':"http://0.0.0.0:4000",
#         'api_key':'NULL' # This is for autogen client, not litellm server
#     }
# ]

# phi3_config = {
#     "seed": 25, # change the seed for different trials
#     "temperature": 0,
#     "config_list": config_list_phi3,
#     "model": "phi3",
#     "timeout": 120,
# }

config_list_phi3=[
    {
        'base_url':"http://0.0.0.0:4000",
        'api_key':'NULL',
        'model': 'phi3', # <-- ADD THIS HERE
        'api_type': 'openai', # <-- ADD THIS (LiteLLM exposes Ollama as an OpenAI-compatible API)
    }
]

phi3_config = {
    "seed": 25, # change the seed for different trials
    "temperature": 0,
    "config_list": config_list_phi3,
    # "model": "phi3", # <-- THIS LINE IS NOW REMOVED
    "timeout": 120,
}


assistant1 = autogen.AssistantAgent(
    name="Assistant1",
    system_message="You are to save to a file.",
    llm_config=phi3_config
)

assistant2 = autogen.AssistantAgent(
    name="Assistant2",
    system_message="You are to save to a file.",
    llm_config=phi3_config
)

# --- User Proxy Agent and Function Registration (from Slide 9) ---
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web", "use_docker": False}, # Disable Docker
    llm_config=phi3_config
)

@user_proxy.register_for_execution()
# @assistant1.register_for_llm(description="Save to file")
# @assistant2.register_for_llm(description="Save to file")
def save_to_file(message: Annotated[str, "The response from the model"]) -> str:
    print("\n--- save_to_file function called ---")
    print(f"Message to save: {message[:100]}...") # Print first 100 chars
    random_number = random.randint(1, 1000)
    file_name = f"saved_file_{random_number}.txt"
    with open(file_name, 'w') as file:
        file.write(message)
    print(f"--- Message saved to {file_name} ---")
    return message # The function needs to return something for the agent to use

group_chat = autogen.GroupChat(agents=[user_proxy, assistant1, assistant2], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=phi3_config)

# --- Initiating the Conversation (from Slide 10) ---
print("\n--- Starting AutoGen Conversation ---")
user_proxy.initiate_chat(
    manager,
    message="Have assistant1 agent give a quote from a famous author, and then when that's done, have assistant2 give another quote from a famous author.",
)
print("\n--- Conversation Finished ---")