from setuptools import setup

setup(
    name='octavious',
    packages=['octavious'],
    version='0.0.1',
    description='lightweight, modular parallelizing framework',
    author='Metglobal',
    author_email='kadir.pekel@metglobal.com',
    url='https://github.com/metglobal/octavious',
    extras_require={
        'celery_parallelizer': ["celery"]
    }
)
