from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from backend.llm.client import LLMFactory
from backend.llm.prompts import CHUNK_EXTRACTION_PROMPT, REDUCE_PROMPT

_map_prompt = ChatPromptTemplate.from_messages([
    ("system", CHUNK_EXTRACTION_PROMPT),
    ("human", "{context}"),
])

_reduce_prompt = ChatPromptTemplate.from_messages([
    ("system", REDUCE_PROMPT),
    ("human", "{context}"),
])

_llm = LLMFactory.create()


async def analyze_chunks(chunks: list[str]) -> str:
    """
    Args:
        chunks: Text chunks produced by `pdf_service.load_and_split`.

    Returns:
        A single coherent summary string.
    """
    # Map phase (parallel)
    inputs = [{"context": chunk} for chunk in chunks]

    map_chain = _map_prompt | _llm | StrOutputParser()
    reduce_chain = _reduce_prompt | _llm | StrOutputParser()

    map_results: list[str] = await map_chain.abatch(
        inputs,
        config=RunnableConfig(max_concurrency=5),  # stay within typical API rate limits
    )

    # Reduce phase
    combined = "\n\n---\n\n".join(map_results)
    return await reduce_chain.ainvoke({"context": combined})
