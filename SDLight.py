import asyncio
from g4f.client import AsyncClient
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import filedialog

# Глобальные переменные
root = None
image_window = None
label = None
photo = None
progress = None


def update_progress(value, message=""):
    """Обновляет прогресс-бар и текст статуса"""
    progress['value'] = value
    progress_label.config(text=message)
    root.update_idletasks()


def save_image(img):
    """Сохранение изображений на диск"""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("PNG файлы", "*.png"), ("JPEG файлы", "*.jpg"), ("Все файлы", "*.*")],
        title="Сохраить изображение"
    )
    if file_path:
        try:
            img.save(file_path)
            mb.showinfo("Успешно", "Изображение сохранено!")
        except Exception as e:
            mb.showerror("Ошибка!", f"Не удалось сохранить: {e}")


def show_image(url):
    global photo, image_window, label, original_image

    # Создаем окно изображения
    if image_window is None or not image_window.winfo_exists():
        update_progress(80, "Загрузка изображения...")
        image_window = Toplevel(root)
        image_window.title('Сгенерированные изображения')
        image_window.geometry('600x600')

        # Основной контейнер
        frame = Frame(image_window)
        frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Label для изображения
        label = Label(frame)
        label.pack(fill=BOTH, expand=True)

        # Кнопки закрытия и сохранения
        btn_frame = Frame(frame)
        btn_frame.pack(fill=X, pady=5)
        Button(btn_frame, text="Сохранить", command=lambda: save_image(original_image)).pack(side=LEFT)
        Button(btn_frame, text="Закрыть", command=image_window.destroy).pack(side=RIGHT)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img.thumbnail((500, 500))

        # Отображаем
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo

        original_image = img.copy()

        # Центрируем окно
        image_window.update_idletasks()
        width = image_window.winfo_width()
        height = image_window.winfo_height()
        x = (image_window.winfo_screenwidth() // 2) - (width // 2)
        y = (image_window.winfo_screenheight() // 2) - (height // 2)
        image_window.geometry(f'+{x}+{y}')

        update_progress(100, "Готово!")
        # Задержка перед скрытием прогресс-бара
        root.after(1000, lambda: update_progress(0, ""))

    except Exception as e:
        update_progress(0, "")
        mb.showerror('Ошибка!', f'Возникла ошибка {e}')
        if image_window:
            image_window.destroy()


async def generate_image(prompt, **kwargs):
    """Генерирует изображение по промпту и возвращает URL"""
    try:
        update_progress(20, "Подготовка к генерации...")
        await asyncio.sleep(0.1)  # Имитация работы

        client = AsyncClient()
        update_progress(40, "Подключение к серверу...")
        await asyncio.sleep(0.1)

        # Получаем негативный промпт из kwargs, если он есть
        negative_prompt = kwargs.get('negative_prompt', None)
        update_progress(60, "Генерация изображения...")

        response = await client.images.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,  # Негативный промпт
            model="prodia",  # Используем Prodia (Stable Diffusion)
            response_format="url",
            steps=30,  # Количество шагов генерации
            cfg_scale=9,  # Сила соответствия промпту (7-10)
            sampler="DPM++ 2M Karras"  # Опционально: метод сэмплирования
        )
        return response.data[0].url if response.data else None
    except Exception as e:
        print(f'Ошибка: {e}')
        return None


async def main():
    """Асинхронная часть: получает промпт, генерирует изображение и возвращает URL"""
    # Получаем позитивный промпт из первого поля
    prompt = pos_prompt.get('1.0', END).strip()
    if not prompt:
        mb.showerror('Ошибка!, Введите описание изображения!')
        return None

    # Получаем негативный промпт из второго поля
    negative_prompt = neg_prompt.get('1.0', END).strip()

    update_progress(10, "Начало генерации...")
    image_url = await generate_image(prompt,
                                     negative_prompt=negative_prompt
                                     )
    if image_url:
        show_image(image_url)
    else:
        update_progress(0, "")
        mb.showerror("Ошибка!", "Не удалось сгенерировать изображение")


def start_async_main():
    """Запускает async_main() в asyncio"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()


root = Tk()
root.title('Stable Diffusion Light')
root.geometry('500x500')

# Позитивный промпт
frame_pos = LabelFrame(root, text='Введите описание изображения', padx=10, pady=10)
frame_pos.pack(pady=10, padx=10)

scrollbar_p = Scrollbar(frame_pos)
scrollbar_p.pack(side=RIGHT, fill=Y)

pos_prompt = Text(frame_pos, width=50, height=5, wrap='word', yscrollcommand=scrollbar_p.set)
pos_prompt.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar_p.config(command=pos_prompt.yview)

# Негативный промпт
frame_neg = LabelFrame(root, text='Что не хотите видеть на изображении', padx=10, pady=10)
frame_neg.pack(pady=10, padx=10)

scrollbar_n = Scrollbar(frame_neg)
scrollbar_n.pack(side=RIGHT, fill=Y)

neg_prompt = Text(frame_neg, width=50, height=3, wrap='word', yscrollcommand=scrollbar_n.set)
neg_prompt.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar_n.config(command=neg_prompt.yview)

# Прогресс-бар
progress_frame = Frame(root)
progress_frame.pack(pady=5, fill=X, padx=10)

progress_label = Label(progress_frame, text="", height=1)
progress_label.pack()

progress = ttk.Progressbar(progress_frame, orient=HORIZONTAL, length=100, mode='determinate')
progress.pack(fill=X)

button_st = Button(root, text='Сгенерировать изображение', command=start_async_main)
button_st.pack()

root.mainloop()
