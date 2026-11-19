"""
Cross-Encoder based reranking for RAG retrieval.

Pipeline:

    User Query
        ↓
    Dense Retrieval (FAISS)
        +
    Sparse Retrieval (BM25)
        ↓
    RRF Fusion
        ↓
    Candidate Documents
        ↓
    Cross-Encoder Reranking
        ↓
    Final Top-K Results

The Cross-Encoder jointly processes:

    [query, document]

and produces a relevance score.

Unlike the bi-encoder used by FAISS,
the Cross-Encoder does not independently
encode the query and document.

It evaluates their relationship together.

This makes it more accurate but more expensive.

Therefore:

    FAISS/BM25/RRF
        = high recall

    Cross-Encoder
        = high precision
"""


from functools import lru_cache

from sentence_transformers import CrossEncoder

from app.ai.rag.hybrid_search import (
    hybrid_search_documents,
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DEFAULT_RERANKER_MODEL = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


DEFAULT_FINAL_TOP_K = 5


class CrossEncoderReranker:
    """
    Rerank retrieved candidate documents
    using a Cross-Encoder model.
    """

    def __init__(
        self,
        model_name: str = DEFAULT_RERANKER_MODEL,
    ):
        """
        Initialize the Cross-Encoder.

        The model is loaded once and reused
        across multiple reranking operations.
        """

        self.model_name = (
            model_name
        )

        self.model = CrossEncoder(
            model_name
        )

    # -----------------------------------------------------
    # Core Reranking
    # -----------------------------------------------------

    def rerank(
        self,
        query: str,
        results: list[dict],
        *,
        top_k: int = DEFAULT_FINAL_TOP_K,
    ) -> list[dict]:
        """
        Rerank candidate documents.

        Parameters
        ----------
        query:
            User's natural-language question.

        results:
            Candidate documents retrieved by
            FAISS, BM25, or hybrid RRF.

        top_k:
            Number of final results to return.

        Returns
        -------
        list[dict]
            Cross-Encoder ranked results.
        """

        if not query or not query.strip():
            raise ValueError(
                "Reranking query cannot be empty."
            )

        if not results:
            return []

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        # -------------------------------------------------
        # Prepare Query-Document Pairs
        # -------------------------------------------------

        pairs = [
            (
                query,
                result["text"],
            )
            for result in results
        ]

        # -------------------------------------------------
        # Cross-Encoder Prediction
        # -------------------------------------------------

        scores = self.model.predict(
            pairs
        )

        # -------------------------------------------------
        # Attach Cross-Encoder Scores
        # -------------------------------------------------

        reranked_results = []

        for result, score in zip(
            results,
            scores,
        ):
            enriched_result = dict(
                result
            )

            enriched_result[
                "reranker_score"
            ] = float(
                score
            )

            reranked_results.append(
                enriched_result
            )

        # -------------------------------------------------
        # Sort by Cross-Encoder Score
        # -------------------------------------------------

        reranked_results.sort(
            key=lambda result: result[
                "reranker_score"
            ],
            reverse=True,
        )

        # -------------------------------------------------
        # Return Final Top-K
        # -------------------------------------------------

        return reranked_results[
            :top_k
        ]


# ---------------------------------------------------------
# Cached Reranker Factory
# ---------------------------------------------------------

@lru_cache(maxsize=1)
def get_reranker() -> CrossEncoderReranker:
    """
    Create and cache the Cross-Encoder reranker.

    Loading transformer models is expensive.

    Caching ensures that the model is loaded only once
    per application process.
    """

    return CrossEncoderReranker()


# ---------------------------------------------------------
# Reranker Service (hybrid + Cross-Encoder)
# ---------------------------------------------------------

class RerankerService:
    """
    Service responsible for the full retrieval +
    Cross-Encoder reranking pipeline.

    Exposes a search API used by RAGService:

        FAISS
          ↓
        BM25
          ↓
        RRF
          ↓
        Cross-Encoder
          ↓
        Final Results
    """

    def __init__(
        self,
        reranker: CrossEncoderReranker,
    ):
        """
        Initialize the reranker service.

        Parameters
        ----------
        reranker:
            Cross-Encoder model wrapper used for
            precision reranking of hybrid candidates.
        """

        self.reranker = reranker

    def search(
        self,
        query: str,
        top_k: int = DEFAULT_FINAL_TOP_K,
        *,
        candidate_k: int | None = None,
        access_level: str | None = None,
        document_type: str | None = None,
        department: str | None = None,
        category: str | None = None,
    ) -> list[dict]:
        """
        Retrieve hybrid candidates and rerank them.

        Parameters
        ----------
        query:
            User's natural-language question.

        top_k:
            Number of final reranked results to return.

        candidate_k:
            Number of hybrid candidates retrieved
            before Cross-Encoder reranking.

        Returns
        -------
        list[dict]
            Cross-Encoder ranked results.
        """

        if candidate_k is None:

            candidate_k = max(
                top_k * 4,
                20,
            )

        hybrid_results = (
            hybrid_search_documents(
                query=query,
                top_k=candidate_k,
                candidate_k=candidate_k,
                access_level=access_level,
                document_type=document_type,
                department=department,
                category=category,
            )
        )

        return self.reranker.rerank(
            query=query,
            results=hybrid_results,
            top_k=top_k,
        )


@lru_cache(maxsize=1)
def get_reranker_service() -> RerankerService:
    """
    Create and cache the reranker service.

    The Cross-Encoder model is loaded once per
    application process and reused.
    """

    return RerankerService(
        reranker=get_reranker(),
    )


# ---------------------------------------------------------
# Complete Retrieval + Reranking Pipeline
# ---------------------------------------------------------

def rerank_documents(
    query: str,
    *,
    top_k: int = DEFAULT_FINAL_TOP_K,
    candidate_k: int | None = None,
    access_level: str | None = None,
    document_type: str | None = None,
    department: str | None = None,
    category: str | None = None,
) -> list[dict]:
    """
    Execute the complete retrieval pipeline.

    Pipeline:

        FAISS
          ↓
        BM25
          ↓
        RRF
          ↓
        Metadata Filtering
          ↓
        Cross-Encoder
          ↓
        Final Results

    candidate_k controls how many documents are
    retrieved before reranking.

    Example:

        candidate_k = 20

        top_k = 5

    means:

        Retrieve 20 candidates
        Rerank 20 candidates
        Return best 5
    """

    return get_reranker_service().search(
        query=query,
        top_k=top_k,
        candidate_k=candidate_k,
        access_level=access_level,
        document_type=document_type,
        department=department,
        category=category,
    )


# ---------------------------------------------------------
# Independent Cross-Encoder Test
# ---------------------------------------------------------

def test_cross_encoder_independently():
    """
    Test the Cross-Encoder without FAISS,
    BM25, or RRF.

    This demonstrates that the Cross-Encoder
    can reorder an existing candidate list
    based on query-document relevance.
    """

    query = (
        "How long does it take "
        "to receive cashback?"
    )

    candidate_results = [

        {
            "text": (
                "Gold customers receive "
                "10% cashback on eligible purchases."
            ),
            "score": 0.7,
        },

        {
            "text": (
                "The maximum cashback per "
                "transaction is ₹500."
            ),
            "score": 0.6,
        },

        {
            "text": (
                "Cashback is credited within "
                "48 hours after successful "
                "transaction settlement."
            ),
            "score": 0.5,
        },
    ]

    reranker = (
        get_reranker()
    )

    results = reranker.rerank(
        query=query,
        results=candidate_results,
        top_k=3,
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "INDEPENDENT CROSS-ENCODER TEST"
    )

    print(
        "=" * 70
    )

    print(
        "\nQuery:",
        query,
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):

        print(
            "\n" + "-" * 70
        )

        print(
            "Rank:",
            rank,
        )

        print(
            "Cross-Encoder Score:",
            result[
                "reranker_score"
            ],
        )

        print(
            "Original Score:",
            result.get(
                "score"
            ),
        )

        print(
            "Text:",
            result["text"],
        )


# ---------------------------------------------------------
# Full Hybrid + RRF + Reranking Test
# ---------------------------------------------------------

def test_hybrid_reranking():
    """
    Test the complete retrieval pipeline.

    FAISS
        ↓
    BM25
        ↓
    RRF
        ↓
    Cross-Encoder
    """

    query = (
        "How long does it take "
        "to receive cashback?"
    )

    results = rerank_documents(
        query=query,
        top_k=3,
        candidate_k=10,
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "HYBRID + RRF + CROSS-ENCODER TEST"
    )

    print(
        "=" * 70
    )

    print(
        "\nQuery:",
        query,
    )

    print(
        "\nFinal Results:",
        len(results),
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):

        metadata = result.get(
            "metadata"
        )

        print(
            "\n" + "-" * 70
        )

        print(
            "Final Rank:",
            rank,
        )

        print(
            "Reranker Score:",
            result.get(
                "reranker_score"
            ),
        )

        print(
            "RRF Score:",
            result.get(
                "rrf_score"
            ),
        )

        print(
            "Dense Score:",
            result.get(
                "dense_score"
            ),
        )

        print(
            "Sparse Score:",
            result.get(
                "sparse_score"
            ),
        )

        if metadata:

            print(
                "Document:",
                metadata.document_name,
            )

            print(
                "Chunk ID:",
                metadata.chunk_id,
            )

        print(
            "Text:",
            result["text"],
        )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    # -----------------------------------------------------
    # Test 1:
    # Cross-Encoder independently
    # -----------------------------------------------------

    test_cross_encoder_independently()

    # -----------------------------------------------------
    # Test 2:
    # Full production-oriented pipeline
    #
    # FAISS
    #   ↓
    # BM25
    #   ↓
    # RRF
    #   ↓
    # Cross-Encoder
    # -----------------------------------------------------

    test_hybrid_reranking()
    
# uv run python -m app.ai.rag.reranker