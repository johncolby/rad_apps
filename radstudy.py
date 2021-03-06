import air_download.air_download as air
import argparse
import glob
import logging
import os
import pandas as pd
import pydicom
import shutil
import tempfile
import zipfile

from datetime import datetime

import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
pandas2ri.activate()


class RadStudy():
    def __init__(self, acc='', zip_path='', model_path='', download_url='',
                 cred_path='', process_url='', output_dir=''):

        self.zip_path = zip_path
        self.model_path = model_path
        self.dir_tmp = ''
        self.dir_study = ''
        self.channels = []
        self.series_picks = pd.DataFrame()
        self.acc = acc
        self.hdr = ''
        self.series = None
        self.study_date = ''
        self.app_name = ''
        self.download_url = download_url
        self.cred_path = cred_path
        self.process_url = process_url
        self.output_dir = output_dir
        # assert self.acc or self.zip_path, 'No input study provided.'

    def process(self):
        raise NotImplementedError

    def download(self):
        """Download study via AIR API"""

        assert not self.zip_path, '.zip path already available.'
        assert self.dir_tmp, 'Working area not setup yet.'
        args = argparse.Namespace()
        args.URL = self.download_url
        args.acc = self.acc
        args.cred_path = self.cred_path
        args.profile = -1
        args.output = os.path.join(self.dir_tmp, f'{self.acc}.zip')
        air.main(args)
        self.zip_path = args.output
        self._extract()
        self.setup()

    def _extract(self):
        """Extract study archive"""
        assert not self.dir_study, 'dir_study already exists.'
        dir_study = os.path.join(self.dir_tmp, 'dcm')
        os.mkdir(dir_study)
        zip_ref = zipfile.ZipFile(self.zip_path, 'r')
        zip_ref.extractall(path=dir_study)
        self.dir_study = os.path.join(dir_study, os.listdir(dir_study)[0])

    def setup(self):
        """Setup study for processing"""
        # Create table of series picks
        if self.series_picks.empty:
            self.series_picks = pd.DataFrame({'class': self.channels,
                                              'prob': '',
                                              'SeriesNumber': '',
                                              'series': ''})
        # Create temporary working directory
        if not self.dir_tmp:
            self.dir_tmp = tempfile.mkdtemp()
            os.mkdir(os.path.join(self.dir_tmp, 'nii'))
            os.mkdir(os.path.join(self.dir_tmp, 'output'))

        # Extract study archive
        if not self.dir_study and self.zip_path:
            self._extract()

        # Load representative DICOM headers
        if self.dir_study and not self.hdr:
            series_paths = glob.glob(f'{self.dir_study}/*')
            series_numbers = [self._get_series_number(series_path) for series_path in series_paths]
            self.series = pd.DataFrame({'SeriesNumber': series_numbers, 'path': series_paths})

            dcm_path = glob.glob(f'{self.dir_study}/*/*.dcm', recursive=True)[0]
            self.hdr = pydicom.read_file(dcm_path)
            self.acc = self.hdr.AccessionNumber
            self.study_date = datetime.strptime(self.hdr.StudyDate, '%Y%m%d').strftime('%m/%d/%Y')

    def classify_series(self):
        """Classify series into modalities"""
        ro.r['library']('dcmclass')
        ro.r['load'](self.model_path)

        self.series_picks = ro.r['predict_headers'](os.path.dirname(self.dir_study), ro.r['models'], ro.r['tb_preproc'])
        paths = [os.path.abspath(os.path.join(self.dir_study, series)) for series in self.series_picks.series.tolist()]
        self.series_picks['series'] = paths

    def add_paths(self, paths):
        """Manually specify directory paths to required series"""
        self.series_picks.series = paths

    def _get_series_number(self, series_path):
        dcm_path = glob.glob(f'{series_path}/*')[0]
        return pydicom.read_file(dcm_path).SeriesNumber

    def series_to_path(self, series):
        """Convert a SeriesNumber to path"""
        return self.series.loc[self.series['SeriesNumber'] == series, 'path'].values[0]

    def report(self):
        """Generate PDF report"""
        ro.r['library']('ucsfreports')
        params = ro.ListVector({'input_path': self.dir_tmp,
                                'patient_name': self.hdr.PatientName.family_comma_given(),
                                'patient_MRN': self.hdr.PatientID,
                                'patient_acc': self.hdr.AccessionNumber,
                                'study_date': self.study_date})
        ro.r['ucsf_report'](self.app_name, output_dir=os.path.join(self.dir_tmp, 'output'), params=params)

    def copy_results(self, output_dir='.'):
        src = os.path.join(self.dir_tmp, 'output')
        dest = os.path.join(self.output_dir, self.acc)
        assert not os.path.exists(dest), 'Output directory already exists.'
        shutil.copytree(src, dest)

    def __str__(self):
        s_picks = str(self.series_picks.iloc[:, 0:3]) if not self.series_picks.empty else ''
        s = ('Radiology study object\n'
             f'  Accession #: {self.acc}\n'
             f'  dir_tmp: {self.dir_tmp}\n'
             f'  Series picks:\n{s_picks}')
        return s

    def rm_tmp(self):
        """Remove temporary working area"""
        if not self.dir_tmp == '':
            shutil.rmtree(self.dir_tmp)
        else:
            print('Nothing to remove.')

    def run(self):
        try:
            self.setup()
            self.download()
            self.process()
            self.report()
            self.copy_results()
            self.rm_tmp()
        except:
            logging.exception('Processing failed.')
            self.rm_tmp()
