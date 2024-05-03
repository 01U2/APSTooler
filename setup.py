import setuptools

with open("Readme.md") as f:
    if f is not None:
        readme = f.read()

setuptools.setup(
    name="APSTooler",
    version="0.0.1",
    author="Olufemi Akinwumi",
    description="A Python toolkit for Autodesk Platform Services",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/01U2/APSTooler.git",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["Autodesk", "APS", "forge", "Python"],
    license= "LICENSE",
    packages=setuptools.find_packages(where="APSTooler"),
    python_requires=">=3.9",
    install_requires=['requests']
)
