from setuptools import find_packages, setup

setup(
    name='rad_apps',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'air_download @ git+https://git.radiology.ucsf.edu/jcolby/air_download.git#egg=air_download',
        'brats_preprocessing @ git+https://git.radiology.ucsf.edu/jcolby/brats_preprocessing.git#egg=brats_preprocessing[classify_series]',
        'Flask',
        'Flask-Bootstrap',
        'Flask-WTF',
        'python-dotenv',
        'redis',
        'rq',
    ]
)
