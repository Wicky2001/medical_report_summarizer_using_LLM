from dotenv import load_dotenv
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
import boto3
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from presidio_anonymizer.entities import  OperatorConfig
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from utills.logging import update_excel_sheet,print_summary

load_dotenv()


def get_aws_client():
    bedrock = boto3.client(
    service_name = "bedrock-runtime",
    region_name = os.getenv("AWS_REGION"),
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    return bedrock



def anonymize_langchain_doc(lang_chain_doc):
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    docs = lang_chain_doc
    full_report = ""
    

    for doc in docs:
        doc.page_content = anonymize_text(input_text=doc.page_content,analyzer=analyzer,anonymizer=anonymizer)
        full_report += doc.page_content
    return docs,full_report



def get_summerized_response(document_location):
    client = get_aws_client()
    llm = init_chat_model("amazon.nova-micro-v1:0",client=client)
   

    loader = PyPDFLoader(document_location)
    docs = loader.load()
    anonymized_docs,full_report = anonymize_langchain_doc(docs)

        
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            "Extract and summarize the following medical report into structured sections. Include the following sections: "
            "1. **Patient Info**: Briefly summarize patient demographics and relevant history. "
            "2. **Diagnosis**: State the primary diagnosis or findings. "
            "3. **Treatment**: Outline the proposed treatment or management plan. "
            "4. **Recommendations**: Highlight any critical follow-up actions or recommendations. "
            "Keep the summary concise and professional.\\n\\n{context}  just only give summer I do not want any other information."
        )
    ]
    )

    # Instantiate chain
    chain = create_stuff_documents_chain(llm, prompt)

    # Invoke chain
    summary = chain.invoke({"context": anonymized_docs})
    # summary = chain.invoke({"context": docs})
   

   

    print_summary(summary=summary)
    print("Updating excel sheet !!!!!!!")
    update_excel_sheet("medical_reports.xlsx", full_report, summary)

    return summary




def anonymize_text(input_text,analyzer,anonymizer):
    


    results_analyzer = analyzer.analyze(text=input_text,language='en')
    # print(results_analyzer)
    

    operators = {"DEFAULT": OperatorConfig("replace")}
    result = anonymizer.anonymize(
        text=input_text,
        analyzer_results=results_analyzer,
        operators=operators
    )

    

    return result.text







