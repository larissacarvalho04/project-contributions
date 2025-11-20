# Chatbot LLM Module (simple)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-8A2BE2?logo=langchain&logoColor=white)
![AWS Bedrock](https://img.shields.io/badge/AWS_Bedrock-FF9900?logo=amazonaws&logoColor=white)
![Boto3](https://img.shields.io/badge/Boto3-232F3E?logo=python&logoColor=white)

## Description
This folder contains the **LLM components** used by a chatbot prototype.  
- The **first file** is a prototype that builds a history-aware conversational retrieval chain using Bedrock/LangChain.  
- The **second file** is a simpler, easier-to-adapt LLM wrapper (Amazon Titan) intended for team integration.

This module covers **only the LLM layer** (model + retrieval chain). It does **not** include the retriever, document store, or the application glue.

## Files
- `llm_lcel.py` — prototype: history-aware conversational chain using Bedrock LLM and LangChain utilities.  
- `llm_chain.py` — simplified LLM wrapper using Bedrock/Titan and a retrieval chain, easier to adapt for the team project.  
- `README.md` — this file.

## Note
- These files are **my LLM implementations only** (prototype → adaptation).  

## Minimal Requirements
- Python 3.10+  
- langchain, langchain_aws, langchain_core (or matching packages used)  
- boto3 (for `llm_chain.py`)  
- AWS credentials configured for Bedrock access

