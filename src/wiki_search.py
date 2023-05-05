import os
import cohere
from typing import List
import pinecone

# load environment variables
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")


MODEL_NAME = "multilingual-22-12"
COLLECTION = "wiki-embed"

# create qdrant and cohere client
cohere_client = cohere.Client(COHERE_API_KEY)

def init_pinecone():
    pinecone.init(api_key= PINECONE_API_KEY,
            environment=PINECONE_ENV)
    index = pinecone.Index(COLLECTION)
    return index


    

index = init_pinecone()


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
    languages = [],
):


    language_mapping = {
        "English": "en",
        "Yoruba": "yo",
        "Igbo": "ig",
        "Hause": "ha",
    }

    # index.query(query_embedding, top_k=num_results, include_metadata=True)

    # prepare filters to narrow down search results
    # if the `match_text` list is not empty then create filter to find exact matching text in the documents
    query_results = index.query(
        top_k=3,
        include_metadata=True,
        vector= query_embedding,
        filter={
            'lang': {'$in': [language_mapping[lang] for lang in languages]}
        }
    )

    metadata = [record["metadata"] for record in query_results["matches"]]

    return metadata


def cross_lingual_document_search(
    user_input: str, num_results: int, languages, text_match
) -> List:
    # create an embedding for the input query
    query_embedding, _ = embed_user_query(user_input)

    # retrieve search results
    metadata = search_wiki_for_query(
        query_embedding,
        num_results,
        languages,
    )

    results = [result['title']+"\n"+result['text'] for result in metadata]

    url_list = [result['url'] + "\n\n" for result in metadata]

    return results + url_list

def document_source(
    user_input: str, num_results: int, languages, text_match
) -> List:
    query_embedding, _ = embed_user_query(user_input)

    # retrieve search results
    metadata = search_wiki_for_query(
        query_embedding,
        num_results,
        languages,
    )

    results = [result['url'] for result in metadata]

    if num_results > len(results):
        remaining_inputs = num_results - len(results)
        for input in range(remaining_inputs):
            results.append("")

    return results


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