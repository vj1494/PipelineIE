import pandas as pd
import os
from pipeline_ie.config import Config
from pathlib import Path


class DataLoader:

    def __init__(self, input_data):
        self.config = Config().config
        self.input = input_data

    def check_input(self):
        try:
            if self.input == "csv":
                return "csv"
            elif self.input == "xlsx":
                return "xlsx"
            else:
                return "text"
        except Exception as e:
            print("Error {}").format(e)

    def load_files(self, flag):
        """
        Reads all files from the given input directory/Read given text/Read text from given xlsx or csv file
        and create a dataframe for the same.

        NOTE: ALl files need to be in either xlsx or csv format and need to have a column name as set in config.ini

        :return: DataFrame with column of Sentences
        """
        col_name = self.config.get('file_directory', 'input_column_name')
        if flag == "text":
            input_text = {col_name: [self.input]}
            df_text = pd.DataFrame(input_text)
        elif self.config.get('file_directory', 'input_file') != 'NA':
            input_file = self.config.get('file_directory', 'input_file')
            flag = Path(input_file).suffix
            if flag == ".csv":
                df_text = pd.read_csv(input_file)
            if flag == ".xlsx":
                df_text = pd.read_excel(input_file)
        else:
            dir_name = self.config.get('file_directory', 'input_file_dir')
            list_files = os.listdir(dir_name)
            list_df = []
            for file in list_files:
                file_path = os.path.join(dir_name, file)
                if flag == "xlsx":
                    df = pd.read_excel(file_path, usecols=[col_name], index_col=None, header=0)
                elif flag == "csv":
                    df = pd.read_csv(file_path, usecols=[col_name], index_col=None, header=0)
                list_df.append(df)
            df_text = pd.concat(list_df, axis=0, ignore_index=True)
        return df_text

    def get_sentences(self):
        """
        Getter to get a DataFrame having sentences from all files in a column named Sentences
        :return: DataFrame
        """
        flag = self.check_input()
        df_text = self.load_files(flag)
        return df_text
