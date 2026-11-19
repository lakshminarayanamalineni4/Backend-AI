from app.ai.llm.gemini_service import generate_response
from app.ai.rag.query_rewriter import QueryRewriterService
from app.ai.rag.reranker import RerankerService


class RAGService:
    """
    Service responsible for the complete Retrieval-Augmented Generation
    workflow.

    Pipeline:

        User Question
              |
              v
        Query Rewriting
              |
              v
        Hybrid Retrieval
        (FAISS + BM25)
              |
              v
        RRF Fusion
              |
              v
        Cross-Encoder Reranking
              |
              v
        Top Ranked Context
              |
              v
        Gemini LLM
              |
              v
        Grounded Answer

    Query rewriting improves retrieval quality.
    The original user question is still used when
    generating the final grounded answer.
    """

    def __init__(
        self,
        reranker_service: RerankerService,
        query_rewriter_service: QueryRewriterService,
    ):
        """
        Initialize the RAG service.

        Parameters
        ----------
        reranker_service:
            Service responsible for retrieving the final
            ranked documents after hybrid search and
            Cross-Encoder reranking.

        query_rewriter_service:
            Service responsible for rewriting vague or
            conversational user questions into clearer
            retrieval queries.
        """

        self.reranker_service = reranker_service
        self.query_rewriter_service = (
            query_rewriter_service
        )
   
    def build_context(
        self,
        results: list[dict],
    ) -> str:
        """
        Build the context that will be provided to the LLM.

        Only the text content of the final reranked
        results is included in the prompt.

        The ranking order is preserved, meaning the
        most relevant result appears first.
        """

        return "\n\n".join(
            result["text"]
            for result in results
        )

    def build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build a grounded prompt for the LLM.

        The LLM is explicitly instructed to use only
        the retrieved context and avoid inventing
        information that is not present in the
        knowledge base.
        """

        return f"""
You are a Cashback Rewards Assistant.

Your task is to answer the user's question using
ONLY the provided context.

Rules:

1. Use only information available in the context.
2. Do not invent or assume information.
3. If the answer is not available in the context,
   say exactly:

   "I could not find that information."

4. Give a concise and accurate answer.
5. Do not mention the retrieval process unless
   explicitly asked.

Context:
--------------------
{context}
--------------------

Question:
{question}

Answer:
"""

    def extract_sources(
        self,
        results: list[dict],
    ) -> list[str]:
        """
        Extract unique source document names from
        the final reranked results.

        The order is preserved based on the first
        occurrence of each source.
        """

        sources = []

        for result in results:

            metadata = result.get(
                "metadata"
            )

            if metadata is None:
                continue

            document_name = getattr(
                metadata,
                "document_name",
                None,
            )

            if (
                document_name
                and document_name not in sources
            ):
                sources.append(
                    document_name
                )

        return sources

    def answer_question(
        self,
        question: str,
        retrieval_top_k: int = 10,
        final_top_k: int = 3,
    ) -> dict:
        """
        Execute the complete RAG pipeline.

        Parameters
        ----------
        question:
            User's natural-language question.

        retrieval_top_k:
            Number of documents retrieved from the
            hybrid retrieval pipeline before reranking.

        final_top_k:
            Number of highest-ranked documents retained
            after Cross-Encoder reranking and sent to
            the LLM.

        Returns
        -------
        dict
            Contains:

            - answer:
                Final LLM-generated answer.

            - sources:
                Source documents used to generate
                the answer.

            - retrieved_results:
                Final reranked results used as context.

            - original_query:
                Original user question.

            - rewritten_query:
                Retrieval-oriented rewritten query.
        """

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        # -------------------------------------------------
        # Step 1: Rewrite the user query
        # -------------------------------------------------
        #
        # Query rewriting happens before retrieval.
        #
        # The rewritten query is used only for:
        #
        #   FAISS -> BM25 -> RRF -> Cross-Encoder
        #
        # The original question is still used for
        # the final grounded LLM answer.

        rewrite_result = (
            self.query_rewriter_service.rewrite(
                question
            )
        )

        original_query = rewrite_result[
            "original_query"
        ]

        rewritten_query = rewrite_result[
            "rewritten_query"
        ]

        # -------------------------------------------------
        # Step 2: Retrieve and rerank documents
        # -------------------------------------------------
        #
        # The RerankerService is responsible for the
        # retrieval pipeline:
        #
        # FAISS
        #   -> BM25
        #   -> RRF
        #   -> Cross-Encoder
        #
        # We retrieve more documents initially
        # than we finally send to the LLM.
        #
        # Example:
        #
        # retrieval_top_k = 10
        # final_top_k = 3
        #
        # This gives the Cross-Encoder more candidates
        # to evaluate before selecting the best context.
        #

        results = (
            self.reranker_service.search(
                query=rewritten_query,
                top_k=retrieval_top_k,
            )
        )

        # -------------------------------------------------
        # Step 3: Keep only the final reranked results
        # -------------------------------------------------

        final_results = results[
            :final_top_k
        ]

        # -------------------------------------------------
        # Step 4: Handle empty retrieval results
        # -------------------------------------------------

        if not final_results:

            return {
                "answer": (
                    "I could not find "
                    "that information."
                ),
                "sources": [],
                "retrieved_results": [],
                "original_query": original_query,
                "rewritten_query": rewritten_query,
            }

        # -------------------------------------------------
        # Step 5: Build context
        # -------------------------------------------------

        context = self.build_context(
            final_results
        )

        # -------------------------------------------------
        # Step 6: Build grounded LLM prompt
        # -------------------------------------------------

        prompt = self.build_prompt(
            question=original_query,
            context=context,
        )

        # -------------------------------------------------
        # Step 7: Generate final answer
        # -------------------------------------------------

        answer = generate_response(
            prompt
        )

        # -------------------------------------------------
        # Step 8: Extract source documents
        # -------------------------------------------------

        sources = self.extract_sources(
            final_results
        )

        # -------------------------------------------------
        # Step 9: Return final RAG response
        # -------------------------------------------------

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_results": final_results,
            "original_query": original_query,
            "rewritten_query": rewritten_query,
        }


def answer_question(
    question: str,
    retrieval_top_k: int = 10,
    final_top_k: int = 3,
) -> dict:
    """
    Public helper function for the RAG pipeline.

    This function provides a simple interface for
    FastAPI routes or other application services.

    Example:

        response = answer_question(
            "How long does it take to receive cashback?"
        )
    """

    # Import here to avoid creating the expensive
    # Cross-Encoder model during module import.
    from app.ai.rag.query_rewriter import (
        get_query_rewriter_service,
    )
    from app.ai.rag.reranker import (
        get_reranker_service,
    )

    reranker_service = (
        get_reranker_service()
    )

    query_rewriter_service = (
        get_query_rewriter_service()
    )

    rag_service = RAGService(
        reranker_service=reranker_service,
        query_rewriter_service=(
            query_rewriter_service
        ),
    )

    return rag_service.answer_question(
        question=question,
        retrieval_top_k=retrieval_top_k,
        final_top_k=final_top_k,
    )


if __name__ == "__main__":

    # Use a vague query so rewriting is visible.
    question = (
        "when do I get my money back?"
    )

    response = answer_question(
        question=question,
        retrieval_top_k=10,
        final_top_k=3,
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "ORIGINAL QUESTION"
    )

    print(
        response[
            "original_query"
        ]
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "REWRITTEN QUERY"
    )

    print(
        response[
            "rewritten_query"
        ]
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "ANSWER"
    )

    print(
        response["answer"]
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "SOURCES"
    )

    for source in response[
        "sources"
    ]:
        print(
            "-",
            source,
        )

    print(
        "\n" + "=" * 70
    )

    print(
        "FINAL RERANKED RESULTS"
    )

    for index, result in enumerate(
        response[
            "retrieved_results"
        ],
        start=1,
    ):

        print(
            "\n" + "-" * 60
        )

        print(
            f"Rank: {index}"
        )

        print(
            "Text:",
            result["text"],
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

        metadata = result.get(
            "metadata"
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

# from app.ai.rag.search import search_documents
# from app.ai.llm.gemini_service import generate_response

# def build_context(results):
#     return "\n\n".join(result["text"] for result in results)

# def answer_question(question: str):
#     results = search_documents(question, top_k=3)
#     context = build_context(results)
#     prompt  = f"""
#                 You are a Cashback Rewards Assistant.

#                 Answer only using the provided context.

#                 If the answer is not available in the context,
#                 say "I could not find that information."

#                 Context:
#                 {context}

#                 Question:
#                 {question}
#                 """
    
#     answer  = generate_response(prompt)
#     sources = list(set(result["source"] for result in results))
    
#     return {
#         "answer"  : answer,
#         "sources" : sources
#     }
    
    

# Interview Knowledge

# What happens after retrieval?
# The retrieved chunks are combined into a prompt and provided to the LLM as context. The LLM generates a response grounded in the retrieved information instead of relying solely on its training data.

# Why does RAG reduce hallucinations?
# Because the model receives relevant business context during inference, allowing it to generate responses based on retrieved information rather than guessing from pre-trained knowledge.

# How do you reduce hallucinations in a RAG system?
# I retrieve relevant context from a knowledge base, constrain the LLM to answer only from retrieved content, and return source references so responses can be verified.