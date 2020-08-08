from setuptools import find_packages, setup

setup(
    name="discord-rpc-mpris",
    version="1.0.0",
    scripts=["discord-rpc-mpris.py"],
    author="Rayzr522",
    url="https://github.com/RayzrDev/discord-rpc-mpris",
    install_requires=[
        "pycairo>=1.19.1",
        "dbus-python>=1.2.4",
        "pypresence>=1.0.9",
        "pygobject>=3.28.3",
    ],
)
