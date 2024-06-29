import autogen


def get_code_executor_agent(llm_config):
    executor_user_proxy = autogen.UserProxyAgent(
        name="Executor",
        system_message="Executor. Execute the code written by the engineer and report the result. ",
        code_execution_config={"last_n_messages": 3, "work_dir": "code_dir", "use_docker": False},
        human_input_mode="NEVER",
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").rstrip(),
    )
    return executor_user_proxy
