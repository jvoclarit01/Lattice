---
name: skill-rag
description: RAG (Retrieval-Augmented Generation) systems best practices. Use when building RAG applications, document QA systems, or knowledge retrieval systems. Covers vector databases, chunking strategies, retrieval methods, and generation optimization.
---

# RAG Domain

RAG (Retrieval-Augmented Generation) systems best practices.

## When to Activate

Activate when building:
- Document QA systems
- Knowledge retrieval systems
- RAG applications
- Chat with your data systems

## Core Principles

1. **Quality Retrieval** — Garbage in, garbage out
2. **Effective Chunking** — Balance context and precision
3. **Semantic Search** — Use embeddings for relevance
4. **Generation Quality** — Optimize for accurate responses

## Architecture

```
┌─────────────┐
│   Documents │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Chunking   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Embeddings  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Vector Store │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Retrieval  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Generation  │
└─────────────┘
```

## Chunking Strategies

### Fixed-Size Chunking
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

chunks = text_splitter.split_documents(documents)
```

### Semantic Chunking
```python
from langchain_experimental.text_splitter import SemanticChunker

text_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile",
)

chunks = text_splitter.create_documents([text])
```

### Document-Based Chunking
```python
# Chunk by natural document boundaries
# (paragraphs, sections, chapters)
```

## Vector Databases

### Pinecone
```python
import pinecone

pinecone.init(api_key="your-api-key", environment="us-east-1")
index = pinecone.Index("my-index")

index.upsert(
    vectors=[
        ("vec1", [0.1, 0.2, 0.3], {"text": "sample text"}),
    ]
)

results = index.query(
    vector=[0.1, 0.2, 0.3],
    top_k=5,
    include_metadata=True,
)
```

### ChromaDB
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("my_collection")

collection.add(
    documents=["sample text"],
    embeddings=[[0.1, 0.2, 0.3]],
    metadatas=[{"source": "doc1"}],
    ids=["doc1"],
)

results = collection.query(
    query_embeddings=[[0.1, 0.2, 0.3]],
    n_results=5,
)
```

### Weaviate
```python
import weaviate

client = weaviate.Client("http://localhost:8080")

client.data_object.create(
    data_object={
        "text": "sample text",
        "vector": [0.1, 0.2, 0.3],
    },
    class_name="Document",
)

results = client.query.get(
    "Document",
    near_vector={"vector": [0.1, 0.2, 0.3]},
    limit=5,
)
```

## Retrieval Methods

### Semantic Search
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings(),
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5},
)
```

### Hybrid Search
```python
# Combine semantic and keyword search
from langchain.retrievers import BM25Retriever, EnsembleRetriever

bm25_retriever = BM25Retriever.from_documents(chunks)
vector_retriever = vectorstore.as_retriever()

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5],
)
```

### Reranking
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

compressor = CohereRerank(top_n_results=5)
reranker = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever,
)
```

## Generation

### Basic RAG
```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)

result = qa_chain("What is the main topic?")
```

### Conversational RAG
```python
from langchain.chains import ConversationalRetrievalChain

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=OpenAI(),
    retriever=retriever,
)

result = qa_chain({
    "question": "What is the main topic?",
    "chat_history": [],
})
```

### Custom Prompt
```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""Use the following pieces of context to answer the question at the end.

Context: {context}

Question: {question}

Answer:""",
    input_variables=["context", "question"],
)

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
)
```

## Best Practices

### Chunking
- Use appropriate chunk size (500-1500 tokens)
- Include overlap (10-20%)
- Consider document structure
- Test different strategies

### Retrieval
- Use semantic search for relevance
- Consider hybrid search for precision
- Implement reranking for quality
- Adjust top-k based on use case

### Generation
- Provide clear context
- Use appropriate prompts
- Include source citations
- Handle edge cases

### Evaluation
```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_relevancy,
)

result = evaluate(
    dataset=eval_dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_relevancy,
    ],
)
```

## Common Patterns

### Multi-Document RAG
```python
# Retrieve from multiple document collections
retrievers = [
    vectorstore1.as_retriever(),
    vectorstore2.as_retriever(),
]

ensemble = EnsembleRetriever(
    retrievers=retrievers,
    weights=[0.5, 0.5],
)
```

### Hierarchical RAG
```python
# Retrieve at different levels of granularity
# (document, section, paragraph)
```

### Agentic RAG
```python
# Use agents to decide retrieval strategy
from langchain.agents import initialize_agent, Tool

tools = [
    Tool(
        name="Search",
        func=retriever.get_relevant_documents,
        description="Search for relevant documents",
    ),
]

agent = initialize_agent(
    tools,
    llm=OpenAI(),
    agent="zero-shot-react-description",
)
```

## Resources

- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering)
- [LlamaIndex RAG Guide](https://docs.llamaindex.ai/en/stable/getting_started/concepts.html)
- [RAGAS Evaluation](https://github.com/explodinggradients/ragas)
