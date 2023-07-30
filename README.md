# Package Overview

## Background
The identification of certain biomarkers that correlate with immunotherapy treatment outcomes has played a crucial role in guiding the appropriate use of immunotherapies in NSCLC. These biomarkers can provide valuable insights into the likelihood of a patient responding positively to immunotherapy, allowing for more personalized treatment plans and improved therapeutic outcomes. However, the successful integration of biomarker-driven precision oncology relies on the analysis and interpretation of vast and complex datasets, which can be challenging for traditional methodologies. Given this challenge, we aim to in this project deliver a framework to make it easier for subject matter experts to compile multiple dataset into a single sensible dataset ready for analysis and modelling. We specifically focus on datasets available from the cancer genomics database cBioPortal (cite) in this project. Our aim is that our approach should be able to curate data deriving from various levels, including patient data, sample data, and tumor genomic data. We will in this project focus on datasets of NSCLC patients who have undergone immunotherapy, but in theory, this framework is translatable across cancer types and scientific question.

## Package Overview
This code repository contains two packages: "Data-Preparation" and "Modelling". The function of each of these is explained below. 

### Data Preparation
A framework for compiling and preparing cancer genomics datasets from the cBioPortal. Source code compiles multiple separate datasets to a single analysis-ready dataset. Requires input from subject matter experts before and while executing the code for: defining gene-mutations of interest, defining columns of interest, and harmonizing categorical columns. 


### Modelling
A framework for creating predictive models of NSCLC immunotherapy treatment outcome. 
