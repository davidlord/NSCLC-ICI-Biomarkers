from pathlib import Path
from typing import Tuple
from datetime import datetime
from functools import reduce
import os
import re
import glob

import pandas as pd
from src.utils import prepare_save_folder, read_config

from preprocess import non_null_one_hotted, main_preprocess

DATA_FOLDER = Path("Modelling/data/preprocessed")

pan_cmpd_mut = ['ABL1','ATM','BRCA2','CARD11','CDC73','EPHA3','EPHA7','ASXL1','BCOR','BRIP1','CD79B','CIC','EPHA5','EPHB1','ERCC4','FLT3','HGF',' AK3','MDC1',
'MET','ERBB4','FGFR4','FOXL2','INHBA','MAX','MED12','MGA','MSH2','NFKBIA','NOTCH2','NUF2','PAX5','PIK3C2G','MRE11','NF2','NOTCH1','NTRK3','PARP1','PGR','PIK3C3',
'PIM1','PPM1D','PTPRD','STAT3','TET1','ZFHX3','PIK3CG','POLE','PPP2R1A','RET','TENT5C','TSC2']

DCB_muts = ['KRAS', 'POLE', 'POLD1', 'MSH2','TP53']

NDB_muts = ['EGFR', 'PTEN', 'STK11', 'KEAP1']


class Preprocessor:
    """Preprocess the data to be used with the models.

    Public methods:
    process -- Loads the data from file, processes it, and saves the results.

    Instance variables:
    config -- The preprocess config
    preprocessor_type -- The name of the preprocessor to use.
    """

    def __init__(self, config_path: Path) -> None:
        """Initialize the processor.

        Arguments:
            config_path -- The path to the configuration file.
        """
        self.config = read_config(config_path)
        self.preprocessor_type = self.config["preprocessor_name"]

    def _load_data(self) -> pd.DataFrame:
        """Load orignal data from disk."""
        self.data_paths = self.config["data_path"]
        clinical_file_name = 'data_clinical_patient.txt'
        sample_file_name = 'data_clinical_sample.txt'
        mutation_file_name = 'data_mutations.txt'
        def get_data_dirs(directory):
            data_dirs = []
            for entry in os.scandir(directory):
                if entry.is_dir():
                    data_dirs.append(entry.path)
                print("Data directories included:") 
            for i in data_dirs:
                print(i)
            return data_dirs
        def read_data(path_list, name, data_dict):
            for path in path_list:
            # Read clinical data files:
                file_path = os.path.join(path, name)
                if os.path.isfile(file_path):
                    df = pd.read_csv(file_path, header=0, delimiter='\t',comment='#')
                    data_dict[path] = df
                    print("Successfully read: " + file_path) 
        # Add column containing study name to each df
        def add_dataframe_name_column(dataframes_dict):
            for df_name in dataframes_dict:
                df = dataframes_dict[df_name]
                df['study_name'] =  os.path.basename(df_name)
        def remove_nonsense_rows(dataframes_dict):
            for df_name in dataframes_dict:
                df = dataframes_dict[df_name]
                df = df.iloc[4:]
                dataframes_dict[df_name] = df
        # Concatinate dataframes in dict into single dataframe: 
        def renaming_fun(x):
            if x.startswith("AGE"):
                return "Diagnosis_Age" # or None
            if x.startswith("SEX"):
                return "Sex"
            if x.startswith("SMOK"):
                return "Smoking_History"
            if x.startswith("PDL"):
                return "PD-L1_Expression"
            if x.endswith("BURDEN"):
                return "TMB"
            if x.startswith("DURABLE"):
                return "Treatment_Outcome"
            else:
                return x
        def concatinate_dfs(df_dict):
            dfs = []
            cols_list = []
            lst = []
            concat_dfs = []
            mylist = ['Patient_id','study_name','Sex','Histology','Age','TMB','PDL1','Smoking_history','smoking', 'smoker', 'nonsynonymous_mutation_burden', 'durable_clinical_benefit','Treatment','PFS']
            mylist_lower = [i.lower() for i in mylist] 
            for df in df_dict.values():
                dfs.append(df)
                for i in dfs:
                    cols_list.append(i.columns.tolist())
                    cols_list_low = [[x.casefold() for x in sublst] for sublst in cols_list]
                for k in mylist_lower:
                    has_match = False
                    for j in cols_list_low:
                        lst.append([item for item in j if item.startswith(k.split()[0])])
                flat_list = [num for sublist in lst for num in sublist]
                flat_list_upper = [y.upper() for y in set(flat_list)]
                for df in dfs:
                    df = df[df.columns & flat_list_upper]
                    df = df.rename(columns=renaming_fun)
                    df = df.loc[:, ~df.columns.duplicated(keep='first')]
                    concat_dfs.append(df) 
            concatinated_df = pd.concat(concat_dfs, ignore_index = True)  
            return concatinated_df
            # Get path to directories included in data folder
        # Define dictionaries to store dataframes   
        data_included = get_data_dirs(self.data_paths)  
        clinical_dfs = {}
        sample_dfs = {}
        mutation_dfs = {}
        # READ DATA tables into dictionary of dataframes
         # Clinical data: 
        read_data(data_included, clinical_file_name, clinical_dfs)
        # Sample data:
        read_data(data_included, sample_file_name, sample_dfs)
        # Mutational data: 
        read_data(data_included, mutation_file_name, mutation_dfs)
        # Mutational data: 
        # CONCATINATE DATAFRAMES in dicts into single dataframe
        #Clinical data:
        add_dataframe_name_column(clinical_dfs)
        all_clinical_data = concatinate_dfs(clinical_dfs)
        # ADD STUDY NAME as column do dataframes in dictionaries
        model_input = {}
        def create_gene_cols(path_list, sample_concat_dict , mutation_concat_dict , mutationMerged_dict):
            model_frame = []
            for path in path_list:
            #create columns for genes of interest and compound counts
            # Read clinical data files:
                mutDF = pd.crosstab( mutation_concat_dict[path]['Tumor_Sample_Barcode'], [ mutation_concat_dict[path]['Hugo_Symbol']], dropna=False).astype(int)
                # if count is greater than 2 set to 1, else 0
                mutDF.iloc[:,1:] = mutDF.iloc[:,1:].applymap(lambda x: 1 if x >= 2 else 0)
                # sum across rows where col in pan_cmpd_mut
                mutDF['Pan_compound_muts'] = mutDF.filter(items=pan_cmpd_mut).sum(1)
                 #  sum across rows where col in DCB_muts
                mutDF['DCB_genes'] = mutDF.filter(items=DCB_muts).sum(1)
                #  sum across rows where col in NDB_muts
                mutDF['NDB_genes'] = mutDF.filter(items=NDB_muts).sum(1)
                mutDF['Tumor_Sample_Barcode'] = mutDF.index
                mutDF.index.name = None
                mutationMerged_dict[path] = sample_concat_dict[path].merge(mutDF.rename(columns={'Tumor_Sample_Barcode': 'SAMPLE_ID'}), 'left')
                getCols =  [cols for cols in mutationMerged_dict[path] for col in list(pan_cmpd_mut+DCB_muts+NDB_muts+['Pan_compound_muts','DCB_genes','NDB_genes']) if col == cols]
                mutationMerged_dict[path] = mutationMerged_dict[path].loc[:,'PATIENT_ID':'TMB_NONSYNONYMOUS'].join(mutationMerged_dict[path].loc[:,getCols].fillna(0).astype(int))
                df_shapes={}
                ## put all shape sizes into a new dict
                for k, v in mutationMerged_dict.items():
                    df_shapes[k] = v.shape[0]
                    # set the index of the smallest dataframe
                    mutationMerged_dict[list(df_shapes.keys())[list(df_shapes.values()).index(min(list(df_shapes.values())))]].index = range(min(list(df_shapes.values())))
                    #set the index of the largest dataframe to include size of smallest
                    mutationMerged_dict[list(df_shapes.keys())[list(df_shapes.values()).index(max(list(df_shapes.values())))]].index = range(min(list(df_shapes.values())), min(list(df_shapes.values()))+max(list(df_shapes.values())))
                    model_frame = reduce(lambda left, right : left.T.join( right.T, how='outer'), list(mutationMerged_dict.values()))
                return model_frame
        all_genetic_data = create_gene_cols(data_included, sample_dfs , mutation_dfs , model_input)
        all_model_data = all_clinical_data.merge(all_genetic_data, on='PATIENT_ID', how='outer')
        all_clinical_data.to_csv('loadData.tsv', index=False, sep ='\t')
        return all_clinical_data
   
    def _save(self, train_data: pd.DataFrame, test_data: pd.DataFrame) -> None:
        """Save the preprocessed data to disk as a training and test sets.

        Arguments:
            train_data -- The training data set.
            test_data -- The test data set.
        """
        # Prepare save folder.
        output_dir = prepare_save_folder(
            DATA_FOLDER,
            self.config["output_name"],
            ["config", "data"],
            {"preprocess_config": self.config},
        )

        # Save data.
        train_data.to_csv(output_dir / "data/train_data.csv", index=False)
        test_data.to_csv(output_dir / "data/test_data.csv", index=False)
        print(f"Saved processed data to {output_dir}")

    def _preprocess(self, data) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Apply the preprocessor specified in the configuration to the data.

        Arguments:
            data -- The data to preprocess.

        Returns:
            A tuple with the training and test data sets.
        """
        if self.preprocessor_type == "main_preprocessor":
            train_dataset, test_dataset = main_preprocess.process(self.config, data)
        elif self.preprocessor_type == "non_null_one_hotted":
            train_dataset, test_dataset = non_null_one_hotted.process(
                self.config, data
            )
        else:
            assert False, "No preprocessor found!"
        return train_dataset, test_dataset

    def process(self) -> None:
        """Load the data from file, process it, and save the results."""
        print("Loading original data set..")
        data = self._load_data()

        print("Processing..")
        train_data, test_data = self._preprocess(data)

        print("Saving processed data..")
        self._save(train_data, test_data)
