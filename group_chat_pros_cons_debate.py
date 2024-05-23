import autogen


config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["llama3"]
    },
)

# construct another config using our config_list from before,
# the config_list is purely connection, here we define other  parameters we want
# when calling the model, such as temperature and seed value,
llm_config = {"config_list": config_list, "seed": 42, "temperature": 0.0}

pros_advocate_prompt = "In charge of arguing for a choice or option. Will follow directions from the debate_moderator and will suggest a pro when asked or will try and rebut an accusation that the option is not to be selected. Only suggest a single pro when prompted, not a list, this allows for fair and even discussion."
pros_advocate = autogen.AssistantAgent(
    name="pros_advocate",
    system_message=pros_advocate_prompt,
    llm_config=llm_config,
)

cons_advocate_prompt = "In charge of arguing against a choice or option. Will follow directions from the debate_moderator and will suggest a con when asked or will try and rebut an accusation that the option is to be selected. Only suggest a single con when prompted, not a list, this allows for fair and even discussion."
cons_advocate = autogen.AssistantAgent(
    name="cons_advocate",
    system_message=cons_advocate_prompt,
    llm_config=llm_config,
)

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

# also note, we could also just pass in a reference to a function, if you prefer not to use lambda
# the process would be the same
user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    system_message="A human admin.",
    human_input_mode="NEVER", # trust the bots completely, what could go wrong?
    is_termination_msg=lambda x: "CONVERSATION_TERMINATE" in x.get("content", "").rstrip(),
    code_execution_config=False,
)

# define a group chat with our agents and user proxy, set an empty list for messages for a fresh chat
# and define the maximum number of rounds of conversation
groupchat = autogen.GroupChat(agents=[user_proxy, debate_moderator, pros_advocate, cons_advocate], messages=[], max_round=50)
# now define a group chat manager by passing the group chat it will manage and the llm that
# will power it.
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="Should I order takeout tonight?")