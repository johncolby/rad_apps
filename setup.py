from setuptools import find_packages, setup

setup(
    name='rad_apps',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'air_download @ git+https://github.com/johncolby/air_download',
        'Flask',
        'Flask-Bootstrap',
        'Flask-Mail',
        'Flask-WTF',
        'WTForms[email]',
        'gunicorn',
        'python-dotenv',
        'redis',
        'rpy2',
        'rq',
        'pandas',
        'pydicom'
    ]
)
