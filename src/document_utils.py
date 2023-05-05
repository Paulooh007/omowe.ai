import os
import sys

import pandas as pd
from typing import List
import pinecone

import cohere
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone, Qdrant
from langchain.chains.question_answering import load_qa_chain

sys.path.append(os.path.abspath('..'))

from src.constants import SUMMARIZATION_MODEL, EXAMPLES_FILE_PATH


PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")



def replace_text(text):
    if text.startswith("The answer is "):
        text = text.replace("The answer is ", "", 1)
    return text


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
    pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_ENV  # next to api key in console
    )
    context = input_document
    # The last element of the `history` list contains the most recent question asked by the user whose answer needs to be generated.
    question = history[-1][0]
    word_list = context.split()

    texts =  [" ".join(word_list[k : k + 200]) for k in range(0, len(word_list), 200)]

    # print(texts)

    embeddings = CohereEmbeddings(
        model="multilingual-22-12", cohere_api_key=COHERE_API_KEY
    )

    context_index = Pinecone.from_texts(texts, embeddings, index_name="wiki-embed")

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
    answer = replace_text(answer) 
    return answer

def generate_questions(input_document: str) -> str:
    co = cohere.Client(COHERE_API_KEY)
    prompt = f"""Write five different questions to test the understanding of the following text. The questions should be short answer, with one or two words each, and vary in difficulty from easy to hard. Provide the correct answer for each question after the question. 
Now write your own questions for this text:

Text: {input_document}

Question 1: (question_1)
Answer: (answer_1)

Question 2: (question_2)
Answer: (answer_2)

Question 3: (question_3)
Answer: (answer_3)

Question 4: (question_4)
Answer: (answer_4)

Question 5: (question_5)
Answer: (answer_5)"""
   # call the generate endpoint with your prompt and other parameters
    response = co.generate(model='command', prompt=prompt, temperature=2, max_tokens=1000, )

    # print the generated text from the response object
    # print('Generated text:\n{}'.format(response.generations[0].text))
    answer = response.generations[0].text.strip()
    print(answer)
    questions = answer.split('\n\n')
    print(questions)
    result = {}
    for question in questions:
        q, a = question.split('\n')
        result[q] = a.split(': ')[1]
    # print(result)
    # prompt = f"Generate 5 different quiz questions to test the understanding of the following text. Here's the provided text: {input_document}. Whats Questions 1 to 5 of the quiz ?:"
    # print(prompt)
    return answer #result.keys(), result.values()


def load_science():
    examples_df = pd.read_csv(EXAMPLES_FILE_PATH)
    science_doc = examples_df["doc"].iloc[0]
    sample_question = examples_df["question"].iloc[0]
    return science_doc, sample_question


def load_history():
    examples_df = pd.read_csv(EXAMPLES_FILE_PATH)
    history_doc = examples_df["doc"].iloc[1]
    sample_question = examples_df["question"].iloc[1]
    return history_doc, sample_question

def show_diff_html(seqm):
    """Unify operations between two compared strings
    seqm is a difflib.SequenceMatcher instance whose a & b are strings
    """
    output = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.b[b0:b1])
        elif opcode == 'insert':
            output.append(f"<span style='background-color:lime;'>{seqm.b[b0:b1]}</span>")
        # elif opcode == 'delete':
        #     output.append(f"<span style='background-color:red;'>{seqm.a[a0:a1]}</span>")
        elif opcode == 'replace':
            output.append(f"<span style='background-color:red;'>{seqm.a[a0:a1]}</span>")
            output.append(f"<span style='background-color:lime;'>{seqm.b[b0:b1]}</span>")
        else:
            if opcode == 'delete':
                continue
            raise RuntimeError("unexpected opcode")
    return ''.join(output)

# define a function to paraphrase text using Cohere API
def paraphrase(text):
    # create a cohere client with your API key
    client = cohere.Client(api_key=COHERE_API_KEY)

    # set the prompt for paraphrasing
    prompt = f"Rephrase this sentence in a different way: {text}"

    # generate a response using the multilingual-22-12 model
    response = client.generate(
        model="command-nightly",
        prompt=prompt,

    )
    # get the generated text
    rephrased_text = response[0].text
    print(rephrased_text)

    # compare the original and rephrased texts using difflib
    sm = difflib.SequenceMatcher(None, text, rephrased_text)
    html = show_diff_html(sm)

    return html

if __name__ == "__main__":
    with open('sample_text.txt', 'r') as file:
        text = file.read()
    # summary = summarize(text, summary_length="short", summary_format="bullets")
    # print(summary)
    # answer = question_answer(text, [["what is photosynthesis", None]])
    # print(answer)
    question = question_answer(text, ["Whats photosynthesis"])
    print(question)
