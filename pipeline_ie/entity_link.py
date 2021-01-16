from collections import defaultdict
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker


class EntityLink:

    def __init__(self, nlp, linkage_mode, data):
        self.sents = data
        self.nlp = nlp
        self.linkage_mode = linkage_mode

    def umls_entlink(self):
        """
        Add UMLS entity linker and abbreviation detector to spaCy pipeline_ie
        """
        abbreviation_pipe = AbbreviationDetector(self.nlp)
        self.nlp.add_pipe(abbreviation_pipe)
        linker = EntityLinker(resolve_abbreviations=True, name="umls")
        self.nlp.add_pipe(linker)

    def spacy_entlink(self):
        """
        Extracts entities for given list of text using spacy entity linker.

        :return:
            - sents: list
            - entities: dict
        list of sentences and a dictionary where key is the sentence number and value its corresponding list of entities
        """
        entities = defaultdict(list)
        count = 0
        for sentence in self.sents:
            doc = self.nlp(sentence)
            ents = [ent for ent in doc.ents]
            entities[str(count)] = ents
            count += 1
        return self.sents, entities

    def entity_linkage(self):
        if self.linkage_mode == "umls":
            self.umls_entlink()
            return self.spacy_entlink()
        elif self.linkage_mode == "spacy":
            return self.spacy_entlink()
