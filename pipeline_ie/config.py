import os
from configparser import ConfigParser


def load_config():
    """
    Load Configurations from config.ini file located in the same directory
    :return: config object
    """
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
    return config


class Config:

    def __init__(self):
        """
        Load configurations from config.ini and call method to set env variables when an object will be instantiated.
        """

        self.config = load_config()
        self.set_env_var()

    def set_env_var(self):
        """
        Load and Set Enviornment Variables
        """

        list_env_vars = self.config.items('environment_variables')
        for env_var in list_env_vars:
            os.environ[env_var[0].upper()] = env_var[1]

    def corenlp_coref_props(self):
        """
        Load corenlp properties for coreference resolution.
        :return:
            - coref_props: dict
                A dictionary consisting of properties for executing coreference resolution annotator.
        """
        coref_props = self.config._sections['corenlp_coref_props']
        return coref_props

    def corenlp_params(self):
        """
        Load parameters required for executing Stanford CoreNLP pipeline_ie.
        :return:
            - memory: str
            - timeout: int
            RAM to be assigned to Stanford CoreNLP and timeout.
        """
        memory = self.config.get('corenlp_params', 'memory')
        timeout = self.config.getint('corenlp_params', 'timeout')
        return memory, timeout
