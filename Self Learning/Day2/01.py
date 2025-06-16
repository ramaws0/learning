import autogen

print("\n🚀 Welcome to the AutoGen Multi-Agent Setup! 🚀")
print("This script guides you through configuring your LLM for AutoGen.")
print("=" * 70)

# =============================================================================
# LESSON 1: Configuring the Language Model (LLM) for AutoGen
# =============================================================================
print("\n📖 LESSON 1: Configuring the Language Model (LLM)")
print("-" * 60)
print("This section defines how AutoGen connects to your local Phi-3 model via LiteLLM.")
print("We specify the base URL of the LiteLLM proxy and the model name.")
print("Note: We're explicitly telling AutoGen to treat LiteLLM as an 'openai' API type,")
print("and we're also disabling 'tools' at the LLM level to avoid a specific parsing issue.")

# Configuration for connecting to the LiteLLM proxy which serves Ollama's Phi-3
# 'api_key': 'NULL' is used because LiteLLM for Ollama doesn't require a key.
# 'api_type': 'openai' is crucial as LiteLLM exposes Ollama in an OpenAI-compatible format.
# 'model': 'phi3' specifies the model to use from your Ollama instance.
config_list_phi3=[
    {
        'base_url':"http://0.0.0.0:4000",
        'api_key':'NULL',
        'model': 'phi3', # Specifies the model within the config_list entry
        'api_type': 'openai',
    }
]

# Overall LLM configuration for agents
# 'seed': for reproducibility of responses.
# 'temperature': controls creativity (0.0 is deterministic, higher means more creative).
# 'timeout': sets a limit for API calls to prevent hanging.
# 'tools': [] - This is important! It explicitly tells AutoGen that this LLM should NOT
#               attempt to call tools directly, which bypasses a known parsing issue
#               with LiteLLM's Ollama integration for tool calls.
phi3_config = {
    "seed": 25,
    "temperature": 0,
    "config_list": config_list_phi3,
    "timeout": 120,
    "tools": [], # Explicitly disable tools for the LLM
}

print("✅ LLM Configuration defined for Phi-3 via LiteLLM:")
print(phi3_config) # Print the configuration to verify
print("-" * 60)

# You can save this configuration for use in other lessons, or re-define it.
# For simplicity, each subsequent lesson file will redefine this config.