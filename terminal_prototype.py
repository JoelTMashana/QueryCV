import requests

def send_query_to_api(user_query):
    url = "http://127.0.0.1:8000/users/1/experiences"
    params = {"user_query": user_query}

    response = requests.get(url, params=params)
    return response.json()

def main():
    while True:
        print("\nEnter your query (or type 'exit' to quit):")
        user_query = input()

        if user_query.lower() == 'exit':
            break

     

        result = send_query_to_api(user_query)
        print("\nGPT Response:\n", result.get("gpt_response", "No response"))

if __name__ == "__main__":
    main()
