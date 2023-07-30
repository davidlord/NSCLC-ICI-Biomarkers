# Package Overview

## Background
The identification of certain biomarkers that correlate with immunotherapy treatment outcomes has played a crucial role in guiding the appropriate use of immunotherapies in NSCLC. These biomarkers can provide valuable insights into the likelihood of a patient responding positively to immunotherapy, allowing for more personalized treatment plans and improved therapeutic outcomes. However, the successful integration of biomarker-driven precision oncology relies on the analysis and interpretation of vast and complex datasets, which can be challenging for traditional methodologies. Given this challenge, we aim to in this project deliver a framework to:
1) Make it easier for subject matter experts to compile multiple dataset into a single sensible dataset ready for analysis and modelling.
2) Create predictive models of patient treatment outcomes given the input data.

We will in this project focus on datasets of NSCLC patients who have undergone immunotherapy, but in theory, this framework is translatable across cancer types and scientific question.

## Package Overview
This code repository contains two packages: "Data-Preparation" and "Modelling". The function of each of these is explained below. 

### Data Preparation
Framework for compiling and preparing cancer genomics datasets from the cBioPortal. Source code compiles multiple separate datasets to a single analysis-ready dataset. Requires input from subject matter experts before- and while executing the code for: defining gene-mutations of interest, defining columns of interest, and harmonizing categorical columns. Output dataset can be used as input for the "Modelling" framework in this repository. 

### Modelling
A framework for creating predictive models of NSCLC immunotherapy treatment outcome. Include capabilities to generate two separate models based on XGBoost and neural network (Keras). Both are classification models predicting whether patients are responders or non-responders given the data. 
