#!/home/biswash/miniconda3/envs/autogen_env/bin/python

from autogen import ConversableAgent, GroupChat, GroupChatManager

# Your Gemini API key
API_KEY = "YOurkey"

# Common LLM config
llm_config = {
    "config_list": [{
        "model": "gemini-1.5-flash",
        "api_key": API_KEY,
        "api_type": "google"
    }],
    "temperature": 0.7
}

# Create different specialized agents
coder = ConversableAgent(
    name="Coder",
    system_message="You are an expert Python programmer. Focus on writing clean, efficient code.",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

reviewer = ConversableAgent(
    name="Reviewer",
    system_message="You are a code reviewer. Analyze code for bugs, improvements, and best practices.",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

explainer = ConversableAgent(
    name="Explainer",
    system_message="You explain code in simple terms for beginners to understand.",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# Create a group chat
group_chat = GroupChat(
    agents=[coder, reviewer, explainer],
    messages=[],
    max_round=6
)

# Create a manager to orchestrate the conversation
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config
)

# Start a collaborative task
print("🚀 Starting multi-agent collaboration...")
print("Task: Create and review a Python function for fibonacci sequence")
print("=" * 60)

# Initiate the conversation
coder.initiate_chat(
    manager,
    message="Please create a Python function to calculate the nth Fibonacci number. Make it efficient and well-documented."
)