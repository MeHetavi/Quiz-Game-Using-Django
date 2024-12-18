
from quiz.models import QuizGenre, QuizQuestion, QuizOption

categories = {
    "Science": [
        {"question": "What is the chemical symbol for water?", "options": ["H2O", "CO2", "O2", "NaCl"], "correct": "H2O"},
        {"question": "What planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "correct": "Mars"},
        {"question": "What gas do plants absorb during photosynthesis?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"], "correct": "Carbon Dioxide"},
        {"question": "What is the speed of light?", "options": ["3 x 10^8 m/s", "1 x 10^6 m/s", "3 x 10^6 m/s", "1 x 10^8 m/s"], "correct": "3 x 10^8 m/s"}
    ] ,
    "History": [
        {"question": "Who discovered America?", "options": ["Christopher Columbus", "Vasco da Gama", "Magellan", "James Cook"], "correct": "Christopher Columbus"},
        {"question": "In what year did World War II end?", "options": ["1945", "1939", "1941", "1950"], "correct": "1945"},
        {"question": "Who was the first President of the United States?", "options": ["Thomas Jefferson", "Abraham Lincoln", "George Washington", "John Adams"], "correct": "George Washington"},
        {"question": "Which empire built the Great Wall of China?", "options": ["Ming", "Qin", "Tang", "Song"], "correct": "Qin"}
    ] ,
    "Geography": [
        {"question": "What is the capital of Australia?", "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "correct": "Canberra"},
        {"question": "Which is the largest ocean?", "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"], "correct": "Pacific Ocean"},
        {"question": "What is the longest river in the world?", "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "correct": "Nile"},
        {"question": "Mount Everest is located in which country?", "options": ["India", "China", "Nepal", "Bhutan"], "correct": "Nepal"}
    ] ,
    "Sports": [
        {"question": "How many players are there in a football team?", "options": ["9", "10", "11", "12"], "correct": "11"},
        {"question": "Which sport is known as the 'king of sports'?", "options": ["Tennis", "Football", "Basketball", "Cricket"], "correct": "Football"},
        {"question": "Which country hosted the 2016 Olympics?", "options": ["China", "USA", "Brazil", "Japan"], "correct": "Brazil"},
        {"question": "Who is known as the fastest man in the world?", "options": ["Usain Bolt", "Mo Farah", "Tyson Gay", "Yohan Blake"], "correct": "Usain Bolt"}
    ] 
}

for category_name, questions in categories.items():
    genre, created = QuizGenre.objects.get_or_create(name=category_name)
    for q_data in questions:
        question = QuizQuestion.objects.create(
            question_text=q_data["question"],
            difficulty="medium",
            genre=genre
        )
        for option_text in q_data["options"]:
            QuizOption.objects.create(
                question=question,
                option_text=option_text,
                is_correct=(option_text == q_data["correct"])
            )

print("Database populated successfully!")
