2024-12-16 — professional-development-day!
==========================================

# focus — embeddings and vector-searching

on this page...
- goal
- why
- out of scope
- concept overview
- plan
- work

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

I gave the use-case reason above, that common key-word searches on "climate change" won't return documents about "global warming". Solr, the indexer we use for many search applications, does have smarts: it'll break out tokens and lemmatize, so that a search on "jumping" will find relevant documents that don't contain the word "jumping", but do contain the words "jump", "jumped", or "jumps". But it won't return items that are about "hopping" or "leaping".


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


## Work


### Get starting data

hmm... there's not a unified Theses and Dissertations collection, rather, it starts by discipline, then within that there's a Theses and Dissertations collection.

I probably could do a solr search to sort of unify all of theses, but for now will just focus on AmCiv theses and dissertations, from [here](https://repository.library.brown.edu/studio/collections/bdr:en3cza8s/).

Ok, for now I'll just start with the abstracts (and titles), since one query returns those.

Code [here](https://github.com/birkin/vector_search_experimentation/blob/main/a__get_starting_data.py).

---

### Populate the sqlite-db

Code [here](https://github.com/birkin/vector_search_experimentation/blob/main/b__populate_db.py).

As an aside, a while ago I watched a video of someone doing something wih sqlite, and the person was able to click right on the db-file and view it from vscode. 

Just did an extension-search, and there are a _bunch_ of such extensions. I just installed the free [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer), and am evaluating it. 

Downsides: 
- read-only
- a subtle ad (I hate ads, but this isn't intrusive)

Upsides: 
- really enjoying being able to easily skim the contents of the db.

Hmm... can I use it to query the db via sql? I see filters where I can type in text, but not where I can type sql queries.

---


### Build the full-text search FTS5 table

FTS5 is an extension for SQLite that provides full-text search capabilities ("FTS" for "full-text-searching"; the "5" is the fifth-iteration of the tool).

In my iterative fashion, I'll copy the original table and then perform the update.

Code [here](https://github.com/birkin/vector_search_experimentation/blob/main/c__add_FTS.py).

Not fully working yet.

I can run these queries:

```
sqlite> 
sqlite> select rowid from fts_amciv_abstracts where abstract match 'poetry' limit 10;
28
sqlite> 
sqlite> select rowid from fts_amciv_abstracts where abstract match 'race' limit 10;
2
8
13
14
15
20
25
26
30
37
sqlite> 
```

...and then from inspecting the regular table see that, eg, id `28` is about `poetry` -- but the instructions make it seem I should be able to query like:

```
sqlite> select rowid, abstract, rank from fts_amciv_abstracts where abstract match 'race' limit 10;
```

...but that yields:

```
Runtime error: no such column: T.id
```

Gotta track that down, but am pausing.

(After I get this working, the next step is the embeddings and vectors!)

---

(end of file)

---
