# This file takes the extracted text from PDF, splits it into small chunks, converts those 
# chunks into numbers (embeddings) and stores them in a vector database so we can 
# search through them later.

# Why do we plit it into chunks?
# Because Gemini LLM has a limit on how much text it can process at once. Instead of sending 
# the entire paper we only send the most relevant small pieces.

# RecursiveCharacterTextSplitter is a class from LangChain
# It splits long text into smaller chunks
# "Recursive" means it tries to split smartly
# First by paragraphs, then by sentences, then by words
from langchain_text_splitters import RecursiveCharacterTextSplitter


# FAISS is our vector database
# It stores embeddings and allows us to search through them
# "Community" means it comes from the community version of LangChain
from langchain_community.vectorstores import FAISS

# HuggingFaceEmbeddings converts text chunks into numbers (embeddings)
# It uses a pretrained model from HuggingFace to do this
from langchain_community.embeddings import HuggingFaceEmbeddings

# This function splits our text into smaller chunks
# It takes the full extracted text as input
def split_text_into_chunks(text) :
     # We create a RecursiveCharacterTextSplitter object
    # chunk_size=1000 means each chunk will be maximum 1000 characters
    # chunk_overlap=200 means each chunk shares 200 characters with the next chunk
    # Why overlap? So we don't lose context at the boundaries of chunks
    # Example: if a sentence starts at end of chunk 1 
    # it will also appear at start of chunk 2

    text_splitters = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap=200
    )

    # split_text() takes our full text and splits it into a list of chunks
    # Each chunk is a string of maximum 1000 characters
    chunks = text_splitters.split_text(text)

    # we return the list of chunks 
    return chunks






# This function creates our vector database from the chunks
# It takes the list of chunks as input
def create_vector_database(chunks):

     # We create a HuggingFaceEmbeddings object
    # model_name tells it which pretrained model to use
    # "all-MiniLM-L6-v2" is a small fast and accurate model
    # It converts each chunk into a vector of 384 numbers
    # Similar chunks will have similar vectors

    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )


    # FAISS.from_texts() does 2 things at once:
    # 1. Converts each chunk into embeddings using our embeddings model
    # 2. Stores all embeddings in a FAISS vector database
    # chunks = list of text chunks
    # embeddings = our embeddings model

    vector_database = FAISS.from_texts(chunks, embeddings)


    # We return the vector database
    # Now we can search through it using semantic search
    return vector_database



# This function searches the vector database for relevant chunks
# It takes the vector database and user question as input
def get_relevant_chunks(vector_database, question):


     # similarity_search() finds the most similar chunks to the question
    # It converts the question to an embedding
    # Then finds chunks with most similar embeddings
    # k=3 means return top 3 most relevant chunks

    relevant_chunks = vector_database.similarity_search(question, k=3)
    context = " ".join([chunk.page_content for chunk in relevant_chunks])
    
    #We returned the combined context
    return context


