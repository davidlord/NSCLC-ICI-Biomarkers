# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 17:35:48 2024

@author: kxvz994
"""

# IMPORT packages:
import os
import re
import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns


# HEATMAP of NULL values
#---------------------------------------

# Create a boolean DataFrame where True is null
null_values = all_patient_sample_data.isnull()

# Set up the matplotlib figure
plt.figure(figsize=(30, 8))

# Draw a heatmap with the boolean values and no cell labels
sns.heatmap(null_values, cbar=False, yticklabels=False)
plt.title("Heatmap of Null Values in DataFrame")
plt.show()

all_patient_sample_data['OS_MONTHS_DMT'].value_counts()