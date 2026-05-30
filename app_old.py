# streamlit is our web app framework
# it allows us to build beautiful web apps using only Python
import streamlit as st


# We import all our custom modules
# that we built in previous steps
from pdf_processor import extract_text_from_pdf, get_pdf_info
from rag_pipeline import split_text_into_chunks, get_relevant_chunks, create_vector_database
from gemini_handler import generate_summary, generate_citation, extract_key_insights, answer_question

# st.set_page_config() configures our web app settings
# page_title → title shown in browser tab
# page_icon → emoji shown in browser tab
# layout → "wide" means app uses full screen width
st.set_page_config(
    page_title="Scholar AI",
    page_icon="🔬",
    layout="wide"
)

# st.title() displays a large heading on the page
st.title("🔬 Scholar AI")

# st.write() displays text on the page
st.write("Your Intelligent Research Paper Assistant powered by Google Gemini")


# This draws a horizontal line across the page
# to separate the header from the rest of the app
st.markdown("---")

# st.sidebar is a panel on the left side of the app
# We use it for file upload and settings
with st.sidebar :

        # Display a heading in the sidebar
        st.header("Upload a Research Paper")

         # st.file_uploader() creates a file upload button
         # type=["pdf"] means only PDF files are accepted
        uploaded_file = st.file_uploader(
                "Choose a PDF file only",
                type=['pdf']
        )

        # If user has uploaded a file
        if uploaded_file is not None : 
                
                        # st.success() displays a green success message
                        st.success("Paper uploaded Successfully.")

                        # Display basic info about the uploaded file
                        # uploaded_file.name gives us the filename
                        st.write(f"File : {uploaded_file.name}")

# We check if a file has been uploaded
# If not we show instructions to the user
if uploaded_file is None :
            # st.info() displays a blue information message
            st.info("Please upload a research paper PDF from the sidebar to get started.")

            # st.markdown() allows us to write formatted text
            st.markdown("""
    ### What ScholarAI can do:
    - 📄 **Summarize** your research paper instantly
    - 🔍 **Extract** key insights and findings
    - 📚 **Generate** academic citations (APA, MLA, Chicago)
    - 💬 **Answer** any question about the paper
    """)

# If a file has been uploaded we process it 
else :
    # st.session_state is like a memory for our app
    # It stores data that we want to keep between interactions
    # Without session_state every time user clicks something
    # the entire app reruns and loses all data

    # This line resets session state if a new file is uploaded
    # It compares current filename with previously stored filename
    if "file_name" not in st.session_state or st.session_state.file_name != uploaded_file.name:
        # Clear all previous session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # Store new filename
        st.session_state.file_name = uploaded_file.name

    # We check if we have already processed this file
    # "processed" is a key we store in session_state

    if "processed" not in st.session_state :
        # st.spinner() shows a loading animation
        # while the code inside it is running

        with st.spinner("Reading and processing your paper..."):
                        # Extract text from PDF using our pdf_processor
                        text = extract_text_from_pdf(uploaded_file)

                        # Split text into chunks using our rag_pipeline
                        chunks = split_text_into_chunks(text)

                        # Create vector database using our rag_pipeline
                        vector_db = create_vector_database(chunks)

                        # Store everything in session_state so we don't
                        # have to reprocess every time user interacts

                        st.session_state.text = text
                        st.session_state.vector_db = vector_db
                        st.session_state.processed = True

                        # Initialize empty chat history list []
                        st.session_state.messages = []

                        # Show success message after processing
                        st.success("Paper processed successfully!")

        
        # Create 3 tabs for our different features
        # tab1 = Summary, tab2 = Key Insights
        # tab3 = Citations, tab4 = Q&A Chat
        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 Summary",
            "🔍 Key Insights", 
            "📚 Citations",
            "💬 Ask Questions"
        ])


        # TAB 1 — SUMMARY
        with tab1:
        
            st.subheader("Paper Summary")
        
            # st.button() creates a clickable button
            # When clicked it returns True
            if st.button("Generate Summary"):
            
                with st.spinner("Generating summary..."):
                
                    # Call our gemini_handler function
                    summary = generate_summary(st.session_state.text)
                
                    # Store summary in session_state
                    st.session_state.summary = summary
        
            # If summary exists in session_state display it
            if "summary" in st.session_state:
                st.markdown(st.session_state.summary)



        # TAB 2 — KEY INSIGHTS
        with tab2:
        
            st.subheader("Key Insights")
        
            if st.button("Extract Key Insights"):
            
                with st.spinner("Extracting key insights..."):
                
                    insights = extract_key_insights(st.session_state.text)
                    st.session_state.insights = insights
        
            if "insights" in st.session_state:
                st.markdown(st.session_state.insights)


        # TAB 3 — CITATIONS
        with tab3:
        
            st.subheader("Academic Citations")
        
            if st.button("Generate Citations"):
            
                with st.spinner("Generating citations..."):
                
                    citations = generate_citation(st.session_state.text)
                    st.session_state.citations = citations
        
            if "citations" in st.session_state:
                st.markdown(st.session_state.citations)



        # TAB 4 — Q&A CHAT
        with tab4:
        
            st.subheader("Ask Questions About the Paper")
        
            # Display all previous chat messages
            # We loop through messages stored in session_state
            for message in st.session_state.messages:
                # st.chat_message() creates a chat bubble
                # "user" creates a user bubble
                # "assistant" creates an AI bubble
                with st.chat_message(message['role']) : 
                      st.write(message[['content']])

            
            # st.chat_input() creates a text input at bottom of page
            # user can type their question here
            question = st.chat_input("Ask any question about your uploaded research paper")

            # if user has typed a question and pressed enter
            if question :
                # Add user question to chat history
                st.session_state.messages.append({
                      "role":"user",
                      "content":question
                })

                # Display user question in chat history
                with st.chat_message("user") :
                      st.write(question)

                # Get relevant context from vector database 
                with st.spinner("Thinking....") :
                    context = get_relevant_chunks(
                          st.session_state.vector_db,
                          question
                    )

                    # Get answer from Gemini
                    answer = answer_question(context, question)
                
                # Add answer to chat history
                st.session_state.messages.append({
                      "role":"assistant",
                      "content":answer
                })

                # Display answer in chat : 
                with st.chat_message("assistant") : 
                      st.write(answer) 