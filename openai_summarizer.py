import csv
import json
import openai
import os

# load the API_KEY from the .env file
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def create_contact_details_json(filename):
    # define a json list
    contact_details = []

    # read a csv and join snippets in the "results" column
    result_snippets_text = ""
    with open(filename, "r") as file:
        # Create a CSV reader
        reader = csv.reader(file)
        # Skip the header
        next(reader)
        # Result structure is: {query, title, snippet, link, position, date}
        # Concatenate the snippet column to a string using newline as the joiner
        # take the top 3 rows
        result_snippets_text = ".\n".join([row[2] for row in reader])

        # extract_contact_details
        contact_details = extract_contact_details(result_snippets_text)

        # dump to a formatted json file
        with open('contact_details.json', 'w') as outfile:
            json.dump(contact_details, outfile, indent=4)


def extract_contact_details(text):
    # define the prompts
    PROMPT_HEAD = "A JSON summarizing contact details:\n\n"
    PROMPT_TAIL = "\n\nJSON Array:"

    # use an LLM to extract contact details
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=PROMPT_HEAD + text + PROMPT_TAIL,
        temperature=0.7,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # convert from string to json
    contact_details = json.loads(response.choices[0].text)
    return contact_details

# test the function
create_contact_details_json('test.csv')