# VFRAME Search Engine

VFrame Search is an image search engine integrating neural networks for indexing and object detection.  It is designed to fit into an automated content ingestion workflow to allow for efficient search and indexing of a continuous stream of incoming media.  As such it is built out of the following components:

- Web-based frontend: search, index, and dashboard
- Flask backend: RESTful API for talking to MySQL and also for running jobs
- Celery worker: performs indexing and other long tasks
- Commandline interface: running tasks, processing images, and integrating into other tasks.

## Quick Start

### 1. Run the Docker daemon and migrate the database

After installing Docker and docker-compose, clone this repo and spin up the Docker containers:

```
git clone https://github.com/adamhrv/vframe_search
cd vframe_search
docker-compose up --build -d
docker-compose logs -f
docker exec -it vframe_search_api_1 python cli_db.py upgrade head
```

Navigate to `http://0.0.0.0:5000/` to use the webapp.  The remaining quick-start links point at your local endpoint.

### 2. Import your images

The folder `data_store/incoming/` is shared with the VFrame Search API instance, so you must move files there first before you can import them.

```
cp -r ~/Downloads/keyframes_1k/ data_store/incoming/
docker exec -it vframe_search_api_1 python cli_data.py add -i ../data_store/incoming/
```

Images are copied into the database and the originals are left in the incoming folder, so please `rm -rf data_store/incoming/*` if you don't need the original archives.

### 3. Build feature indexes

To get started, first download some pre-trained image classification models from our model zoo, e.g.:

* [BVLC AlexNet at 224px on Imagenet](http://0.0.0.0:5000/modelzoo/caffe_bvlc_alexnet_imagenet/show/)

Next, [create a new feature vector](http://0.0.0.0:5000/feature/new/) for each of these networks.

Finally, navigate to the [Task Manager](http://0.0.0.0:5000/task/) and click "update index" to begin processing the vectors.

### 4. Search your database

Once processing completes, you are ready to begin using the [search engine](http://0.0.0.0:5000/search/).

## Documentation

- [Overview](docs/overview.md) - a brief look at the system
- [API](docs/api.md) - about our RESTful API
- [Commandline interface](docs/commands.md) - about commandline scripting
- [Model zoo](docs/modelzoo.md) - about our model zoo
- [Docker setup](docs/docker.md) - notes on installing with Docker
- [Manual setup](docs/setup.md) - notes on installing everything locally
- [Version history](docs/version-history.md) - changelog

## About this project

For more information, please see our website at [vframe.io](https://vframe.io).
