from setuptools import setup, find_packages

setup(
    name='gandalf-python-sdk',
    version='0.0.2',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'ariadne-codegen==0.13.0',
        'click==8.1.7',
        'ecdsa==0.19.0',
        'httpx==0.27.0',
        'pydantic==2.7.4',
        'pydantic_core==2.18.4',
        'requests==2.28.2',
        'websockets==12.0',

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
