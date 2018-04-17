# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    install_requires=[
        'scrapy-redis>=',
        'setuptools>=16.0',
    ],
    entry_points = {'scrapy': ['settings = scrapyredis.settings']},
)
