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

print("\n🚀 Welcome to the AutoGen Multi-Agent Setup! 🚀")
print("This script guides you through registering custom functions (tools).")
print("=" * 70)

# =============================================================================
# LESSON 3: Registering Custom Functions (Tools)
# =============================================================================
print("\n📖 LESSON 3: Registering Custom Functions (Tools)")
print("-" * 60)
print("We define a 'save_to_file' function that the user_proxy can execute.")
print("Note: Assistants will not directly call this tool via LLM generation due to prior issues.")
print("The user_proxy will decide when to execute this based on the conversation flow.")

@user_proxy.register_for_execution() # Only the user_proxy can directly execute this function
def save_to_file(message: Annotated[str, "The content to be saved to a file."]) -> str:
    """
    Saves the given message content to a uniquely named text file.
    """
    print("\n--- save_to_file function called ---")
    # Truncate message for printing to keep console clean
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

print("✅ 'save_to_file' function registered for execution by user_proxy.")
print("-" * 60)

# You would typically continue by setting up the group chat and initiating conversation.
