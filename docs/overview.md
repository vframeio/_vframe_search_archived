# Overview

The VFrame Search system is designed to let researchers gain insight into a large amount of image and video data, especially when researchers' time is limited and there is too much video to be looked at manually.  To this end, we have designed a system that uses neural networks to search images qualitatively, using activations from the "last layer in the network" as a feature vector which offers a metric of image similarity based on content.  Thus a network trained to see cars should offer different results than one trained on scene similarity.  Furthermore, it offers a testbed for new neural networks based on image content trained on [synthetic data](https://vframe.io/research/synthetic-datasets/), which is the other half of this project.

We offer a variety of pre-trained models in our model zoo, taken from various sources online.  More information can be found by browsing the model zoo on the running sytem.


## Usage

To the user, the system should be operated in the following order (similar to the steps in the (quick start guide)[../README.md]).

- Media is added to the system
- Pre-trained neural network models are downloaded
- Features are extracted using these models
- These features are then indexed
- Indexes are then searchable through the interface

The system has four major components, which we will touch on:

- Web-based frontend: search, index, and dashboard
- Flask backend: RESTful API for talking to MySQL and communicating with workers
- Celery worker: performs indexing and other long tasks
- Commandline interface: running tasks, processing images, and integrating into other tasks.

## Web frontend

The web frontend offers an intuitive way to search images using other images, as well as monitoring other aspects of the system.  The frontend is built using React, which allowed us to make reusable components efficiently, and Redux to manage data flow and application state.

### Search

The search engine allows access to a variety of indexed features, which can be used to search by image.  Images can be uploaded.  Search by a random image from the database is also avaiable.  Starting from a single image, you can browse the database either by searching on search results, or by viewing the rest of the video frames when the result comes from a video.  As the models used can be quite large, only one feature can be used at a time to perform searches.

### Collections

Images found in search can be added to a collection, which offers a starting point for an investigation.  Collections can be exported as a ZIP file, which will contain all the images in the collection, a report written in Markdown, the Markdown rendered as HTML, and a JSON file containing the same information in a more machine-friendly format.

### Model Zoo

The Model Zoo contains all the models currently incorporated.  Feature indexes should be created from the models you are interested in.

### Dashboard

The dashboard offers an overview of the running system, including the size of the database and the quantity of material therein, as well as running background tasks, allowing you to monitor long-running index jobs in realtime.


## Backend

### RESTful API

The frontend communicates with a backend server written in Python using the Flask framework.  The server offers a RESTful API to handle ingesting image uploads, running searches, and talking to the database.  Read more about [API documentation](api.md).

### Disk-based media datastore

All media is stored on disk in a hashtree-based directory store.

### MySQL database

Contains a list of all the media in the system, user collections, as well as current indexes.  Used to store progress when generating features.

### Redis datastore

Used for communicating with running workers.

### Celery workers

Perform long-running background tasks, such as downloading models and building feature indexes.

### Feature indexes

We currently support three types of nearest-neighbor indexes, though more may be added in the future.

- Flat indexes keep all vectors in memory and are adequate for small datasets (less than 100K images)
- [FAISS](https://github.com/facebookresearch/faiss) indexes also live in memory, but use optimization techniques to scale up to millions of images.
- [ANNOY](https://github.com/spotify/annoy) is a disk-based vector store, which is suitable when RAM is at a premium.

### Commandline interface

Most of the low-level functionality is accessible through the CLI.  Read more about [commands](commands.md).

