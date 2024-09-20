# Document Intelligence Repository

This is a public repository designed to help understand and implement document intelligence. In this repository, you will find scripts demonstrating the use of different document intelligence models, along with corresponding Jupyter notebooks to guide you through their application.

## Getting Started

### Prerequisites

To run the scripts and Jupyter notebooks in this repository, ensure you have the following installed:

- Python 3.8+
- [Azure Form Recognizer](https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/overview)
- [Azure Search Client](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
- [OpenAI for Azure](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview)
- [Dotenv](https://pypi.org/project/python-dotenv/)

You will also need to create a `.env` file with the following environment variables:

```bash
DOC_INTEL_ENDPOINT=<Your Azure Form Recognizer Endpoint>
DOC_INTEL_KEY=<Your Azure Form Recognizer Key>
