from functools import cache

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from backend.llm.factory import LLMFactory
from backend.llm.prompts import CHUNK_EXTRACTION_PROMPT, REDUCE_PROMPT

# Prompts are pure data — safe to build at import time
_map_prompt = ChatPromptTemplate.from_messages([
    ("system", CHUNK_EXTRACTION_PROMPT),
    ("human", "{context}"),
])

_reduce_prompt = ChatPromptTemplate.from_messages([
    ("system", REDUCE_PROMPT),
    ("human", "{context}"),
])


@cache
def _get_chains() -> tuple:
    """Build and cache the LLM chains on first request.

    """
    llm = LLMFactory.create()
    return _map_prompt | llm | StrOutputParser(), _reduce_prompt | llm | StrOutputParser()


async def analyze_chunks(chunks: list[str]) -> str:
    """
    Args:
        chunks: Text chunks produced by `pdf_service.load_and_split`.

    Returns:
        A single coherent summary string.
    """
    map_chain, reduce_chain = _get_chains()

    # Map phase (parallel)
    map_results: list[str] = await map_chain.abatch(
        [{"context": chunk} for chunk in chunks],
        config=RunnableConfig(max_concurrency=5),
    )

    # Reduce phase
    combined = "\n\n---\n\n".join(map_results)
    return await reduce_chain.ainvoke({"context": combined})
