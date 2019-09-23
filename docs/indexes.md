# Indexes

VFRAME can index any of the classification models in the model zoo. Detection models are currently only used for visualization. This is temporary as we are developing new object models for cluster munition detection.

## Download some models

- Download GoogLeNet trained on ImageNet: `python cli_models.py download -m caffe_bvlc_googlenet_imagenet`
- Download AlexNet trained on ImageNet: `python cli_models.py download -m caffe_bvlc_alexnet_imagenet,`
- Download all available detection and classification models: `python cli_models.py download --all` (might take a while)


## Add some media

This will import all images in a folder into the database:

```
python cli_data.py add -i '../data_store_local/keyframes_1k/' --no-check
```

## Tell VFRAME which feature types to index

Run the Flask server:

```
python cli_flask.py run
```

Visit the Model Zoo to see which models are downloaded: <http://127.0.0.1:5000/modelzoo/>

Models can be indexed if they are (a) downloaded and have valid (b) layers and (c) dimensions in the Model Zoo yaml.

Next, add the model here so it will be indexed: <http://127.0.0.1:5000/features/new/>

## Build the indexes

Finally, run these three scripts to build the indexes:

```
python cli_data.py extract
python cli_data.py index
```

Restart the Flask server and the first index will be loaded.  Test it out on <http://127.0.0.1:5000/search/> :)

## Commands

### cli_data.py add

| Parameter    | Description                    |
| ------------ | ------------------------------ |
| -i           | Directory to add               |
| --no-check   | Disable image validity check (makes import much faster) |

Add a folder of images to the database.  Folder is indexed recursively.

### cli_data.py extract

Loads all indexed feature types from the database, then extracts the feature vectors.  Model must be downloaded already.

### cli_data.py index

Index all feature vectors using the index defined in the database (flat, faiss, annoy)

