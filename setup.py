import setuptools

with open("README.md", "r") as fh:
    _LONG_DESCRIPTION = fh.read()


setuptools.setup(
    name="lint",
    version="1",
    python_requires=">=3.11",
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(),
    zip_safe=False,
    install_requires=["gamla"],
    entry_points={
        "console_scripts": [
            "static-analysis=lint.static_analysis:main",
            "make-api-doc=lint.make_api_doc:main",
            "format-csv=lint.format_csv:main",
            "format-assistant-configuration=lint.format_assistant_configuration:main",
            "validate-triplets=lint.validate_triplets:main",
        ],
    },
    include_package_data=True,
)
