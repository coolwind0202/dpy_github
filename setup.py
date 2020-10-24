from setuptools import setup

requires = []
with open("requirements.txt") as f:
    requires = f.read().splitlines()

setup(
    name="dpy_github",
    packages=["dpy_github"]
    author="coolwind0202",
    version="1.0.0",
    url="https://github.com/coolwind0202/dpy_github",
    python_requires=">=3.5.3",
    install_requires=requires,
    license="MIT"   
)
