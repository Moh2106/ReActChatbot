from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.core import SummaryIndex, VectorStoreIndex

from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector



def get_router_query_engine(file_path: str, llm=None, embed_model=None):
    """Get router query engine."""
    llm = llm
    embed_model = embed_model

    # load documents
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    # splitter documents
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    # Vectorize documents
    vector_index = VectorStoreIndex(nodes, embed_model=embed_model)

    vector_query_engine = vector_index.as_query_engine(llm=llm)

    return vector_query_engine
