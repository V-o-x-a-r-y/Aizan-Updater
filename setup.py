from setuptools import setup, find_packages

setup(
    name='Aizan-Updater',
    version='1.0.0',
    author='Isaac Allard',
    author_email='isaac.allard@voxary.site',
    description='Updater for Aizan',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/V-o-x-a-r-y/Aizan-Updater',
    license='MIT',
    packages=find_packages(exclude=['tests', 'docs']),
    install_requires=[
        'requests',
        'json',  # Note: 'json' is part of the Python standard library and does not need to be listed as a separate dependency.
        'concurrent.futures',
        'tqdm',
    ],
)
