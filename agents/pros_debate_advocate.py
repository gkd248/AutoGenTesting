import autogen


def get_pros_debate_advocate(llm_config):
    pros_advocate_prompt = "In charge of arguing for a choice or option. Will follow directions from the debate_moderator and will suggest a pro when asked or will try and rebut an accusation that the option is not to be selected. Only suggest a single pro when prompted, not a list, this allows for fair and even discussion."
    pros_advocate = autogen.AssistantAgent(
        name="pros_advocate",
        system_message=pros_advocate_prompt,
        llm_config=llm_config,
    )
    return pros_advocate
