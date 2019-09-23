# Setup

Note: There are many updates happening. No need to file an issue as we are already aware of many issues and are working to update the repo.


## Docker Installation

This is the recommended way. See [docker.md](Docker setup guide) to install Docker and Docker Compose on your system. Then run:

- `docker-compose up;  # starts docker`
- `docker-compose down;  # stops docker`

Accces docker images while running:

- TODO

## Conda Installation

Dependencies can also be installed on your system using conda and npm.

### Python environment

```
conda env create -f environment.yml
conda activate vframe_search
```

### Node environemnt

```
npm install
npm run build
```

### MySQL

Log into MySQL as root: `mysql -u root` and create a database.  Put the appropriate values in `.env`.

```
CREATE USER 'vframe_search'@'localhost' IDENTIFIED BY 'a very secure password';
CREATE DATABASE vframe_search;
GRANT ALL PRIVILEGES ON vframe_search TO 'vframe_search'@'localhost';
```

### Redis and Celery

Run the celery command from inside `cli/`.

```
python `which celery` worker -A app.tasks.celery --loglevel=info -E
redis-server /usr/local/etc/redis.conf
```

### Run web app

With socket support:

```
python cli_flask.py socket
```

Without socket support:

```
python cli_flask.py run
```

Then open `http://127.0.0.1:5000/`
