from autogen import AssistantAgent

def create_writing():
    return AssistantAgent(name="WritingAgent", llm_config={"model": "gpt-4", "context_docs": ["docs/Q2_update.pdf"]})