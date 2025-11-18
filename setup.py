"""Setup script for Legend AI (legacy support)."""

from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Add CLI-specific requirements
cli_requirements = [
    'typer[all]>=0.12.0',
    'rich>=13.7.0',
    'pyyaml>=6.0.1',
]

setup(
    name='legend-ai',
    version='1.0.0',
    description='Professional trading pattern scanner and analysis platform',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Legend AI Team',
    author_email='contact@legend-ai.com',
    url='https://github.com/Stockmasterflex/legend-ai-python',
    packages=find_packages(include=['app', 'app.*', 'legend_cli', 'legend_cli.*']),
    install_requires=requirements + cli_requirements,
    extras_require={
        'tui': ['textual>=0.47.0'],
        'dev': [
            'pytest==8.4.2',
            'pytest-asyncio==1.3.0',
            'pytest-cov==6.0.0',
            'mypy==1.13.0',
            'black>=23.0.0',
            'ruff>=0.1.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'legend=legend_cli.main:app',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Environment :: Console',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
