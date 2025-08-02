import asyncio
from g4f.client import AsyncClient
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Глобальные переменные
root = None
image_window = None
label = None
photo = None


def show_image(url):
    global photo, image_window, label
    try:
        # Создаем окно только при генерации изображения
        image_window = Toplevel(root)
        image_window.title('Сгенерированные изображения')
        label = Label(image_window)
        label.pack(pady=10)

        response = requests.get(url, stream=True)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img.thumbnail((500, 500))

        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo
    except Exception as e:
        mb.showerror('Ошибка!', f'Возникла ошибка {e}')
        if image_window:
            image_window.destroy()


async def generate_image(prompt, **kwargs):
    """Генерирует изображение по промпту и возвращает URL"""
    try:
        client = AsyncClient()
        # Получаем негативный промпт из kwargs, если он есть
        negative_prompt = kwargs.get('negative_prompt', None)
        response = await client.images.generate(
            prompt=prompt,
            negative_prompt=negative_prompt, # Негативный промпт
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

    image_url = await generate_image(prompt,
                                     negative_prompt=negative_prompt
                                     )
    if image_url:
        show_image(image_url)
    else:
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

button_st = Button(root, text='Сгенерировать изображение', command=start_async_main)
button_st.pack()

root.mainloop()
