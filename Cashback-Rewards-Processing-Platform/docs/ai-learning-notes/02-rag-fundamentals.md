# RAG Fundamentals

## Overview

Retrieval-Augmented Generation (RAG) is an AI architecture that enhances Large Language Models by retrieving relevant information from external knowledge sources before generating a response.

RAG combines:

* Information Retrieval
* Vector Search
* Large Language Models

This allows AI systems to answer questions using current and domain-specific information without retraining the model.

---

## Why Do We Need RAG?

LLMs have several limitations:

* Training data may be outdated
* Business-specific information is unavailable
* Responses may contain hallucinations
* Retraining models is expensive

RAG solves these problems by providing relevant information during inference.

---

## Traditional LLM Flow

Without RAG:

User Question
↓
LLM
↓
Response

Problem:

The model only uses its training knowledge.

---

## RAG Flow

With RAG:

User Question
↓
Convert Question to Embedding
↓
Search Vector Database
↓
Retrieve Relevant Documents
↓
Send Context + Question to LLM
↓
Generate Response

The model answers using retrieved information instead of relying solely on training data.

---

## Example

Knowledge Base:

Gold customers receive 10% cashback.

User Question:

What cashback do Gold customers receive?

RAG Process:

1. User question is converted into an embedding.
2. Similar documents are searched.
3. Relevant document is retrieved.
4. Context is sent to the LLM.
5. LLM generates an answer.

Response:

Gold customers receive 10% cashback on eligible purchases.

---

## Core Components of RAG

### Knowledge Base

A collection of documents containing business information.

Examples:

* Policies
* FAQs
* Campaign Information
* Product Documentation

### Embeddings

Numerical vector representations of text.

Embeddings allow semantic similarity search.

### Vector Database

Stores embeddings and enables efficient similarity search.

Examples:

* FAISS
* Pinecone
* ChromaDB
* Weaviate

### Retriever

Finds the most relevant document chunks based on user queries.

### LLM

Generates the final response using retrieved context.

---

## Benefits of RAG

### More Accurate Responses

Uses business-specific information.

### Up-to-Date Information

Documents can be updated without retraining the model.

### Reduced Hallucinations

Responses are grounded in retrieved context.

### Lower Cost

No need to retrain large models.

---

## RAG Usage in This Project

The Cashback Assistant will use RAG to answer questions related to:

* Cashback policies
* Reward calculations
* Campaign information
* Referral programs
* Customer FAQs

Documents stored in the knowledge base will be converted into embeddings and stored in a vector database.

When users ask questions, relevant information will be retrieved and provided to the LLM for response generation.

---

## Interview Questions

### What is RAG?

Retrieval-Augmented Generation is an AI architecture that retrieves relevant information from external sources and provides it to an LLM before generating a response.

### Why is RAG needed?

RAG helps overcome limitations of LLMs such as outdated knowledge, hallucinations, and lack of domain-specific information.

### What are the main components of a RAG system?

* Knowledge Base
* Embeddings
* Vector Database
* Retriever
* LLM

### How does RAG reduce hallucinations?

The model generates answers using retrieved factual context rather than relying solely on learned patterns.

### What is the difference between fine-tuning and RAG?

Fine-tuning modifies model behavior by training on additional data, while RAG retrieves external information at runtime without retraining the model.

### Explain a RAG pipeline.

You can now confidently explain:

1. Store business documents

2. Split into chunks

3. Generate embeddings

4. Store embeddings in FAISS

5. Convert user query into embedding

6. Perform similarity search

7. Retrieve top chunks

8. Pass chunks to LLM

9. Generate final answer