import setuptools

with open("README.md", "r") as fh:
    _LONG_DESCRIPTION = fh.read()


setuptools.setup(
    name="lint",
    version="0.0.1",
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(),
    zip_safe=False,
    install_requires=["gamla", "toolz"],
    entry_points={
        "console_scripts": [
            "static-analysis=lint.static_analysis:main",
            "make-api-doc=lint.make_api_doc:main",
        ],
    },
    include_package_data=True,
)
