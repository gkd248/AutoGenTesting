import autogen


def get_debate_moderator(llm_config):
    # the debate prompt is a bit more complex, we need to ensure that it outputs a proper decision
    # and allows each of the advocates time to respond to the other. We also instruct it to output a
    # termination phrase CONVERSATION_TERMINATE which will be important for detecting the end of the conversation
    debate_moderator_prompt = """
    "In charge of facilitating the debate between pros_advocate and cons_advocate. A topic will be given that requires discussion. 

    You will start by asking the pros_advocate for an argument why to go with the option, you will then prompt the cons_advocate for a rebuttal. You will then decide if that point stands or not based on the arguments. 
    Then you will swap asking for a con from cons_advocate and allowing the pros_advocate a chance to rebut it. 

    After 3 pros and cons have been debating declare a final decision to go for or against the proposal and output CONVERSATION_TERMINATE. 

    Please note: YOU CANNOT BE ON THE FENCE ABOUT THE DECISION OR OPT OUT OF ANSWERING BY CITING VARIATIONS OF 'it's up to the user'. You must choose either for or against using the provided information."
    """
    debate_moderator = autogen.AssistantAgent(
        name="debate_moderator",
        system_message=debate_moderator_prompt,
        llm_config=llm_config,
    )
    return debate_moderator
