# name of cohere's summarization model
SUMMARIZATION_MODEL = "summarize-xlarge"

# whether to use multilingual embeddings to represent the documents or not
USE_MULTILINGUAL_EMBEDDING = True

# name of cohere's multilingual embedding model
MULTILINGUAL_EMBEDDING_MODEL = "multilingual-22-12"

# name of cohere's default embedding model
ENGLISH_EMBEDDING_MODEL = "large"

# The name with which you want to create a collection in Qdrant
CREATE_QDRANT_COLLECTION_NAME = "wiki-embed"

# name of cohere's model which will be used for generating the translation of an input document
TEXT_GENERATION_MODEL = "command-xlarge-nightly"
