"""
Hybrid document retrieval using:

1. Dense retrieval
   - FAISS
   - Sentence Transformer embeddings

2. Sparse retrieval
   - BM25

3. Metadata filtering

4. Reciprocal Rank Fusion (RRF)

The purpose of this service is to combine semantic retrieval
and lexical retrieval into a single ranked candidate list.

Pipeline:

    Query
      ↓
    Dense Search
      ↓
    Sparse Search
      ↓
    Metadata Filtering
      ↓
    RRF Fusion
      ↓
    Hybrid Results
"""

from functools import lru_cache

from app.ai.rag.search import DocumentSearchService
from app.ai.rag.search import get_search_service

from app.ai.rag.sparse_search import (
    BM25SearchService,
    get_sparse_search_service,
)


# ---------------------------------------------------------
# RRF Configuration
# ---------------------------------------------------------

DEFAULT_RRF_K = 60


class HybridSearchService:
    """
    Service responsible for hybrid retrieval.

    Combines:

    - Dense retrieval from FAISS
    - Sparse retrieval from BM25

    using Reciprocal Rank Fusion (RRF).

    The resulting documents are ranked using their
    combined RRF score.
    """

    def __init__(
        self,
        dense_search_service: DocumentSearchService,
        sparse_search_service: BM25SearchService,
        rrf_k: int = DEFAULT_RRF_K,
    ):
        self.dense_search_service = (
            dense_search_service
        )

        self.sparse_search_service = (
            sparse_search_service
        )

        self.rrf_k = rrf_k

    # -----------------------------------------------------
    # Public Hybrid Search
    # -----------------------------------------------------

    def search(
        self,
        query: str,
        *,
        top_k: int = 5,
        candidate_k: int | None = None,
        access_level: str | None = None,
        document_type: str | None = None,
        department: str | None = None,
        category: str | None = None,
    ) -> list[dict]:
        """
        Perform hybrid dense + sparse retrieval.

        Parameters
        ----------
        query:
            User's natural-language question.

        top_k:
            Number of final hybrid results to return.

        candidate_k:
            Number of candidates retrieved from each
            retrieval system before RRF fusion.

        access_level:
            Optional metadata filter.

        document_type:
            Optional metadata filter.

        department:
            Optional metadata filter.

        category:
            Optional metadata filter.

        Returns
        -------
        list[dict]
            RRF-ranked hybrid retrieval results.
        """

        if not query or not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        if candidate_k is None:
            # Retrieve more candidates than the final
            # requested result count.
            #
            # This is important because RRF should have
            # enough candidates from both retrieval systems
            # to produce a high-quality combined ranking.
            candidate_k = max(
                top_k * 3,
                10,
            )

        # -------------------------------------------------
        # Step 1: Dense Retrieval
        # -------------------------------------------------

        dense_results = (
            self.dense_search_service.search(
                query=query,
                top_k=candidate_k,
            )
        )

        # -------------------------------------------------
        # Step 2: Sparse Retrieval
        # -------------------------------------------------

        sparse_results = (
            self.sparse_search_service.search(
                query=query,
                top_k=candidate_k,
            )
        )

        # -------------------------------------------------
        # Step 3: Metadata Filtering
        # -------------------------------------------------

        dense_results = self._filter_results(
            dense_results,
            access_level=access_level,
            document_type=document_type,
            department=department,
            category=category,
        )

        sparse_results = self._filter_results(
            sparse_results,
            access_level=access_level,
            document_type=document_type,
            department=department,
            category=category,
        )

        # -------------------------------------------------
        # Step 4: Reciprocal Rank Fusion
        # -------------------------------------------------

        fused_results = self._rrf_fuse(
            dense_results=dense_results,
            sparse_results=sparse_results,
        )

        # -------------------------------------------------
        # Step 5: Return Top-K Hybrid Candidates
        # -------------------------------------------------

        return fused_results[:top_k]

    # -----------------------------------------------------
    # Metadata Filtering
    # -----------------------------------------------------

    @staticmethod
    def _filter_results(
        results: list[dict],
        *,
        access_level: str | None = None,
        document_type: str | None = None,
        department: str | None = None,
        category: str | None = None,
    ) -> list[dict]:
        """
        Filter retrieval results using metadata.

        Metadata filtering happens before RRF so that
        restricted or irrelevant documents do not
        participate in the final ranking.
        """

        filtered_results = []

        for result in results:

            metadata = result.get(
                "metadata"
            )

            if metadata is None:
                continue

            # ---------------------------------------------
            # Access Level
            # ---------------------------------------------

            if (
                access_level is not None
                and metadata.access_level
                != access_level
            ):
                continue

            # ---------------------------------------------
            # Document Type
            # ---------------------------------------------

            if (
                document_type is not None
                and metadata.document_type
                != document_type
            ):
                continue

            # ---------------------------------------------
            # Department
            # ---------------------------------------------

            if (
                department is not None
                and metadata.department
                != department
            ):
                continue

            # ---------------------------------------------
            # Category
            # ---------------------------------------------

            if (
                category is not None
                and metadata.category
                != category
            ):
                continue

            filtered_results.append(
                result
            )

        return filtered_results

    # -----------------------------------------------------
    # RRF Fusion
    # -----------------------------------------------------

    def _rrf_fuse(
        self,
        *,
        dense_results: list[dict],
        sparse_results: list[dict],
    ) -> list[dict]:
        """
        Combine dense and sparse rankings using
        Reciprocal Rank Fusion.

        RRF formula:

            RRF(d) =
                Σ 1 / (k + rank(d))

        where:

            k = smoothing constant

        A document appearing in both rankings receives
        contributions from both retrieval systems.

        The original dense and sparse scores are preserved
        for debugging and observability.
        """

        fused_documents = {}

        # -------------------------------------------------
        # Dense Ranking
        # -------------------------------------------------

        for rank, result in enumerate(
            dense_results,
            start=1,
        ):
            document_key = (
                self._get_document_key(
                    result
                )
            )

            if document_key not in fused_documents:

                fused_documents[
                    document_key
                ] = {
                    "text": result["text"],
                    "metadata": result[
                        "metadata"
                    ],
                    "dense_score": None,
                    "sparse_score": None,
                    "rrf_score": 0.0,
                }

            fused_documents[
                document_key
            ]["dense_score"] = result.get(
                "score"
            )

            fused_documents[
                document_key
            ]["rrf_score"] += (
                1
                / (
                    self.rrf_k
                    + rank
                )
            )

        # -------------------------------------------------
        # Sparse Ranking
        # -------------------------------------------------

        for rank, result in enumerate(
            sparse_results,
            start=1,
        ):
            document_key = (
                self._get_document_key(
                    result
                )
            )

            if document_key not in fused_documents:

                fused_documents[
                    document_key
                ] = {
                    "text": result["text"],
                    "metadata": result[
                        "metadata"
                    ],
                    "dense_score": None,
                    "sparse_score": None,
                    "rrf_score": 0.0,
                }

            fused_documents[
                document_key
            ]["sparse_score"] = result.get(
                "score"
            )

            fused_documents[
                document_key
            ]["rrf_score"] += (
                1
                / (
                    self.rrf_k
                    + rank
                )
            )

        # -------------------------------------------------
        # Sort by RRF Score
        # -------------------------------------------------

        fused_results = sorted(
            fused_documents.values(),
            key=lambda result: result[
                "rrf_score"
            ],
            reverse=True,
        )

        return fused_results

    # -----------------------------------------------------
    # Document Identity
    # -----------------------------------------------------

    @staticmethod
    def _get_document_key(
        result: dict,
    ) -> str:
        """
        Generate a stable identity for a retrieved chunk.

        chunk_id is preferred because the same chunk
        may appear in both dense and sparse retrieval.

        If chunk_id is unavailable, fall back to
        document/page/text identity.
        """

        metadata = result.get(
            "metadata"
        )

        if metadata is not None:

            chunk_id = getattr(
                metadata,
                "chunk_id",
                None,
            )

            if chunk_id:
                return str(
                    chunk_id
                )

            document_id = getattr(
                metadata,
                "document_id",
                "",
            )

            page_number = getattr(
                metadata,
                "page_number",
                "",
            )

            return (
                f"{document_id}:"
                f"{page_number}:"
                f"{result['text']}"
            )

        return result["text"]


# ---------------------------------------------------------
# Cached Service Factory
# ---------------------------------------------------------

@lru_cache(maxsize=1)
def get_hybrid_search_service() -> HybridSearchService:
    """
    Create and cache the hybrid search service.

    Dense and sparse retrieval services are initialized
    once per application process.
    """

    dense_search_service = (
        get_search_service()
    )

    sparse_search_service = (
        get_sparse_search_service()
    )

    return HybridSearchService(
        dense_search_service=(
            dense_search_service
        ),
        sparse_search_service=(
            sparse_search_service
        ),
    )


# ---------------------------------------------------------
# Public Helper
# ---------------------------------------------------------

def hybrid_search_documents(
    query: str,
    *,
    top_k: int = 5,
    candidate_k: int | None = None,
    access_level: str | None = None,
    document_type: str | None = None,
    department: str | None = None,
    category: str | None = None,
) -> list[dict]:
    """
    Public helper used by higher-level RAG services.
    """

    service = (
        get_hybrid_search_service()
    )

    return service.search(
        query=query,
        top_k=top_k,
        candidate_k=candidate_k,
        access_level=access_level,
        document_type=document_type,
        department=department,
        category=category,
    )


# ---------------------------------------------------------
# Manual Test
# ---------------------------------------------------------

if __name__ == "__main__":

    query = (
        "How long does it take "
        "to receive cashback?"
    )

    results = hybrid_search_documents(
        query=query,
        top_k=5,
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "HYBRID SEARCH TEST"
    )

    print(
        "=" * 70
    )

    print(
        "\nQuery:",
        query,
    )

    print(
        "Retrieved:",
        len(results),
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):

        metadata = result[
            "metadata"
        ]

        print(
            "\n" + "-" * 70
        )

        print(
            "Rank:",
            rank,
        )

        print(
            "RRF Score:",
            result[
                "rrf_score"
            ],
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
        
# uv run python -m app.ai.rag.hybrid_search