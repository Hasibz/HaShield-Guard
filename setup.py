import os
from setuptools import setup, find_packages

setup(
    name="hashield-guard", 
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "sentence-transformers",
        "transformers",
        "torch"
    ],
    author="Md. Hasib Ur Rahman",
    author_email="your.email@example.com", 
    description="A mathematical, zero-latency prompt injection and AUP guardrail.",
    # The fix is right here:
    long_description=open('README.md', encoding='utf-8').read() if os.path.exists('README.md') else '',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)