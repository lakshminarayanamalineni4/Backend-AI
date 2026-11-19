# Enterprise Knowledge Base Design

## 1. Purpose

The knowledge base provides realistic enterprise data for developing and evaluating the AI-powered document processing and enterprise knowledge platform.

The corpus will support:

* Advanced RAG
* Hybrid Search
* Reranking
* Metadata Filtering
* Access Control
* Source Attribution
* RAG Evaluation
* LLMOps

---

## 2. Knowledge Base Structure

```text
knowledge_base/
│
├── enterprise/
│   ├── engineering/
│   │   ├── backend/
│   │   ├── architecture/
│   │   └── devops/
│   │
│   ├── ai/
│   │   ├── rag/
│   │   ├── generative_ai/
│   │   └── llmops/
│   │
│   ├── security/
│   └── hr/
│
├── public_docs/
│   ├── python/
│   ├── fastapi/
│   ├── postgresql/
│   └── docker/
│
└── demo/
    └── cashback/
```

---

## 3. Knowledge Sources

The project will use three types of knowledge sources.

### Enterprise Documents

Synthetic but realistic internal enterprise documents created specifically for this project.

Examples:

* Engineering guidelines
* Architecture documents
* AI policies
* Security policies
* HR policies

These will be the primary dataset for Advanced RAG development.

### Public Technical Documentation

Selected public technical documentation from appropriate sources with compatible licensing or permitted reuse terms.

Examples:

* Python
* FastAPI
* PostgreSQL
* Docker

Source and license information will be tracked as metadata.

### Demo / Regression Data

The existing cashback documents will be preserved as a small regression dataset.

They will be used to verify that changes to the retrieval pipeline do not break previously working functionality.

---

## 4. Document Size Guidelines

Documents should have realistic and varied sizes.

| Document Type                           | Approximate Size  |
| --------------------------------------- | ----------------- |
| Small policy / FAQ                      | 1,000–2,500 words |
| Medium technical guideline              | 2,500–4,000 words |
| Large architecture / technical document | 4,000–8,000 words |

Documents should not all have identical sizes.

Larger documents are useful for testing:

* Chunking
* Context preservation
* Retrieval precision
* Retrieval recall
* Reranking
* Context window management

---

## 5. Initial Enterprise Corpus

The initial corpus will contain approximately 15 documents covering:

* Backend Engineering
* Software Architecture
* DevOps
* RAG
* Generative AI
* LLMOps
* AI Security
* HR
* Document Access Control

The documents should contain multiple sections and related concepts so that retrieval systems must identify the most relevant chunks rather than simply retrieving an entire small document.

---

## 6. Chunking Strategy

The initial implementation will use fixed-size chunking as a baseline.

Chunking strategies will later be evaluated experimentally.

Possible configurations include:

```text
300 tokens / 15% overlap
500 tokens / 20% overlap
800 tokens / 20% overlap
```

The final configuration will be selected based on:

* Retrieval quality
* Context precision
* Context recall
* Answer quality
* Token usage
* Cost

The goal is to measure and compare chunking strategies rather than assuming one configuration is always optimal.

---

## 7. Metadata Requirements

Each chunk should retain metadata that allows it to be traced back to its source document.

Important metadata includes:

* `document_id`
* `document_name`
* `source_type`
* `source_uri`
* `license`
* `document_type`
* `department`
* `category`
* `access_level`
* `version`
* `section`
* `chunk_index`

Metadata will support:

* Access control
* Metadata filtering
* Source attribution
* Provenance
* Document versioning
* Retrieval debugging

Detailed metadata design is documented in:

`08-document-metadata-and-provenance.md`

---

## 8. Future Retrieval Architecture

The knowledge base will eventually support:

```text
User Query
    ↓
Authentication
    ↓
Access Control
    ↓
Metadata Filtering
    ↓
Hybrid Retrieval
    ├── BM25
    └── Dense Vector Search
    ↓
Result Fusion
    ↓
Reranking
    ↓
Context Selection
    ↓
Prompt Construction
    ↓
LLM
    ↓
Answer Validation
    ↓
Source Attribution
```

Access control must be applied before retrieval so that unauthorized documents are not passed to the LLM.

---

## 9. Future LLMOps Considerations

As the system evolves, the knowledge base will also track information such as:

* Document version
* Document hash
* Ingestion timestamp
* Parser version
* OCR usage
* Chunking strategy
* Chunk size
* Chunk overlap
* Embedding model
* Embedding model version

This metadata will support reproducibility, debugging, evaluation, and continuous improvement of the RAG system.
