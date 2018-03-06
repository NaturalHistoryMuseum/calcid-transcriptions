
from pip.req import parse_requirements
from setuptools import setup

install_requirements = parse_requirements('./requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='api',
    version='0.1',
    description='MLM Transcription API',
    author='Ben Scott',
    author_email='ben@benscott.co.uk',
    packages=['api'],
    install_requires=requirements,
    entry_points={}
)
