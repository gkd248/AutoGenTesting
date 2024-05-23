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

# next we define the prompt for our agent, basically the instructions for our agent,
# this will also help AutoGen know when to engage this agent in conversation by looking at
# it's definition here
pros_cons_agent_instruction_prompt = "This agent will provide a list of pros and cons for a given suggestion. If there is no indication of how many pros and cons make 3 each. If there is no suggestion introduce yourself and prompt for one."

# next we use AssistantAgent to actually make our agent,
# we give it a name to identify itself from other agents that is unique to itself,
# the system_message which acts as our agent prompt, and the llm_config defining
# where and how to call the llm that powers it
pros_cons_agent = autogen.AssistantAgent(
    name="pros_cons_agent",
    system_message=pros_cons_agent_instruction_prompt,
    llm_config=llm_config,
)

#If you want human in the loop instead of bots talking to each other
user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    system_message="A human admin.",
    human_input_mode="ALWAYS",
    code_execution_config=False,
)

topic_suggester_prompt = "You will suggest 3 topics for analysis. You will output each 1 at a time and allow for user feedback for each. Once 3 have been submitted you will then output TERMINATE."
topic_suggester=  autogen.AssistantAgent(
    name="topic_suggester",
    system_message=topic_suggester_prompt,
    llm_config=llm_config,
)

# have our pros cons agent initiate a chat with the user and give the initial message to get the ball rolling.
pros_cons_agent.initiate_chat(topic_suggester, message="Hello! I'm an AI assistant designed to provide a balanced view on any topic by listing pros and cons. Please provide a suggestion or a topic you'd like me to analyze.")

