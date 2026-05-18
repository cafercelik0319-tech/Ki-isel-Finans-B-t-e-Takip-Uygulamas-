import sys
import os
import tkinter as tk

# Yolu en başta bir kere ekliyoruz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.main_window import AnaEkran

def main():
    root = tk.Tk()
    app = AnaEkran(root)
    root.mainloop()

if __name__ == "__main__":
    main()
