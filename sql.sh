#!/usr/bin/env bash
docker exec -i -e "PGPASSWORD=docker" pg10docker psql -U docker docker -c 'CREATE DATABASE data OWNER docker'
docker exec -i -e "PGPASSWORD=docker" pg10docker psql -U docker docker -c ''
