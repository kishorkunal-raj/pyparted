FROM ezee/docker_ubuntu_git_build_essential_autoconf_pkg_config_p7zip_curl

ENV DEBIAN_FRONTEND=nonintercative

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y git \
    python3 \
    python3-pip\
    gettext \
    libgettextpo-dev \
    python3-coverage \
    udev \
#    && git clone https://github.com/pykickstart/pykickstart \
#    && cd pykickstart \
    && apt-get clean
RUN pip3 install pocketlint
#WORKDIR /pykickstart
CMD ["/bin/bash"]
