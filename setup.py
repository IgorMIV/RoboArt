from setuptools import setup, find_packages

setup(name='khirolib',
        version='0.0.1',
        description='Library for robot painting',
        packages=find_packages(include=[
            'roboart',
            'roboart.*'
        ]),
        python_requires=">=3.6",
        install_requires=[
            'matplotlib'
        ]
)