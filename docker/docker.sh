#!/bin/bash

# Build the image
echo "Building Docker image..."
docker build -t my-tkinter-app .

# Run the container
echo "Starting application..."
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $(pwd):/app \
    my-tkinter-app