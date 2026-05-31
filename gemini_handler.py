# This file connects to Google Gemini LLM and handles all AI powered features of our app.

"""
Summary Generation     → sends text to Gemini → gets summary
Key Insights           → sends text to Gemini → gets insights
Citation Generation    → sends text to Gemini → gets citation
Question Answering     → sends context + question → gets answer
"""


# google.generativeai is the official Google library
# that allows us to connect and talk to Gemini LLM
# import google.generativeai as genai -> not working 
from google import genai


# os library allows us to access environment variables
# We use it to read our API key from .env file
import os

# load_dotenv() reads our .env file and loads
# all variables inside it into our environment
# So we can safely access our API key
from dotenv import load_dotenv

# # This line actually loads the .env file
# # After this line GEMINI_API_KEY is available in our environment
# load_dotenv()


# # os.getenv() reads the value of GEMINI_API_KEY from environment
# # This is how we safely get our API key without writing it in code
# api_key = os.getenv("GEMINI_API_KEY")

import streamlit as st

load_dotenv()

# Try Streamlit secrets first (for deployment)
# Then fall back to .env file (for local development)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY")


# genai.configure() sets up our connection to Gemini
# We pass our API key so Google knows who we are
client=genai.Client(api_key=api_key)


# We create a Gemini model object
# "gemini-1.5-flash" is a fast and free version of Gemini
# We will use this model for all our AI features
# model = genai.GenerativeModel("gemini-1.5-flash") -> not working
# MODEL = "gemini-2.0-flash" -> NOT using because of quota limit exceeded
# MODEL="gemini-1.5-flash-latest"
MODEL = "gemini-2.5-flash"

# This function generates a comprehensive summary of the paper
# It takes the full extracted text as input
def generate_summary(text) :

     # We only send first 5000 characters to Gemini
    # Because sending entire paper at once is too much
    # First 5000 characters usually contain abstract and introduction
    # which are the most important parts for summary

    text_preview = text[:5000]

    # This is our prompt — instructions we give to Gemini
    # We tell it exactly what we want it to do

    prompt = f"""
    You are an expert academic research assistant.
    Please analyze the following research paper and provide a comprehensive summary.
    
    Structure your summary as follows:
    1. Main Objective
    2. Methodology Used
    3. Key Findings
    4. Conclusion
    
    Research Paper:
    {text_preview}
    
    Provide a clear and concise summary that a student can easily understand.
    """

    import time
    for attempt in range(3):
        try:
            # model.generate_content() sends our prompt to Gemini
            # and gets back a response
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            # response.text contains the actual text response from Gemini
            return response.text
        
        except Exception as e : 
            if attempt < 2 : 
                # Wait 3 seconds before retrying.
                time.sleep(3)
            else:
                return "Gemini is currently busy. Please try again in a few seconds!"




# This function extracts key insights from the paper
# It takes the full extracted text as input
def extract_key_insights(text) :
    text_preview = text[:5000]


    prompt = f"""
    You are an expert academic research assistant.
    Please extract the key insights from the following research paper.
    
    Provide insights in this format:
    1. Problem Statement
    2. Proposed Solution
    3. Dataset Used (if any)
    4. Results and Performance
    5. Limitations
    6. Future Work
    
    Research Paper:
    {text_preview}
    
    Be specific and concise for each point.
    """

    import time
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text
        
        except Exception as e : 
            if attempt < 2 : 
                # Wait 3 seconds before retrying.
                time.sleep(3)
            else:
                return "Gemini is currently busy. Please try again in a few seconds!"






# This function generates a proper academic citation for the paper
# It takes the full extracted text as input
def generate_citation(text) :

    # For citation we only need first 1000 characters
    # Because title, authors and year are usually at the beginning

    # text_preview = text[:5000] -> Changed to below line : 
    text_preview = text[:1000]

    prompt = f"""
    You are an expert academic research assistant.
    Please generate proper academic citations for this research paper.
    
    Provide citations in these 3 formats:
    1. APA Format
    2. MLA Format  
    3. Chicago Format
    
    Extract the following from the paper:
    - Title
    - Authors
    - Year
    - Journal/Conference (if available)
    
    Research Paper Beginning:
    {text_preview}
    
    If any information is not available write "Not Available"
    """

    import time
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text
        
        except Exception as e : 
            if attempt < 2 : 
                # Wait 3 seconds before retrying.
                time.sleep(3)
            else:
                return "Gemini is currently busy. Please try again in a few seconds!"



# This function answers user questions about the paper
# It takes the relevant context and user question as input
# context comes from our FAISS vector database (relevant chunks)
# question comes from the user


# This function is being replaced by another one which will be written below it :
# def answer_question(context,question):

#     prompt = f"""
#     You are an expert academic research assistant.
#     Answer the following question based ONLY on the provided research paper context.
#     If the answer is not in the context say "I could not find this information in the paper"
    
#     Context from Research Paper:
#     {context}
    
#     Question:
#     {question}
    
#     Provide a clear, accurate and helpful answer.
#     """

#     # response = model.generate_content(prompt) -> NOT Working
#     response = client.models.generate_content(
#         model=MODEL,
#         contents=prompt
#     )

#     return response.text



# Another answer_question function : 
# def answer_question(context, question, chat_history=[]):

    # # We format previous messages so Gemini knows
    # # what was said before in the conversation
    # formatted_history = ""
    # for message in chat_history:
    #     role = "User" if message["role"] == "user" else "Assistant"
    #     formatted_history += f"{role}: {message['content']}\n\n"

    # prompt = f"""
    # You are an expert academic research assistant.
    
    # You have access to:
    # 1. The research paper context below
    # 2. The conversation history below
    
    # Use BOTH to answer the question.
    # If user refers to something from previous conversation use that.
    # If answer is not available say "I could not find this information in the paper"
    
    # Research Paper Context:
    # {context}
    
    # Conversation History:
    # {formatted_history}
    
    # Current Question:
    # {question}
    
    # Provide a clear, accurate and helpful answer.
    # """

    # response = client.models.generate_content(
    #     model=MODEL,
    #     contents=prompt
    # )

    # return response.text



def answer_question(context, question, chat_history=[]):

    # Format conversation history properly
    # We only take last 10 messages to avoid
    # sending too much data to Gemini
    recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history

    formatted_history = ""
    for message in recent_history:
        role = "User" if message["role"] == "user" else "Assistant"
        formatted_history += f"{role}: {message['content']}\n\n"

    prompt = f"""
    You are an expert academic research assistant
    having a conversation with a user about a research paper.

    IMPORTANT RULES:
    1. Always check conversation history FIRST
    2. If user refers to something you said before
       use THAT information to answer
    3. Only use paper context if conversation history
       does not have the answer
    4. Never ignore what was previously discussed
    5. If user asks to summarize or rephrase your
       previous answer — do exactly that

    Conversation History:
    {formatted_history}

    Research Paper Context:
    {context}

    Current Question:
    {question}

    Answer based on conversation history first
    then paper context if needed.
    """


    # Try 3 times before giving up
    # Sometimes Gemini is busy and needs a retry
    import time
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text
        
        except Exception as e : 
            if attempt < 2 : 
                # Wait 3 seconds before retrying.
                time.sleep(3)
            else:
                return "Gemini is currently busy. Please try again in a few seconds!"