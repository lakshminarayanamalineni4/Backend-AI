# Document Metadata and Provenance

## 1. What is Document Metadata?

Document metadata is additional information about a document or chunk that helps the RAG system understand, filter, secure, and trace retrieved content.

Instead of storing only:

```python
{
    "text": "FastAPI dependency injection allows..."
}
```

we store the text along with metadata:

```python
{
    "text": "FastAPI dependency injection allows...",

    "metadata": {
        "document_id": "doc-001",
        "document_name": "fastapi_guidelines.md",
        "source_type": "internal",
        "source_uri": None,
        "license": None,
        "document_type": "technical_documentation",
        "department": "engineering",
        "category": "backend",
        "access_level": "engineering",
        "version": "1.0",
        "section": "Dependency Injection",
        "chunk_index": 3
    }
}
```

---

## 2. Why is Metadata Important in RAG?

Metadata helps with:

* Filtering documents before retrieval
* Access control
* Source attribution
* Document provenance
* Document versioning
* Organizing the knowledge base
* Debugging retrieval results

For example, if a user belongs to the Engineering department, the system can restrict retrieval to authorized Engineering documents before performing semantic or keyword search.

---

## 3. Document Metadata vs Chunk Metadata

A document contains the original source content.

A chunk is a smaller section created from the document for embedding and retrieval.

The relationship is:

```text
Document
    ↓
Section
    ↓
Chunks
    ↓
Embeddings
```

Each retrieved chunk should retain enough metadata to trace it back to the original document.

```text
Answer
    ↓
Retrieved Chunk
    ↓
Section
    ↓
Document
    ↓
Original Source
```

---

## 4. Current Metadata Schema

Our current project uses the following metadata:

| Field           | Purpose                                                     |
| --------------- | ----------------------------------------------------------- |
| `document_id`   | Unique identifier for the document                          |
| `document_name` | Name of the original document                               |
| `source_type`   | Identifies where the document came from                     |
| `source_uri`    | Original location or URL of the document                    |
| `license`       | License information for public documents                    |
| `document_type` | Type of document, such as policy or technical documentation |
| `department`    | Department associated with the document                     |
| `category`      | More specific classification of the document                |
| `access_level`  | Defines who can access the document                         |
| `version`       | Tracks document versions                                    |
| `section`       | Section from which the chunk was created                    |
| `chunk_index`   | Position of the chunk within the document                   |

---

## 5. Example

```python
{
    "text": "FastAPI dependency injection allows reusable dependencies.",

    "metadata": {
        "document_id": "doc-001",
        "document_name": "fastapi_guidelines.md",
        "source_type": "internal",
        "source_uri": None,
        "license": None,
        "document_type": "technical_documentation",
        "department": "engineering",
        "category": "backend",
        "access_level": "engineering",
        "version": "1.0",
        "section": "Dependency Injection",
        "chunk_index": 3
    }
}
```

---

## 6. Metadata in the RAG Pipeline

The metadata will eventually be used as follows:

```text
User Query
    ↓
Authentication
    ↓
Identify User Permissions
    ↓
Metadata / Access Filtering
    ↓
Hybrid Retrieval
    ├── BM25
    └── FAISS
    ↓
Reranking
    ↓
Prompt Construction
    ↓
LLM
    ↓
Answer + Source Attribution
```

Access filtering should happen **before retrieval** so that unauthorized documents are never included in the retrieved context sent to the LLM.

---

## 7. Provenance

Provenance means keeping track of where information came from.

For example:

```text
Answer
    ↓
Chunk
    ↓
Section
    ↓
Document
    ↓
Source URI
```

This allows users to verify the information used to generate an answer.

For public technical documentation, provenance should also record the source and license.

Example:

```python
{
    "source_type": "public",
    "source_uri": "https://example.com/docs",
    "license": "MIT"
}
```

---

## 8. Future Metadata

As the project evolves, we may add metadata related to:

* Embedding model
* Embedding model version
* Chunking strategy
* Chunk size
* Chunk overlap
* Document hash
* Parser version
* OCR usage
* Ingestion timestamp

These fields will become useful for advanced RAG, document versioning, debugging, evaluation, and LLMOps.

For now, we will implement only the current metadata schema and expand it when the project requires it.
