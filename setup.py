from setuptools import setup, find_packages

setup(
    name='Score Board',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        'attrs',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'scoreboard = dune_tournament_scoreboard.cli.main:scoreboard',
        ],
    },
)
