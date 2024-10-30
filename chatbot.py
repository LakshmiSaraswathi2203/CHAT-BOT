import csv
from difflib import get_close_matches

# Load knowledge base from CSV
def load_knowledge_base(file_path: str) -> dict:
    knowledge_base = {"questions": []}
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            knowledge_base["questions"].append({"questions": row["questions"], "answer": row["answer"]})
    return knowledge_base

# Save knowledge base to CSV
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["questions", "answer"])
        writer.writeheader()
        for item in data["questions"]:
            writer.writerow(item)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["questions"] == question:
            return q["answer"]

def load_additional_data(file_path: str, knowledge_base: dict):
    """Load additional data from a CSV file into the knowledge base."""
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            knowledge_base["questions"].append({"questions": row["questions"], "answer": row["answer"]})

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.csv')

    # Load additional data if needed
    # load_additional_data('additional_data.csv', knowledge_base)
    print("Welcome to the HLM Personalized Chatbot!😍😍")
    print("I'm here to help you with Machine Learning topics... 😊😊😁")
    while True:
        user_input: str = input('You: ')

        # Check for exit commands
        if user_input.lower() in ['exit', 'bye', 'see you']:
            print('Bot: Goodbye! Have a great day!😍😍')
            break

        best_match: str | None = find_best_match(user_input, [q["questions"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?😁😜')
            new_answer: str = input('Type the answer or "skip" to skip: 👍')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"questions": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.csv', knowledge_base)
                print('Bot: Thank you! I learned a new response.😁😃')

if __name__ == '__main__':
    chat_bot()
