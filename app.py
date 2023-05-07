# coding: utf-8

import gradio as gr
from src.document_utils import (
    summarize,
    question_answer,
    generate_questions,
    load_history,
    load_science,
    generate_questions,
    load_history,
    load_science,
    paraphrase,
)
from src.wiki_search import cross_lingual_document_search, translate_text
from src.theme import CustomTheme


max_search_results = 3


def reset_chatbot():
    return gr.update(value="")


def get_user_input(input_question, history):
    return "", history + [[input_question, None]]


def study_doc_qa_bot(input_document, history):
def study_doc_qa_bot(input_document, history):
    bot_message = question_answer(input_document, history)
    history[-1][1] = bot_message
    return history

# def translate_text(doc):
#     translator = EasyGoogleTranslate()

#     doc = " ".join(doc.split()[:4800])
#     result = translator.translate(doc, target_language='en')
#     return result
    

custom_theme = CustomTheme()


with gr.Blocks(theme=custom_theme) as demo:
    gr.HTML(
        """<html><center><img src='file/logo/omowe_logo.png', alt='omowe.ai logo', width=820, height=312 /></center><br></html>"""
        """<html><center><img src='file/logo/omowe_logo.png', alt='omowe.ai logo', width=820, height=312 /></center><br></html>"""
    )

    qa_bot_state = gr.State(value=[])

    with gr.Tabs():
        
        with gr.TabItem("Document Search"):
            gr.HTML(
                """<p style="text-align:center;font-size:24px;"><b>Search across a set of study materials in your own native language or even a mix of languages.</p>"""
            )
            gr.HTML(
                """<p style="text-align:center; font-style:italic; font-size:16px;">Get started with a pre-indexed set of study materials spaning various subjects (History, Literature, Philosophy, Government etc) in 4 different languages.</p>"""
            )

            with gr.Row():
                text_match = gr.CheckboxGroup(
                    ["Full Text Search"], label="find exact text in documents", visible=False
                )

            with gr.Row():
                lang_choices = gr.CheckboxGroup(
                    [
                        "English",
                        "Yoruba",
                        "Igbo",
                        "Hausa",
                    ],
                    label="Filter results based on language",
                    value = "Yoruba"
                )

            with gr.Row():
                with gr.Column():
                    user_query = gr.Text(
                        label="Enter query here",
                        placeholder="Search through all your documents",
                    )

                    num_search_results = gr.Slider(
                        1,
                        max_search_results,
                        visible=False,
                        value=max_search_results,
                        step=1,
                        interactive=True,
                        label="How many search results to show:",
                    )

                    with gr.Row():

                        with gr.Column():
                            query_match_out_1 = gr.Textbox(
                                label= f"Search Result 1"
                                )

                        with gr.Column():
                            with gr.Accordion("Translate Search Result", open=False):
                                translate_1 = gr.Button(
                                    label="Translate",
                                    value="Translate",
                                    variant="primary",
                                )
                                translate_res_1 = gr.Textbox(
                                    label=f"Translation Result 1"
                                )

                    with gr.Row():
                        with gr.Column():
                            query_match_out_2 = gr.Textbox(label=f"Search Result 2")

                        with gr.Column():
                            with gr.Accordion("Click to View Source", open=False):
                                source_res_2 = gr.Textbox(
                                    label=f"Source Url"
                                )

                                translate_btn_2 = gr.Button(
                                    label="Translate Text",
                                    value="Translate Text",
                                    variant="primary",
                                )
                                translate_res_2 = gr.Textbox(
                                    label=f"Translation in English",

                                )

                    with gr.Row():
                        with gr.Column():
                            query_match_out_3 = gr.Textbox(label=f"Search Result 3")

                        with gr.Column():
                            with gr.Accordion("Click to View Source", open=False):
                                source_res_3 = gr.Textbox(
                                    label=f"Source Url"
                                )
                                translate_btn_3 = gr.Button(
                                    label="Translate Text",
                                    value="Translate Text",
                                    variant="primary",
                                )
                                translate_res_3= gr.Textbox(
                                    label=f"Translation in English",
                                )

        with gr.TabItem("Q&A"):
            gr.HTML(
                """<p style="text-align:center; font-size:16px;"><b>Looking to breeze through your study materials effortlessly? Simply upload your documents and fire away any questions you have!</p>"""
            )
            with gr.Row():
                with gr.Accordion("Click to use preloaded examples", open=False):
            
                    example_2 = gr.Button(
                        "Load History of Nigeria", variant="primary"
                    )
                    example_1 = gr.Button(
                        "Load Science of Photosynthesis", variant="primary"
                    )

            with gr.Row():
                with gr.Column():
                    input_document = gr.Text(label="Copy your document here", lines=2)
                    input_document_pdf = gr.inputs.File(label="Uplaod file")


                with gr.Column():
                    chatbot = gr.Chatbot(label="Chat History")
                    input_question = gr.Text(
                        label="Ask a question",
                        placeholder="Type a question here and hit enter.",
                    )
                    clear = gr.Button("Clear", variant="primary")


        
        with gr.TabItem("Summarize"):
            gr.HTML(
                """<p style="text-align:center; font-size:24px;"><b> Get the most out of your study materials!</p>"""
            )
            gr.HTML(
                """<p style="text-align:center; font-size:16px;"><b>You can easily upload your documents and generate quick summaries and practice questions in a flash.</p>"""
            )

            with gr.Row():
                with gr.Accordion("Click to use preloaded examples", open=False):
                    example_4 = gr.Button(
                        "Load History of Nigeria", variant="primary"
                    )
                    example_3 = gr.Button(
                        "Load Science of Photosynthesis", variant="primary"
                    )

            with gr.Row():
                with gr.Column():
                    summary_input = gr.Text(label="Document", lines=5)
                with gr.Column():
                    summary_output = gr.Text(label="Generated Summary", lines=5)
                    invisible_comp = gr.Text(label="Dummy Component", visible=False)

            with gr.Row():
                with gr.Column():
                    with gr.Accordion("Summary Settings", open=False):
                        summary_length = gr.Radio(
                            ["short", "medium", "long"],
                            label="Summary Length",
                            value="long",
                        )
                    
                        summary_format = gr.Radio(
                            ["paragraph", "bullets"],
                            label="Summary Format",
                            value="bullets",
                        )
                        extractiveness = gr.Radio(
                            ["low", "medium", "high"],
                            label="Extractiveness",
                            info="Controls how close to the original text the summary is.",
                            visible=False,
                            value="high",
                        )
                        temperature = gr.Slider(
                            minimum=0,
                            maximum=5.0,
                            value=0.64,
                            step=0.1,
                            interactive=True,
                            visible=False,
                            label="Temperature",
                            info="Controls the randomness of the output. Lower values tend to generate more “predictable” output, while higher values tend to generate more “creative” output.",
                        )

            
            with gr.Row():
                generate_summary = gr.Button("Generate Summary", variant="primary")
            
            with gr.Row():
                generate_questions_btn = gr.Button("Generate practice questions", variant="primary")
            with gr.Row():
                generate_output = gr.Text(label="Generated questions", lines=5)


    # fetch answer for submitted question corresponding to input document
    input_question.submit(
        get_user_input,
        [input_question, chatbot],
        [input_question, chatbot],
        queue=False,
    ).then(study_doc_qa_bot, [input_document, chatbot], chatbot)

    # reset the chatbot Q&A history when input document changes
    input_document.change(fn=reset_chatbot, inputs=[], outputs=chatbot)

    # Loading examples on click for Q&A module
    example_1.click(
        load_history,
        [],
        [input_document, input_question],
        queue=False,
    )

    example_2.click(
        load_science,
        [],
        [input_document, input_question],
        queue=False,
    )

    # Loading examples on click for Q&A module
    example_3.click(
        load_history,
        [],
        [summary_input, invisible_comp],
        queue=False,
    )

    example_4.click(
        load_science,
        [],
        [summary_input, invisible_comp],
        queue=False,
    )

    # generate summary corresponding to document submitted by the user.
    generate_summary.click(
        summarize,
        [summary_input, summary_length, summary_format, extractiveness, temperature],
        [summary_output],
        queue=False,
    )

    generate_questions_btn.click(
        generate_questions,
        [summary_input],
        [generate_output],
        queue=False,
    )

    # generate paraphrase corresponding to document submitted by the user.
    generate_paraphrase.click(
        paraphrase,
        [paraphrase_input],
        [paraphrase_output],
        queue=False,
    )

    # clear the chatbot Q&A history when this button is clicked by the user
    clear.click(lambda: None, None, chatbot, queue=False)

    # run search as user is typing the query
    user_query.change(
        cross_lingual_document_search,
        [user_query, num_search_results, lang_choices, text_match],
        [query_match_out_1, query_match_out_2, query_match_out_3],
        queue=False,
    )

    # run search if user submits query
    user_query.submit(
        cross_lingual_document_search,
        [user_query, num_search_results, lang_choices, text_match],
        [query_match_out_1, query_match_out_2, query_match_out_3, \
            translate_res_1,translate_res_2,translate_res_3],
        [query_match_out_1, query_match_out_2, query_match_out_3, \
            source_res_1,source_res_2,source_res_3],
        queue=False,
    )


    # translate results corresponding to 1st search result obtained if user clicks 'Translate'
    translate_btn_1.click(
        translate_text,
        [query_match_out_1],
        [translate_res_1],
        queue=False,
    )
    translate_btn_2.click(
        translate_text,
        [query_match_out_2],
        [translate_res_2],
        queue=False,
    )
    translate_btn_3.click(
        translate_text,
        [query_match_out_3],
        [translate_res_3],
        queue=False,
    )


if __name__ == "__main__":
    demo.launch(debug=True)
