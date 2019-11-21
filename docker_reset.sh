#!/bin/bash

docker-compose down
rm -rf data_store/docker/redis/*
rm -rf data_store/docker/mysql/*
rm -rf data_store/features/*
rm -rf data_store/indexes/*
mv data_store/media/* data_store/incoming/

docker volume rm vframe_search_datastore
docker volume rm vframe_search_mysql
docker volume rm vframe_search_redis
