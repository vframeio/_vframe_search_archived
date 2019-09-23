# VFRAME Search Engine

Note: There are many updates happening. No need to file an issue as we are already aware of many issues and are working to update the repo.

## Quick Start

### 1. Run the Docker daemon

```
git clone https://github.com/adamhrv/vframe_search
cd vframe_search
docker-compose up --build
docker-compose up
docker-compose logs -f
```

Navigate to `http://0.0.0.0:5000/` to use the webapp.

### 2. Import your images

The folder `data_store/incoming/` is shared with the VFrame Search API instance, so you must move files there first before you can import them.

```
cp ~/Downloads/keyframes_1k/ data_store/incoming/  # or use your image dataset!
docker exec -it vframe_search_api_1 python cli_data.py add -i ../data_store/incoming/
```

Images are copied into the database and the originals are left in the incoming folder, so please `rm -rf data_store/incoming/*` if you don't need the original archives.

### 3. Build feature indexes

To get started, first download some pre-trained image classification models from our model zoo:

* [BVLC AlexNet at 224px on Imagenet](http://0.0.0.0:5000/modelzoo/caffe_bvlc_alexnet_imagenet/show/)
* [BVLC GoogleNet at 224px on Imagenet](http://0.0.0.0:5000/modelzoo/caffe_bvlc_googlenet_imagenet/show/)

Next, [create a new feature vector](http://0.0.0.0:5000/feature/new/) for each of these networks.

Finally, navigate to the [Task Manager](http://0.0.0.0:5000/task/) and click "update index" to begin processing the vectors.

### 4. Search your database

Once processing completes, you are ready to begin using the [search engine](http://0.0.0.0:5000/search/).

## Docs (in progress):

- [Getting started](docs/setup.md)
- [Setting up Docker](docs/docker.md)
- [Model zoo](docs/modelzoo.md)

--------

## Help Wanted

### Model Zoo

- Add descriptions, licenses, usage notes, and demo images for all current models

### Image Classification

- Locate and implement a Multi-class VOC Caffe model
- Locate other relevant .caffemodel and darknet .weights files

## Object Detection

- Locate other relevant .caffemodel and darknet .weights files

### Docker

- Improvements to docker entrypoints, setup, optioning
- Conform scripts to best practices
- Ensure compatibilty for OSX, Linux, Windows

