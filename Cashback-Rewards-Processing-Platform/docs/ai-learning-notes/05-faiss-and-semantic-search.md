# FAISS and Semantic Search

## Overview

FAISS (Facebook AI Similarity Search) is an open-source library developed by Meta for efficient similarity search and clustering of high-dimensional vectors.

In Retrieval-Augmented Generation (RAG) systems, FAISS is commonly used to store embeddings and retrieve the most relevant documents based on semantic similarity.

In this project, FAISS is used to search cashback policies, campaign information, and FAQs based on user questions.

---

## Why Do We Need FAISS?

After generating embeddings, we have numerical vector representations of our documents.

Example:

Document:

Gold customers receive 10% cashback.

Embedding:

[0.123, -0.456, 0.789, ...]

Question:

What rewards do Gold users receive?

Embedding:

[0.118, -0.442, 0.781, ...]

To find relevant information, we need a way to compare the query embedding with thousands of stored embeddings efficiently.

FAISS provides optimized algorithms for performing this similarity search.

---

## What Problem Does FAISS Solve?

Without FAISS:

1. Convert user query into an embedding.
2. Compare it with every document embedding manually.
3. Calculate similarity scores one by one.
4. Return the most relevant documents.

This becomes slow and expensive as the number of documents grows.

With FAISS:

1. Store embeddings in a vector index.
2. Search millions of vectors efficiently.
3. Retrieve the most similar results quickly.

---

## What is a Vector Index?

A vector index is a data structure optimized for storing embeddings and performing nearest-neighbor searches.

Example:

Stored Embeddings:

Vector 1 → Cashback Policy

Vector 2 → Referral Campaign

Vector 3 → FAQ

User Query Embedding

↓

FAISS Index

↓

Top Matching Vectors

↓

Relevant Documents

---

## FAISS in the RAG Pipeline

### Indexing Phase

Knowledge Base Documents
↓
Chunking
↓
Generate Embeddings
↓
Store in FAISS

### Retrieval Phase

User Question
↓
Generate Query Embedding
↓
Search FAISS Index
↓
Retrieve Relevant Chunks
↓
Send Context to LLM

---

## What is Similarity Search?

Similarity search finds vectors that are closest to a query vector.

Instead of looking for exact keywords, it searches for similar meanings.

Example:

Document:

Gold customers receive 10% cashback.

User Query:

What benefits do Gold members receive?

Although the wording is different, the semantic meaning is similar.

FAISS retrieves the relevant document because their embeddings are close in vector space.

---

## What is Semantic Search?

Semantic search retrieves information based on meaning rather than exact keyword matching.

### Traditional Keyword Search

Query:

Gold Rewards

Document:

Gold customers receive cashback.

Keyword matching may fail because the exact words differ.

### Semantic Search

Query:

What rewards do Gold users get?

Document:

Gold customers receive cashback.

Embeddings capture the meaning of both sentences and retrieve the correct result.

---

## Similarity Metrics

FAISS uses mathematical distance calculations to determine similarity.

Common metrics include:

### Euclidean Distance (L2)

Measures the straight-line distance between vectors.

Example:

IndexFlatL2

### Cosine Similarity

Measures the angle between vectors.

Frequently used in semantic search applications.

### Inner Product

Measures vector similarity using dot products.

Often used in recommendation systems.

---

## FAISS Index Types

### IndexFlatL2

* Exact similarity search
* Simple implementation
* Good for small datasets
* Used in this project

### IVF (Inverted File Index)

* Faster search for large datasets
* Uses clustering techniques

### HNSW

* Approximate nearest neighbor search
* Very fast retrieval
* Common in production systems

---

## FAISS in This Project

Current Workflow:

Knowledge Base Documents
↓
Chunking
↓
Embeddings
↓
FAISS Index
↓
User Query
↓
Query Embedding
↓
Similarity Search
↓
Relevant Chunks Retrieved

Example:

Query:

What cashback do Gold customers receive?

Retrieved Context:

Gold customers receive 10% cashback on eligible purchases.

The retrieved chunk will later be sent to an LLM to generate a final response.

---

## Benefits of Semantic Search

### Better User Experience

Users can ask questions naturally without matching exact document wording.

### Improved Retrieval Accuracy

Relevant information is retrieved based on meaning.

### Supports Natural Language Queries

Questions can be phrased in multiple ways.

### Foundation of Modern RAG Systems

Most enterprise AI assistants rely on semantic retrieval.

---

## Challenges and Learnings

### Poor Chunking

If chunks split sentences or words incorrectly:

Example:

Customers receive ₹100 for ev

ery successful referral

Retrieval quality decreases.

### Embedding Quality

Better embedding models generally improve retrieval performance.

### Large Knowledge Bases

As document volume increases, efficient indexing becomes critical.

---

## Interview Questions

### What is FAISS?

FAISS (Facebook AI Similarity Search) is a library developed by Meta for efficient similarity search and clustering of high-dimensional vectors.

### Why is FAISS used in RAG systems?

FAISS stores embeddings and enables fast retrieval of semantically similar documents.

### What is a vector index?

A vector index is a data structure optimized for storing embeddings and performing nearest-neighbor searches.

### What is semantic search?

Semantic search retrieves information based on meaning rather than exact keyword matching.

### What is similarity search?

Similarity search finds vectors that are closest to a query vector using distance or similarity metrics.

### Why is semantic search better than keyword search?

Semantic search understands meaning and can retrieve relevant information even when the query wording differs from the stored documents.

### What is IndexFlatL2?

IndexFlatL2 is a FAISS index type that performs exact nearest-neighbor search using Euclidean distance.

### What role does FAISS play in the RAG pipeline?

FAISS stores document embeddings and retrieves the most relevant chunks before they are passed to the LLM for response generation.

---

## Summary

* FAISS is a vector search library developed by Meta.
* It stores embeddings and performs efficient similarity searches.
* Semantic search retrieves information based on meaning rather than keywords.
* FAISS is a core component of many RAG systems.
* In this project, FAISS retrieves relevant cashback and rewards information before passing it to an LLM.
* Retrieval quality depends heavily on chunking strategy, embedding quality, and vector search performance.
