# Command line interface

The VFrame Search application comes with various scripts for accessing the indexing and image processing functions.  These scripts were developed using [Click](https://click.palletsprojects.com/en/7.x/). Wrapper scripts live inside `cli/` and the commands themselves are in `cli/app/commands/`.  Scripts should be run within the Conda environment (loaded by default inside Docker) from the `cli/` directory.  All commands can be run using `--help` for more information.

## CLI Commands

Commands dealing with data import, export, and indexing.  Normally the scripts should be run in this order: add, extract, index.  Extract and index are also available through the website.

### data add

| Parameter    | Description                    |
| ------------ | ------------------------------ |
| --input DIR  | Directory to add               |
| --no-check   | Disable image validity check (makes import much faster) |

Copies a folder of images into the database.

### data export

| Parameter       | Description                    |
| --------------- | ------------------------------ |
| --collection ID | Collection ID                  |

Export a collection as a ZIP file containing all media.

### data extract

Extract feature vectors based on the currently configured [feature types](http://0.0.0.0:5000/feature/).

### data index

Rebuild all feature vector indexes.

### data query

Runs a test query using media from the database.


## db.py

Manages running database migrations.  This is simply a copy of the [Alembic CLI script](https://alembic.sqlalchemy.org/en/latest/api/commands.html).  These are the most important commands for development:

### db.py upgrade head

Upgrade the database to the latest migration.

### db.py current

Show current migration.

### db revision --autogenerate -m 'message'

Create a new migration automatically, based on changes to the models.


## docs

Helper scripts for generating documentation.

### docs routes

Generates (API documentation)[api.md].


## flask

Commandline interface for Flask.  Mainly used for running the development server.  More information exists on [Flask's documentation](https://flask.palletsprojects.com/en/1.1.x/cli/).

### flask run

Runs the web server.  Background tasks not enabled.

### flask socket

Runs the web server with socket support.  Background tasks accessible.

### flask routes

Print Flask's URL routing table.


## image

### image features

| Parameter     | Description                    |
| ------------- | ------------------------------ |
| --input DIR   | Input folder of images         |
| --output FILE | Output .pkl file         |
| --model NAME  | Name of model from the Model Zoo |

Converts directory of images to feature vectors.  Deprecated.


## models

### models download

| Parameter    | Description                    |
| ------------ | ------------------------------ |
| --all        | Download all models         |
| --model NAME | Download a specific model from the Model Zoo |
| --no-model   | Skips pretrained model file  |
| --no-config  | Skips model config file  |
| --no-labels  | Skips labels file |

Download DNN models.  A full list of models can be found by running this script with `--help`.

### models layers

| Parameter    | Description                    |
| ------------ | ------------------------------ |
| --model      | Download a specific model from the Model Zoo |

Print DNN layer info to find feature vector layer.

### models pbtxt_graph

| Parameter     | Description                    |
| ------------- | ------------------------------ |
| --input FILE  | Path to frozen .pb  |
| --output FILE | Path to output .pbtxt  |
| --config FILE | Path to TF config |
| --type TYPE   | Type of network |

Creates OpenCV DNN specific graph .pbtxt

### models pbtxt_labelmap

| Parameter     | Description                    |
| ------------- | ------------------------------ |
| --input FILE  | Path to label map .pbtxt  |
| --output FILE | Path to output text file |

Convert TF pbtxt label map to label lines txt

### models sync

| Parameter    | Description                    |
| ------------ | ------------------------------ |
| --model NAME | Sync a specific model |
| --all        | Sync all models |
| --list       | List models and exit |

Sync models to S3 storage.

### models test

| Parameter    | Description                    |
| ------------ | ------------------------------ |
| --model NAME     | Name of model |
| --action ACTION  | Action to verify (verify, props, features, infer) |
| --image FILE      | Path to image to test classification or inference |

Test ModelZoo models.


## simple

Simple image search (deprecated) using models from our model zoo.  For more information, see (simple-search.md)[simple-search.md].
