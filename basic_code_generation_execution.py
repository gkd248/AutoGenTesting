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
Only output runnable code.
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
    system_message="Executor. Execute the code written by the engineer and report the result. ",
    code_execution_config={"last_n_messages": 3, "work_dir": "code_dir", "use_docker": False},
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").rstrip(),
)

engineer_agent.initiate_chat(executor_user_proxy, message="Hello! I'm an AI assistant designed to write code. Please tell me what code I should write.")
