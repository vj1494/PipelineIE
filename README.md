# PipelineIE
PipelineIE is an Information Extraction Pipeline primarily based on spaCy that lets you extract information from free text and provides the flexibility to run general to domain specific pipeline like the biomedical domain for information extraction.

Currently the pipeline extracts information in the form of triplets and consists of Coreference Resolution ([Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) / [neuralcoref](https://github.com/huggingface/neuralcoref)) >> Entity Linking ([spaCy](https://spacy.io/) / [ScispaCy](https://github.com/allenai/scispacy) / custom spaCy model) >> Triplet  Extraction (Currently Subject - Verb - Object Rule using [textaCy](https://github.com/chartbeat-labs/textacy)).


How does it help? / What problem does it solve?
1. It is important to resolve coreferences in the text before entities and triplets can be extracted so that they contain the original entities rather than pronouns.
2. Usually, the subject and object does not represent the complete entity (which can be a sequence of many words) and might only represent a substring of the original entity. The Entity Linker in the pipeline helps to solve this problem while extracting triplets.
3. Finally, in a few lines, anyone can extract triplets from text using the default pipeline or the biomedical pipeline, taking care of the above 2 problems, and use their custom pipeline making it easy to try different options on the input data.


## Installation

Install [neuralcoref](https://github.com/huggingface/neuralcoref) from source as mentioned below (referenced from their github repo)
```bash
venv .env
source .env/bin/activate
git clone https://github.com/huggingface/neuralcoref.git
cd neuralcoref
pip install -r requirements.txt
pip install -e .
```

Optional:
Download and unzip [CoreNLP 4.2.0](http://nlp.stanford.edu/software/stanford-corenlp-latest.zip) if CoreNLP has to be used for coreference resolution.

Install PipelineIE
```bash
git clone https://github.com/vj1494/PipelineIE.git
cd pipeline_ie
python setup.py build
python setup.py install
```

## Usage
Biomedical Pipeline

```python
from pipeline_ie.pipeline_ie import PipelineIE

text = "Co-culture of NK cells with transfected EC enhanced E-selectin, IL-8, and NF-kappaB-dependent promoter activity."

#Biomedical PipelineIE
#Default Biomedical Pipeline uses ScispaCy en_core_sci_lg model
#Same model is used for neuralcoref, entity linkage and triple extraction 
#pipeline_ie="default" uses spacy en model
pie = PipelineIE(text, pipeline="biomedical")

#Returns a dataframe
df = pie.pipeline_triplet()

```

## Additional Usage and Example
Please refer to the [example]() for Additional Usage.

## License
[MIT](https://choosealicense.com/licenses/mit/)
