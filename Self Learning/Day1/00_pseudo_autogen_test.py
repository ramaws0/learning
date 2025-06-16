# Test AutoGen installation
try:
    import autogen
    print("✅ AutoGen imported successfully!")
    print(f"AutoGen version: {autogen.__version__}")
    
    from autogen import ConversableAgent
    print("✅ ConversableAgent imported successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    
# Simple test to create an agent
try:
    agent = ConversableAgent(
        name="test_agent",
        llm_config=False,  # No LLM for this test
        human_input_mode="NEVER"
    )
    print("✅ Agent created successfully!")
    print(f"Agent name: {agent.name}")
    
except Exception as e:
    print(f"❌ Error creating agent: {e}")
