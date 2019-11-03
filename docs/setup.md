# Setup

There are two ways of running the VFrame Search application: you can use Docker, or you can install everything by hand.  Following setup, please refer to steps 2-4 in the [README.md](../README.md).

## Manual Installation

Dependencies can also be installed on your system manually.

### Python environment

```
conda env create -f environment.yml
conda activate vframe_search
```

### Node environemnt

We developed the frontend using Node v10 (LTS).  We recommend using `nvm` to manage your local Node installation.

```
npm install
npm run build
```

### MySQL

Log into MySQL as root: `mysql -u root` and create a database. Corresponding settings should be put in the file `.env` in the root directory of the repo.  Please see the file `.env-sample` for a template.

```
CREATE USER 'vframe_search'@'localhost' IDENTIFIED BY 'a very secure password';
CREATE DATABASE vframe_search;
GRANT ALL PRIVILEGES ON vframe_search TO 'vframe_search'@'localhost';
```

### Redis and Celery

The Redis server can be run as a daemon, or manually using `screen(1)`.  Run the Celery command from inside `cli/`.

```
python `which celery` worker -A app.tasks.celery --loglevel=info -E
redis-server /usr/local/etc/redis.conf
```

### Run web app

With socket support:

```
python cli_flask.py socket
```

Without socket support (background indexing disabled):

```
python cli_flask.py run
```

Then open `http://127.0.0.1:5000/`
