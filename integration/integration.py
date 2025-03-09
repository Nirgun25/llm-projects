from langchain.document_loaders import PyPDFLoader, CSVLoader, TextLoader, WebBaseLoader, YoutubeLoader

def load_integration_data(integration_type,path,content):
    loaders = {
        "pdf": PyPDFLoader,
        "csv": CSVLoader,
        "text": TextLoader,
        "web": WebBaseLoader,
        "youtube": YoutubeLoader.from_youtube_url
    }
    if integration_type not in loaders:
        raise ValueError(f"Unsupported integration type: {integration_type}")
    loader_function = loaders[integration_type]
    loaded_documents = loader_function(path).load()
    if content and loaded_documents:
        return (
            loaded_documents[0].page_content
            if content == 'page_content'
            else loaded_documents[0].metadata
        )
    return loaded_documents