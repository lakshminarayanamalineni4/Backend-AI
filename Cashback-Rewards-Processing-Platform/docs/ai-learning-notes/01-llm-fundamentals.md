# LLM Fundamentals

## Overview

Large Language Models (LLMs) are advanced deep learning models trained on massive amounts of text data. They are designed to understand, generate, summarize, translate, and answer questions using natural language.

Examples of popular LLMs include:

* GPT (OpenAI)
* Gemini (Google)
* Claude (Anthropic)
* Llama (Meta)

---

## Why Are LLMs Important?

LLMs enable applications such as:

* Chatbots
* Virtual Assistants
* Code Generation
* Text Summarization
* Translation
* Question Answering
* Content Creation

In this project, an LLM will be used to generate intelligent responses for the Cashback Assistant.

---

## How Does an LLM Work?

An LLM learns patterns from large amounts of text during training.

Instead of memorizing answers, it learns relationships between words, phrases, and concepts.

At inference time, the model predicts the most probable next token based on the provided context.

Example:

Input:

I drink coffee in the

Possible Prediction:

morning

The model generates responses one token at a time until the answer is complete.

---

## What Are Tokens?

LLMs do not process complete sentences directly.

Text is broken into smaller units called tokens.

Example:

Sentence:

I love cashback rewards

Tokens:

["I", "love", "cashback", "rewards"]

The number of tokens determines:

* Input size
* Output size
* Model cost
* Context window usage

---

## Transformer Architecture

Modern LLMs are based on the Transformer architecture.

Key advantages:

* Processes text efficiently
* Understands long-range relationships
* Supports parallel computation
* Uses self-attention mechanisms

Transformers have become the foundation of modern Generative AI systems.

---

## Common Capabilities of LLMs

* Text Generation
* Summarization
* Translation
* Question Answering
* Sentiment Analysis
* Code Generation
* Conversational AI

---

## Limitations of LLMs

### Outdated Knowledge

The model only knows information available during training.

### Hallucinations

The model may generate confident but incorrect responses.

### No Real-Time Business Data

The model does not automatically know company-specific information.

### Context Window Limitations

The amount of information processed in a single request is limited.

These limitations are one of the reasons why RAG systems are used.

---

## LLM Usage in This Project

The Cashback Assistant will use an LLM to:

* Answer customer questions
* Explain cashback policies
* Provide campaign information
* Respond using retrieved business knowledge

The LLM will not directly rely on training data alone.

Instead, it will receive relevant information through a RAG pipeline.

---

## Interview Questions

### What is an LLM?

A Large Language Model is a deep learning model trained on massive text datasets to understand and generate human-like language.

### How does an LLM generate responses?

It predicts the most probable next token based on the given context and previously generated tokens.

### What are tokens?

Tokens are the basic units of text processed by an LLM.

### What is a Transformer?

A Transformer is a neural network architecture that uses self-attention mechanisms to process and understand language efficiently.

### What are the limitations of LLMs?

* Outdated knowledge
* Hallucinations
* Lack of domain-specific information
* Context window limitations
