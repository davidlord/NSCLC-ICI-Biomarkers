# Package Overview

## Background
The identification of biomarkers that correlate with immunotherapy treatment outcomes has played a crucial role in guiding the appropriate use of immunotherapies in NSCLC. These biomarkers can provide valuable insights into the likelihood of a patient responding positively to immunotherapy, allowing for more personalized treatment plans and improved therapeutic outcomes. However, the successful integration of biomarker-driven precision oncology relies on the analysis and interpretation of vast and complex data, which can be challenging for traditional methodologies. Given this challenge, we aim to in this project deliver a framework to:
1) Deliver a framework for subject matter experts to compile multiple dataset into a single sensible dataset ready for analysis and modelling.
2) Generate predictive machine learning models of patient treatment outcomes given the input data.

## Project Scope
This project aims to predict immunotherapy treatment response in NSCLC-patients through machine learning. The data used to train these models are derived from the cancer genomics database cBioPortal (https://www.cbioportal.org/). 
Although the scope of this project is limited to NSCLC, the framework presented in this repository may be reused for data processing and modelling of treatment response in other cancer types. 

## Package Overview
This code repository contains two packages: "Data-Preparation" and "Modelling". The function of each of these is explained below. 

### Data Preparation
Framework for compiling and preparing cancer genomics datasets from the cBioPortal. Source code compiles multiple separate datasets to a single analysis-ready dataset. This process requires input from subject matter experts to correctly harmonize the data. Output dataset can then be used for analysis as well as input for the subsequent modelling module in this repository. 

### Modelling
A module for creating predictive machine learning models for immunotherapy treatment outcome. XGBoost classification model predicting whether patients are responders or non-responders (>= 6 months progression-free survival) given the data. 
