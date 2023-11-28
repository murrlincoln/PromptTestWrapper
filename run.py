import openai
import json


# Function to process each line with OpenAI
def process_with_openai(task_id, prompt):
    modified_prompt = f"{prompt}\n# Please append example test cases to this prompt that will aid in its ability to be used by an LLM to create functional code. Return the entire JSON as your response."
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # or the model of your choice
        prompt=modified_prompt,
        max_tokens=1000  # Adjust as per your requirement
    )
    # Extracting only the text part of the response
    text_response = response.choices[0].text.strip()
    # Extracting only the JSON-like part of the response
    start_idx = text_response.find('{')
    end_idx = text_response.rfind('}')
    if start_idx != -1 and end_idx != -1:
        json_like_part = text_response[start_idx:end_idx+1]
        try:
            # Try to parse it as JSON to ensure it's valid
            parsed_json = json.loads(json_like_part)
            return json.dumps(parsed_json)  # Convert back to string
        except json.JSONDecodeError:
            # In case the extracted part is not valid JSON
            return None
    else:
        return None

# Read from source JSONL and write to destination JSONL
def process_jsonl(source_file, destination_file):
    with open(source_file, 'r') as src, open(destination_file, 'w') as dest:
        for line in src:
            data = json.loads(line)
            processed_data = process_with_openai(data['task_id'], data['prompt'])
            # Writing only the necessary JSON data to the destination file
            json.dump({"task_id": data['task_id'], "modified_prompt": processed_data}, dest)
            dest.write('\n')

# Replace 'source.jsonl' and 'destination.jsonl' with your filenames
process_jsonl('source.jsonl', 'destination-3.5.jsonl')
