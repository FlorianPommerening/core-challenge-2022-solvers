FROM ubuntu:20.04

#------------------------------------------------
# (1) install fundamental commands
#------------------------------------------------
RUN \
    apt update && \
    apt -y upgrade && \
    apt install -y curl git man unzip vim wget sudo

RUN DEBIAN_FRONTEND=noninteractive TZ="America/New_York" apt-get -y install tzdata

RUN apt install -y \
    build-essential \
    software-properties-common \
    g++ \
    curl \
    time

RUN apt install -y python3-pip
RUN pip3 install Cheetah3

#------------------------------------------------
# (2) clone the 2022solver directory to /
#------------------------------------------------
RUN git clone https://github.com/core-challenge/2022solver.git

# Also nab the benchmarks
RUN git clone https://github.com/core-challenge/2022benchmark.git /BENCHMARKS

# Grab the large queens file, since git doesn't seem to want to
RUN  wget --output-document /BENCHMARKS/benchmark/queen/queen200x200.col https://github.com/core-challenge/2022benchmark/blob/main/benchmark/queen/queen200x200.col?raw=true




#############################################
# build the cplex solver if available
#############################################

COPY ILOG_COS_20.10_LINUX_X86_64.bin /ILOG_COS_20.10_LINUX_X86_64.bin
ENV CPLEX_INSTALLER=/ILOG_COS_20.10_LINUX_X86_64.bin
ENV CPLEX_ROOT=/opt/ibm/ILOG/CPLEX_Studio201/

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        default-jre     \
        libgmp3-dev     \
        python3         \
        python3-distutils \
        unzip        && \
    rm -rf /var/lib/apt/lists/* && \
    ./$CPLEX_INSTALLER -DLICENSE_ACCEPTED=TRUE -i silent && \
    python3 $CPLEX_ROOT/python/setup.py install && \
    #rm -r $CPLEX_INSTALLER $CPLEX_ROOT && \
    rm -r $CPLEX_INSTALLER && \
    apt-get purge -y default-jre && apt -y autoremove


COPY custom/build /SOLVER
COPY custom/build/run.sh /2022solver/run.sh
COPY custom/utils.py /2022solver/utils.py


WORKDIR /2022solver
