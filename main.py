"""メインアプリケーション"""
import tkinter as tk
from gui import GPSTimeSyncGUI

def main():
    root = tk.Tk()
    app = GPSTimeSyncGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()