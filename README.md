*This project has been created as part of the 42 curriculum by lupalomi*

# Description
A `RAG`, which stand for **Retrieval-Augmented Generation**, or in spanish **Recuperación Aumentada de Generación**, is a pattern that implements `parametric memory` and `Non parametric memory` learnt by the model during its training plus an external index that is queried at the time.

A RAG system is divided in two parts: "**Indexing**" and "**Retrieval and Generation**"

<div align="center">
    <img src="./assets/rag_diagram.png" />
</div>

The final quality depends far more on the recovery than on the model.

### Types of memory
As it been said, the pattern will implement two kinds of memory:

- **Parametric memory**: What the model learnt during training and which has been encoded in its parameters. It is fast, always available, and cannot be directly accessed or corrected.

- **Non parametric memory**: An external index that is consulted in real time. It can be updated, audited and cited.

## System Architecture

## Chunking Strategy

## Retrieval Method

## Performance Analysis

## Design Decisions

## Challenges Faced

## Example Usage

# Instructions

# Resources

## Indexing
⚠️ ​*Since my main language is spanish, these links are from spanish websites* ⚠️​

- [How create a RAG system with your own documents](https://underc0de.org/guias/inteligencia-artificial/como-crear-un-sistema-rag-con-documentos-propios/)
- [What's an index in RAG data bases and how optimise it?](https://dinogeek.me/ES/RAG/Que-es-un-indice-en-las-bases-de-datos-RAG-y-como-optimizarlo.html)