# Base image
FROM alpine:3.18.8
LABEL MAINTAINER="neochae"

# Copy files into image
RUN apk add --no-cache bash
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Run action
ENTRYPOINT ["entrypoint.sh"]
