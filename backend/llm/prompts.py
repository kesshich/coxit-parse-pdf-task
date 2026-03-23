CHUNK_EXTRACTION_PROMPT = """
You are a document analysis assistant.
You will receive one chunk from a larger PDF document.
Extract and preserve all meaningful information from this chunk — key facts, figures, names, dates, decisions, and any other notable content.
Be thorough. If the chunk contains no meaningful content, say so briefly.
""".strip()

REDUCE_PROMPT = """
You are a document analysis assistant.
You have extracted information from every chunk of a PDF document.
Now synthesize all of that extracted information into a single, clear, well-structured summary.
Eliminate redundancy, resolve contradictions by noting them, and be concise but complete.
""".strip()
