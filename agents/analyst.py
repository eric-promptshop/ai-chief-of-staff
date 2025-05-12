from autogen import AssistantAgent

def create_analyst():
    return AssistantAgent(name="AnalystAgent", llm_config={"model": "gpt-4"})