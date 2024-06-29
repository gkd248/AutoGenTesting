import autogen


def get_user_proxy(llm_config):
    # also note, we could also just pass in a reference to a function, if you prefer not to use lambda
    # the process would be the same
    user_proxy = autogen.UserProxyAgent(
        name="User_Proxy",
        system_message="A human admin.",
        human_input_mode="NEVER",  # trust the bots completely, what could go wrong?
        is_termination_msg=lambda x: "CONVERSATION_TERMINATE" in x.get("content", "").rstrip(),
        code_execution_config=False,
    )
    return user_proxy
