from typing import Annotated
import autogen
import random
import os

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

print("\n🚀 Welcome to the AutoGen Multi-Agent Setup! 🚀")
print("This script guides you through setting up the group chat and manager.")
print("=" * 70)

# =============================================================================
# LESSON 4: Setting up the Group Chat and Manager
# =============================================================================
print("\n📖 LESSON 4: Setting up the Group Chat and Manager")
print("-" * 60)
print("The GroupChat defines the participants, and the GroupChatManager orchestrates")
print("the conversation among them.")

# Create a GroupChat with the agents.
# 'messages': start with an empty list.
# 'max_round': limits the number of turns in the conversation to prevent infinite loops.
group_chat = autogen.GroupChat(
    agents=[user_proxy, assistant1, assistant2],
    messages=[],
    max_round=12
)
print("➡️ GroupChat defined with user_proxy, Assistant1, and Assistant2.")

# Create a GroupChatManager to orchestrate the conversation.
manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config=phi3_config # Manager also needs LLM access for its decisions
)
print("➡️ GroupChatManager created to orchestrate the conversation.")
print("-" * 60)

# You would typically continue by initiating the conversation in the next step.
