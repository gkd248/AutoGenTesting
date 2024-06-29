import autogen

config_list = autogen.config_list_from_json(
    "../OAI_CONFIG_LIST",
    filter_dict={
        "model": ["llama3"]
    },
)

# construct another config using our config_list from before,
# the config_list is purely connection, here we define other  parameters we want
# when calling the model, such as temperature and seed value,
llm_config = {"config_list": config_list, "seed": 42, "temperature": 0.0}