#!/bin/bash
docker exec -it $(docker-compose ps | tail -1 | cut -d' ' -f 1) /bin/bash
