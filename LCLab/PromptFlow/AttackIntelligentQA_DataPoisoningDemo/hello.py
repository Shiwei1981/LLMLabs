# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from promptflow.core import tool

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

import os
from langsmith.wrappers import wrap_openai
from langsmith import traceable
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
import PyPDF2
from PyPDF2 import PdfReader

os.environ["AZURE_OPENAI_API_VERSION"] = "2023-12-01-preview"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gtp-35-tb-deployment"

def chunk_processing():
    """
    Process a PDF file, extracting text and splitting it into chunks.
    """
    directory = "./"
    all_chunks = []

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            # Open the PDF file in binary mode
            pdf = open(filename, 'rb')
            pdf_reader = PdfReader(pdf)
        
            text = ""
            for page in pdf_reader.pages:        
                text += page.extract_text()
                
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text=text)
            all_chunks.extend(chunks)

    return all_chunks

def embeddings(chunks):
    """
    Create embeddings for text chunks using OpenAI.
    """
    # Initialize OpenAI embeddings
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="emb3s",
        openai_api_version="2023-05-15",
    )
    # Create vector store using FAISS
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store

def generation(VectorStore, input):
    """
    Generate responses based on prompts and embeddings.
    """
    retriever = VectorStore.as_retriever()
    
    # Define template for prompts
    template = """Respond to the prompt based on the following context: {context}
    Questions: {questions}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    model = AzureChatOpenAI(
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    )
    # Define processing chain
    chain = (
        {"context": retriever, "questions": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    # Invoke the processing chain with user input
    output = chain.invoke(input)
    return output

@tool
def my_python_tool(input1: str) -> str:
    model = AzureChatOpenAI(
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    )

    # Process the PDF file into chunks
    processed_chunks = chunk_processing()

    # Embed the processed chunks using OpenAI embeddings
    embedded_chunks = embeddings(processed_chunks)

    # Generate responses based on the embedded chunks
    generated_response = generation(embedded_chunks, input1)

    # Print the generated response
    print(generated_response)

    return generated_response
