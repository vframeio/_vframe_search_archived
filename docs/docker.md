# Docker

## Known issues

Could not resolve 'archive.ubuntu.com' can be fixed by making the following changes:

- Uncomment the following line in `/etc/default/docker DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"`
- Restart the Docker service sudo service docker restart
- Delete any images which have cached the invalid DNS settings. Build again and the problem should be solved.
- Credit [Andrew SB](https://www.digitalocean.com/community/questions/docker-on-ubuntu-14-04-could-not-resolve-archive-ubuntu-com)


