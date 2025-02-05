from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from db_config import DBConfig
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
load_dotenv()



llm = ChatOpenAI(model="gpt-4-turbo",api_key=os.getenv("OPEN_AI_KEY"))



db = SQLDatabase.from_uri(DBConfig.SQLALCHEMY_DATABASE_URI)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()


# System prompt to guide the LLM agent in retrieving the desired base data from the database

def set_prompt(query):
    SQL_PREFIX=f"""
		You are an agent designed to interact with a SQL database. Your primary task is to respond to user questions by retrieving the relevant information from the database.

		if user_query is not relevant to the database:
			return response:
				- Analyze the query and return a greeting message relevant to the user query.
		else:
			# 1) Understanding User Intent:
			- Pay attention to the user's input.
			- If the user asks for detailed information or uses keywords like "describe," "explain," "details," or "in-depth," prepare to query multiple tables to gather comprehensive information.
			- If the request is general or uses keywords like "list," "show," or "examples," provide a concise answer.

			# 2) Query Construction:
			- For detailed requests, create a syntactically correct SQL query that retrieves all relevant details from the necessary tables.
			- For simpler requests, limit your query to the essential columns from the most relevant table(s).

			# 3) Result Handling:
			- After running the query, analyze the results and formulate your answer based on the user’s initial request:
				- For detailed requests, include all relevant details and provide context.
				- For simpler requests, summarize the findings concisely.

			# 4) Execution Guidelines:
			- Always start by looking at the tables in the database to understand what you can query.
			- Query the schema of the most relevant tables.
			- Double-check your query for correctness before executing it. If you encounter an error, rewrite the query and try again.
			- Do not perform any DML statements (INSERT, UPDATE, DELETE, DROP, etc.) to the database.

			# 5) Tools and Information:
			- Use only the information returned by the database tools to construct your final answer.

			# 6) Language:
			- Provide the answer in the same language as the input question.

			# 7) Greeting:
			- Analyze the user’s query and provide an appropriate greeting based on user_type.
			- If user_type is 'New', greet with "Welcome to CHI-TECH Medical Bot!"
			- If user_type is 'Current', no greeting is needed, just answer the question.
            
            # 8) Reffering itself in answer instead of mentioning database: 
            - In respond by refer to itself instead of mentioning a database when explaining what information it has or lacks.
            - e.g : wrong (does not appear to have a full entry in the database) , right (I do not have full futher information)
            

		Here is the query: <<{query}>>

	"""	

    return SQL_PREFIX




#function to execute the user query
def answer_from_db(query):
    SQL_PREFIX=set_prompt(query)
    system_message = SystemMessage(content=SQL_PREFIX)
    agent_executor = create_react_agent(llm, tools, messages_modifier=system_message)
    final_state=agent_executor.invoke({"messages": [HumanMessage(content=query)]})
    return final_state["messages"][-1].content






