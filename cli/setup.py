"""
Setup script for Legend AI CLI
"""

from setuptools import setup

setup(
    name="legend-cli",
    version="1.0.0",
    description="Command-line interface for Legend AI Trading Pattern Scanner",
    author="Legend AI",
    author_email="support@legend-ai.com",
    py_modules=["legend-cli"],
    install_requires=[
        "httpx>=0.24.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "legend-cli=legend-cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
