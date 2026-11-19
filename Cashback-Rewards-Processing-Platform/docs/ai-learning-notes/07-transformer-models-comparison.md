# 07 - Transformer Models Comparison

# Transformer Models Comparison

## Introduction

Modern AI models are built on the Transformer architecture, but they are designed for different purposes. Some models specialize in understanding text, while others specialize in generating text.

Choosing the correct model depends on the problem you are trying to solve.

---

# Transformer Family

```text
                    Transformer
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
   Encoder Models                   Generative Models
        │                                   │
 BERT, MiniLM,                     GPT, Gemini,
Sentence Transformers             Llama, Claude
```

Although all of these models are based on the Transformer architecture, they are optimized for different tasks.

---

# Model Comparison

| Model                 | Architecture                     | Primary Purpose             | Common Use Cases                           |
| --------------------- | -------------------------------- | --------------------------- | ------------------------------------------ |
| BERT                  | Encoder                          | Understand text             | Classification, Sentiment Analysis, Search |
| Sentence Transformers | Encoder                          | Generate embeddings         | Semantic Search, RAG, Vector Search        |
| GPT                   | Decoder                          | Generate text               | Chatbots, Coding, Summarization            |
| Gemini                | Transformer-based Generative LLM | Reasoning & Text Generation | AI Assistants, RAG, Multimodal AI          |
| Llama                 | Transformer-based Generative LLM | Open-source text generation | Local AI, Fine-tuning                      |
| Claude                | Transformer-based Generative LLM | Long-context reasoning      | Enterprise AI, Document Analysis           |

---

# BERT

## Full Form

**Bidirectional Encoder Representations from Transformers**

### Architecture

Encoder-only Transformer.

### Purpose

BERT is designed to understand text by considering words from both left and right contexts simultaneously.

Example:

```
The bank is near the river.
```

```
I deposited money in the bank.
```

BERT understands that the word **bank** has different meanings because it analyzes the surrounding context.

### Common Use Cases

* Text Classification
* Named Entity Recognition (NER)
* Search
* Sentiment Analysis
* Question Answering

### Strengths

* Excellent language understanding
* Strong contextual awareness

### Limitations

* Does not naturally generate long-form text.

---

# Sentence Transformers

Sentence Transformers are built on encoder models (such as MiniLM or BERT) and are optimized to convert entire sentences into dense vector embeddings.

Example:

```
Gold customers receive 10% cashback.
```

↓

```
[0.123, -0.456, ..., 0.782]
```

### Common Use Cases

* Semantic Search
* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Recommendation Systems
* Similarity Search

### Used in This Project

```python
SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
```

Purpose:

* Convert document chunks into embeddings.
* Convert user queries into embeddings.
* Enable semantic search using FAISS.

---

# GPT

## Full Form

**Generative Pre-trained Transformer**

### Architecture

Decoder-only Transformer.

### Purpose

Generate human-like text based on a given prompt.

Example:

User:

```
Explain Retrieval-Augmented Generation.
```

↓

GPT generates a detailed explanation.

### Common Use Cases

* Chatbots
* Content Generation
* Coding Assistance
* Translation
* Summarization

### Strengths

* Excellent natural language generation.
* Strong reasoning abilities.

### Limitations

* Knowledge is limited to training data unless combined with external retrieval (RAG).

---

# Gemini

Gemini is Google's family of Transformer-based Generative AI models.

### Capabilities

* Text Generation
* Code Generation
* Reasoning
* Multimodal Understanding
* Function Calling
* Conversational AI

### Used in This Project

```python
model.generate_content(prompt)
```

Purpose:

* Read retrieved context.
* Understand the user's question.
* Generate an accurate natural language response.

---

# Llama

Developed by Meta.

### Type

Open-source Transformer-based Generative LLM.

### Common Use Cases

* Local AI Applications
* Fine-tuning
* Enterprise AI
* Research

### Strengths

* Can be deployed on local infrastructure.
* Highly customizable.

---

# Claude

Developed by Anthropic.

### Features

* Long-context understanding
* Enterprise safety
* Document analysis
* Conversational AI

### Common Use Cases

* Enterprise Assistants
* Legal Document Analysis
* Knowledge Management

---

# Which Model Should I Use?

| Task                | Recommended Model          |
| ------------------- | -------------------------- |
| Generate Embeddings | Sentence Transformers      |
| Semantic Search     | Sentence Transformers      |
| Vector Databases    | Sentence Transformers      |
| Chatbot             | Gemini, GPT, Claude, Llama |
| Summarization       | Gemini, GPT                |
| Translation         | Gemini, GPT                |
| Text Classification | BERT                       |
| Sentiment Analysis  | BERT                       |
| Question Answering  | Gemini, GPT                |

---

# How These Models Work Together in a RAG System

```
Knowledge Base
        │
        ▼
Sentence Transformer
(Encoder)
        │
Generate Embeddings
        │
        ▼
FAISS Vector Search
        │
Retrieve Relevant Chunks
        │
        ▼
Gemini
(Generative LLM)
        │
Reasoning + Response Generation
        ▼
Final Answer
```

---

# How They Are Used in the Cashback Assistant

## Sentence Transformer

Responsibilities:

* Read document chunks.
* Understand semantic meaning.
* Generate vector embeddings.
* Enable semantic retrieval with FAISS.

Pipeline:

```
Document
      ↓
Transformer Encoder
      ↓
Embedding Vector
      ↓
FAISS
```

---

## Gemini 2.5 Flash

Responsibilities:

* Read retrieved context.
* Understand the user's question.
* Perform reasoning.
* Generate the final response.

Pipeline:

```
Question
+
Retrieved Context
        ↓
Gemini
        ↓
Generated Answer
```

---

# Interview Questions

## Why did you use Sentence Transformers instead of Gemini for embeddings?

Sentence Transformers are optimized to generate high-quality semantic embeddings efficiently, making them ideal for similarity search and vector databases. Gemini is optimized for reasoning and text generation. Separating retrieval and generation results in a more efficient and scalable RAG pipeline.

---

## Why can't Sentence Transformers answer user questions directly?

Sentence Transformers are encoder models designed to understand text and generate embeddings. They are not trained to generate fluent natural language responses. Therefore, a generative LLM such as Gemini is used after retrieval to produce the final answer.

---

## What is the difference between BERT and GPT?

BERT is an encoder model designed to understand text and extract contextual information. GPT is a decoder model designed to generate coherent and context-aware text.

---

## Why does a RAG system require both an embedding model and an LLM?

The embedding model converts documents and user queries into vector representations for semantic retrieval. The LLM then uses the retrieved context to reason over the information and generate accurate, natural language responses.

---

# Key Takeaways

* All modern LLMs are based on the Transformer architecture.
* Encoder models specialize in understanding text.
* Sentence Transformers generate embeddings for semantic search.
* Generative LLMs such as Gemini and GPT generate natural language responses.
* A RAG system combines an embedding model for retrieval with a generative model for response generation.
* Selecting the right model depends on the task rather than using a single model for everything.
