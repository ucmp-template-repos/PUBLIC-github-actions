
# Base image
FROM python:3.10.4
LABEL MAINTAINER="neochae"

# Make working directory
RUN mkdir /source
WORKDIR /source

# Copy files into image
COPY . /source

# Image settings
ENV LC_ALL C.UTF-8
ENV LANG =C.UTF-8
ENV PYTHONPATH /source

# Run action
ENTRYPOINT ["/source/entrypoint.sh"]
