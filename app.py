import streamlit as st
from pdf_processor import extract_text_from_pdf
from rag_pipeline import split_text_into_chunks, create_vector_database, get_relevant_chunks
from gemini_handler import generate_summary, extract_key_insights, generate_citation, answer_question



st.set_page_config(
    page_title="ScholarAI",
    page_icon="🔬",
    layout="wide"
)

# Add this right here ↓
# st.markdown("""
#     <style>
#     .stSpinner { margin-top: -50px; }
#     </style>
# """, unsafe_allow_html=True)



# Initialize session state variables at the very top
# This ensures they always exist before anything else runs
if "processed" not in st.session_state:
    st.session_state.processed = False

if "text" not in st.session_state:
    st.session_state.text = None

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "summary" not in st.session_state:
    st.session_state.summary = None

if "insights" not in st.session_state:
    st.session_state.insights = None

if "citations" not in st.session_state:
    st.session_state.citations = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

# Header
st.title("🔬 ScholarAI")
st.write("Your Intelligent Research Paper Assistant powered by Google Gemini")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Upload Research Paper")
    uploaded_file = st.file_uploader(
        "Choose a PDF file only",
        type=["pdf"]
    )

    if uploaded_file is not None:
        # If a new file is uploaded reset everything
        if st.session_state.file_name != uploaded_file.name:
            st.session_state.processed = False
            st.session_state.text = None
            st.session_state.vector_db = None
            st.session_state.summary = None
            st.session_state.insights = None
            st.session_state.citations = None
            st.session_state.messages = []
            st.session_state.file_name = uploaded_file.name

        st.success("Paper uploaded Successfully.")
        st.write(f"File : {uploaded_file.name}")

# Main content
if uploaded_file is None:
    st.info("Please upload a research paper PDF from the sidebar to get started!")
    st.markdown("""
    ### What ScholarAI can do:
    - 📄 **Summarize** your research paper instantly
    - 🔍 **Extract** key insights and findings
    - 📚 **Generate** academic citations (APA, MLA, Chicago)
    - 💬 **Answer** any question about the paper
    """)

else:
    # Process the file only once
    if not st.session_state.processed:
        with st.spinner("Reading and processing your paper..."):
            text = extract_text_from_pdf(uploaded_file)
            chunks = split_text_into_chunks(text)
            vector_db = create_vector_database(chunks)

            st.session_state.text = text
            st.session_state.vector_db = vector_db
            st.session_state.processed = True

        st.success("Paper processed successfully!")

    # Always show tabs as long as file is uploaded
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Summary",
        "🔍 Key Insights",
        "📚 Citations",
        "💬 Ask Questions"
    ])

    # TAB 1 — SUMMARY
    with tab1:
        st.subheader("Paper Summary")

        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                st.session_state.summary = generate_summary(
                    st.session_state.text
                )

        if st.session_state.summary is not None:
            st.markdown(st.session_state.summary)

    # TAB 2 — KEY INSIGHTS
    with tab2:
        st.subheader("Key Insights")

        if st.button("Extract Key Insights"):
            with st.spinner("Extracting key insights..."):
                st.session_state.insights = extract_key_insights(
                    st.session_state.text
                )

        if st.session_state.insights is not None:
            st.markdown(st.session_state.insights)

    # TAB 3 — CITATIONS
    with tab3:
        st.subheader("Academic Citations")

        if st.button("Generate Citations"):
            with st.spinner("Generating citations..."):
                st.session_state.citations = generate_citation(
                    st.session_state.text
                )

        if st.session_state.citations is not None:
            st.markdown(st.session_state.citations)
 
  

# TAB 4 — Q&A CHAT
    # with tab4:
    #     st.subheader("Ask Questions About the Paper")

    #     # Clear chat button only when messages exist
    #     if len(st.session_state.messages) > 0:
    #         if st.button("Clear Chat"):
    #             st.session_state.messages = []
    #             st.session_state.question_input = ""
    #             st.rerun()

    #     st.markdown("---")

    #     # Display all previous messages
    #     for message in st.session_state.messages:
    #         with st.chat_message(message["role"]):
    #             st.write(message["content"])

    #     st.markdown("---")

    #     # Question input at bottom
    #     col1, col2 = st.columns([5, 1])

    #     with col1:
    #         question = st.text_input(
    #             label="question",
    #             key="question_input",
    #             label_visibility="collapsed",
    #             placeholder="Ask anything about the paper..."
    #         )

    #     with col2:
    #         ask_button = st.button("Ask")

    #     # When user clicks Ask button
    #     if ask_button and question:

    #         # Save question before clearing input
    #         user_question = question

    #         # Clear input box
    #         st.session_state.question_input = ""

    #         # Add question to history
    #         st.session_state.messages.append({
    #             "role": "user",
    #             "content": user_question
    #         })

    #         # Get answer from Gemini
    #         with st.spinner("Thinking..."):
    #             context = get_relevant_chunks(
    #                 st.session_state.vector_db,
    #                 user_question
    #             )
    #             answer = answer_question(
    #                 context,
    #                 user_question,
    #                 st.session_state.messages
    #             )

    #         # Add answer to history
    #         st.session_state.messages.append({
    #             "role": "assistant",
    #             "content": answer
    #         })

    #         # Rerun to refresh page with new messages
    #         st.rerun()







            # TAB 4 — Q&A CHAT
    with tab4:
        st.subheader("Ask Questions About the Paper")

        # Clear chat button only when messages exist
        if len(st.session_state.messages) > 0:
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.rerun()

        st.markdown("---")

        # Display all previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        st.markdown("---")

        # Question input at bottom
        col1, col2 = st.columns([5, 1])

        with col1:
            question = st.text_input(
                label="question",
                label_visibility="collapsed",
                placeholder="Ask anything about the paper...",
                key=f"question_{st.session_state.input_counter}"
            )

        with col2:
            ask_button = st.button("Ask")

        # When user clicks Ask button
        if ask_button and question:

            # Add question to history
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            # Get answer from Gemini
            with st.spinner("Thinking..."):
                context = get_relevant_chunks(
                    st.session_state.vector_db,
                    question
                )
                answer = answer_question(
                    context,
                    question,
                    st.session_state.messages
                )

            # Add answer to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            # Increment counter to create new input widget
            # This effectively clears the input box
            st.session_state.input_counter += 1

            # Rerun to refresh page
            st.rerun()





        # Question input at bottom
        # col1, col2 = st.columns([5, 1])

        # with col1:
        #     question = st.text_input(
        #         label="question",
        #         label_visibility="collapsed",
        #         placeholder="Ask anything about the paper...",
        #         value=""
        #     )

        # with col2:
        #     ask_button = st.button("Ask")

        # # When user clicks Ask button
        # if ask_button and question:

        #     # Add question to history
        #     st.session_state.messages.append({
        #         "role": "user",
        #         "content": question
        #     })

        #     # Get answer from Gemini
        #     with st.spinner("Thinking..."):
        #         context = get_relevant_chunks(
        #             st.session_state.vector_db,
        #             question
        #         )
        #         answer = answer_question(
        #             context,
        #             question,
        #             st.session_state.messages
        #         )

        #     # Add answer to history
        #     st.session_state.messages.append({
        #         "role": "assistant",
        #         "content": answer
        #     })

        #     # Rerun to refresh page with new messages
        #     st.rerun()