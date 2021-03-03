#!/usr/bin/env bash

case $* in
    rebuild )
        docker-compose down; sleep 2; docker-compuse up -d
        ;;
    shell )
        docker exec -it $(docker-compose ps | tail -1 | cut -d' ' -f 1) /bin/bash
        ;;
    start )
        docker-compose up -d
        ;;
    stop )
        docker-compose down
        ;;
    logs )
        docker-compose logs
        ;;
    tlogs )
        docker-compose logs -f --tail 100
        ;;
    status )
        docker-compose ps
        ;;
    "" )
        echo 'PyLudus control, usage: ./pyludus [command]'
        echo ''
        echo 'start         start the PyLudus docker container'
        echo 'stop          stop the PyLudus docker container'
        echo 'status        show the status of PyLudus docker container'
        echo 'shell         start a shell in the docker container'
        echo 'rebuild       rebuild the docker containers'
        exit 1
esac