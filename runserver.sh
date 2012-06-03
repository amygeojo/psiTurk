#!/bin/bash

LOCALHOST=0.0.0.0
PORT=8000
THREADS=4

exec gunicorn -w $THREADS -b "$LOCALHOST:$PORT" app:app
