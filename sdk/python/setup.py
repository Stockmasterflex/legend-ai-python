"""
Setup script for Legend AI Python SDK
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="legend-ai",
    version="1.0.0",
    author="Legend AI",
    author_email="support@legend-ai.com",
    description="Professional Python SDK for Legend AI Trading Pattern Scanner API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Stockmasterflex/legend-ai-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
        ],
    },
    keywords="trading stocks patterns technical-analysis finance api-client",
    project_urls={
        "Bug Reports": "https://github.com/Stockmasterflex/legend-ai-python/issues",
        "Source": "https://github.com/Stockmasterflex/legend-ai-python",
        "Documentation": "https://github.com/Stockmasterflex/legend-ai-python/blob/main/docs/guides/python-sdk.md",
    },
)
