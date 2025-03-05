from langchain.document_loaders import PyPDFLoader, CSVLoader, TextLoader, WebBaseLoader, YoutubeLoader

def load_integration_data(request_data):
    loaders = {
        "pdf": PyPDFLoader,
        "csv": CSVLoader,
        "text": TextLoader,
        "web": WebBaseLoader,
        "youtube": YoutubeLoader.from_youtube_url
    }
    if request_data.integration_type not in loaders:
        raise ValueError(f"Unsupported integration type: {request_data.integration_type}")
    loader_function = loaders[request_data.integration_type]
    loaded_documents = loader_function(request_data.path).load()
    if request_data.content and loaded_documents:
        return (
            loaded_documents[0].page_content
            if request_data.content == 'page_content'
            else loaded_documents[0].metadata
        )
    return loaded_documents