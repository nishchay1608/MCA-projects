import tkinter as tk
import math

class ScientificCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Scientific Calculator")

        self.expression = ""
        self.input_field = tk.Entry(master, width=30, borderwidth=5)
        self.input_field.grid(row=0, column=0, columnspan=5)

        # Create buttons
        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('C', 5, 3)
        ]

        for (text, row, col) in buttons:
            self.create_button(text, row, col)

    def create_button(self, text, row, col):
        button = tk.Button(self.master, text=text, padx=20, pady=20, command=lambda: self.on_button_click(text))
        button.grid(row=row, column=col)

    def on_button_click(self, char):
        if char == '=':
            try:
                result = str(eval(self.expression))
                self.input_field.delete(0, tk.END)
                self.input_field.insert(0, result)
                self.expression = result
            except Exception as e:
                self.input_field.delete(0, tk.END)
                self.input_field.insert(0, "Error")
                self.expression = ""
        elif char == 'C':
            self.input_field.delete(0, tk.END)
            self.expression = ""
        elif char in ['sin', 'cos', 'tan']:
            self.expression += f"math.{char}(math.radians("
            self.input_field.insert(tk.END, f"{char}(")
        else:
            self.expression += str(char)
            self.input_field.insert(tk.END, str(char))

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()