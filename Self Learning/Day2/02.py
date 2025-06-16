import autogen
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

print("\n🚀 Welcome to the AutoGen Multi-Agent Setup! 🚀")
print("This script guides you through creating your AutoGen agents.")
print("=" * 70)

# =============================================================================
# LESSON 2: Creating the Agents for the Group Chat
# =============================================================================
print("\n📖 LESSON 2: Creating the Agents")
print("-" * 60)
print("We define two AssistantAgents and one UserProxyAgent.")
print("AssistantAgents will generate content, and the UserProxyAgent will act as")
print("an intermediary, potentially executing code or managing the flow.")

# AssistantAgent 1: Designed to provide a quote from a famous author.
assistant1 = autogen.AssistantAgent(
    name="Assistant1",
    system_message="You are a helpful assistant. Provide a quote from a famous author when asked.",
    llm_config=phi3_config # Connects to our configured Phi-3 LLM
)
print("➡️ Created AssistantAgent: Assistant1")

# AssistantAgent 2: Designed to provide another quote from a famous author.
assistant2 = autogen.AssistantAgent(
    name="Assistant2",
    system_message="You are a helpful assistant. Provide another quote from a famous author when asked.",
    llm_config=phi3_config # Connects to our configured Phi-3 LLM
)
print("➡️ Created AssistantAgent: Assistant2")

# UserProxyAgent: Simulates a human user, capable of running code and managing the chat.
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",              # Agent won't ask for human input during the chat
    max_consecutive_auto_reply=10,        # Max auto-replies before potentially stopping
    # Defines when the conversation should terminate (e.g., if a message ends with "TERMINATE")
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    # Configuration for code execution. 'web' as work_dir, Docker disabled.
    code_execution_config={"work_dir": "web", "use_docker": False},
    llm_config=phi3_config # Connects to our configured Phi-3 LLM
)
print("➡️ Created UserProxyAgent: user_proxy")
print("-" * 60)

# You would typically continue by defining functions and the group chat in subsequent steps.