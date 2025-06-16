from typing import Annotated
import autogen
import random
import os
import time

# Re-defining LLM config for self-containment for this lesson
config_list_phi3=[
    {
        'base_url':"http://0.0.0.0:4000",
        'api_key':'NULL',
        'model': 'phi3',
        'api_type': 'openai',
    }
]

phi3_config = {
    "seed": 25,
    "temperature": 0,
    "config_list": config_list_phi3,
    "timeout": 120,
    "tools": [],
}

# Re-creating agents for self-containment for this lesson
assistant1 = autogen.AssistantAgent(
    name="Assistant1",
    system_message="You are a helpful assistant. Provide a quote from a famous author when asked.",
    llm_config=phi3_config
)
assistant2 = autogen.AssistantAgent(
    name="Assistant2",
    system_message="You are a helpful assistant. Provide another quote from a famous author when asked.",
    llm_config=phi3_config
)
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web", "use_docker": False},
    llm_config=phi3_config
)

# Re-defining save_to_file for self-containment for this lesson
@user_proxy.register_for_execution()
def save_to_file(message: Annotated[str, "The content to be saved to a file."]) -> str:
    print("\n--- save_to_file function called ---")
    print(f"Attempting to save message (first 100 chars): {message[:100]}...")
    random_number = random.randint(1, 1000)
    file_name = f"saved_file_{random_number}.txt"
    try:
        with open(file_name, 'w') as file:
            file.write(message)
        print(f"--- Message successfully saved to {file_name} ---")
        return f"Successfully saved content to {file_name}."
    except Exception as e:
        print(f"--- ERROR saving file: {e} ---")
        return f"Failed to save content: {e}"

# Re-creating group_chat and manager for self-containment for this lesson
group_chat = autogen.GroupChat(
    agents=[user_proxy, assistant1, assistant2],
    messages=[],
    max_round=12
)
manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config=phi3_config
)

print("\n🚀 Welcome to the AutoGen Multi-Agent Setup! 🚀")
print("This script guides you through initiating the agent conversation.")
print("=" * 70)

# =============================================================================
# LESSON 5: Initiating the Conversation
# =============================================================================
print("\n📖 LESSON 5: Initiating the Conversation")
print("-" * 60)
print("This is where the magic happens! The user_proxy starts the chat with an initial prompt.")
print("The agents will then interact to fulfill the request.")

# Start the multi-agent conversation
user_proxy.initiate_chat(
    manager,
    message="Assistant1, please provide a quote from a famous author. Assistant2, once Assistant1 is done, please provide a different quote from a famous author. Once both quotes are provided, user_proxy, please collect all quotes and save them to a file."
)

print("\n--- AutoGen Conversation Finished ---")
print("=" * 70)
print("Check your project directory for 'saved_file_XXX.txt' files!")
