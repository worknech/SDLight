from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import requests
from PIL import Image, ImageTk
from io import BytesIO

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

root.mainloop()
