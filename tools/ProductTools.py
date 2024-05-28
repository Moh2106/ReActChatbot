from . import RagTools, Setings
from llama_index.core import Settings
from llama_index.core.tools import QueryEngineTool
from llama_index.core import PromptTemplate
from llama_index.core.tools import FunctionTool


class ProductTools:
    path = "data/marba_shop.pdf"

    def __init__(self):
        self.llm = Setings.get_llm()
        self.embed_model = Setings.get_embeddings()
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model

    def product_tools(self):
        product_query_engine = RagTools.get_router_query_engine(file_path=self.path,
                                                                llm=self.llm, embed_model=self.embed_model)

        product_vector_tool = QueryEngineTool.from_defaults(
            query_engine=product_query_engine,
            description=(
                "Useful for retrieving specific information about products.\n"
                "Do not invent information that does not exist in this document.\n"
                "Gives clear and precise answers."
            ),
        )

        return product_vector_tool

    def complaint_tools(self):

        template = (
            "You are an assistant for customer’s complaint about product.\n"
            "First, reassure the customer about the product.\n"
            "Then ask the customer for their name, their email, their number and the cause of their complaint.\n"
            "Finally, summarize the complaint and send them to the customer."
        )
        qa_template = PromptTemplate(template=template)

        # Convert to message prompts (for chat API)
        messages = qa_template.format_messages()

        return messages

    def complaint_tool_query(self):

        tool = FunctionTool.from_defaults(
            fn=self.complaint_tools,
            description="Useful for when you want to answer queries about complaints."
            # async_fn=aget_weather,  # optional!
        )

        return tool
