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

engineer_agent_prompt = """You are an engineer able to write python code to solve a problem. 
The user will give you a problem to solve and you will need to write code to get the answer. 
The user will run the code and report any problems or errors, you will then create an updated version of your code to address these as they arise. 
If the code executes successfully and returns the needed values output TERMINATE."""
engineer_agent = autogen.AssistantAgent(
    name="engineer_agent_prompt",
    system_message=engineer_agent_prompt,
    llm_config=llm_config,
)

# to dig a bit more into the code_execution_config, when this agent is prompted it will
# look at the last_n_messages in the conversation, if it detects a code block in those messages
# it will attempt to execute them. The work_dir is a directory where it will store code as it runs it,
# and the use_docker is pretty self explanatory, set to false it won't run docker,
# however if we want to use docker we instead set this value as a string that is the name of the
# container we want to run the code in.

executor_user_proxy = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 3, "work_dir": "code_dir", "use_docker": False},
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").rstrip(),
)

# our task is pretty straightforward, go to this url and extract some data
# we also tell the agent we have some common packages installed so it doesn't waste time
# trying to install them, sometimes the agents will insist on creating bash scripts to install
# everything without verifying if the environment has the packages first, so it's useful to let
# the agent know what it does or does not have at their disposal
initial_message="""Provided url: https://medium.com/@coldstart_coder/basics-of-the-walrus-operator-in-python-a9b18ca1469c

The provided url is for a medium article. I need you to write a script that will fetch the page, parse the html and print out the title of the article, the author and when it was published. 

I have BeautifulSoup and requests installed so I should be good to go there. 
"""
# start the conversation!
executor_user_proxy.initiate_chat(engineer_agent, message=initial_message)