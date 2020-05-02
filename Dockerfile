FROM continuumio/miniconda3

# Setup ubuntu packages
RUN apt update
RUN apt install -y build-essential dcm2niix curl libcurl4-openssl-dev libssl-dev graphviz texlive-xetex ghostscript pandoc pandoc-citeproc

# Setup FSL
ENV FSLDIR /usr/local/fsl
RUN curl -O https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py
RUN /usr/bin/python2 fslinstaller.py -d ${FSLDIR} -q
ENV FSLOUTPUTTYPE NIFTI_GZ
ENV PATH ${FSLDIR}/bin:${PATH}
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$FSLDIR

# Setup R
ARG GIT_TOKEN
RUN echo "deb http://cran.us.r-project.org/bin/linux/debian buster-cran35/" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
RUN apt update && apt install -y r-base
RUN R -e "install.packages(c('neurobase', 'tidyverse', 'oro.dicom', 'remotes', 'dplyr', 'tibble', 'tidyr', 'purrr', 'readr', 'stringr', 'rlang', 'tidytext', 'tm', 'caret', 'glue', 'remotes', 'git2r', 'xgboost', 'bookdown'), repos = 'http://cran.us.r-project.org')"
RUN R -e "remotes::install_git('https://git.radiology.ucsf.edu/jcolby/dcmclass.git',    credentials=git2r::cred_token('GIT_TOKEN'), upgrade='never')"
RUN R -e "remotes::install_git('https://git.radiology.ucsf.edu/jcolby/ucsfreports.git', credentials=git2r::cred_token('GIT_TOKEN'), upgrade='never')"

# Setup python
RUN conda install python=3.7
RUN conda install -c conda-forge gdcm
COPY requirements.txt ./
RUN /bin/bash -c 'pip install -r requirements.txt'

# Add fonts
ARG FONT_PATH
RUN mkdir -p /usr/local/share/fonts/truetype/
COPY $FONT_PATH /usr/local/share/fonts/truetype/
RUN fc-cache -f -v

# Add Flask app files
COPY model.Rdata ./

# Setup environment
ENV TZ America/Los_Angeles