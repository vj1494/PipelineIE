from stanza.server import CoreNLPClient
import pandas as pd
import neuralcoref
from pipeline_ie.config import Config
import time

class Coref:

    def __init__(self, nlp, coref_mode, data, coref_output=False):
        self.nlp = nlp
        self.coref_mode = coref_mode
        self.data = data
        self.coref_output = coref_output
        self.configuration = Config()

    def input_data(self):
        """
        Create a list of text from the column of given DataFrame.

        NOTE: Any processing if required to be done on sentences can be written here.

        :return:
            - list_text: list
                list of sentences
        """
        col_name = self.configuration.config.get('file_directory', 'input_column_name')
        list_text = self.data[col_name].astype(str).tolist()
        return list_text

    @staticmethod
    def coref_output_file(texts):
        """
        Write output after coreference resolution on given text to a csv file.
        :param texts: list
                list of texts.
        """
        df_coref_resolved = pd.DataFrame(texts, columns=['Coref_Resolved_Text'])
        df_coref_resolved.to_csv('Text_Coref.csv')

    @staticmethod
    def create_phrase(mention, ann):
        """
        Create a list of tokens for given mention
        :param mention: mention object
        :param ann: annotation object
        Annotation object contains all mentions and coref chains for given text
        :return:
            - phrase: list
            phrase is a list containing all tokens for the given mention
        """
        phrase = []
        for i in range(mention.beginIndex, mention.endIndex):
            phrase.append(ann.sentence[mention.sentenceIndex].token[i].word)
        return phrase

    def corenlp_coref_resolution(self, memory, timeout, properties):
        """
        Perform coreference resolution on given text using Stanford CoreNLP
        :param
            - memory: str
            - timeout: int
            - properties: dict
        :return:
            - texts: list,
                List of sentences resolved and unresolved by coreference resolution operation.
        """

        # Start CoreNLP Server with required properties
        with CoreNLPClient(pipeline='StanfordCoreNLP', timeout=timeout, memory=memory,
                           properties=properties) as client:
            texts = self.input_data()
            index = 0
            time.sleep(10)
            for text in texts:
                doc = self.nlp(text)
                modified_text = [sentence.string.strip() for sentence in doc.sents]
                # submit the request to the server
                ann = client.annotate(text)
                # In each chain, replace the anaphora with the correct representative
                for coref in ann.corefChain:
                    mts = [mention for mention in coref.mention]
                    representative = coref.representative
                    phrase_rep = self.create_phrase(mts[coref.representative], ann)
                    antecedent = ' '.join(word for word in phrase_rep)
                    check_rep = 0
                    for mention in coref.mention:
                        if check_rep == representative:
                            check_rep += 1
                            continue
                        phrase = self.create_phrase(mts[check_rep], ann)
                        anaphor = ' '.join(word for word in phrase)
                        anaphor = anaphor + ' '
                        antecedent = antecedent + ' '
                        modified_text[mention.sentenceIndex] = modified_text[mention.sentenceIndex].replace(anaphor,
                                                                                                            antecedent)
                        check_rep += 1
                modified_text = ' '.join(modified_text)
                texts[index] = modified_text
                index += 1
        if self.coref_output is True:
            self.coref_output_file(texts)
        return texts

    def neural_coref_resolution(self):
        """
        Perform coreference resolution operation on given text using neuralcoref.
        Supports domain specific coreference resolution as per the spacy model used.

        :return:
            - texts: list,
                List of sentences resolved and unsresolved by coreference resolution operation.
        """
        coref = neuralcoref.NeuralCoref(self.nlp.vocab)
        self.nlp.add_pipe(coref, name='neuralcoref')
        texts = self.input_data()
        for index, text in enumerate(texts):
            doc = self.nlp(text)
            texts[index] = doc._.coref_resolved
        if self.coref_output is True:
            self.coref_output_file(texts)
        return texts

    def coref_resolution(self):
        """
        Execute coreference resolution methodology as per the coref mode mentioned either explicitly or implicitly.
        :return:
            - texts: list.
        """
        if self.coref_mode == "corenlp":
            properties = self.configuration.corenlp_coref_props()
            params = self.configuration.corenlp_params()
            memory, timeout = params[0], params[1]
            texts = self.corenlp_coref_resolution(memory, timeout, properties)
        elif self.coref_mode == "neuralcoref":
            texts = self.neural_coref_resolution()
        return texts
