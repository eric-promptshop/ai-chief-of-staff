from autogen import AssistantAgent

def create_comms():
    return AssistantAgent(name="CommsAgent", llm_config={"model": "gpt-4"})