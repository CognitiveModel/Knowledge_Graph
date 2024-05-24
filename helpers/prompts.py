import sys
import os
from dotenv import load_dotenv
from groq import Groq

from yachalk import chalk
sys.path.append("..")

import json
# import ollama.client as client

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
# api_key = "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"
client = Groq(
    api_key=api_key,
)

def extractConcepts(prompt: str, metadata={}, model="mistral-openorca:latest"):
    SYS_PROMPT = (
        "Your task is extract the key concepts (and non personal entities) mentioned in the given context. "
        "Extract only the most important and atomistic concepts, if  needed break the concepts down to the simpler concepts."
        "Categorize the concepts in one of the following categories: "
        "[event, concept, place, object, document, organisation, condition, misc]\n"
        "Format your output as a list of json with the following format:\n"
        "[\n"
        "   {\n"
        '       "entity": The Concept,\n'
        '       "importance": The concontextual importance of the concept on a scale of 1 to 5 (5 being the highest),\n'
        '       "category": The Type of Concept,\n'
        "   }, \n"
        "{ }, \n"
        "]\n"
    )
    chat_completion = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
           
            {
                "role": "system",
                "content": SYS_PROMPT
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": prompt,
            }
        ],

        # The language model which will generate the completion.
        model=model,

        
    )
    # response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=prompt)
    response = chat_completion.choices[0].message.content
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result


def graphPrompt(input: str, metadata={}, model="mistral-openorca:latest"):
    if model == None:
        model = "mistral-openorca:latest"

    # model_info = client.show(model_name=model)
    # print( chalk.blue(model_info))

    SYS_PROMPT = (
        # "You are a network graph maker who extracts terms and their relations from a given context. "
        # "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
        # "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
        # "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
        #     "\tTerms may include object, entity, location, organization, person, \n"
        #     "\tcondition, acronym, documents, service, concept, etc.\n"
        #     "\tTerms should be as atomistic as possible\n\n"
        # "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
        #     "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
        #     "\tTerms can be related to many other terms\n\n"
        # "Thought 3: Find out the relation between each such related pair of terms. \n\n"
        # "Format your output as a list of json. Each element of the list contains a pair of terms"
        # "and the relation between them, like the follwing: \n"
        # "[\n"
        # "   {\n"
        # '       "node_1": "A concept from extracted ontology",\n'
        # '       "node_2": "A related concept from extracted ontology",\n'
        # '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"\n'
        # "   }, {...}\n"
        # "]"
        '''You are a skilled Formatter specializing in extracting information from text and organizing it into a structured format. 
        Your task is to create a JSON representation of a knowledge graph based on a given input text chunk. 
        This involves identifying different entities mentioned in the text and representing them as nodes, as well as capturing the relationships between these entities as edges in the graph.
        Use the following template to guide your extraction process and creation of the knowledge graph in JSON format:
        [
            {
                "node_1": "A concept from extracted ontology",
                "node_2": "A related concept from extracted ontology",
                "edge": "relationship between the two concepts, node_1 and node_2 in short"
            }, {...}
        ]

        Your objective is to extract meaningful entities and relationships from the text chunk and create a coherent and informative JSON representation of the knowledge graph.
       '''
    )

    USER_PROMPT = f"context: ```{input}``` \n\n output: "
    # response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=USER_PROMPT)
    chat_completion = client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
           
            {
                "role": "system",
                "content": SYS_PROMPT
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": USER_PROMPT,
            }
        ],

        # The language model which will generate the completion.
        model=model,
        temperature=0.0,

        
    )
    # response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=prompt)
    response = chat_completion.choices[0].message.content
    result = json.loads(response)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result
    # return response
