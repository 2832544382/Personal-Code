import os
import sys

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import re

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

import base64
from io import BytesIO

from IPython.display import HTML, display
from PIL import Image

sys.path.append("./readtext")
from readtext import text_rec as gt


def is_path(input_value):
    return os.path.exists(input_value)

def convert_to_base64(pil_image):
    """
    Convert PIL images to Base64 encoded strings

    :param pil_image: PIL image
    :return: Re-sized Base64 string
    """

    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def plt_img_base64(img_base64):
    """
    Disply base64 encoded string as image

    :param img_base64:  Base64 string
    """
    # Create an HTML img tag with the base64 string as the source
    image_html = f'<img src="data:image/png;base64,{img_base64}" />'
    # Display the image by rendering the HTML
    display(HTML(image_html))

def prompt_func(data):
    text = data["text"]
    image = data["image"]

    image_part = {
        "type": "image_url",
        "image_url": f"data:image/png;base64,{image}",
    }

    content_parts = []

    text_part = {"type": "text", "text": text}

    content_parts.append(image_part)
    content_parts.append(text_part)

    return [HumanMessage(content=content_parts)]


def parse_rhythm_result(rhythm_result):
    # Extract notes from the input string
    notes = rhythm_result

    # Define the pattern to extract content within square brackets
    pattern = r'\[(.*?)\]'

    # Find all matches of the pattern in the notes string
    matches = re.findall(pattern, notes)

    # Initialize an empty list to store the final result
    result = []

    # Iterate over each matched group
    for match in matches:
        # Find all numbers in the matched group
        numbers = re.findall(r'\d+', match)

        # Initialize a list to store split numbers
        split_numbers = []

        # Iterate over each found number
        for number in numbers:
            # Convert each digit in the number to an integer and store it in a list
            split_numbers.append([int(digit) for digit in number])

        # Append the list of split numbers to the result list
        result.append(split_numbers)

    return result

def bot_chat():

    notes = ""

    print("Bot: Hello there, how can I help you?")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "play"]:
            print("wait a second, I will play it for you!")
            break

        if is_path(user_input) == True:

            rhythm_result = gt.get_text(user_input)

            #print('Bot:',rhythm_result)

            #Cannot recognize large size figure
            '''
            llm = ChatOllama(model="llava-llama3")
            chain = prompt_func | llm | StrOutputParser()
            pil_image = Image.open(user_input)
            image_b64 = convert_to_base64(pil_image)
            plt_img_base64(image_b64)
            rhythm_result = chain.invoke(
            {"text": "Give me the number inside the image, you must return all numbers in only 1 square bracket "
                     "and use - to connect them, the format is [1-2-3-4]", "image": image_b64})

            print("wait a second, I will play it for you!")
            '''


        elif is_path(user_input) == False:
            template = """Question: {question}

            Answer: Let's think step by step."""

            prompt = ChatPromptTemplate.from_template(template)

            llm = OllamaLLM(model="llama3")

            chain = prompt | llm
            rhythm_result = chain.invoke({
                "question": f"""you are asking to make a music score with Numbered Musical Notation style.
                                        For the output you must follow these: 
                                        A single number is a note.
                                        For each beat, it can take crotchets: 1, quavers: 12, 
                                        and semiquavers: 1234 (must build up by 4 numbers), 
                                        quavers must build up by 2 notes, semiquavers must build up by 4 notes.
                                        crotchets,quavers,semiquavers are counted as a beat.
                                        Each beat can only take one of crotchets, quavers, semiquavers,no longer than these length
                                        Here is a sample of music score '[1-47-33-4561]' with square bracket, 
                                        there are 4 beats in the score they are: 1(crotchets),47(quavers),33(quavers),4561(semiquavers), 
                                        there are no symbols between notes, '-' symbol is used to separate beats. 
                                        The all notes in the Numbered Musical Notation can only build with 1,2,3,4,5,6,7,8, never use other numbers.
                                        Do not cosider any other factors, no speed, no tempo, no BPM. 
                                        They will ask you to give a music score with numerous beats, 
                                        remember in each beat, only crotchets, quavers, semiquavers is acceptable.
                                        And all the beats should write in one music score, which means all in a single square bracket.
                                        do not write other things, also the limitations of the notes.
                                        You only need to make a music score do not ask questions, and remember the score need square bracket.
                                        Do not give the user any coding advice.
                                        Then, ask user them need another music score or play the beats:
                                        {user_input}"""}
            )
        print("Bot:", rhythm_result)
        notes = rhythm_result
    result = parse_rhythm_result(notes)
    return result

bot_chat()
