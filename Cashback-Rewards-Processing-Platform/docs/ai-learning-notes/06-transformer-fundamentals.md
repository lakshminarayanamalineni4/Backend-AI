# 06 - Transformer Fundamentals

# Transformer Fundamentals

## Introduction

Transformers are deep learning architectures introduced in the 2017 paper **"Attention Is All You Need."** They revolutionized Natural Language Processing (NLP) by replacing sequential models such as RNNs and LSTMs with a parallel processing architecture based on **Self-Attention**.

Today, almost every modern AI model—including BERT, GPT, Gemini, Llama, Sentence Transformers, and Claude—is built on the Transformer architecture.

---

# Evolution of NLP Models

## 1. Bag of Words (BoW)

The earliest NLP approach represented text by counting the occurrence of words.

Example:

Sentence:

```
Gold customers receive cashback.
```

Representation:

| Word      | Count |
| --------- | ----: |
| Gold      |     1 |
| customers |     1 |
| receive   |     1 |
| cashback  |     1 |

### Limitations

* Ignores word order
* Cannot understand context
* Cannot capture semantic meaning

---

## 2. Word Embeddings (Word2Vec, GloVe)

Word embeddings represent each word as a numerical vector.

Example:

```
Cashback
```

↓

```
[-0.32, 0.18, 0.74, ...]
```

Advantages:

* Captures semantic similarity
* Similar words have similar vector representations

Limitations:

Each word has only one embedding.

Example:

```
Bank
```

may refer to:

* River bank
* Financial bank

The model cannot distinguish between different meanings.

---

## 3. Recurrent Neural Networks (RNN)

RNNs process text one word at a time.

```
The
 ↓
cashback
 ↓
was
 ↓
credited
```

Advantages:

* Maintains memory of previous words

Limitations:

* Sequential processing
* Slow training
* Difficulty remembering long-range dependencies
* Vanishing gradient problem

---

## 4. Long Short-Term Memory (LSTM)

LSTMs improve RNNs by introducing memory cells.

Advantages:

* Better long-term memory
* Improved sequence understanding

Limitations:

* Still sequential
* Difficult to parallelize
* Performance decreases for very long sequences

---

## 5. Transformers

Transformers process all words simultaneously using the **Self-Attention** mechanism.

Instead of reading:

```
Word1
 ↓
Word2
 ↓
Word3
```

Transformers process:

```
Word1 ↔ Word2
  ↕       ↕
Word3 ↔ Word4
```

This enables much better understanding of long-range relationships while significantly improving training speed.

---

# What is Self-Attention?

Self-Attention is the mechanism that allows every word in a sentence to evaluate the importance of every other word.

Example:

```
Gold customers receive cashback.
```

The model automatically learns relationships such as:

| Word      | Pays Attention To   |
| --------- | ------------------- |
| Gold      | customers, cashback |
| customers | Gold, receive       |
| receive   | cashback            |
| cashback  | Gold, receive       |

Instead of treating every word equally, the model focuses on the most relevant words.

---

# Why is it Called Self-Attention?

It is called **Self-Attention** because each word attends to other words **within the same input sentence**.

Example:

```
Cashback is credited after the transaction because it was successful.
```

The model learns that:

```
it
```

refers to

```
transaction
```

by assigning higher attention to the relevant word.

---

# Advantages of Transformers

* Parallel processing
* Better contextual understanding
* Captures long-range dependencies
* Faster training than RNNs
* Highly scalable
* Foundation of modern Large Language Models

---

# Encoder vs Decoder

Transformers can be divided into two major categories.

## Encoder

Purpose:

Understand text.

Input:

```
Sentence
```

↓

```
Encoder
```

↓

```
Embedding
```

Encoder models are commonly used for:

* Semantic Search
* Text Classification
* Information Retrieval
* Embedding Generation

Examples:

* BERT
* MiniLM
* Sentence Transformers

---

## Decoder

Purpose:

Generate text.

Input:

```
Question
```

↓

```
Decoder
```

↓

```
Answer
```

Decoder models are commonly used for:

* Chatbots
* Question Answering
* Text Generation
* Summarization
* Translation

Examples:

* GPT
* Gemini
* Llama
* Claude

---

# How Transformers Are Used in the Cashback Assistant

## Sentence Transformer

Model:

```
sentence-transformers/all-MiniLM-L6-v2
```

Purpose:

* Understand document chunks
* Generate embeddings
* Enable semantic search with FAISS

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

Purpose:

* Understand retrieved context
* Perform reasoning
* Generate natural language responses

Pipeline:

```
Question
+
Retrieved Context
        ↓
Transformer LLM
        ↓
Generated Answer
```

---

# Complete RAG Architecture

```
Knowledge Base
        ↓
Chunking
        ↓
Sentence Transformer (Encoder)
        ↓
Embeddings
        ↓
FAISS Vector Search
        ↓
Relevant Chunks
        ↓
Gemini 2.5 Flash (Generative LLM)
        ↓
Answer
        ↓
FastAPI Response
```

---

# Interview Questions

### Why were Transformers introduced?

Transformers were introduced to overcome the limitations of RNNs and LSTMs, such as sequential processing and difficulty handling long-range dependencies. They use Self-Attention to process all words in parallel, making them faster and more effective.

---

### What is Self-Attention?

Self-Attention is a mechanism that allows each word in a sentence to evaluate the importance of every other word in the same sentence, helping the model understand context and relationships.

---

### What is the difference between an Encoder and a Decoder?

An Encoder is designed to understand text and convert it into meaningful representations such as embeddings.

A Decoder is designed to generate text based on the provided context.

---

### Which Transformer models are used in this project?

* Sentence Transformer (all-MiniLM-L6-v2) for embedding generation and semantic search.
* Gemini 2.5 Flash for reasoning and answer generation.

---

# Key Takeaways

* Transformers replaced RNNs and LSTMs.
* Self-Attention is the core mechanism behind Transformers.
* Encoder models understand text.
* Decoder models generate text.
* Sentence Transformers create embeddings.
* Gemini generates responses.
* Both models work together in a Retrieval-Augmented Generation (RAG) pipeline.
