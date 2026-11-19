from app.ai.rag.loaders.document_loader import load_documents
from app.ai.rag.schemas import ChunkMetadata


DEFAULT_CHUNK_SIZE = 200
DEFAULT_CHUNK_OVERLAP = 40


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """
    Split text into fixed-size character chunks with overlap.

    This is the baseline chunking strategy.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0."
        )

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    chunks = []

    start = 0

    step = chunk_size - chunk_overlap

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start += step

    return chunks


def create_chunks(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict]:
    """
    Load all knowledge-base documents and convert them
    into metadata-aware chunks.
    """

    documents = load_documents()

    all_chunks = []

    global_chunk_index = 0

    for document in documents:

        document_metadata = document["metadata"]

        for page in document["pages"]:

            text = page["text"]

            page_number = page["page_number"]

            chunks = chunk_text(
                text=text,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            for local_chunk_index, chunk in enumerate(
                chunks
            ):

                chunk_id = (
                    f"{document_metadata.document_id}"
                    f"-chunk-{global_chunk_index}"
                )

                chunk_metadata = ChunkMetadata(
                    document_id=(
                        document_metadata.document_id
                    ),
                    document_name=(
                        document_metadata.document_name
                    ),
                    source_type=(
                        document_metadata.source_type
                    ),
                    source_path=(
                        document_metadata.source_path
                    ),
                    document_type=(
                        document_metadata.document_type
                    ),
                    department=(
                        document_metadata.department
                    ),
                    category=(
                        document_metadata.category
                    ),
                    access_level=(
                        document_metadata.access_level
                    ),
                    version=(
                        document_metadata.version
                    ),
                    source_uri=(
                        document_metadata.source_uri
                    ),
                    license=(
                        document_metadata.license
                    ),
                    section=None,
                    chunk_id=chunk_id,
                    chunk_index=local_chunk_index,
                    page_number=page_number,
                    chunking_strategy=(
                        "fixed_character"
                    ),
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )

                all_chunks.append(
                    {
                        "text": chunk,
                        "metadata": chunk_metadata,
                    }
                )

                global_chunk_index += 1

    return all_chunks


if __name__ == "__main__":

    chunks = create_chunks()
    
    print(chunks[-1])

    print(
        f"Total Chunks: {len(chunks)}"
    )

    for chunk in chunks[:10]:

        print("\n" + "=" * 60)

        print(
            "Chunk ID:",
            chunk["metadata"].chunk_id,
        )

        print(
            "Document:",
            chunk["metadata"].document_name,
        )

        print(
            "Source:",
            chunk["metadata"].source_type,
        )

        print(
            "Page:",
            chunk["metadata"].page_number,
        )

        print(
            "Chunk Index:",
            chunk["metadata"].chunk_index,
        )

        print(
            "Text:",
            chunk["text"],
        )

# from pathlib import Path


# # Folder that holds the knowledge base text files used for chunking.
# KNOWLEDGE_BASE_DIR = Path("app/ai/knowledge_base")


# def load_documents():
#     documents = []

#     # Read every .txt file in the knowledge base and keep its name as the source.
#     for file_path in KNOWLEDGE_BASE_DIR.glob("*.txt"):
#         with open(file_path, "r", encoding="utf-8") as file:
#             content = file.read()

#             documents.append(
#                 {
#                     "source": file_path.name,
#                     "content": content,
#                 }
#             )

#     return documents


# def chunk_text(text, chunk_size=200):
#     chunks = []

#     # Split the text into fixed-size slices so each chunk stays within the limit.
#     for i in range(0, len(text), chunk_size):
#         chunks.append(text[i:i + chunk_size])

#     return chunks


# def create_chunks():
#     documents = load_documents()

#     all_chunks = []

#     # Attach metadata to each chunk so later stages know where it came from.
#     for document in documents:
#         chunks = chunk_text(document["content"])

#         for index, chunk in enumerate(chunks):
#             all_chunks.append(
#                 {
#                     "source": document["source"],
#                     "chunk_id": index,
#                     "text": chunk,
#                 }
#             )

#     return all_chunks


# if __name__ == "__main__":
#     chunks = create_chunks()

#     # Simple CLI output for verifying how many chunks were produced.
#     print(f"Total Chunks: {len(chunks)}")

#     for chunk in chunks:
#         print(chunk)
        
        
# Interview Questions

# What is chunking?
# Chunking is the process of splitting large documents into smaller sections before generating embeddings. It improves retrieval accuracy and reduces the amount of context sent to the LLM.

# Why not embed an entire document?
# Large documents contain multiple topics, making retrieval less precise. Chunking allows retrieval systems to return only the most relevant information.

# How do you choose chunk size?
# Chunk size is chosen based on retrieval quality and context requirements. Very small chunks lose context, while very large chunks reduce retrieval precision.

# What challenges did you face while building a RAG system?
# Initially I used fixed character-based chunking, which split sentences and words. This reduced retrieval quality. I later improved chunking strategies to preserve semantic meaning.


# python -m app.ai.rag.chunk


