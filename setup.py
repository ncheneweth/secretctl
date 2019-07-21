import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awssm",
    version="0.0.1",
    author="Nic Cheneweth",
    author_email="nic.cheneweth@thoughtworks.com",
    description="Command-line tool to interact with aws secrets management service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncheneweth/awssm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=['invoke', 'boto3', 'pyyaml', 'requests'],
    entry_points={
        'console_scripts': ['awssm = awssm.main:program.run']
    }
)