import autogen


def get_cons_debate_advocate(llm_config):
    cons_advocate_prompt = "In charge of arguing against a choice or option. Will follow directions from the debate_moderator and will suggest a con when asked or will try and rebut an accusation that the option is to be selected. Only suggest a single con when prompted, not a list, this allows for fair and even discussion."
    cons_advocate = autogen.AssistantAgent(
        name="cons_advocate",
        system_message=cons_advocate_prompt,
        llm_config=llm_config,
    )
    return cons_advocate
