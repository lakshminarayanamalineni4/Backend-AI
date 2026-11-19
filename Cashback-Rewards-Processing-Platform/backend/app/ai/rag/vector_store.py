from pathlib import Path
import pickle

import faiss
import numpy as np

from app.ai.rag.embed import EmbeddingService


# Directory where the persistent FAISS index and metadata
# will be stored.
VECTOR_STORE_DIR = Path("app/ai/vector_store")

# Persistent FAISS index file.
FAISS_INDEX_PATH = VECTOR_STORE_DIR / "index.faiss"

# Persistent metadata file.
# FAISS does not store arbitrary Python metadata,
# so we persist chunk information separately.
METADATA_PATH = VECTOR_STORE_DIR / "metadata.pkl"


class FAISSVectorStore:
    """
    Persistent FAISS vector store.

    Responsibilities:

    1. Generate embeddings for document chunks.
    2. Build a FAISS similarity index.
    3. Persist the FAISS index to disk.
    4. Persist chunk metadata separately.
    5. Load the persisted index.
    6. Search for semantically similar chunks.
    7. Map FAISS result positions back to chunk metadata.
    """

    def __init__(
        self,
        index_path: Path = FAISS_INDEX_PATH,
        metadata_path: Path = METADATA_PATH,
    ):
        """
        Initialize the vector store.

        Parameters
        ----------
        index_path:
            Location of the persisted FAISS index.

        metadata_path:
            Location of the persisted chunk metadata.
        """

        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)

        # FAISS index.
        # It will be populated when build_index() or load() is called.
        self.index = None

        # List of chunk dictionaries corresponding
        # position-by-position with FAISS vectors.
        self.metadata: list[dict] = []

    def build_index(
        self,
        chunks: list[dict],
        embeddings: np.ndarray,
    ) -> None:
        """
        Build a FAISS index from document embeddings.

        The order of `chunks` MUST match the order
        of `embeddings`.

        Example:

            chunks[0] <-> embeddings[0]
            chunks[1] <-> embeddings[1]
            chunks[2] <-> embeddings[2]

        This positional relationship is critical because
        FAISS returns vector positions rather than document IDs.
        """

        if not chunks:
            raise ValueError(
                "Cannot build FAISS index from empty chunks."
            )

        if embeddings.size == 0:
            raise ValueError(
                "Cannot build FAISS index from empty embeddings."
            )

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        # FAISS expects float32 NumPy arrays.
        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        # The number of columns represents the
        # embedding vector dimension.
        dimension = embeddings.shape[1]

        # IndexFlatIP performs inner-product similarity search.
        #
        # Because our embeddings are normalized in embed.py,
        # inner product is equivalent to cosine similarity.
        self.index = faiss.IndexFlatIP(dimension)

        # Add all document vectors to the FAISS index.
        self.index.add(embeddings)

        # Preserve the exact order of chunks.
        #
        # FAISS position:
        #
        # 0 -> metadata[0]
        # 1 -> metadata[1]
        # 2 -> metadata[2]
        #
        # This allows search results to be mapped back
        # to the original document chunks.
        self.metadata = chunks

    def save(self) -> None:
        """
        Persist the FAISS index and metadata to disk.
        """

        if self.index is None:
            raise RuntimeError(
                "FAISS index has not been built."
            )

        # Create the directory if it does not exist.
        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Save the FAISS vector index.
        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        # Save chunk metadata separately.
        with open(
            self.metadata_path,
            "wb",
        ) as file:

            pickle.dump(
                self.metadata,
                file,
            )

    def load(self) -> None:
        """
        Load a previously persisted FAISS index
        and its corresponding metadata.
        """

        if not self.index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found: "
                f"{self.index_path}"
            )

        if not self.metadata_path.exists():
            raise FileNotFoundError(
                f"Metadata file not found: "
                f"{self.metadata_path}"
            )

        # Load the FAISS index.
        self.index = faiss.read_index(
            str(self.index_path)
        )

        # Load the metadata mapping.
        with open(
            self.metadata_path,
            "rb",
        ) as file:

            self.metadata = pickle.load(file)

        # Validate that FAISS and metadata
        # contain the same number of records.
        if self.index.ntotal != len(
            self.metadata
        ):
            raise RuntimeError(
                "FAISS index size does not match "
                "metadata size."
            )

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search the FAISS index using a query embedding.

        Returns the most relevant chunks together
        with similarity scores.
        """

        if self.index is None:
            raise RuntimeError(
                "FAISS index is not loaded."
            )

        if not self.metadata:
            raise RuntimeError(
                "Metadata is not loaded."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        # Avoid requesting more results
        # than the index actually contains.
        top_k = min(
            top_k,
            self.index.ntotal,
        )

        # Ensure the query has the expected shape.
        query_embedding = np.asarray(
            query_embedding,
            dtype="float32",
        )

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(
                1,
                -1,
            )

        # Search the FAISS index.
        #
        # distances:
        # Similarity scores returned by FAISS.
        #
        # indices:
        # Positions of the matching vectors.
        distances, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(
            distances[0],
            indices[0],
        ):

            # FAISS can return -1 when a result
            # is unavailable.
            if index == -1:
                continue

            # Map FAISS vector position
            # back to the original chunk.
            chunk = self.metadata[index]

            results.append(
                {
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                    "score": float(score),
                }
            )

        return results


def build_and_persist_vector_store() -> None:
    """
    Offline indexing pipeline.

    This function should be executed when the knowledge base
    changes or when the vector index needs to be rebuilt.

    Pipeline:

        Documents
            ↓
        Chunking
            ↓
        Embeddings
            ↓
        FAISS Index
            ↓
        Persist to Disk
    """

    embedding_service = EmbeddingService()

    # Load documents, create chunks,
    # and generate embeddings.
    chunks, embeddings = (
        embedding_service.embed_knowledge_base()
    )

    vector_store = FAISSVectorStore()

    # Build the FAISS index.
    vector_store.build_index(
        chunks=chunks,
        embeddings=embeddings,
    )

    # Persist both the vectors and metadata.
    vector_store.save()

    print(
        f"FAISS index created successfully."
    )

    print(
        f"Total vectors: "
        f"{vector_store.index.ntotal}"
    )

    print(
        f"Embedding dimension: "
        f"{vector_store.index.d}"
    )

    print(
        f"Index path: "
        f"{vector_store.index_path}"
    )

    print(
        f"Metadata path: "
        f"{vector_store.metadata_path}"
    )


if __name__ == "__main__":

    build_and_persist_vector_store()
    
    
# uv run python -m app.ai.rag.vector_store