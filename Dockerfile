# ------------------------------------------------------
#
# VFRAME / VCAT Search Engine
# https://github.com/vframeio/vframe_search
#
# ------------------------------------------------------

FROM ubuntu:18.04

# [ Install system dependencies ]

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt upgrade -y
RUN apt-get update && apt-get install -y --no-install-recommends \
         build-essential \
         cmake \
         git \
         curl \
         vim \
         ca-certificates \
         python-qt4 \
         libjpeg-dev \
         zip \
         unzip \
         netbase \
         dnsutils \
         libpng-dev &&\
rm -rf /var/lib/apt/lists/*
RUN apt update

# [ env vars ]

ENV DOCKER_USER root
ENV USER_DIR /root
WORKDIR ${USER_DIR}

# [ Install Miniconda ]

ENV PYTHON_VERSION=3.7
RUN curl -o ${USER_DIR}/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ${USER_DIR}/miniconda.sh && \
     ${HOME}/miniconda.sh -b -p /opt/conda && \
     rm ${USER_DIR}/miniconda.sh && \
    /opt/conda/bin/conda install conda-build

ENV PATH=$PATH:/opt/conda/bin/

# [ install apt packages ]

RUN apt update && \
    apt install -y \
    nginx

# [ Install Node.js ]

WORKDIR ${USER_DIR}
ENV NODE_VERSION 10.15.3
ENV NVM_DIR ${USER_DIR}/.nvm
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
RUN . ${NVM_DIR}/nvm.sh && nvm install ${NODE_VERSION} && nvm alias default ${NODE_VERSION}
RUN ln -sf ${NVM_DIR}/versions/node/v${NODE_VERSION}/bin/node /usr/bin/nodejs
RUN ln -sf ${NVM_DIR}/versions/node/v${NODE_VERSION}/bin/node /usr/bin/node
RUN ln -sf ${NVM_DIR}/versions/node/v${NODE_VERSION}/bin/npm /usr/bin/npm

# [ build conda env ] 

ENV VFRAME_SEARCH_DIR vframe_search
WORKDIR ${USER_DIR}/${VFRAME_SEARCH_DIR}/
COPY environment.yml ${USER_DIR}/${VFRAME_SEARCH_DIR}/
RUN conda env create -f environment.yml
RUN echo "source activate vframe_search" > ~/.bashrc
ENV PATH /opt/conda/envs/vframe_search/bin:$PATH

# [ mysql ]

ENV MYSQL_DATABASE vframe_search

# [ Copy Frontend React app ]

COPY frontend ${USER_DIR}/${VFRAME_SEARCH_DIR}/frontend/
COPY package.json ${USER_DIR}/${VFRAME_SEARCH_DIR}/
COPY webpack.config.dev.js ${USER_DIR}/${VFRAME_SEARCH_DIR}/
COPY webpack.config.prod.js ${USER_DIR}/${VFRAME_SEARCH_DIR}/
COPY static ${USER_DIR}/${VFRAME_SEARCH_DIR}/static/
RUN npm install
RUN npm run build:production

# [ Copy Backend Python app ]

COPY cli ${USER_DIR}/${VFRAME_SEARCH_DIR}/cli/
COPY modelzoo ${USER_DIR}/${VFRAME_SEARCH_DIR}/modelzoo/

# [ Run Flask app ]

VOLUME "/root/vframe_search/data_store"

WORKDIR ${USER_DIR}/${VFRAME_SEARCH_DIR}/cli/
CMD ["/opt/conda/envs/vframe_search/bin/python", "cli_flask.py", "socket", "--host=0.0.0.0"]
