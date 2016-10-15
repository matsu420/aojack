from setuptools import setup, find_packages

setup(
        name = "aojack",
        version = "0.1",
        packages = ['aojack'],
        entry_points = {
            'console_scripts': [
                'aojack = aojack.main:aojack'
                ]
            },
        )
