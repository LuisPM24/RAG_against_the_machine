*This project has been created as part of the 42 curriculum by lupalomi*

# Description
A `RAG`, which stand for **Retrieval-Augmented Generation**, or in spanish **Recuperación Aumentada de Generación**, is a pattern that implements `parametric memory` and `Non parametric memory` learnt by the model during its training plus an external index that is queried at the time.

A RAG system is divided in two parts: "**Indexing**" and "**Retrieval and Generation**"

<div align="center">
    <img src="./assets/rag_diagram.png" />
</div>

The final quality depends far more on the recovery than on the model.

### Types of memory
As it's been said, the pattern will implement two kinds of memory:

- **Parametric memory**: What the model learnt during training and which has been encoded in its parameters. It is fast, always available, and cannot be directly accessed or corrected.

- **Non parametric memory**: An external index that is consulted in real time. It can be updated, audited and cited.

### Why non parametric memory changes the problem?
When you move the knowledge out of the model, its possible to update the sources wihtout training, the answer can be quoted and its possible control the access if an user doesn't have the correct permissions.

### When is it useful to implement a RAG system?
A RAG system is only useful when **information is constantly changing**, **the model has not identified the desired knowledge** or **it is necessary to cite the source of a statement**.

### When is it not useful to implement a RAG system?
A RAG system is not useful when **the output format is too specific**, **a repetitive task with many examples**, **the model doesn't understand the prompt** or **when the given documents are too small**.

## Indexing

### Chunking Strategy

## System Architecture

## Retrieval Method

## Performance Analysis

## Design Decisions

## Challenges Faced

## Example Usage

# Instructions

# Resources

## Libraries and tools
- [Python Fire](https://github.com/google/python-fire)
- [TQDM](https://github.com/tqdm/tqdm)

## Indexing
⚠️ ​*Since my main language is spanish, many of these links are from spaniards websites* ⚠️​

- [How create a RAG system with your own documents](https://underc0de.org/guias/inteligencia-artificial/como-crear-un-sistema-rag-con-documentos-propios/)
- [What's an index in RAG data bases and how optimise it?](https://dinogeek.me/ES/RAG/Que-es-un-indice-en-las-bases-de-datos-RAG-y-como-optimizarlo.html)
