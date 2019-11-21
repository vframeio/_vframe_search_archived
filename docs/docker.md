# Docker

## Docker Installation

This is the recommended way to run the VFrame Search application.  Docker is available from [www.docker.com](https://www.docker.com).


```
# Install docker-compose
pip install docker-compose

# Start Docker
docker-compose up

# Stop Docker
docker-compose down

# List running Docker containers
docker ps

# Get a shell on the running Docker
docker run -i -t --network vframe_search_dev --entrypoint /bin/bash vframe_search_api

# Remove inactive docker instances
docker system prune
```

Once Docker is running, please follow steps 2-4 from (README.md)[../README.md].

## Docker and MySQL

The first time you spin up the docker instance, the MySQL database will be empty, and takes a few seconds to initialize.  Therefore you must run the migration command to finish setting it up before you can start importing media.

```
docker exec -it vframe_search_api_1 python cli_db.py upgrade head
```

## Errata

Could not resolve 'archive.ubuntu.com' can be fixed by making the following changes:

- Uncomment the following line in `/etc/default/docker DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"`
- Restart the Docker service sudo service docker restart
- Delete any images which have cached the invalid DNS settings. Build again and the problem should be solved.
- Credit [Andrew SB](https://www.digitalocean.com/community/questions/docker-on-ubuntu-14-04-could-not-resolve-archive-ubuntu-com)
