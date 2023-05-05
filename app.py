# coding: utf-8

import gradio as gr
from src.document_utils import (
    summarize,
    question_answer,
    load_gpl_license,
    load_pokemon_license,
    paraphrase,
)
from src.wiki_search import cross_lingual_document_search, translate_search_result
from src.theme import CustomTheme

max_search_results = 3


def reset_chatbot():
    return gr.update(value="")


def get_user_input(input_question, history):
    return "", history + [[input_question, None]]


def legal_doc_qa_bot(input_document, history):
    bot_message = question_answer(input_document, history)
    history[-1][1] = bot_message
    return history


custom_theme = CustomTheme()


with gr.Blocks(theme=custom_theme) as demo:
    gr.HTML(
        """<html><center><img src='file/logo/flc_design4.png', alt='Legal-ease logo', width=250, height=250 /></center><br></html>"""
    )

    qa_bot_state = gr.State(value=[])

    with gr.Tabs():
        with gr.TabItem("Q&A"):
            gr.HTML(
                """<p style="text-align:center;"><b>Legal documents can be difficult to comprehend and understand. Add a legal document below and ask any questions related to it.</p>"""
            )

            with gr.Row():
                with gr.Column():
                    input_document = gr.Text(label="Copy your document here", lines=10)

                with gr.Column():
                    chatbot = gr.Chatbot(label="Chat History")
                    input_question = gr.Text(
                        label="Ask a question",
                        placeholder="Type a question here and hit enter.",
                    )
                    clear = gr.Button("Clear", variant="primary")

            with gr.Row():
                with gr.Accordion("Show example inputs I can load:", open=False):
                    example_1 = gr.Button(
                        "Load GPL License Document", variant="primary"
                    )
                    example_2 = gr.Button(
                        "Load Pokemon Go Terms of Service", variant="primary"
                    )

        with gr.TabItem("Summarize"):
            gr.HTML(
                """<p style="text-align:center;"><b>Reading through long text can be very time-consuming. Add your document below and generate a quick summary for it.</p>"""
            )

            with gr.Row():
                with gr.Column():
                    summary_input = gr.Text(label="Document", lines=10)
                    generate_summary = gr.Button("Generate Summary", variant="primary")

                with gr.Column():
                    summary_output = gr.Text(label="Summary", lines=10)
                    invisible_comp = gr.Text(label="Dummy Component", visible=False)

            with gr.Row():
                with gr.Accordion("Advanced Settings:", open=False):
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
                with gr.Accordion("Show example inputs I can load:", open=False):
                    example_3 = gr.Button(
                        "Load GPL License Document", variant="primary"
                    )
                    example_4 = gr.Button(
                        "Load Pokemon Go Terms of Service", variant="primary"
                    )
        with gr.TabItem("Paraphrase"):
            gr.HTML(
                """<p style="text-align:center;"><b>Paraphraser. Add your document below and generate a rephrase for it.</p>"""
            )

            with gr.Row():
                with gr.Column():
                    paraphrase_input = gr.Text(label="Document", lines=10)
                    generate_paraphrase = gr.Button("Paraphrase", variant="primary")

                with gr.Column():
                    paraphrase_output = gr.HTML(label="Paraphrase", lines=10)
                    invisible_comp = gr.Text(label="Dummy Component", visible=False)

            with gr.Row():
                with gr.Accordion("Advanced Settings:", open=False):
                    paraphrase_length = gr.Radio(
                        ["short", "medium", "long"],
                        label="Paraphrase Length",
                        value="long",
                    )
                    paraphrase_format = gr.Radio(
                        ["paragraph", "bullets"],
                        label="Paraphrase Format",
                        value="bullets",
                    )
                    extractiveness = gr.Radio(
                        ["low", "medium", "high"],
                        label="Extractiveness",
                        info="Controls how close to the original text the paraphrase is.",
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

        with gr.TabItem("Document Search"):
            gr.HTML(
                """<p style="text-align:center;"><b>Search across a set of study materials in your own native language or even a mix of languages.</p>"""
            )
            gr.HTML(
                """<p style="text-align:center; font-style:italic;">Get started with a pre-indexed set of study materials spaning various subjects (History, Literature, Philosophy, Government etc) in 4 different languages.</p>"""
            )

            with gr.Row():
                text_match = gr.CheckboxGroup(
                    ["Full Text Search"], label="find exact text in documents"
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
                            with gr.Accordion("Translate Search Result", open=False):
                                translate_2 = gr.Button(
                                    label="Translate",
                                    value="Translate",
                                    variant="primary",
                                )
                                translate_res_2 = gr.Textbox(
                                    label=f"Translation Result 2"
                                )

                    with gr.Row():
                        with gr.Column():
                            query_match_out_3 = gr.Textbox(label=f"Search Result 3")

                        with gr.Column():
                            with gr.Accordion("Translate Search Result", open=False):
                                translate_3 = gr.Button(
                                    label="Translate",
                                    value="Translate",
                                    variant="primary",
                                )
                                translate_res_3 = gr.Textbox(
                                    label=f"Translation Result 3"
                                )

    # fetch answer for submitted question corresponding to input document
    input_question.submit(
        get_user_input,
        [input_question, chatbot],
        [input_question, chatbot],
        queue=False,
    ).then(legal_doc_qa_bot, [input_document, chatbot], chatbot)

    # reset the chatbot Q&A history when input document changes
    input_document.change(fn=reset_chatbot, inputs=[], outputs=chatbot)

    # Loading examples on click for Q&A module
    example_1.click(
        load_gpl_license,
        [],
        [input_document, input_question],
        queue=False,
    )

    example_2.click(
        load_pokemon_license,
        [],
        [input_document, input_question],
        queue=False,
    )

    # Loading examples on click for Q&A module
    example_3.click(
        load_gpl_license,
        [],
        [summary_input, invisible_comp],
        queue=False,
    )

    example_4.click(
        load_pokemon_license,
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
        [query_match_out_1, query_match_out_2, query_match_out_3],
        queue=False,
    )

    # translate results corresponding to 1st search result obtained if user clicks 'Translate'
    translate_1.click(
        translate_search_result,
        [query_match_out_1, user_query],
        [translate_res_1],
        queue=False,
    )

    # translate results corresponding to 2nd search result obtained if user clicks 'Translate'
    translate_2.click(
        translate_search_result,
        [query_match_out_2, user_query],
        [translate_res_2],
        queue=False,
    )

    # translate results corresponding to 3rd search result obtained if user clicks 'Translate'
    translate_3.click(
        translate_search_result,
        [query_match_out_3, user_query],
        [translate_res_3],
        queue=False,
    )


if __name__ == "__main__":
    demo.launch(debug=True)
