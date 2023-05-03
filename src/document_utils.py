import os
import pandas as pd
from typing import List
from dotenv import load_dotenv

import cohere
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Qdrant
from langchain.chains.question_answering import load_qa_chain

from src.constants import SUMMARIZATION_MODEL, EXAMPLES_FILE_PATH


# load environment variables
CWD = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(os.path.dirname(CWD), ".env")
load_dotenv(dotenv_path)
# load environment variables
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")


def summarize(
    document: str,
    summary_length: str,
    summary_format: str,
    extractiveness: str = "high",
    temperature: float = 0.6,
) -> str:
    """
    Generates a summary for the input document using Cohere's summarize API.
        Args:
            document (`str`):
                The document given by the user for which summary must be generated.
            summary_length (`str`):
                A value such as 'short', 'medium', 'long' indicating the length of the summary.
            summary_format (`str`):
                This indicates whether the generated summary should be in 'paragraph' format or 'bullets'.
            extractiveness (`str`, *optional*, defaults to 'high'):
                A value such as 'low', 'medium', 'high' indicating how close the generated summary should be in meaning to the original text.
            temperature (`str`):
                This controls the randomness of the output. Lower values tend to generate more “predictable” output, while higher values tend to generate more “creative” output.
        Returns:
            generated_summary (`str`):
                The generated summary from the summarization model.
    """

    summary_response = cohere.Client(COHERE_API_KEY).summarize(
        text=document,
        length=summary_length,
        format=summary_format,
        model=SUMMARIZATION_MODEL,
        extractiveness=extractiveness,
        temperature=temperature,
    )
    generated_summary = summary_response.summary
    return generated_summary


def question_answer(input_document: str, history: List) -> str:
    """
    Generates an appropriate answer for the question asked by the user based on the input document.
        Args:
            input_document (`str`):
                The document given by the user for which summary must be generated.
            history (`List[List[str,str]]`):
                A list made up of pairs of input question asked by the user & corresponding generated answers. It is used to keep track of the history of the chat between the user and the model.
        Returns:
            answer (`str`):
                The generated answer corresponding to the input question and document received from the user.
    """
    context = input_document
    # The last element of the `history` list contains the most recent question asked by the user whose answer needs to be generated.
    question = history[-1][0]

    texts = [context[k : k + 256] for k in range(0, len(context.split()), 256)]

    embeddings = CohereEmbeddings(
        model="multilingual-22-12", cohere_api_key=COHERE_API_KEY
    )
    context_index = Qdrant.from_texts(
        texts, embeddings, url=QDRANT_HOST, api_key=QDRANT_API_KEY
    )

    prompt_template = """Text: {context}
    Question: {question}
    Answer the question based on the text provided. If the text doesn't contain the answer, reply that the answer is not available."""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Generate the answer given the context
    chain = load_qa_chain(
        Cohere(
            model="command-xlarge-nightly", temperature=0, cohere_api_key=COHERE_API_KEY
        ),
        chain_type="stuff",
        prompt=PROMPT,
    )
    relevant_context = context_index.similarity_search(question)
    answer = chain.run(input_documents=relevant_context, question=question)
    answer = answer.replace("\n", "").replace("Answer:", "")
    return answer


def load_gpl_license():
    pass

def load_pokemon_license():
    pass

if __name__ == "__main__":
    with open('sample_text.txt', 'r') as file:
        text = file.read()
    # summary = summarize(text, summary_length="short", summary_format="bullets")
    # print(summary)
    answer = question_answer(text, [["what is photosynthesis", None]])
    print(answer)
