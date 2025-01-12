import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

import certifi

# Set the SSL_CERT_FILE environment variable to the path of certifi's bundle


#langsmith tracking
# os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_TRACING_V2"]="true"
# os.environ["LANGCHAIN_PROJECT"]=" Q&A chatbot with OPENAI"
os.environ["SSL_CERT_FILE"] = certifi.where()
# api_key = os.getenv('OPENAI_API_KEY')
# openai.api_key = os.getenv('OPENAI_API_KEY')


#PROMPT TEMPLATE
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","you are an helpful Assistant.please response to the user queries with accuate and precised answers"),
        ("user","Question:{question}")
    ]
)

#function
def generate_response(question,api_key,llm,temperature,max_tokens):
    llm=ChatOpenAI(model=llm,openai_api_key=api_key)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer



#Streamlit app
st.title("Enhanced Q&A Chatbot With OpenAI")

st.sidebar.title("Settings")
api_key_input=st.sidebar.text_input("Enter your open AI API key:",type="password")

#DROP DOWN
llm=st.sidebar.selectbox("Select An OPENAI Model",["gpt-4o","gpt-4-turbo","gpt-4"])

#adjust temperature parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max tokens",min_value=50,max_value=300,value=150)


#MAIN INTERFACE for user input
st.write("Go Ahead an Ask any Question")
user_input=st.text_input("YOU:")


# if user_input:
#     response=generate_response(user_input,api_key,llm,temperature,max_tokens)
#     st.write(response)
# else:
#     st.write("Please provide the Query")    
# st.write(api_key_input)

if api_key_input:  # Ensure the user provides the API key
    if user_input:
        # try:
            response = generate_response(user_input, api_key_input, llm, temperature, max_tokens)
            
            st.write(response)
        # except Exception as e:
        #     st.write(f"Error: {str(e)}")
    else:
        st.write("Please provide a query.")
else:
    st.write("Please enter a valid OpenAI API key.")




   

