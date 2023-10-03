FROM ubuntu

RUN apt-get update && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update

# Install the other dependencies
RUN apt-get install -y git curl gcc build-essential

# Install tzdata non-iteractively
# https://stackoverflow.com/questions/44331836/apt-get-install-tzdata-noninteractive/44333806#44333806
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

# Install the Python versions
RUN apt install -y python2 python2-dev && \
    apt install -y python3.7 python3.7-dev python3.7-venv && \
    apt install -y python3.8 python3.8-dev python3.8-venv && \
    apt install -y python3.9 python3.9-dev python3.9-venv && \
    apt install -y python3.10 python3.10-dev python3.10-venv && \
    apt install -y python3.11 python3.11-dev python3.11-venv && \
    apt install -y python3.12 python3.12-dev python3.12-venv

# Make Python 3.12 the default `python`
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 10

# Get pip
RUN python -m ensurepip --upgrade

ADD requirements.txt requirements.txt

# Install benchmarking dependencies
RUN python -m pip install -r requirements.txt

# Work around https://bugs.launchpad.net/ubuntu/+source/tzdata/+bug/1899343, which messes with `moment`
RUN echo "Etc/UTC" | tee /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Clone the upstream. If you want to use your local copy, run the container with a volume that overwrites this.
RUN git clone https://github.com/closeio/ciso8601.git && \
    chmod +x /ciso8601/benchmarking/run_benchmarks.sh

WORKDIR /ciso8601/benchmarking
ENTRYPOINT ./run_benchmarks.sh
