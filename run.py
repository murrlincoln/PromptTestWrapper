from openai import OpenAI

client = OpenAI()
import json


# Function to process each line with OpenAI
def process_with_openai(task_id, prompt):
    modified_prompt = f"{task_id, prompt}\n# Based on the above programming task, generate practical test cases that would help in verifying the correctness of a solution. Format your response where the value includes the original prompt, entirely unchanged but not including the task id, followed by the generated test cases. Ensure the response is concise and directly usable in a JSON object and will not cause parsing or decoding errors."
    print(modified_prompt)
    response = client.chat.completions.create(model="gpt-4",  # or the model of your choice
    messages=[{
          "role": "user",
          "content": modified_prompt
        }])
    # Extracting only the JSON-like part of the response that is in the "prompt" part of the JSON object
    #try:
    #    response_json = json.loads(response.choices[0].text.strip())
    #    return response_json.get('prompt', None)  # Return None if 'prompt' key is not found
    #except json.JSONDecodeError:
        # Return the text part of the return if no valid JSON is found
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()


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
process_jsonl('sourceTest.jsonl', 'destinationTest.jsonl')
