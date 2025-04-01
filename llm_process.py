from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from prompt_templates import *

class PostAuthenticityChecker():
    def __init__(self):
        load_dotenv()
        self.groq_api=os.getenv('GROC_LLM_API')

        self.llm=ChatGroq(api_key=self.groq_api,
                          model=os.getenv('LLM_MODEL_NAME')
                          )
        if self.llm:
            print("LLM connection established successfully.")
        else: 
            print("Failed to establish LLM connection.")



    def check_post_authenticity(self, post_content:str) -> bool:
        prompt=PromptTemplate(template=templates,input_variables=['post_content'])

        chains=RunnableSequence(prompt,self.llm, StrOutputParser())
        result=chains.invoke(input={"post_content":post_content})
        print(result)
