from autogen import GroupChat
from agents.chief_of_staff import create_chief_of_staff
from agents.analyst import create_analyst
from agents.comms import create_comms
from agents.writing import create_writing
from agents.research import create_research

if __name__ == "__main__":
    chief = create_chief_of_staff()
    analyst = create_analyst()
    comms = create_comms()
    writing = create_writing()
    research = create_research()

    group = GroupChat(
        agents=[chief, analyst, comms, writing, research],
        messages=[],
        max_round=10
    )

    group.run("Prepare weekly team report using research and draft in comms tone")