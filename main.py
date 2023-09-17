import os
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from jira_agent import JiraSearchTool

model = ChatOpenAI(model="gpt-3.5-turbo-0613")
tools = [JiraSearchTool()]
open_ai_agent = initialize_agent(tools,
                                 model,
                                 agent=AgentType.OPENAI_FUNCTIONS,
                                 verbose=True)

while True:
    try:
        question = input("Question: ")
        tool_result = open_ai_agent.run(question)
        print("Answer: ", tool_result)
    except KeyboardInterrupt:
        break

# template = """
# You are an AI assistant specializing in creating Jira tickets. 
# You can open a ticket related to a specific project,
# issue type, summary, description, and priority. 
# A ticket can be opened within a particular project and issue type. 
# If the ticket pertains to IT production or the system engineers team, use the project key "PROD" and issue type key "Requests". 
# If the ticket concerns office IT, use the project key "OFFICE" and issue type key "Requests". 
# Based on this information, I need to open a ticket for {input}."""

# _prompt = PromptTemplate(
#     input_variables=["input"],
#     template=template
# )
# prompt = _prompt.format(
#     input="I need a new Elasticsearch cluster for my new mobile service")

# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# agent.run(prompt)
