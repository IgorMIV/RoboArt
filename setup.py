from setuptools import setup, find_packages

setup(name='roboart',
        version='0.0.5',
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