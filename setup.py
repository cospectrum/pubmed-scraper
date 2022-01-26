from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='pubmed-scraper',
    version='1.0',
    license='MIT',
    description='PubMed scraper',
    long_description=long_description,
    author='Alexey Severin',
    install_requires=requirements,
    keywords=['pubmed', 'scraper'],
)
