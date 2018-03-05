from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as readme:
    long_description = readme.read()


setup(
    name='mvmedia',
    version='1.0.0',
    license='MIT',
    description='Safely move photos and videos',
    long_description=long_description,
    url='https://github.com/samiconductor/move-media',
    author='Sam Simmons',
    author_email='sam@samiconductor.com',
    classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Unix',
            'Intended Audience :: System Administrators',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Utilities',
            'Topic :: System :: Systems Administration',
    ],
    keywords='cli media',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.4',
    install_requires=[
        'exifread',
        'python-magic'
    ],
    extras_require={
        'dev': ['readme_renderer', 'wheel', 'twine']
    },
    entry_points={
        'console_scripts': [
            'mvmedia=move_media:main'
        ],
    },
    project_urls={
        'Source': 'https://github.com/samiconductor/move-media'
    },
)
