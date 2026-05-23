#-----------------------------------------

# This is First code :  (not working as such)

#----------------------------------------------------
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import PromptTemplate

# from groq import Groq

# import streamlit as st
# import time
# import os
# from dotenv import load_dotenv

# # ---------------- LOAD ENV ----------------
# load_dotenv()

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(page_title="LawGPT")

# col1, col2, col3 = st.columns([1,4,1])

# # with col2:
# #     st.image(
# #         "https://github.com/harshitv804/LawGPT/assets/100853494/ecff5d3c-f105-4ba2-a93a-500282f0bf00"
# #     )

# # ---------------- CUSTOM CSS ----------------
# st.markdown(
#     """
#     <style>
# div.stButton > button:first-child {
#     background-color: #ffd0d0;
# }

# div.stButton > button:active {
#     background-color: #ff6262;
# }

# div[data-testid="stStatusWidget"] div button {
#     display: none;
# }

# .reportview-container {
#     margin-top: -2em;
# }

# #MainMenu {visibility: hidden;}
# .stDeployButton {display:none;}
# footer {visibility: hidden;}
# #stDecoration {display:none;}

# button[title="View fullscreen"]{
#     visibility: hidden;
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # ---------------- RESET CHAT ----------------
# def reset_conversation():
#     st.session_state.messages = []

# # ---------------- SESSION MEMORY ----------------
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ---------------- EMBEDDINGS ----------------
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# # ---------------- LOAD VECTOR DB ----------------
# db = FAISS.load_local(
#     "ipc_vector_db",
#     embeddings,
#     allow_dangerous_deserialization=True
# )

# db_retriever = db.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 8}
# )

# # ---------------- PROMPT TEMPLATE ----------------
# prompt_template =  """
# You are an advanced Indian Legal AI Assistant specializing in:

# - DPDP Act
# - Motor Vehicle Rules
# - Indian Penal Code (IPC)
# - Indian legal compliance
# - Legal case analysis

# Your responsibilities:

# 1. Understand the user query or case study carefully.
# 2. Determine whether the matter falls under:
#    - DPDP Act
#    - Motor Vehicle Rules
#    - IPC
#    - Other Indian legal provisions

# 3. Prioritize retrieving and using the provided legal context.
# 4. Use legal reasoning and explain conclusions clearly.
# 5. Provide structured, detailed, and professional responses.
# 6. Avoid hallucinations or unsupported legal claims.
# 7. If information is insufficient, clearly mention limitations.
# 8. Maintain a neutral and legally sound tone.
# 9. Do NOT provide personal opinions.
# 10. If necessary, recommend consulting a qualified legal expert.

# ------------------------------
# RETRIEVED LEGAL CONTEXT:
# {context}
# ------------------------------

# USER QUESTION:
# {question}

# ------------------------------
# RESPONSE FORMAT:

# ## 1. Case Summary
# Briefly summarize the legal issue.

# ## 2. Relevant Legal Provisions
# Mention applicable sections, acts, or rules.

# ## 3. Legal Analysis and Opinion
# Provide detailed legal reasoning using the retrieved context.

# ## 4. Supporting References
# Mention relevant legal concepts, provisions, or precedents if available.

# ## 5. Limitations
# Mention if the available context is insufficient or uncertain.

# ------------------------------

# ANSWER:
# """

# prompt = PromptTemplate(
#     template=prompt_template,
#     input_variables=["context", "question"]
# )

# # ---------------- GROQ CLIENT ----------------
# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )

# # ---------------- DISPLAY OLD CHAT ----------------
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# # ---------------- USER INPUT ----------------
# input_prompt = st.chat_input("Ask your legal question")

# if input_prompt:

#     # Show user message
#     with st.chat_message("user"):
#         st.write(input_prompt)

#     st.session_state.messages.append({
#         "role": "user",
#         "content": input_prompt
#     })

#     # ---------------- RETRIEVE DOCUMENTS ----------------
#     docs = db_retriever.invoke(input_prompt)

#     context = "\n\n".join(
#     doc.page_content[:1500]
#     for doc in docs
#     )

#     final_prompt = prompt.format(
#         context=context,
#         question=input_prompt
#     )

#     # ---------------- ASSISTANT RESPONSE ----------------
#     with st.chat_message("assistant"):

#         with st.status("Thinking 💡...", expanded=True):

#             response = client.chat.completions.create(
#                 model="llama-3.3-70b-versatile",
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": final_prompt
#                     }
#                 ],
#                 temperature=0.4,
#                 max_tokens=1200
#             )

#             answer = response.choices[0].message.content

#             message_placeholder = st.empty()

#             full_response = (
#                 "⚠️ **_Note: Information provided may be inaccurate._**\n\n"
#             )

#             # Typing effect
#             for chunk in answer:
#                 full_response += chunk
#                 time.sleep(0.01)

#                 message_placeholder.markdown(full_response + "▌")

#             message_placeholder.markdown(full_response)

#         st.button(
#             "Reset All Chat 🗑️",
#             on_click=reset_conversation
#         )

#     # Save assistant response
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer
#     })


#-------------------------------------------------

# This is Second (full working code )

#------------------------------------------------------
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.prompts import PromptTemplate

# from groq import Groq

# import streamlit as st
# import time
# import os
# from dotenv import load_dotenv

# # ---------------- LOAD ENV ----------------
# load_dotenv()

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="Legal Assistant",
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------------- CUSTOM CSS ----------------
# st.markdown("""
# <style>

# /* MAIN APP */
# .stApp {
#     background-color: #0E1117;
#     color: white;
# }

# /* REMOVE STREAMLIT DEFAULT ELEMENTS */
# #MainMenu {
#     visibility: hidden;
# }

# footer {
#     visibility: hidden;
# }

# header {
#     visibility: hidden;
# }

# /* HERO SECTION */
# .hero {
#     padding: 2rem;
#     border-radius: 20px;
#     background: linear-gradient(135deg, #1f4037, #99f2c8);
#     color: white;
#     text-align: center;
#     margin-bottom: 2rem;
# }

# .hero h1 {
#     font-size: 3rem;
#     font-weight: 700;
# }

# .hero p {
#     font-size: 1.2rem;
#     opacity: 0.9;
# }

# /* FEATURE CARDS */
# .card {
#     background-color: #161B22;
#     padding: 20px;
#     border-radius: 16px;
#     border: 1px solid #30363d;
#     transition: 0.3s;
#     height: 180px;
# }

# .card:hover {
#     border: 1px solid #58A6FF;
#     transform: translateY(-5px);
# }

# .card-title {
#     font-size: 20px;
#     font-weight: bold;
#     margin-bottom: 10px;
# }

# .card-text {
#     color: #c9d1d9;
#     font-size: 15px;
# }

# /* SIDEBAR */
# section[data-testid="stSidebar"] {
#     background-color: #161B22;
# }

# /* CHAT MESSAGE */
# [data-testid="stChatMessage"] {
#     background-color: #161B22;
#     border-radius: 15px;
#     padding: 12px;
#     margin-bottom: 10px;
#     border: 1px solid #30363d;
# }

# /* CHAT INPUT */
# .stChatInputContainer {
#     border-top: 1px solid #30363d;
#     background-color: #0E1117;
# }

# /* BUTTON */
# .stButton>button {
#     background: linear-gradient(90deg, #238636, #2ea043);
#     color: white;
#     border-radius: 12px;
#     border: none;
#     padding: 10px 20px;
#     font-weight: bold;
# }

# .stButton>button:hover {
#     background: linear-gradient(90deg, #2ea043, #238636);
# }

# /* STATUS BOX */
# div[data-testid="stStatusWidget"] {
#     border-radius: 15px;
#     border: 1px solid #30363d;
# }

# </style>
# """, unsafe_allow_html=True)

# # ---------------- RESET CHAT ----------------
# def reset_conversation():
#     st.session_state.messages = []

# # ---------------- SESSION MEMORY ----------------
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ---------------- SIDEBAR ----------------
# with st.sidebar:

#     st.title("⚖️ Legal Assistant")

#     st.markdown("---")

#     st.markdown("""
#     ### Features
#     - DPDP Act Analysis
#     - IPC Legal Assistance
#     - Motor Vehicle Rules
#     - AI Legal Reasoning
#     - Context-based RAG System
#     """)

#     st.markdown("---")

#     st.info(
#         "This AI provides legal information "
#         "for educational purposes only."
#     )

#     st.button(
#         "🗑️ Reset Chat",
#         on_click=reset_conversation,
#         use_container_width=True
#     )

# # ---------------- HERO SECTION ----------------
# st.markdown("""
# <div class="hero">
#     <h1>⚖️ Legal Assistant</h1>
#     <p>
#         AI-powered Indian Legal Assistant for DPDP Act,
#         IPC, Motor Vehicle Rules, and Legal Case Analysis
#     </p>
# </div>
# """, unsafe_allow_html=True)

# # ---------------- FEATURE CARDS ----------------
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.markdown("""
#     <div class="card">
#         <div class="card-title">📘 DPDP Act</div>
#         <div class="card-text">
#             Analyze data privacy compliance,
#             consent requirements, and legal
#             obligations under DPDP Act.
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown("""
#     <div class="card">
#         <div class="card-title">🚗 Motor Vehicle Rules</div>
#         <div class="card-text">
#             Get legal insights regarding
#             traffic rules, liability,
#             accidents, and transport laws.
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# with col3:
#     st.markdown("""
#     <div class="card">
#         <div class="card-title">⚖️ IPC & Legal Analysis</div>
#         <div class="card-text">
#             Understand IPC sections,
#             legal reasoning, and
#             case-based legal analysis.
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)

# # ---------------- EMBEDDINGS ----------------
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# # ---------------- LOAD VECTOR DB ----------------
# db = FAISS.load_local(
#     "ipc_vector_db",
#     embeddings,
#     allow_dangerous_deserialization=True
# )

# db_retriever = db.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 8}
# )

# # ---------------- PROMPT TEMPLATE ----------------
# prompt_template = """
# You are an advanced Indian Legal AI Assistant specializing in:

# - DPDP Act
# - Motor Vehicle Rules
# - Indian Penal Code (IPC)
# - Indian legal compliance
# - Legal case analysis

# Your responsibilities:

# 1. Understand the user query or case study carefully.
# 2. Determine whether the matter falls under:
#    - DPDP Act
#    - Motor Vehicle Rules
#    - IPC
#    - Other Indian legal provisions

# 3. Prioritize retrieving and using the provided legal context.
# 4. Use legal reasoning and explain conclusions clearly.
# 5. Provide structured, detailed, and professional responses.
# 6. Avoid hallucinations or unsupported legal claims.
# 7. If information is insufficient, clearly mention limitations.
# 8. Maintain a neutral and legally sound tone.
# 9. Do NOT provide personal opinions.
# 10. If necessary, recommend consulting a qualified legal expert.

# ------------------------------
# RETRIEVED LEGAL CONTEXT:
# {context}
# ------------------------------

# USER QUESTION:
# {question}

# ------------------------------
# RESPONSE FORMAT:

# ## 1. Case Summary
# Briefly summarize the legal issue.

# ## 2. Relevant Legal Provisions
# Mention applicable sections, acts, or rules.

# ## 3. Legal Analysis and Opinion
# Provide detailed legal reasoning using the retrieved context.

# ## 4. Supporting References
# Mention relevant legal concepts, provisions, or precedents if available.

# ## 5. Limitations
# Mention if the available context is insufficient or uncertain.

# ------------------------------

# ANSWER:
# """

# prompt = PromptTemplate(
#     template=prompt_template,
#     input_variables=["context", "question"]
# )

# # ---------------- GROQ CLIENT ----------------
# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )

# # ---------------- DISPLAY OLD CHAT ----------------
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):

#         if message["role"] == "user":
#             st.markdown(f"👨‍💼 {message['content']}")
#         else:
#             st.markdown(f"⚖️ {message['content']}")

# # ---------------- USER INPUT ----------------
# input_prompt = st.chat_input(
#     "Ask your legal question..."
# )

# if input_prompt:

#     # ---------------- USER MESSAGE ----------------
#     with st.chat_message("user"):
#         st.markdown(f"👨‍💼 {input_prompt}")

#     st.session_state.messages.append({
#         "role": "user",
#         "content": input_prompt
#     })

#     # ---------------- RETRIEVE DOCUMENTS ----------------
#     docs = db_retriever.invoke(input_prompt)

#     context = "\n\n".join(
#         doc.page_content[:1500]
#         for doc in docs
#     )

#     final_prompt = prompt.format(
#         context=context,
#         question=input_prompt
#     )

#     # ---------------- ASSISTANT RESPONSE ----------------
#     with st.chat_message("assistant"):

#         with st.status(
#             "⚖️ Analyzing Legal Context...",
#             expanded=True
#         ):

#             response = client.chat.completions.create(
#                 model="llama-3.3-70b-versatile",
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": final_prompt
#                     }
#                 ],
#                 temperature=0.4,
#                 max_tokens=1200
#             )

#             answer = response.choices[0].message.content

#             message_placeholder = st.empty()

#             full_response = (
#                 "⚠️ **Legal Disclaimer:** "
#                 "AI-generated legal information "
#                 "may not always be accurate.\n\n"
#             )

#             # ---------------- TYPING EFFECT ----------------
#             for chunk in answer:
#                 full_response += chunk
#                 time.sleep(0.005)

#                 message_placeholder.markdown(
#                     full_response + "▌"
#                 )

#             message_placeholder.markdown(full_response)

#     # ---------------- SAVE RESPONSE ----------------
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer
#     })


from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

from groq import Groq

import streamlit as st
import time
import os

from dotenv import load_dotenv

from langdetect import detect
from deep_translator import GoogleTranslator

# =====================================================
# LOAD ENV
# =====================================================
load_dotenv()

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* REMOVE STREAMLIT DEFAULTS */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* HERO SECTION */
.hero {
    padding: 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 700;
}

.hero p {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* FEATURE CARDS */
.card {
    background-color: #161B22;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #30363d;
    transition: 0.3s;
    height: 200px;
}

.card:hover {
    border: 1px solid #58A6FF;
    transform: translateY(-5px);
}

.card-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}

.card-text {
    color: #c9d1d9;
    font-size: 15px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #161B22;
}

/* CHAT MESSAGE */
[data-testid="stChatMessage"] {
    background-color: #161B22;
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 10px;
    border: 1px solid #30363d;
}

/* CHAT INPUT */
.stChatInputContainer {
    border-top: 1px solid #30363d;
    background-color: #0E1117;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #238636, #2ea043);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #2ea043, #238636);
}

/* EXPANDER */
.streamlit-expanderHeader {
    background-color: #161B22;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# RESET CHAT
# =====================================================
def reset_conversation():
    st.session_state.messages = []

# =====================================================
# SESSION MEMORY
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.title("⚖️ Legal Assistant")

    st.markdown("---")

    st.markdown("""
    ### Features

    ✅ DPDP Act Analysis  
    ✅ IPC Legal Assistance  
    ✅ Motor Vehicle Rules  
    ✅ Legal Citations  
    ✅ Multilingual Support  
    ✅ Confidence Scoring  
    """)

    st.markdown("---")

    st.info(
        "This AI provides legal information "
        "for educational purposes only."
    )

    st.button(
        "🗑️ Reset Chat",
        on_click=reset_conversation,
        use_container_width=True
    )

# =====================================================
# HERO SECTION
# =====================================================
st.markdown("""
<div class="hero">
    <h1>⚖️ Legal Assistant</h1>
    <p>
        AI-powered Legal RAG System for DPDP Act,
        IPC, Motor Vehicle Rules, and Legal Analysis
    </p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# FEATURE CARDS
# =====================================================

row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">📘 DPDP Act</div>
        <div class="card-text">
            Analyze Indian Digital Personal Data Protection
            Act compliance, consent management,
            lawful processing, and privacy obligations.
        </div>
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">🇪🇺 GDPR</div>
        <div class="card-text">
            Understand GDPR principles,
            lawful basis of processing,
            user rights, compliance,
            and international privacy regulations.
        </div>
    </div>
    """, unsafe_allow_html=True)

with row1_col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">🔐 Privacy Policies</div>
        <div class="card-text">
            Analyze organizational privacy policies,
            third-party data sharing,
            retention policies,
            and compliance obligations.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# SECOND ROW
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">👨‍💼 Employee Policies</div>
        <div class="card-text">
            Review employee privacy policies,
            workplace monitoring,
            HR data handling,
            and employment-related compliance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with row2_col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">🚗 Motor Vehicle Rules</div>
        <div class="card-text">
            Get legal insights regarding
            transport regulations,
            accident liability,
            insurance compliance,
            and traffic violations.
        </div>
    </div>
    """, unsafe_allow_html=True)

with row2_col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">⚖️ Legal Analysis</div>
        <div class="card-text">
            AI-powered legal reasoning
            using citation-based Retrieval-Augmented Generation (RAG)
            for structured legal assistance.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# EMBEDDINGS
# =====================================================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================================
# VECTOR DATABASE
# =====================================================
db = FAISS.load_local(
    "ipc_vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 8}
)

# =====================================================
# PROMPT TEMPLATE
# =====================================================
prompt_template = """
You are an advanced Indian Legal AI Assistant specializing in:

- DPDP Act
- Motor Vehicle Rules
- Indian Penal Code (IPC)
- Indian legal compliance
- Legal case analysis

Your responsibilities:

1. Understand the user query or case study carefully.
2. Determine whether the matter falls under:
   - DPDP Act
   - Motor Vehicle Rules
   - IPC
   - Other Indian legal provisions

3. Prioritize retrieving and using the provided legal context.
4. Use legal reasoning and explain conclusions clearly.
5. Provide structured, detailed, and professional responses.
6. Avoid hallucinations or unsupported legal claims.
7. If information is insufficient, clearly mention limitations.
8. Maintain a neutral and legally sound tone.
9. Do NOT provide personal opinions.
10. If necessary, recommend consulting a qualified legal expert.

------------------------------
RETRIEVED LEGAL CONTEXT:
{context}
------------------------------

USER QUESTION:
{question}

------------------------------
RESPONSE FORMAT:

 1. Case Summary
Briefly summarize the legal issue.

 2. Relevant Legal Provisions
Mention applicable sections, acts, or rules.

 3. Legal Analysis and Opinion
Provide detailed legal reasoning using the retrieved context.

 4. Supporting References
Mention relevant legal concepts, provisions, or precedents if available.

 5. Limitations
Mention if the available context is insufficient or uncertain.

------------------------------

ANSWER:
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# =====================================================
# GROQ CLIENT
# =====================================================
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# USER INPUT
# =====================================================
query = st.chat_input(
    "Ask your legal question..."
)

# =====================================================
# PROCESS QUERY
# =====================================================
if query:

    original_query = query

    # =================================================
    # LANGUAGE DETECTION
    # =================================================
    detected_lang = detect(query)

    # Translate to English if not English
    if detected_lang != "en":

        query = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(query)

    # =================================================
    # SHOW USER MESSAGE
    # =================================================
    with st.chat_message("user"):
        st.markdown(original_query)

    st.session_state.messages.append({
        "role": "user",
        "content": original_query
    })

    # =================================================
    # RETRIEVE DOCUMENTS
    # =================================================
    docs = retriever.invoke(query)

    # =================================================
    # CONFIDENCE SCORE
    # =================================================
    confidence_score = round(
        min(len(docs) / 5, 1.0) * 100,
        2
    )

    # =================================================
    # CONTEXT + CITATIONS
    # =================================================
    formatted_context = []

    citations = []

    for doc in docs:

        source = os.path.basename(
            doc.metadata.get("source", "Unknown")
        )

        page = doc.metadata.get("page", "N/A")

        snippet = doc.page_content[:600]

        citations.append({
            "source": source,
            "page": page,
            "snippet": snippet
        })

        formatted_context.append(
            f"""
SOURCE: {source}
PAGE: {page}

CONTENT:
{snippet}
"""
        )

    context = "\n\n".join(formatted_context)

    # =================================================
    # FINAL PROMPT
    # =================================================
    final_prompt = prompt.format(
        context=context,
        question=query
    )

    # =================================================
    # ASSISTANT RESPONSE
    # =================================================
    with st.chat_message("assistant"):

        with st.status(
            "⚖️ Analyzing Legal Documents...",
            expanded=True
        ):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1200
            )

            answer = response.choices[0].message.content

            # =============================================
            # TRANSLATE BACK
            # =============================================
            if detected_lang != "en":

                answer = GoogleTranslator(
                    source="en",
                    target=detected_lang
                ).translate(answer)

            final_response = f"""
⚠️ **Legal educational information only**

### Confidence Score
**{confidence_score}%**

---

{answer}
"""

            # =============================================
            # TYPING EFFECT
            # =============================================
            message_placeholder = st.empty()

            full_response = ""

            for chunk in final_response:

                full_response += chunk

                time.sleep(0.002)

                message_placeholder.markdown(
                    full_response + "▌"
                )

            message_placeholder.markdown(full_response)

            # =============================================
            # CITATIONS
            # =============================================
            with st.expander("📚 Citations & Sources"):

                for i, cite in enumerate(citations):

                    st.markdown(
                        f"### Citation {i+1}"
                    )

                    st.write(
                        f"**Source File:** {cite['source']}"
                    )

                    st.write(
                        f"**Page:** {cite['page']}"
                    )

                    st.write(
                        cite["snippet"]
                    )

                    st.markdown("---")

    # =================================================
    # SAVE CHAT
    # =================================================
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_response
    })