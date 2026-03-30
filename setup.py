from setuptools import setup, find_packages

setup(
    name='webpeek',
    version='1.1.0',
    description='OSINT CLI tool for web reconnaissance',
    author='JorgeRosbel',
    author_email='jorge@rosbel.dev',
    url='https://github.com/JorgeRosbel/webpeek',
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
        'playwright>=1.40',
        'pyee>=10.0',
        'greenlet>=3.0',
    ],
    entry_points={
        'console_scripts': [
            'webpeek=webpeek.cli:cli',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
