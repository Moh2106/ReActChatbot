from llama_index.core.agent import ReActAgent
from tools import ProductTools, Setings
from llama_index.core import PromptTemplate


class Agent():

    def __init__(self):
        self.llm = Setings.get_llm()

    def initialize_agents(self):

        # product_tool = ProductTools.ProductTools()
        product_vector_tool = ProductTools.ProductTools().product_tools()
        complaint_vector_tool = ProductTools.ProductTools().complaint_tool_query()


        # initialize ReAct agent
        agent = ReActAgent.from_tools([product_vector_tool, complaint_vector_tool],
                                      llm=self.llm, chat_mode="react", verbose=True)

        #agent.update_prompts()
        return agent
