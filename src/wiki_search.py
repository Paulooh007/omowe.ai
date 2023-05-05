import os
import cohere
from typing import List
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client import models

CWD = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(os.path.dirname(CWD), ".env")
load_dotenv(dotenv_path)
# load environment variables
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

MODEL_NAME = "multilingual-22-12"
COLLECTION = "wiki-embed"

# create qdrant and cohere client
cohere_client = cohere.Client(COHERE_API_KEY)

qdrant_client = QdrantClient(
    url=QDRANT_HOST,
    prefer_grpc=True,
    api_key=QDRANT_API_KEY,
)

def embed_user_query(user_query):

    embeddings = cohere_client.embed(
        texts=[user_query],
        model=MODEL_NAME,
    )
    query_embedding = embeddings.embeddings[0]
    return query_embedding, user_query


def search_wiki_for_query(
    query_embedding,
    num_results = 3,
    user_query= "",
    languages = [],
    match_text = None,
):
    filters = []

    language_mapping = {
        "English": "en",
        "Yoruba": "yo",
        "Igbo": "ig",
        "Hause": "ha",
    }

    # prepare filters to narrow down search results
    # if the `match_text` list is not empty then create filter to find exact matching text in the documents
    if match_text:
        filters.append(
            models.FieldCondition(
                key="text",
                match=models.MatchText(text=user_query),
            )
        )

    # filter documents based on language before performing search:
    if languages:
        for lang in languages:
            filters.append(
                models.FieldCondition(
                    key="lang",
                    match=models.MatchValue(
                        value=language_mapping[lang],
                    ),
                )
            )

    # perform search and get results
    results = qdrant_client.search(
        collection_name=COLLECTION,
        query_filter=models.Filter(should=filters),
        search_params=models.SearchParams(hnsw_ef=128, exact=False),
        query_vector=query_embedding,
        limit=num_results,
    )
    return results


def cross_lingual_document_search(
    user_input: str, num_results: int, languages, text_match
) -> List:
    """
    Wrapper function for performing search on the collection of documents for the given user query.
    Prepares query embedding, retrieves search results, checks if expected number of search results are being returned.
        Args:
            user_input (`str`):
                The user input based on which search will be performed.
            num_results (`str`):
                The number of expected search results.
            languages (`str`):
                The list of languages based on which search results must be filtered.
            text_match (`str`):
                A field based on which it is decided whether to perform full-text-match while performing search.
        Returns:
            final_results (`List[str]`):
                A list containing the final search results corresponding to the given user input.
    """
    # create an embedding for the input query
    query_embedding, _ = embed_user_query(user_input)

    # retrieve search results
    result = search_wiki_for_query(
        query_embedding,
        num_results,
        user_input,
        languages,
        text_match,
    )
    final_results = [result[i].payload["text"] for i in range(len(result))]
    
    # check if number of search results obtained (i.e. `final_results`) is matching with number of expected search results i.e. `num_results`
    if num_results > len(final_results):
        remaining_inputs = num_results - len(final_results)
        for input in range(remaining_inputs):
            final_results.append("")

    return final_results

def document_source(
    user_input: str, num_results: int, languages, text_match
) -> List:
    query_embedding, _ = embed_user_query(user_input)

    # retrieve search results
    result = search_wiki_for_query(
        query_embedding,
        num_results,
        user_input,
        languages,
        text_match,
    )
    sources = [result[i].payload["url"] for i in range(len(result))]
    
    # check if number of search results obtained (i.e. `final_results`) is matching with number of expected search results i.e. `num_results`
    if num_results > len(sources):
        remaining_inputs = num_results - len(sources)
        for input in range(remaining_inputs):
            sources.append("")

    return sources


def translate_search_result():
    pass

if __name__ == "__main__":
    # query_embedding, user_query = embed_user_query("Who is the president of Nigeria")
    # result = search_wiki_for_query(query_embedding,user_query=user_query)

    # for item in result:
    #     print(item.payload["url"])
    result = cross_lingual_document_search("Who is the president of Nigeria", 
                                        num_results=3, 
                                        languages=["Yoruba"], 
                                        text_match=False)
    print(result, len(result))