import autogen


def get_coder_agent(llm_config):
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
    return engineer_agent
