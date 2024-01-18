import requests
import json

def fetch_json_from_github(url):
    response = requests.get(url)
    return response.json()

def personalize_questions(artist_name, questions):
    personalized_questions = []
    for question in questions:
        personalized_questions.append(question.replace("[name]", artist_name))
    return personalized_questions

def ask_gpt(question, api_key):
    response = requests.post(
        "https://api.openai.com/v1/engines/davinci-codex/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"prompt": question, "max_tokens": 60}
    )
    return response.json().get('choices', [{}])[0].get('text', '').strip()

def main():
    # URLs to the JSON files in the GitHub repository
    artists_url = "https://github.com/mrkfshr/SeatClub/blob/main/artists.json"
    questions_url = "https://github.com/mrkfshr/SeatClub/blob/main/artistquestions.json"

    # Fetching data from GitHub
    artists = fetch_json_from_github(artists_url)
    questions_template = fetch_json_from_github(questions_url)["artist questions"]

    api_key = "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"

    for artist in artists:
        artist_name = artist.get("name")
        personalized_questions = personalize_questions(artist_name, questions_template)
        
        for question in personalized_questions:
            answer = ask_gpt(question["question"], api_key)
            print(f"Q: {question['question']}\nA: {answer}\n")

if __name__ == "__main__":
    main()
