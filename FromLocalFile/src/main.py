import os
import re
import logging
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import Optional


# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Fetch endpoint and key from environment
DOC_INTEL_ENDPOINT  = os.getenv("DOC_INTEL_ENDPOINT")
DOC_INTEL_KEY  = os.getenv("DOC_INTEL_KEY")
MODEL_ID = "prebuilt-layout"

def create_client(endpoint: str, key: str):
    try:
        return DocumentAnalysisClient(endpoint, AzureKeyCredential(key))
    except Exception as e:
        logging.error(f"Failed to create DocumentAnalysisClient: {e}")
        raise


def extract_page_text(page) -> str:
    content = ''
    try:
        content = '\n'.join([line.content for line in page.lines])
    except Exception as e:
        logging.error(f"Error extracting text from page: {e}")
    return content


def normalize_text(s, sep_token=" \n "):
    s = re.sub(r'\s+', ' ', s).strip()  # Replace multiple spaces with a single space
    s = re.sub(r". ,", "", s)  # Remove incorrect space before commas
    s = s.replace("..", ".")
    s = s.replace(". .", ".")
    s = s.strip()
    return s

# Example file path to analyze
file_path = "document_example/Azure_whats_new.pdf"

def analyze_document(client: DocumentAnalysisClient, model_id: str, file_path: str) -> None:
    try:
        with open(file_path, "rb") as document:
            poller = client.begin_analyze_document(model_id=model_id, document=document)
            result = poller.result()
            
            for page_num, page in enumerate(result.pages, start=1):
                content = extract_page_text(page)
                normalized_content = normalize_text(content)
                logging.info(f"Page {page_num} content:\n{normalized_content}\n")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Error analyzing document: {e}")



if __name__ == "__main__":
    if not DOC_INTEL_ENDPOINT or not DOC_INTEL_KEY:
        logging.error("Environment variables DOC_INTEL_ENDPOINT or DOC_INTEL_KEY are not set.")
        exit(1)

    client = create_client(DOC_INTEL_ENDPOINT, DOC_INTEL_KEY)

    file_path = "document_example/Azure_whats_new.pdf"
    
    analyze_document(client, MODEL_ID, file_path)