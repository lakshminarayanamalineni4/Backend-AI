from functools import lru_cache
from typing import Any

from app.ai.rag.embed import EmbeddingService
from app.ai.rag.vector_store import FAISSVectorStore


# Number of FAISS candidates retrieved for every
# requested result when metadata filtering is enabled.
#
# Example:
#
# top_k = 3
# candidate_k = max(3 * 5, 20)
#            = 20
#
# We retrieve more candidates than we finally return
# because some candidates may be removed by metadata filters.
DEFAULT_CANDIDATE_MULTIPLIER = 5

MINIMUM_CANDIDATE_K = 20


class DocumentSearchService:
    """
    Service responsible for semantic document retrieval.

    The retrieval pipeline is:

    1. Receive the user's natural-language query.

    2. Generate an embedding for the query using
       the same Sentence Transformer used during
       document indexing.

    3. Search the persisted FAISS vector index.

    4. Retrieve a larger candidate pool.

    5. Apply optional metadata filters.

    6. Return the requested top-K matching results.

    The service uses:

    - Sentence Transformer
      for semantic query embeddings.

    - FAISS
      for dense vector similarity search.

    - Persisted metadata
      to identify the source document and chunk.

    - Application-level metadata filtering
      to restrict retrieval based on structured metadata.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: FAISSVectorStore,
    ):
        """
        Initialize the document search service.

        Parameters
        ----------
        embedding_service:
            Service responsible for generating
            embeddings for user queries.

        vector_store:
            Persistent FAISS vector store used
            for similarity search.
        """

        self.embedding_service = (
            embedding_service
        )

        self.vector_store = vector_store

    @staticmethod
    def _metadata_matches(
        metadata: Any,
        *,
        department: str | None = None,
        category: str | None = None,
        access_level: str | None = None,
        document_type: str | None = None,
    ) -> bool:
        """
        Check whether a metadata record satisfies
        all requested metadata filters.

        All provided filters are combined using
        AND logic.

        Example:

            department="Finance"
            category="Rewards"

        means that a document must satisfy:

            department == "Finance"
            AND
            category == "Rewards"

        Parameters
        ----------
        metadata:
            Metadata object associated with a retrieved chunk.

        department:
            Optional department filter.

        category:
            Optional category filter.

        access_level:
            Optional access-level filter.

        document_type:
            Optional document-type filter.

        Returns
        -------
        bool
            True if the metadata satisfies all
            provided filters.
        """

        # If a department filter was provided,
        # the metadata must contain the same department.
        if department is not None:

            if metadata.department != department:
                return False

        # If a category filter was provided,
        # the metadata must contain the same category.
        if category is not None:

            if metadata.category != category:
                return False

        # If an access-level filter was provided,
        # the metadata must contain the same access level.
        if access_level is not None:

            if metadata.access_level != access_level:
                return False

        # If a document-type filter was provided,
        # the metadata must contain the same document type.
        if document_type is not None:

            if metadata.document_type != document_type:
                return False

        # If none of the filters rejected the document,
        # the metadata matches successfully.
        return True

    @staticmethod
    def _calculate_candidate_k(
        top_k: int,
    ) -> int:
        """
        Calculate the number of FAISS candidates
        that should be retrieved before filtering.

        We intentionally retrieve more results than
        the final requested top-K.

        This prevents metadata filtering from leaving
        us with too few results.

        Example:

            top_k = 3

            candidate_k =
                max(
                    3 * 5,
                    20,
                )

            candidate_k = 20
        """

        return max(
            top_k
            * DEFAULT_CANDIDATE_MULTIPLIER,
            MINIMUM_CANDIDATE_K,
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        *,
        department: str | None = None,
        category: str | None = None,
        access_level: str | None = None,
        document_type: str | None = None,
    ) -> list[dict]:
        """
        Search the knowledge base for relevant chunks.

        The search performs:

        Query
            ↓
        Query Embedding
            ↓
        FAISS Candidate Search
            ↓
        Metadata Filtering
            ↓
        Top-K Results

        Parameters
        ----------
        query:
            User's natural-language question.

        top_k:
            Maximum number of relevant chunks to return.

        department:
            Optional department metadata filter.

        category:
            Optional category metadata filter.

        access_level:
            Optional access-level metadata filter.

        document_type:
            Optional document-type metadata filter.

        Returns
        -------
        list[dict]
            Retrieved chunks with metadata and
            similarity scores.
        """

        # ---------------------------------------------------------
        # 1. Validate the query
        # ---------------------------------------------------------

        if not query or not query.strip():

            raise ValueError(
                "Search query cannot be empty."
            )

        # ---------------------------------------------------------
        # 2. Validate top_k
        # ---------------------------------------------------------

        if top_k <= 0:

            raise ValueError(
                "top_k must be greater than 0."
            )

        # ---------------------------------------------------------
        # 3. Generate the query embedding
        # ---------------------------------------------------------

        # The query must be embedded using the same
        # embedding model used for document chunks.
        #
        # This ensures that both document vectors
        # and query vectors exist in the same
        # 384-dimensional vector space.

        query_embedding = (
            self.embedding_service.model.encode(
                [query],
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
        )

        # ---------------------------------------------------------
        # 4. Calculate candidate search size
        # ---------------------------------------------------------

        # We retrieve more results than the final top_k
        # because metadata filtering may remove some
        # of the retrieved candidates.

        candidate_k = (
            self._calculate_candidate_k(
                top_k
            )
        )

        # ---------------------------------------------------------
        # 5. Search the persistent FAISS index
        # ---------------------------------------------------------

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=candidate_k,
        )

        # ---------------------------------------------------------
        # 6. Apply metadata filtering
        # ---------------------------------------------------------

        filtered_results = []

        for result in results:

            metadata = result["metadata"]

            # Check whether the retrieved document
            # satisfies all requested metadata filters.
            if not self._metadata_matches(
                metadata,
                department=department,
                category=category,
                access_level=access_level,
                document_type=document_type,
            ):
                continue

            # The document passed all filters.
            filtered_results.append(
                result
            )

            # Stop once we have the requested
            # number of results.
            if len(filtered_results) >= top_k:

                break

        # ---------------------------------------------------------
        # 7. Return the final top-K results
        # ---------------------------------------------------------

        return filtered_results


@lru_cache(maxsize=1)
def get_search_service() -> DocumentSearchService:
    """
    Create and cache a reusable search service.

    The embedding model is expensive to load,
    so we should not recreate it for every request.

    The FAISS index is also loaded once and reused.

    This function is intentionally cached so that
    the application process keeps a single initialized
    retrieval service.

    Returns
    -------
    DocumentSearchService
        Reusable document search service.
    """

    # Create the embedding service.

    embedding_service = EmbeddingService()

    # Create the persistent FAISS vector store.

    vector_store = FAISSVectorStore()

    # Load the persisted FAISS index
    # and associated metadata.

    vector_store.load()

    # Return the initialized search service.

    return DocumentSearchService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )


def search_documents(
    query: str,
    top_k: int = 5,
    *,
    department: str | None = None,
    category: str | None = None,
    access_level: str | None = None,
    document_type: str | None = None,
) -> list[dict]:
    """
    Public helper function used by the RAG service.

    This function provides a simple interface
    for the rest of the application.

    Example:

        results = search_documents(
            "How long does cashback take?",
            top_k=3,
        )

    Example with metadata filtering:

        results = search_documents(
            "What is the cashback policy?",
            top_k=3,
            department="Finance",
            category="Rewards",
        )
    """

    # Get the cached search service.

    search_service = (
        get_search_service()
    )

    # Execute the semantic search
    # with optional metadata filtering.

    return search_service.search(
        query=query,
        top_k=top_k,
        department=department,
        category=category,
        access_level=access_level,
        document_type=document_type,
    )


if __name__ == "__main__":

    # ---------------------------------------------------------
    # Example 1: Semantic search without filters
    # ---------------------------------------------------------

    query = (
        "How long does it take "
        "to receive cashback?"
    )

    results = search_documents(
        query=query,
        top_k=3,
        access_level = "internal",
        document_type = "text"
    )

    print(
        f"\nQuery: {query}"
    )

    print(
        f"Retrieved {len(results)} results."
    )

    for index, result in enumerate(
        results,
        start=1,
    ):

        print(
            "\n" + "=" * 60
        )

        print(
            f"Result {index}"
        )

        print(
            "Score:",
            result["score"],
        )

        print(
            "Document:",
            result["metadata"].document_name,
        )

        print(
            "Department:",
            result["metadata"].department,
        )

        print(
            "Category:",
            result["metadata"].category,
        )

        print(
            "Access Level:",
            result["metadata"].access_level,
        )

        print(
            "Document Type:",
            result["metadata"].document_type,
        )

        print(
            "Page:",
            result["metadata"].page_number,
        )

        print(
            "Chunk ID:",
            result["metadata"].chunk_id,
        )

        print(
            "Text:",
            result["text"],
        )

# # Step 1

# # Imports:

# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer

# from app.ai.rag.embed import generate_embeddings


# # Load the same embedding model used to build the index, so the query
# # vector lives in the same vector space as the stored chunk vectors.
# model = SentenceTransformer(
#     "sentence-transformers/all-MiniLM-L6-v2"
# )

# # Search Function
# def search_documents(query, top_k=3):
#     # Build the searchable FAISS index and keep the matching chunk metadata.
#     index, chunks = create_faiss_index()

#     # Turn the user's question into a vector (wrapped in a list because the
#     # model expects a batch of texts, not a single string).
#     query_embedding = model.encode([query])

#     # FAISS requires float32 vectors, so cast to match that format.
#     query_embedding = np.array(query_embedding).astype("float32")

#     # Ask FAISS for the top_k closest chunk vectors to the query vector.
#     # 'distances' = how far each match is, 'indices' = their positions.
#     distances, indices = index.search(query_embedding, top_k)
#     results = []

#     # Map each returned position back to its original chunk of text.
#     for idx in indices[0]:
#         results.append(chunks[idx])

#     return results

# # What Happens Here?

# # Suppose:
# # What rewards do Gold users get?
# # becomes:
# # [0.111, 0.444, 0.777, ...]

# # FAISS compares it with:
# # Chunk 1 Vector
# # Chunk 2 Vector
# # Chunk 3 Vector
# # ...

# # and returns the closest vectors.


# # Step 2

# # Create index:

# def create_faiss_index():
#     # Get all chunk texts and their precomputed embedding vectors.
#     chunks, embeddings = generate_embeddings()

#     # FAISS needs a float32 NumPy array as input.
#     embeddings = np.array(embeddings).astype("float32")

#     # Number of values per vector (e.g. 384 for all-MiniLM-L6-v2); the index
#     # must be created with this exact dimension.
#     dimension  = embeddings.shape[1]

#     # IndexFlatL2 does an exact nearest-neighbour search using L2 distance.
#     index = faiss.IndexFlatL2(dimension)

#     # Load every chunk vector into the index so it becomes searchable.
#     index.add(embeddings)

#     return index, chunks

# # What is Happening?

# # Example:
# # Embedding
# # [0.12, 0.45, 0.78, ...]

# # gets stored inside:
# # FAISS Index

# # Think of FAISS as:
# # Google Search
# # for vectors

# # Step 3
# # Test:

# if __name__ == "__main__":
#     # index, chunks = create_faiss_index()

#     # print("Total Vectors:", index.ntotal)

#     # print("Sample Chunk:")
#     # print(chunks[0]["text"])
    
#     # query = "What cashback do Gold customers receive?"
#     # query = "How does the referral program work?"
#     query = "When will I receive my cashback?"

#     # Run the full search pipeline for a sample query and print the matches.
#     results = search_documents(query)

#     print(f"\nQuery: {query}\n")

#     for i, result in enumerate(results, start=1):
#         print(f"Result {i}")
#         print(result["text"])
#         print("-" * 50)
    

# Interview Questions

# What is FAISS?
# FAISS (Facebook AI Similarity Search) is a library developed by Meta for efficient similarity search and clustering of high-dimensional vectors.

# Why store embeddings in FAISS?
# FAISS enables fast nearest-neighbor search, allowing retrieval of semantically similar documents from large collections of embeddings.

# What does IndexFlatL2 do?
# IndexFlatL2 performs exact similarity search using Euclidean (L2) distance between vectors.

# What is a vector index?
# A vector index is a data structure optimized for storing embeddings and performing efficient similarity searches.
    
# How does FAISS retrieval work?
# User queries are converted into embeddings. FAISS compares the query vector against stored document vectors and returns the most similar results based on vector distance.

# What is semantic search?
# Semantic search retrieves information based on meaning rather than exact keyword matching.

# Why is semantic search better than keyword search?
# Example:
# Query:
# What benefits do Gold members receive?

# Document:
# Gold customers receive 10% cashback.
# Keyword search may fail.
# Semantic search understands the meaning and retrieves the correct document.

# python -m app.ai.rag.search