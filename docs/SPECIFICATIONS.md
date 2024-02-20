# Technical Specification Document

## 1. Front Matter

- Title: LLM Debugging Experiment Tool for QuixBugs
- Author(s): Lucy Xu
- Created on: 2024-02-08

## 2. Introduction

### a. Overview, Problem Description, Summary, or Abstract

- Problem: The project aims to evaluate the performance of LLM (Large Language Models) in auto-debugging task.
- Context: This is a research project for a master's thesis.
- Suggested Solution: The project will utilize LLM models to auto-debug code and compare the results across multiple LLM models. Additionally, the project will assess the performance of LLM models in different programming languages.
- Stakeholders: The primary user of this project is a student conducting research for a master's thesis.

### b. Glossary or Terminology

- APR: Automated Program Repair. This refers to the process of inputting a buggy code and getting the correct code as output.
- SFL: Software Fault Localization. This refers to the process of finding the position (mostly line number) of the bug occur.
- Plausible Patches: These are the fixed codes that can pass all test cases.
- Correct Patches: These are the fixed codes that are syntactically or semantically equivalent to the reference patches.
- QuixBugs: This is the dataset used in the experiment.

### c. Context or Background

pass

### d. Goals or Product and Technical Requirements

- Product requirements in the form of user stories
- Technical requirements

### e. Non-Goals or Out of Scope

- Product and technical requirements that will be disregarded

### f. Future Goals

- Product and technical requirements slated for a future time

### g. Assumptions

- Conditions and resources that need to be present and accessible for the solution to work as described.

## 3. Solutions

### a. Current or Existing Solution / Design

- Current solution description: The current solution is a collection of Jupyter Notebook files that call APIs and clean the input and output of the experimental data.
- Pros of the current solution: The current solution was quick to write and the results were available early in the process.
- Cons of the current solution: The current solution lacks a clear connection between actions and contains a lot of redundant code, which makes it hard to read and modify.

### b. Suggested or Proposed Solution / Design

- External components that the solution will interact with and that it will alter

- Dependencies of the current solution

- Pros and cons of the proposed solution

- Data Model / Schema Changes
  - Schema definitions
  - New data models
  - Modified data models
  - Data validation methods
- Business Logic
  - API changes
  - Pseudocode
  - Flow
