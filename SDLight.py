import asyncio
from g4f.client import AsyncClient
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import requests
from PIL import Image, ImageTk
from io import BytesIO


async def main():
    """Асинхронная часть: получает промпт, генерирует изображение и возвращает URL"""
    prompt = pos_prompt.get('1.0', END)
    if not prompt:
        mb.showerror('Ошибка!, Введите описание изображения!')
        return None

    image_url = await generate_image(prompt)
    if image_url:
        print(image_url)
        return image_url
    else:
        mb.showerror("Ошибка!", "Не удалось сгенерировать изображение")
        return None


async def generate_image(prompt, **kwargs):
    """Генерирует изображение по промпту и возвращает URL"""
    try:
        client = AsyncClient()
        response = await client.images.generate(
            prompt=prompt,
            model="flux",
            response_format="url"
        )
        return response.data[0].url if response.data else None
    except Exception as e:
        print(f'Ошибка: {e}')
        return None


def start_async_main():
    """Запускает async_main() в asyncio"""
    asyncio.run(main())


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

top_level_window = Toplevel(root)
top_level_window.title('Сгенерированные изображения')
label = Label(top_level_window, text='Изображения')
label.pack(pady=10)

root.mainloop()
