import textacy
import pandas as pd
from textacy import extract


class InformationExtraction:

    def __init__(self, nlp, sentence_list, entities):
        self.nlp = nlp
        self.sentence_list = sentence_list
        self.entities = entities

    def triplet_extraction(self):
        """
        Given a list of sentences and dictionary of entities for particular sentences,
        this function firstly extracts tuple based on Subject Verb Object rule using textaCy,
        resolves the subject and object with the original entity by using list of entities obtained through
        entity linker and noun phrases and returns the dataframe of sentences and its respective triplets.

        :return
         - df: Dataframe
                Dataframe having column of Sentences and column of Triplets.

                As a sentence contain multiple triplets, the column of Triplets will be a list of multiple
                lists, each being a triplet, where the 0th index contains the subject, 1st index the predicate
                and the 2nd index the object.
        """
        sentence_list = self.sentence_list
        entities = self.entities
        count = 0
        df = pd.DataFrame(columns=['Sentences', 'Triplet'])
        for sentence in sentence_list:
            doc = self.nlp(sentence)
            text_ext = textacy.extract.subject_verb_object_triples(doc)
            tuples = self.get_triplet(text_ext)
            ent_list = entities[str(count)]
            tups = []
            for triple in tuples:
                if not ent_list:
                    tups.append(triple)
                    continue
                chunk = textacy.extract.noun_chunks(doc)
                for noun_chunk in chunk:
                    ent_list.append(noun_chunk)
                ents = {e.start: e for e in ent_list}
                try:
                    ent_subj_dict = {k: len(v.text) for k, v in ents.items() if
                                     (triple[0].text in v.text) and (triple[0].start in range(v.start, v.end + 1) and
                                                                triple[0].end in range(v.start, v.end + 1))}
                    ent_subj_index = max(ent_subj_dict, key=ent_subj_dict.get)
                    ent1 = ents[ent_subj_index]
                    ent_obj_dict = {k: len(v.text) for k, v in ents.items() if
                                    (triple[2].text in v.text) and (triple[2].start in range(v.start, v.end) and
                                                               triple[2].end in range(v.start, v.end + 1))}
                    ent_obj_index = max(ent_obj_dict, key=ent_obj_dict.get)
                    ent2 = ents[ent_obj_index]
                except:
                    continue
                tups.append([ent1, str(triple[1]), ent2])
            count += 1
            df.at[count, 'Sentences'] = str(sentence)
            df.at[count, 'Triplet'] = tups
        return df

    @staticmethod
    def get_triplet(text_ext):
        for i in text_ext:
            yield i
