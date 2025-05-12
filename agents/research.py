from autogen import AssistantAgent

def create_research():
    return AssistantAgent(name="ResearchAgent", llm_config={"model": "gpt-4"})