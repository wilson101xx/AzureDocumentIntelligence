from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient 
from openai import AzureOpenAI
import re
import requests
import uuid
import os
from dotenv import load_dotenv
load_dotenv()


endpoint = os.getenv("DOC_INTEL_ENDPOINT")
key = os.getenv("DOC_INTEL_KEY")

client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))
model_id = "prebuilt-layout"  

#You will need too run this "from_local" folder
# Example python src/main.py
file_path = "document_example/Azure_whats_new.pdf"

def get_text(page):
    content = ''
    try:
        # Iterate over the lines in the page and concatenate them
        for line in page.lines:
            content += line.content + '\n'
    except Exception as e:
        print(f"Error retrieving text: {e}")
    return content


def normalize_text1(s, sep_token = " \n "):
    s = re.sub(r'\s+', ' ', s).strip()  # Replace multiple spaces with a single space
    s = re.sub(r". ,", "", s)  # Remove incorrect space before commas
    s = s.replace("..", ".")
    s = s.replace(". .", ".")
    s = s.strip()
    return s


def analyze_document(client, model_id, file_path):

    with open(file_path, "rb") as document:
        poller = client.begin_analyze_document(
            model_id=model_id,
            document=document
        )

        result = poller.result()
        count = 0
        for page in result.pages:
            count += 1
            content = get_text(page)
            normalized_content = normalize_text1(content)
            print(f"Page {count} has the following content:")
            print(normalized_content)
            print("\n")

if __name__ == "__main__":
    analyze_document(client, model_id, file_path)