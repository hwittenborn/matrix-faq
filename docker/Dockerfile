# To build this image, run the following command from the root of the repository:
#
#    docker build ./ -f docker/Dockerfile
#

FROM ubuntu:focal

# Install needed dependencies
RUN apt-get update
RUN DEBIAN_FRONTENT=noninteractive apt-get install python3 \
                                                   python3-requests \
                                                   python3-markdown \
                                                   python3-sqlalchemy \
                                                   python3-yaml -y

# Copy over source files
COPY "./src/" "/usr/local/share/matrix-faq/"

# Set working directory to /data, as we want to place configuration data there.
WORKDIR "/data/"

ENTRYPOINT ["/usr/local/share/matrix-faq/main.py"]
