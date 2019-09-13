FROM continuumio/miniconda3

# Setup ubuntu packages
RUN apt update
RUN apt install -y build-essential r-base dcm2niix curl libcurl4-openssl-dev libssl-dev graphviz texlive-xetex ghostscript pandoc pandoc-citeproc

# Setup python
RUN conda install python=3.7
ARG GIT_TOKEN
COPY requirements.txt ./
RUN /bin/bash -c 'pip install -r requirements.txt'

# Setup FSL
ENV FSLDIR /usr/local/fsl
RUN curl -O https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py
RUN /usr/bin/python2 fslinstaller.py -d ${FSLDIR} -q
ENV FSLOUTPUTTYPE NIFTI_GZ
ENV PATH ${FSLDIR}/bin:${PATH}
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$FSLDIR

# Setup R
ENV TAR /bin/tar
RUN R -e "install.packages(c('neurobase', 'tidyverse', 'oro.dicom', 'remotes', 'dplyr', 'tibble', 'tidyr', 'purrr', 'readr', 'stringr', 'rlang', 'tidytext', 'tm', 'caret', 'glue', 'remotes', 'git2r', 'xgboost'), repos = 'http://cran.us.r-project.org')"
RUN R -e "remotes::install_git('https://git.radiology.ucsf.edu/jcolby/dcmclass.git',    credentials=git2r::cred_token('GIT_TOKEN'), upgrade='never')"
RUN R -e "remotes::install_git('https://git.radiology.ucsf.edu/jcolby/ucsfreports.git', credentials=git2r::cred_token('GIT_TOKEN'), upgrade='never')"

# Add fonts
ARG FONT_PATH
RUN mkdir -p /usr/local/share/fonts/truetype/
COPY $FONT_PATH /usr/local/share/fonts/truetype/
RUN fc-cache -f -v

# Add Flask app files
WORKDIR /app
COPY app app
COPY model.Rdata rad_apps.py config.py ./

# Setup environment
ENV TZ America/Los_Angeles