from setuptools import setup, find_packages


URL = 'https://github.com/cospectrum/pubmed-scraper.git'

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='pubmed-scraper',
    version='0.1.0',
    license='MIT',
    url=URL,
    description='PubMed scraper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alexey Severin',
    install_requires=requirements,
    packages=find_packages(),
    keywords=['pubmed', 'scraper'],
)
