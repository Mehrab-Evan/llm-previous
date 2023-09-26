import os
import pandas as pd
# import matplotlib.pyplot as plt
# from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
# from langchain.llms import OpenAIChat
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
import PyPDF2
from langchain.text_splitter import CharacterTextSplitter
import pickle
from langchain.chains.question_answering import load_qa_chain
import testing_intent

load_dotenv()
# You MUST add your PDF to local files in this notebook (folder icon on left hand side of screen)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        prompt = "You will act as an AI assistant of the following organization it is your organization. When user will ask you will response from these texts providing below. If user ask any out of contexts question you shall tell him that you can only talk about these following text mentioning. Ask user questions all the time if he needs anything else to know. and response if user thanks you or show gratitude Take these as prompts : "
    return prompt + text


# raw_text = extract_text_from_pdf("Assessment Procedure.pdf")

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
# chunks = text_splitter.split_text(raw_text)

# print(chunks[0])
#
# token_counts = [count_tokens(chunk.page_content) for chunk in chunks]
#
# # Create a DataFrame from the token counts
# df = pd.DataFrame({'Token Count': token_counts})
#
# # Create a histogram of the token count distribution
# df.hist(bins=40, )
#
# # Show the plot
# plt.show()

# Get embedding model
# embeddings = OpenAIEmbeddings()
# embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
# DID ONCE NOW STOPPING
# knowledgebase = FAISS.from_texts(texts=chunks, embedding=embeddings)
# print(type(knowledgebase))
# print((knowledgebase))
# pickled_str = pickle.dumps(knowledgebase)
# testing_intent.insert("111224", knowledgebase)
result = testing_intent.get_msg_history("111224")
knowledgebase = result["knowledge"]
print(type(knowledgebase))
# print((pickled_str))
# kbase = pickle.loads(kb)
# print(type(kbase))
print((knowledgebase))

# Check similarity search is working
# query = "What are you about?"
# docs = knowledgebase.similarity_search(query)
# print(docs[0])
# result = testing_intent.get_msg_history("1112")
# kb = result["embedded_txt"]
# print((kb))
# knowledgebase = pickle.loads(kb)
# Create QA chain to integrate similarity search with user queries (answer query from knowledge base)

# chain = load_qa_chain(ChatOpenAI(temperature=0.9), chain_type="stuff")
chat_history = []
qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.9), knowledgebase.as_retriever())

while(True):
    query = input("Human Message : ")
    docs = knowledgebase.similarity_search(query)
    # x = chain.run(input_documents=docs, question=query)


    result = qa({"question": query, "chat_history": chat_history})

    chat_history.append((query, result['answer']))

    print("Chatbot : "+result["answer"])
    # print(chat_history)

