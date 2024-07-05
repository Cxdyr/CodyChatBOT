import json

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def print_data(data):
    for item in data:
        print(f"Q: {item['question']}")
        print(f"A: {item['answer']}")
        if 'follow_up_responses' in item:
            print("Follow-up responses:")
            for response_key, response_value in item['follow_up_responses'].items():
                print(f"  {response_key.capitalize()}: {response_value}")

def main():
    data = load_data('data.json')
    print_data(data)

if __name__ == "__main__":
    main()
