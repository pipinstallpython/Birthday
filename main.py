import tkinter as tk
import random
from PIL import ImageTk, Image
from playsound import playsound
import threading
import requests
from io import BytesIO

# Создаем список пожеланий
wishes = ["С днем рождения!", "Счастья, здоровья и успехов!", "Пусть все мечты сбываются!",
          "Пусть жизнь будет насыщенной и яркой!", "Желаем Вам радости и улыбок каждый день!",
          "Пусть все задачи решаются легко и быстро!", "Счастья и любви в личной жизни!",
          "Пусть Вы всегда оставаться на пике своего мастерства!", "Пусть карьера и успех Вас не покидают!"]


# Создаем функцию для вывода случайного пожелания и проигрывания звукового эффекта
def display_wish():
    # Выбираем случайное пожелание из списка
    random_wish = random.choice(wishes)
    # Выводим пожелание в окно
    wish_label.config(text=random_wish)

    # Если звук еще не играет, проигрываем звуковой эффект
    if not thread_event.is_set():
        thread_event.set()
        threading.Thread(target=play_sound).start()


def play_sound():
    # Проигрываем звуковой эффект
    playsound('happy_birthday.mp3')
    # Устанавливаем флаг в False, чтобы можно было проиграть звук снова
    thread_event.clear()


# Создаем главное окно приложения
root = tk.Tk()
root.title("Поздравление с днем рождения!")
root.geometry("650x500")

# Создаем метку с заголовком
title_label = tk.Label(root, text="Сегодня день рождения лучшего преподавателя!", font=("Arial", 14))
title_label.pack(pady=10)

# Создаем метку для пожелания
wish_label = tk.Label(root, text="", font=("Arial", 12))
wish_label.pack(pady=20)

# Создаем кнопку для генерации случайного пожелания
wish_button = tk.Button(root, text="Сгенерировать пожелание", font=("Arial", 12), command=display_wish)
wish_button.pack()

# Создаем анимацию смайлика
canvas = tk.Canvas(root, width=300, height=350)
canvas.pack(pady=20)
# Загружаем анимированную гифку
response = requests.get("https://i.gifer.com/4SHX.gif")
smile_gif = Image.open(BytesIO(response.content))
# Создаем список кадров гифки
frames = []
try:
    while True:
        frames.append(ImageTk.PhotoImage(smile_gif.copy()))
        smile_gif.seek(len(frames))  # Переходим к следующему кадру
except EOFError:
    pass


# Создаем функцию для анимации смайлика
def animate_smile(counter=0):
    smile_item = canvas.create_image(150, 150, image=frames[0])
    canvas.itemconfig(smile_item, image=frames[counter])
    root.after(50, animate_smile, (counter + 1) % len(frames))


# Запускаем анимацию смайлика
animate_smile()

# Инициализируем объект Event для управления звуковым эффектом
thread_event = threading.Event()

# Запускаем главный
root.mainloop()
