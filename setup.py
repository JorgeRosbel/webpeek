from setuptools import setup, find_packages

setup(
    name='webpeek',
    version='1.0.0',
    description='OSINT CLI tool for web reconnaissance',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'click>=8.0',
        'requests>=2.28',
        'dnspython>=2.1',
        'Whois>=0.9',
        'beautifulsoup4>=4.9',
        'lxml>=4.6',
        'colorama>=0.4',
        'tldextract>=3.1',
        'pwntools>=4.0',
    ],
    entry_points={
        'console_scripts': [
            'webpeek=webpeek.cli:cli',
        ],
    },
    python_requires='>=3.8',
)
