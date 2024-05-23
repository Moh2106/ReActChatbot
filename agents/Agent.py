from llama_index.core.agent import ReActAgent
from tools import ProductTools, Setings
from llama_index.core import PromptTemplate


class Agent():

    def __init__(self):
        self.llm = Setings.get_llm()

    def agent_prompt(self):
        react_system_header_str = """\

                    You are an AI assistant who is responsible for answering customer questions.
                     You have to be kind and jovial. 

                    ## Tools
                    You have access to a wide variety of tools. You are responsible for using
                    the tools in any sequence you deem appropriate to complete the task at hand.
                    This may require breaking the task into subtasks and using different tools
                    to complete each subtask.
                    ```

                    You should keep repeating the above format until you have enough information
                    to answer the question without using any more tools. At that point, you MUST respond
                    in the one of the following two formats:
                    
                    ```
                    Thought: Hello.
                    Answer: Hello, what can I do for you?
                    ```
                    
                    ```
                    Thought: thank you for your service.
                    Answer: We are happy to help
                    ```

                    ```
                    Thought: I can answer without using any more tools.
                    Answer: [your answer here]
                    ```

                    ```
                    Thought: I cannot answer the question with the provided tools.
                    Answer: Sorry, I cannot answer your query.
                    ```

                    ## Additional Rules
                    - The answer MUST contain a sequence of bullet points that explain how you arrived at the answer. This can include aspects of the previous conversation history.
                    - You MUST obey the function signature of each tool. Do NOT pass in no arguments if the function expects arguments.

                    ## Current Conversation
                    Below is the current conversation consisting of interleaving human and assistant messages.

                    """

        react_system_prompt = PromptTemplate(react_system_header_str)

        return react_system_prompt

    def initialize_agents(self):

        # product_tool = ProductTools.ProductTools()
        product_vector_tool = ProductTools.ProductTools().product_tools()
        complaint_vector_tool = ProductTools.ProductTools().complaint_tool_query()


        # initialize ReAct agent
        agent = ReActAgent.from_tools([product_vector_tool, complaint_vector_tool],
                                      llm=self.llm, chat_mode="react")

        #agent.update_prompts()
        return agent
