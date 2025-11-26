Here's a standalone Python script that performs the tasks you specified. This script uses the `httpx` library to make HTTP requests and interacts with a web page and an API. Before running the script, ensure you have the `httpx` and `httpx` libraries installed. You can install them using pip if you haven't done so:

```bash
pip install httpx
```

Now, here’s the script:

```python
import httpx
import re

# Define the URLs and headers
quiz_page_url = "https://tds-llm-analysis.s-anand.net/demo"
api_url = "https://aipipe.org/openrouter/v1/chat/completions"
api_token = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjEwMDIyOTlAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.TvaYmYK75PCqqQ9NeIIyOvDfUIQMwPuuUuw5Vh6-sCI"
model = "gpt-4o-mini"

def get_quiz_question():
    response = httpx.get(quiz_page_url)
    if response.status_code == 200:
        # Use regex to extract the quiz question from the response text
        match = re.search(r'<div class="quiz-question">(.+?)</div>', response.text, re.DOTALL)
        if match:
            return match.group(1).strip()
    return None

def generate_answer(question):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    
    response = httpx.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    return None

def submit_answer(answer):
    # Locate the submission endpoint (assuming it's also available on the quiz page)
    submission_endpoint = quiz_page_url + "/submit"  # Placeholder for actual endpoint
    payload = {
        "answer": answer
    }
    
    response = httpx.post(submission_endpoint, json=payload)
    return response.status_code == 200

def main():
    question = get_quiz_question()
    if question:
        print(f"Quiz Question: {question}")
        answer = generate_answer(question)
        if answer:
            print(f"Generated Answer: {answer}")
            if submit_answer(answer):
                print("Answer submitted successfully.")
            else:
                print("Failed to submit the answer.")
        else:
            print("Failed to generate an answer.")
    else:
        print("Could not retrieve quiz question.")

if __name__ == "__main__":
    main()
```

### Notes:
1. The script starts by requesting the quiz page to extract the quiz question using a regex pattern. This pattern may need to be adjusted depending on the actual HTML structure of the page.
2. It then calls the AIPIPE API with the extracted question to generate an answer.
3. Finally, the generated answer is submitted back to the server, assuming a submission endpoint can be guessed (please adjust as necessary).
4. Ensure that you have the necessary permissions and credentials to access the API and the quiz submission endpoint.

Before executing, make sure the endpoint for answer submission is correct, as the script assumes a placeholder that appends `/submit` to the page URL. Adjust it according to the actual URL structure from the quiz page.