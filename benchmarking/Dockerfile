FROM ubuntu

RUN apt-get update && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update

# Install the Python versions
RUN apt install -y python python-dev && \
    apt install -y python3.5 python3.5-dev python3.5-venv && \
    apt install -y python3.6 python3.6-dev python3.6-venv && \
    apt install -y python3.7 python3.7-dev python3.7-venv && \
    apt install -y python3.8 python3.8-dev python3.8-venv && \
    apt install -y python3.9 python3.9-dev python3.9-venv && \
    apt install -y python3.10 python3.10-dev python3.10-venv

# Install the other dependencies
RUN apt-get install -y git curl gcc build-essential

# Make Python 3.10 the default `python`
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 10

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
