from setuptools import setup, find_packages

with open("README.md", "r") as frm:
    long_description = frm.read()

setup(
    name="pipeline_ie",
    version="0.1.0",
    author="Vinit Jain",
    author_email="vj1494@gmail.com",
    description="A package that consists of a pipeline_ie to extract information like triplets from free text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_package/homepage/",
    packages=find_packages(),
    install_requires=['spacy==2.3.5',
                      'stanza==1.0.0',
                      'textacy==0.10.1',
                      'openpyxl==3.0.5',
                      'pandas',
                      'scispacy==0.3.0'
                     ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License"
                ],
    keywords=[
        'Natural Language Processing',
        'Named Entity Recognition',
        'Information Extraction',
        'Coreference Resolution',
        'Triple Extraction'
    ]
    )
