from pipeline_ie.data_loader import DataLoader
from pipeline_ie.coref import Coref
from pipeline_ie.entity_link import EntityLink
from pipeline_ie.information_extraction import InformationExtraction
from pipeline_ie.utils import sent_segmentation, write_config_file
import spacy

class PipelineIE:

    def __init__(self, input_text="NA", file_name="NA", folder_dir="NA", col_name="NA", spacy_model=None, pipeline="default", coref_output=False,
                 config_file=False, corenlp_home="NA", properties={'coref': 'neuralcoref', 'entity_link': 'spacy', 'ie': 'triplet'}):
        """
        :param input_text: str
            Pass a string for raw text.
            If input consist of a single/multiple files, pass "csv" or "xlsx" as per the file format.
        :param file_name: str
            File Name to be passed if not mentioned in config ini file and config_file=False
        :param folder_dir: str
            File Directory to be passed if not mentioned in config ini file and config_file=False
        :param col_name: str
            Column Name to be passed if not mentioned in config ini file and config_file=False
        :param spacy_model: str
            Pass custom spaCy model.
        :param pipeline: str
            if pipeline_ie="default" the pipeline_ie with 'en' spaCy model will be executed.
            if pipeline_ie="biomedical" the pipeline_ie with 'en_core_sci_lg' scispaCy model will be executed and neuralcoref
            will also use the same biomedical model for coreference resolution.
        :param config_file: bool
            If configurations not added in config file and passed as parameters, pass config_file=False
        :param coref_output: bool
            Outputs a file of text after coreference operation if True.
        :param corenlp_home: str
            CORENLP_HOME dir location to be passed if not mentioned in config.ini and config_file=False
        :param properties: dict
            Consists of default pipeline_ie {'coref': 'neuralcoref', 'entity_link': 'spacy', 'ie': 'triplet'}
            In order to use corenlp's coreference resolution, use value 'corenlp' for key 'coref'
            In order to use umls entity linker, use value 'umls' for key 'entity_link'
        """
        self.input_text = input_text
        self.file_name = file_name
        self.folder_dir = folder_dir
        self.col_name = col_name
        self.spacy_model = spacy_model
        self.pipeline = pipeline
        self.coref_output = coref_output
        self.config_file = config_file
        self.corenlp_home = corenlp_home
        self.properties = properties

    def load_spacy_model(self):
        """
        Load spaCy model.
        If pipeline_ie is default, then select spaCy's 'en' model.
        If pipeline_ie is biomedical, then select scispaCy's 'en_core_sci_lg' model.
        A user can pass their custom spaCy model.
        :return: nlp object
                    spaCy's loaded model.
        """
        if self.spacy_model is not None:
            nlp = spacy.load(self.spacy_model)
        elif self.pipeline == "default":
            nlp = spacy.load('en')
        elif self.pipeline == "biomedical":
            nlp = spacy.load('en_core_sci_lg')
        return nlp

    def pipeline_triplet(self):
        """
        Executes Triplet Extraction pipeline_ie for biomedical, general purpose and custom domain.
        Triplet Extraction consists of pipeline_ie Coreference Resolution>>Entity Linking>>Triplet Extraction using SVO.
        :return: Dataframe
                    Dataframe having column of sentences and a column of Triplets as list of lists.
        """
        if self.config_file is False:
            write_config_file(self.corenlp_home, self.folder_dir, self.file_name, self.col_name)
        data_load = DataLoader(self.input_text)
        data = data_load.get_sentences()
        nlp = self.load_spacy_model()

        #Coref
        coref = Coref(nlp, self.properties['coref'], data, self.coref_output)
        texts = coref.coref_resolution()
        sentences = sent_segmentation(texts, nlp)

        #Entity Linking
        entity_link = EntityLink(nlp, self.properties['entity_link'], sentences)
        sentence, entities = entity_link.entity_linkage()

        #Triplet
        triplet_ext = InformationExtraction(nlp, sentence, entities)
        return triplet_ext.triplet_extraction()
