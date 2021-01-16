import configparser

def write_config_file(corenlp_home, folder_dir, file_name, col_name):
    config = configparser.ConfigParser()
    config['environment_variables'] = {}
    config['environment_variables']['CORENLP_HOME'] = corenlp_home
    config['file_directory'] = {'input_file_dir': folder_dir,
                                'input_file': file_name,
                                'input_column_name': col_name}
    config['corenlp_coref_props'] = {'annotators': 'coref',
                                     'algorithm': 'neural'}
    config['corenlp_params'] = {'timeout': '60000',
                                'memory': '4G'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def sent_segmentation(texts, nlp):
    """
    It takes text as input and returns list of sentences.

    :param texts: list
    :param nlp: spaCy model
    :return: text_to_sentences: lis
    """
    text_to_sentences = []
    for text in texts:
        doc = nlp(text)
        sentences = [sentence.string.strip() for sentence in doc.sents]
        text_to_sentences.extend(sentences)
    return text_to_sentences
