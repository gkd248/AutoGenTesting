import autogen
import agents.pros_debate_advocate as pros_debater
import agents.cons_debate_advocate as cons_debater
import agents.debate_moderator as moderator
import agents.user_proxy as user


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

pros_advocate = pros_debater.get_pros_debate_advocate(llm_config)
cons_advocate = cons_debater.get_cons_debate_advocate(llm_config)

debate_moderator = moderator.get_debate_moderator(llm_config)

user_proxy = user.get_user_proxy(llm_config)

# define a group chat with our agents and user proxy, set an empty list for messages for a fresh chat
# and define the maximum number of rounds of conversation
groupchat = autogen.GroupChat(agents=[user_proxy, debate_moderator, pros_advocate, cons_advocate], messages=[], max_round=50)
# now define a group chat manager by passing the group chat it will manage and the llm that
# will power it.
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message="Should I order takeout tonight?")