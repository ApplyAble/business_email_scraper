import csv
import json
import openai
import os

# load the API_KEY from the .env file
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def create_contact_details_file(filename):
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
        # result_snippets_text = ".\n".join([row[2] for row in reader])

        # divide the whole text into chunks of 9 rows each
        # each chunk will be processed separately
        # this is to avoid the 5000 token limit
        for i, row in enumerate(reader):
            if i % 9 == 0:
                # process the chunk
                contact_details += json.loads(process_contact_details(result_snippets_text))
                # reset the text
                result_snippets_text = ""
            result_snippets_text += row[2] + ".\n"
                

        # remove duplicates from the list
        # contact_details = [dict(t) for t in {tuple(d.items()) for d in contact_details}]

        # dump to a formatted json file
        with open('contact_details.json', 'w') as outfile:
            json.dump(contact_details, outfile, indent=4)

def process_contact_details(text):
    # extract_contact_details
    contact_details = extract_contact_details(text)

    # filter the contact details which contain email
    contact_details = [contact for contact in contact_details]

    # convert to JSON
    contact_details = json.dumps(contact_details)
    return contact_details

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

# convert all keys to lowercase in a JSON
def convert_keys_to_lowercase(json):
    # define an empty dictionary
    new_json = {}

    # iterate through the json
    for key, value in json.items():
        # convert the key to lowercase
        key = key.lower()

        # if the value is a dictionary
        if isinstance(value, dict):
            # convert the keys to lowercase
            value = convert_keys_to_lowercase(value)

        # add the key and value to the new json
        new_json[key] = value

    return new_json

# find the value of a key in a nested JSON
def find_value_of_key(json, key):
    # iterate through the json
    for k, v in json.items():
        # if the key is found
        if k == key:
            # return the value
            return v

        # if the value is a dictionary
        if isinstance(v, dict):
            # find the value of the key in the dictionary
            item = find_value_of_key(v, key)
            if item is not None:
                return item

# convert a given json into csv
def json_to_csv(filename):
    # read the json file
    with open(filename, 'r') as f:
        contact_details = json.load(f)
        contact_details = [convert_keys_to_lowercase(contact) for contact in contact_details]

    # open a file for writing
    contact_details_data = open('contact_details.csv', 'w')

    # create the csv writer object
    csvwriter = csv.writer(contact_details_data)

    # write the header
    header = ['name', 'email']
    csvwriter.writerow(header)

    # write the data
    for contact in contact_details:
        name = find_value_of_key(contact, 'name')
        email = find_value_of_key(contact, 'email')
        csvwriter.writerow([name, email])

    # close the file
    contact_details_data.close()

# function to remove entries with duplicate emails from the csv
# also remove entries which don't match an email
def remove_duplicates(filename):
    # create a dictionary to store the email and name
    email_name_dict = {}

    # open the csv file
    with open(filename, 'r') as f:
        # create a csv reader object
        csvreader = csv.reader(f)

        # skip the header
        next(csvreader)

        # iterate through the rows
        for row in csvreader:
            # get the email and name
            email = row[1]
            name = row[0]

            # if the email is not in the dictionary
            if email not in email_name_dict:
                # add the email and name to the dictionary
                email_name_dict[email] = name

    # open a file for writing
    contact_details_data = open('contact_details.csv', 'w')

    # create the csv writer object
    csvwriter = csv.writer(contact_details_data)

    # write the header
    header = ['name', 'email']
    csvwriter.writerow(header)

    # write the data
    for email, name in email_name_dict.items():
        csvwriter.writerow([name, email])

    # close the file
    contact_details_data.close()

# test the function
# create_contact_details_file('test.csv')

json_to_csv('contact_details.json')
remove_duplicates('contact_details.csv')