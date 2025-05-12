from autogen import GroupChatManager

def create_chief_of_staff():
    return GroupChatManager(
        name="ChiefOfStaffAgent",
        system_message="You are the orchestrator. Receive user commands, assign tasks to agents, and log behavior.",
        llm_config={"model": "gpt-4"},
    )