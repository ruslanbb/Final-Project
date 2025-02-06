import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import TOKEN


bot = telebot.TeleBot(TOKEN)


questions = [
    {
        "question": "Вопрос 1: Я — железный человек.",
        "options": ["Человек-паук: Возвращение домой", "Мстители: Финал", "Тёмный рыцарь", "Доктор Стрэндж"],  
        "correct": 1
    },
    {
        "question": "Вопрос 2: Я — твой отец.",
        "options": ["Терминатор 2: Судный день", "Звёздные войны: Империя наносит ответный удар", "Хоббит: Нежданное путешествие", "Гарри Поттер и Кубок огня"],
        "correct": 1
    },
    {
        "question": "Вопрос 3: Почему бы и нет? Почему бы и да?",
        "options": ["Властелин колец: Две крепости", "Гарри Поттер и Принц-полукровка", "Достать ножи", "Джокер"],
        "correct": 1
    },
    {
        "question": "Вопрос 4: До бесконечности и дальше!",
        "options": ["История игрушек", "Король Лев", "Гадкий Я", "Тайная жизнь домашних животных"],
        "correct": 0
    },
    {
        "question": "Вопрос 5: Сила пребудет с тобой, всегда.",
        "options": ["Стражи Галактики", "Матрица", "Звёздные войны: Новая надежда", "Бегущий по лезвию"],
        "correct": 2
    },
    {
        "question": "Вопрос 6: Они могут отнять у нас жизнь, но никогда не отнимут нашу свободу!",
        "options": ["Гладиатор", "Храброе сердце", "Троя", "300 спартанцев"],
        "correct": 1
    },
    {
        "question": "Вопрос 7: Ты не пройдёшь!",
        "options": ["Гарри Поттер и Дары смерти", "Властелин колец: Братство кольца", "Человек из стали", "Перси Джексон и похититель молний"],
        "correct": 1
    },
    {
        "question": "Вопрос 8: Леген... подожди... дарно! Легендарно!",
        "options": ["Очень страшное кино", "Теория большого взрыва", "Как я встретил вашу маму", "Дэдпул"],
        "correct": 2
    },
    {
        "question": "Вопрос 9: С великой силой приходит великая ответственность.",
        "options": ["Человек-паук (2002)", "Железный человек", "Мстители", "Люди Икс"],
        "correct": 0
    },
    {
        "question": "Вопрос 10 Я гуляю тут!",
        "options": ["Один дома 2", "Форрест Гамп", "Охотники за привидениями", "Волк с Уолл-стрит"],
        "correct": 0
    }
]


user_data = {}

@bot.message_handler(commands=["start"])
def start_quiz(message):
    
    user_data[message.chat.id] = {"current_question": 0, "score": 0}

    # Отправляем приветственное сообщение
    bot.send_message(message.chat.id, "Привет! Добро пожаловать в квиз-бота. Я задам тебе несколько вопросов с цитатами из фильмов, и ты должен выбрать правильный ответ. Помни за каждый неправильный ответ будет отниматься 1 балл. Удачи! 🎉")

    # Отправляем первый вопрос
    send_question(message.chat.id)

def send_question(chat_id):
    """ Функция отправки вопроса пользователю """
    
    user = user_data.get(chat_id)  # Получаем данные пользователя
    if user is None:
        return
    
    question_index = user["current_question"]  # Номер текущего вопроса

    if question_index < len(questions):  # Если ещё есть вопросы
        question = questions[question_index]  # Берём текущий вопрос
        markup = InlineKeyboardMarkup()  # Создаём клавиатуру

        # Создаём кнопки с вариантами ответа
        for i, option in enumerate(question["options"]):
            markup.add(InlineKeyboardButton(text=option, callback_data=f"answer_{i}"))

        # Отправляем вопрос с кнопками
        bot.send_message(chat_id, question["question"], reply_markup=markup)
    else:
        # Если вопросы закончились, показываем итог
        bot.send_message(chat_id, f"Квиз завершён! Ваш результат: {user['score']} из {len(questions)}")

# Обработчик нажатий на кнопки с ответами
@bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
def process_answer(call):
    """ Функция обработки ответа пользователя """

    chat_id = call.message.chat.id  # Получаем ID чата (пользователя)
    user = user_data.get(chat_id)  # Получаем данные пользователя

    if user is None:
        return

    question_index = user["current_question"]  # Номер текущего вопроса
    question = questions[question_index]  # Текущий вопрос
    selected_answer = int(call.data.split("_")[1])  # Узнаём, какой вариант выбрал пользователь

    # Проверяем правильность ответа
    if selected_answer == question["correct"]:
        user["score"] += 1  # Увеличиваем счёт
        bot.answer_callback_query(call.id, "Правильно! 🎉")  # Уведомляем пользователя
    else:
        bot.answer_callback_query(call.id, "Неправильно ❌")  # Уведомляем о неверном ответе
        # Вычитаем за неправильный ответ

    user["current_question"] += 1  # Переход к следующему вопросу
    send_question(chat_id)  # Отправляем следующий вопрос

# Запуск бота
bot.polling(none_stop=True)