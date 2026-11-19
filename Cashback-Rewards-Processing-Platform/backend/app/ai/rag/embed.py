from sentence_transformers import SentenceTransformer

from app.ai.rag.chunk import create_chunks


EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


class EmbeddingService:
    """
    Service responsible for generating embeddings
    for metadata-aware document chunks.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL_NAME,
    ):
        self.model_name = model_name

        self.model = SentenceTransformer(
            model_name
        )

    def generate_embeddings(
        self,
        chunks: list[dict],
    ):
        """
        Generate embeddings for the provided chunks.

        The order of embeddings is guaranteed to match
        the order of the input chunks.
        """

        if not chunks:
            return []

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        if len(embeddings) != len(chunks):
            raise RuntimeError(
                "Number of embeddings does not match "
                "number of chunks."
            )

        return embeddings

    def embed_knowledge_base(
        self,
    ):
        """
        Load the knowledge base, create chunks,
        and generate embeddings.
        """

        chunks = create_chunks()

        embeddings = self.generate_embeddings(
            chunks
        )

        return chunks, embeddings


if __name__ == "__main__":

    embedding_service = EmbeddingService()

    chunks, embeddings = (
        embedding_service.embed_knowledge_base()
    )

    print(
        "Total Chunks:",
        len(chunks),
    )

    print(
        "Total Embeddings:",
        len(embeddings),
    )

    if embeddings.size > 0:

        print(
            "Embedding Dimension:",
            embeddings.shape[1],
        )

    print("\nFirst Chunk:")

    print(
        chunks[0]["text"]
    )

    print("\nFirst Chunk Metadata:")

    print(
        chunks[0]["metadata"]
    )

    print("\nFirst Embedding:")

    print(
        embeddings[0]
    )


# from sentence_transformers  import SentenceTransformer
# from app.ai.rag.chunk import create_chunks

# # Load the embedding model once at import time so it is reused across calls
# # instead of being reloaded (which is slow) on every embedding request.
# model = SentenceTransformer(
#     "sentence-transformers/all-MiniLM-L6-v2"
# )
# # What Is This Model?

# # It is a lightweight embedding model.

# # Advantages:

# # Fast
# # Free
# # Good semantic search performance
# # Interview friendly

# # Step 3 - Generate Embeddings
# def generate_embeddings():
#     # Build the chunks (text + metadata) from the knowledge base files.
#     chunks = create_chunks()

#     # Pull out just the raw text from each chunk to feed into the model.
#     texts       = [chunk["text"] for chunk in chunks]

#     # Convert every chunk of text into its numeric vector representation.
#     embeddings  = model.encode(texts)

#     # Return both so callers can pair each vector back to its source chunk.
#     return chunks, embeddings

# # What Happens Here?

# # Example:
# # Gold customers receive 10% cashback.

# # becomes:
# # [0.12, -0.45, 0.88, ...]

# # The actual vector length is usually:
# # 384 dimensions  

# # Step 4 - Test

# # Add:

# if __name__ == "__main__":
#     chunks, embeddings = generate_embeddings()
    
#     print("Chunks:", len(chunks))
#     print("Embeddings:", len(embeddings))

#     print("\nFirst Chunk:")
#     print(chunks[0]["text"])
#     # print(type(chunks[0]))
#     # print(chunks[0])

#     print("\nEmbedding Dimension:")
#     print(len(embeddings[0]))
    
#     print("Chunks:", chunks)
#     print("Embeddings:", embeddings)
    


# Interview Questions

# What is an embedding model?
# An embedding model converts text into numerical vectors that capture semantic meaning and relationships between pieces of information.

# Why use embeddings instead of keywords?
# Embeddings enable semantic similarity search, allowing retrieval of relevant information even when the wording differs.

# What does the embedding dimension mean?
# The embedding dimension represents the number of numerical features used to encode semantic information about the text.
# For all-MiniLM-L6-v2:
# 384 dimensions

# Why are similar texts close together?
# Because the embedding model is trained to place semantically related text near each other in vector space.    

# python -m app.ai.rag.embed    



