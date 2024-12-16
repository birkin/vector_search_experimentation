2024-12-16 — professional-development-day!
==========================================

# focus — embeddings and vector-searching

on this page...
- goal
- why
- out of scope
- concept overview
- plan

---


## Goal...

To get some hands-on experience with working with embeddings and vector-searching.

---


## Why...

As the website I'm using today puts it:

_"...The primary use-case for sqlite-vec and other vector search tools is to offer "semantic search" to text data. Full-text search (aka keyword search) alone doesn't always give great results — Queries like "climate change" won't return documents that say "global warming..."_ ([link](https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html))

---


## Out of scope (for now)

The process I'll go through, using a model to turn text into numbers representing meaning, can also work for images, using a multi-modal model. I'd love to experiment with that too -- maybe on the next professional-development day -- but will focus on text today.

---

## Concept overview


### use-case 

I gave the use-case reason above, that common key-word searches on "climate change" won't return documents about "global warming". Solr, the indexer we use for many search applications, does have smarts: it'll break out tokens and lemmatize, so that a search on "jumping" will find relevant documents that don't contain the word "jumping", but do contain the words "jump", "jumped", or "jumping". But it won't return items that are about "hopping".


### embeddings

_(thanks to chatgpt for helping draft this part)_

Embeddings are mathematical representations of data. They take complex data—like words, sentences, images, or even whole documents—and convert them into dense vectors (lists of numbers).

For example, the word "dog" might be represented as [0.1, 0.8, 0.5], while "puppy" might be [0.1, 0.75, 0.55]. These vectors are close to each other because "dog" and "puppy" are similar in meaning. Meanwhile, an unrelated word like "car" might have a completely different vector, such as [1.5, 0.2, 2.1].

Embeddings are created using machine-learning-models trained on massive datasets (like billions of web pages and books).


### vector-search

Embeddings (vectors) can be stored in a database or an index. So an initial step might be to take many text-documents, and for each:
- assign the document an id
- generate a looooong vector representing that document  

Then, when searching for something, an embedding for the query is generated -- and that query-embedding is compared to the stored embeddings. The matching process uses mathematical algorithms (like cosine similarity) to find the vectors that are closest -- which represent the data most similar in meaning to your query.

---


## Plan

I'll extract some theses and dissertation data from the BDR, and use it as the source-data for following the tutorial.

I'm going to go through a great writeup about using an extension to sqlite that enables it to handle embeddings and vector-search: <https://alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search/index.html>

---


## Getting starting data

hmm... there's not a unified Theses and Dissertations collection, rather, it starts by discipline, then within that there's a Theses and Dissertations collection.

I probably could do a solr search to sort of unify all of theses, but for now will just focus on AmCiv theses and dissertations, from [here](https://repository.library.brown.edu/studio/collections/bdr:en3cza8s/).

(end of file)

---
