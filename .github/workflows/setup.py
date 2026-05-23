"""
setup.py — CampusFind Package Configuration
Used by the CD pipeline to build a Python wheel artifact.
"""
from setuptools import setup, find_packages

setup(
    name="campusfind",
    version="1.0.0",
    description="CampusFind Smart Campus Lost and Found System",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MissDidiza",
    python_requires=">=3.11",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "fastapi>=0.111.0",
        "uvicorn>=0.29.0",
        "pydantic>=2.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=9.0.0",
            "httpx>=0.27.0",
            "pytest-cov>=5.0.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Framework :: FastAPI",
    ],
)
