FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip cmake

# setup directory
RUN mkdir /api
ADD . /api
WORKDIR /api

# install py
RUN pip3 install -r requirements.txt

# cleanup packages for build
RUN apt-get purge -y cmake
RUN apt-get autoremove -y
RUN rm -rf /root/.cache/
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# images register
RUN python3 first_register.py

# run api server
CMD ["python3", "api_server.py"]