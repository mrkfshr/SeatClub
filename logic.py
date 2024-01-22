import json
import aiohttp
import asyncio
import requests

def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def personalize_questions(artist_name, questions):
    personalized_questions = []
    for question_dict in questions:
        question_text = question_dict["question"]  # Extract the question text from the dictionary
        personalized_question = question_text.replace("[name]", artist_name)
        personalized_questions.append(personalized_question)
    return personalized_questions


async def ask_gpt(question, api_key):
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                "https://api.openai.com/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"prompt": question, "max_tokens": 60}
            )
            response_json = await response.json()
            print(f"Response: {response_json}")  # Log the response
            return response_json.get('choices', [{}])[0].get('text', '').strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error in processing the question."


async def main():
    # Paths to the local JSON files
    artists_file_path = "/Users/mrk/Desktop/seatclub/artists.json"  # Update with the actual file path
    questions_file_path = "/Users/mrk/Desktop/seatclub/artistquestions.json"  # Update with the actual file path

    # Loading data from local files
    artists = load_json_from_file(artists_file_path)['performers']
    questions_template = load_json_from_file(questions_file_path)["artist questions"]

    api_key = "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"  # Replace with your API key

    for artist in artists:
        artist_name = artist.get("name")
        personalized_questions = personalize_questions(artist_name, questions_template)
        
        # Gather all questions and send them at once
        tasks = [ask_gpt(question, api_key) for question in personalized_questions]
        answers = await asyncio.gather(*tasks)

        for question, answer in zip(personalized_questions, answers):
            print(f"Q: {question}\nA: {answer}\n")


if __name__ == "__main__":
    asyncio.run(main())
