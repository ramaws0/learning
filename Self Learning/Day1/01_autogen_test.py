#!/home/biswash/miniconda3/envs/autogen_env/bin/python

# Fix 1: Use correct import
from autogen import ConversableAgent  # Correct import

# Fix 2: Proper Gemini configuration
API_KEY = "YOurkey"

# Fix 3: Configure for Gemini properly
agent = ConversableAgent(
    name="test_agent",
    llm_config={
        "config_list": [{
            "model": "gemini-1.5-flash",  # Specify exact Gemini model
            "api_key": API_KEY,
            "api_type": "google",  # Specify Google API
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
        }]
    },
    human_input_mode="NEVER"  # Prevent hanging on input
)

# Test the agent
messages = [{"role": "user", "content": "Explain AutoGen in 1 sentence."}]

try:
    reply = agent.generate_reply(messages=messages)
    print("✅ Success!")
    print(f"Reply: {reply}")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Let's try a simpler approach...")