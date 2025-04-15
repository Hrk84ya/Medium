from setuptools import setup, find_packages

setup(
    name="medium-analysis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4==4.12.2",
        "lxml==4.9.3",
        "requests==2.31.0",
        "pandas==2.1.1",
        "numpy==1.24.3",
        "scikit-learn==1.3.1",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.2",
            "pytest-cov==4.1.0",
            "pytest-mock==3.11.1",
            "pytest-xdist==3.3.1",
            "coverage==7.3.2",
        ],
    },
    python_requires=">=3.8",
) 