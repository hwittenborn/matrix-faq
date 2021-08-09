FROM ubuntu

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y
RUN apt-get install python3 python3-requests python3-markdown python3-sqlalchemy python3-yaml -y

COPY "../src/" "/usr/local/share/matrix-faq/"

WORKDIR "/usr/local/share/matrix-faq/"

ENTRYPOINT ["/usr/localshare/matrix-faq/main.py"]
