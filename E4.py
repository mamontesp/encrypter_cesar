import tkinter as tk
from tkinter import ttk

# -----------------------------------------
# 1. Diccionario de transliteración Latin → Cirílico
# -----------------------------------------
ENCRYPT_MAP = {
    'ya': 'Ä',
    'yu': 'Ӱ',
    'ch': 'Ч',
    'll': 'Ль',
    'rr': 'Рь',
    'sh': 'Ш',
    'a': 'А',
    'b': 'Б',
    'c': 'К',
    'd': 'Д',
    'e': 'Е',
    'f': 'Ф',
    'g': 'Г',
    'h': 'ɥ',
    'i': 'И',
    'j': 'Х',
    'k': 'ʞ',
    'l': 'Л',
    'm': 'М',
    'n': 'Н',
    'ñ': 'Нь',
    'o': 'О',
    'p': 'П',
    'q': 'ǰ',
    'r': 'Р',
    's': 'С',
    't': 'Т',
    'u': 'У',
    'v': 'В',
    'w': 'Ў',
    'x': 'Խ',
    'y': 'Й',
    'z': 'З',
}
DECRYPT_MAP = {v: k for k, v in ENCRYPT_MAP.items()}

def sort_keys_by_length(mapping):
    return sorted(mapping.keys(), key=len, reverse=True)

ENCRYPT_KEYS = sort_keys_by_length(ENCRYPT_MAP)
DECRYPT_KEYS = sort_keys_by_length(DECRYPT_MAP)

def transliterate(text: str) -> str:
    text = text.lower()
    i, result = 0, []
    while i < len(text):
        for key in ENCRYPT_KEYS:
            if text.startswith(key, i):
                result.append(ENCRYPT_MAP[key])
                i += len(key)
                break
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)

def detransliterate(text: str) -> str:
    i, result = 0, []
    while i < len(text):
        for key in DECRYPT_KEYS:
            if text.startswith(key, i):
                result.append(DECRYPT_MAP[key])
                i += len(key)
                break
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)

# --------------------------
# Cifrado César
# --------------------------
ALPHABET = list("abcdefghijklmnñopqrstuvwxyz")
ALPHA_LEN = len(ALPHABET)

def caesar_shift(text: str, shift: int) -> str:
    text = text.lower()
    out = []
    for ch in text:
        if ch in ALPHABET:
            idx = (ALPHABET.index(ch) + shift) % ALPHA_LEN
            out.append(ALPHABET[idx])
        else:
            out.append(ch)
    return ''.join(out)

def caesar_unshift(text: str, shift: int) -> str:
    return caesar_shift(text, -shift)

# --------------------------
# GUI
# --------------------------
root = tk.Tk()
root.title("Cifrado y Descifrado César + Transliteration")

notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10)

frame_encrypt = ttk.Frame(notebook)
frame_decrypt = ttk.Frame(notebook)

notebook.add(frame_encrypt, text='Encriptar')
notebook.add(frame_decrypt, text='Desencriptar')

# --- Encriptar Tab ---
tk.Label(frame_encrypt, text="Encriptado César (0–26):")\
    .grid(row=0, column=0, sticky="w")
spin_shift_enc = tk.Spinbox(frame_encrypt, from_=0, to=26, width=5)
spin_shift_enc.grid(row=0, column=1, sticky="w")

tk.Label(frame_encrypt, text="Texto a encriptar:")\
    .grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
txt_input_enc = tk.Text(frame_encrypt, height=6, width=60)
txt_input_enc.grid(row=2, column=0, columnspan=2, padx=5)

tk.Label(frame_encrypt, text="Resultado:")\
    .grid(row=3, column=0, columnspan=2, sticky="w")
txt_output_enc = tk.Text(frame_encrypt, height=6, width=60)
txt_output_enc.grid(row=4, column=0, columnspan=2, padx=5)

def on_encrypt():
    shift = int(spin_shift_enc.get())
    plain = txt_input_enc.get("1.0", tk.END).strip()
    shifted = caesar_shift(plain, shift)
    cipher = transliterate(shifted)
    txt_output_enc.delete("1.0", tk.END)
    txt_output_enc.insert(tk.END, cipher)

tk.Button(frame_encrypt, text="Encriptar", command=on_encrypt)\
    .grid(row=5, column=0, columnspan=2, pady=10)

# --- Desencriptar Tab ---
tk.Label(frame_decrypt, text="Shift César (0–26):")\
    .grid(row=0, column=0, sticky="w")
spin_shift_dec = tk.Spinbox(frame_decrypt, from_=0, to=26, width=5)
spin_shift_dec.grid(row=0, column=1, sticky="w")

tk.Label(frame_decrypt, text="Texto a desencriptar:")\
    .grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
txt_input_dec = tk.Text(frame_decrypt, height=6, width=60)
txt_input_dec.grid(row=2, column=0, columnspan=2, padx=5)

tk.Label(frame_decrypt, text="Resultado:")\
    .grid(row=3, column=0, columnspan=2, sticky="w")
txt_output_dec = tk.Text(frame_decrypt, height=6, width=60)
txt_output_dec.grid(row=4, column=0, columnspan=2, padx=5)

def on_decrypt():
    shift = int(spin_shift_dec.get())
    cipher = txt_input_dec.get("1.0", tk.END).strip()
    detrans = detransliterate(cipher)
    original = caesar_unshift(detrans, shift)
    txt_output_dec.delete("1.0", tk.END)
    txt_output_dec.insert(tk.END, original)

tk.Button(frame_decrypt, text="Desencriptar", command=on_decrypt)\
    .grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()