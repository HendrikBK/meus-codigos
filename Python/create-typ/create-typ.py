import subprocess
import os
import tkinter as tk
from tkinter import simpledialog

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'Python/create-typ')
    os.chdir(path)
    user_input = simpledialog.askstring("Input", "Informe o número")
    subprocess.run(["typst", "compile", "--input",  "number=5", "texto.typ"])
    files = os.listdir(path)