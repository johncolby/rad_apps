FROM continuumio/miniconda3

# Setup ubuntu packages
RUN apt update
RUN apt install -y build-essential dcm2niix curl libcurl4-openssl-dev libssl-dev libxml2-dev

# Setup R
RUN echo "deb https://cloud.r-project.org/bin/linux/debian buster-cran35/" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
RUN apt update && apt install -y r-base
RUN R -e "install.packages(c('neurobase', 'tidyverse', 'remotes', 'git2r', 'bookdown'), repos = 'http://cran.us.r-project.org')"
RUN R -e "remotes::install_github('johncolby/dcmclass', upgrade='never')"

# Setup python
RUN conda install python=3.7
RUN conda install -c conda-forge gdcm
COPY requirements.txt ./
RUN /bin/bash -c 'pip install -r requirements.txt'
