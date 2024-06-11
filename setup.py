from setuptools import setup, find_packages

setup(
    name='gandalf-python-sdk',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'ariadne-codegen',
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'eyeofsauron=eyeofsauron.cli:cli',
        ],
    },
    package_data={
        '': ['*.graphql', '*.yml'],
    },
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gandalf-network/gandalf-sdk-python',
    author='gandalf.network',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
