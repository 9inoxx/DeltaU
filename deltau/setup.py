from setuptools import setup, find_packages

setup(
    name="DeltaU",
    version="1.1.0",  # Version number
    author="Julian Fortis",
    description="A backtesting and performance analysis package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/9inoxx/deltau",  # URL to package repo
    packages=find_packages(where='deltau'),
    install_requires=[  # List of dependencies
        "pandas",
        "plotly",
        'nbformat>=4.2.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.7",  # Python version requirement
)
