#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 19:01:44 2023

@author: davidlord
"""
# Import packages:
import os
import pandas as pd
import glob


os.getcwd()
os.chdir('/Users/davidlord/Desktop/Data prep')


# CLINICAL DATA

# Read files


clinical_data_1 = pd.read_csv('Data/luad_mskcc_2015/data_clinical_patient.txt', header=0, delimiter='\t')
e
clinical_data_2 = pd.read_csv('Data/luad_mskcc_2020/data_clinical_patient.txt', header=0, delimiter='\t')
e






