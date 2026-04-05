import tkinter as tk
import math
import re
from tkinter import messagebox

class ComplexCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Complex Calculator")
        self.root.resizable(False, False)

        # Calculator state
        self.current_expression = ""
        self.memory = 0
        self.angle_mode = "degrees"  # or "radians"

        # Create GUI
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2C2C2C")
        main_frame.pack(padx=10, pady=10)

        # Display frame
        display_frame = tk.Frame(main_frame, bg="#2C2C2C")
        display_frame.pack(fill="x", pady=(0, 10))

        # Expression display
        self.expression_label = tk.Label(display_frame, text="", font=("Arial", 12),
                                       bg="#2C2C2C", fg="#888888", anchor="e",
                                       height=1, wraplength=400)
        self.expression_label.pack(fill="x")

        # Result display
        self.result_label = tk.Label(display_frame, text="0", font=("Arial", 24, "bold"),
                                   bg="#2C2C2C", fg="white", anchor="e",
                                   height=1)
        self.result_label.pack(fill="x")

        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#2C2C2C")
        buttons_frame.pack()

        # Button layout
        button_layout = [
            ["MC", "MR", "M+", "M-"],
            ["MS", "±", "C", "←"],
            ["sin", "cos", "tan", "log"],
            ["ln", "√", "x²", "xʸ"],
            ["π", "e", "(", ")"],
            ["n!", "1/x", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", "00", ".", "="]
        ]

        # Colors
        self.button_colors = {
            'numbers': '#505050',
            'operators': '#FF9500',
            'functions': '#666666',
            'memory': '#333333',
            'clear': '#A6A6A6'
        }

        # Create buttons
        for row_idx, row in enumerate(button_layout):
            for col_idx, button_text in enumerate(row):
                self.create_button(buttons_frame, button_text, row_idx, col_idx)

        # Mode selection
        mode_frame = tk.Frame(main_frame, bg="#2C2C2C")
        mode_frame.pack(pady=(10, 0))

        self.angle_var = tk.StringVar(value="degrees")
        degrees_radio = tk.Radiobutton(mode_frame, text="Degrees", variable=self.angle_var,
                                     value="degrees", bg="#2C2C2C", fg="white",
                                     selectcolor="#2C2C2C", command=self.change_angle_mode)
        degrees_radio.pack(side="left", padx=(0, 10))

        radians_radio = tk.Radiobutton(mode_frame, text="Radians", variable=self.angle_var,
                                     value="radians", bg="#2C2C2C", fg="white",
                                     selectcolor="#2C2C2C", command=self.change_angle_mode)
        radians_radio.pack(side="left")

    def create_button(self, parent, text, row, col):
        # Determine button color
        if text in "0123456789.":
            bg_color = self.button_colors['numbers']
        elif text in "+-×÷=":
            bg_color = self.button_colors['operators']
        elif text in ["C", "⌫", "←"]:
            bg_color = self.button_colors['clear']
        elif text in ["MC", "MR", "M+", "M-", "MS"]:
            bg_color = self.button_colors['memory']
        else:
            bg_color = self.button_colors['functions']

        button = tk.Button(parent, text=text, font=("Arial", 12, "bold"),
                          bg=bg_color, fg="white", width=6, height=2,
                          relief="raised", borderwidth=2,
                          command=lambda: self.button_click(text))
        button.grid(row=row, column=col, padx=2, pady=2)

        # Hover effect
        button.bind("<Enter>", lambda e: button.config(bg=self.lighten_color(bg_color)))
        button.bind("<Leave>", lambda e: button.config(bg=bg_color))

        # Ensure left arrow is treated as backspace
        if text == "←":
            button.config(command=self.backspace)

    def lighten_color(self, color):
        # Simple color lightening for hover effect
        if color == '#505050':
            return '#606060'
        elif color == '#FF9500':
            return '#FFA500'
        elif color == '#666666':
            return '#777777'
        elif color == '#333333':
            return '#444444'
        elif color == '#A6A6A6':
            return '#B6B6B6'
        return color

    def button_click(self, text):
        try:
            if text == "=":
                self.calculate()
            elif text == "C":
                self.clear_all()
            elif text in ["⌫", "←"]:
                self.backspace()
            elif text == "±":
                self.negate()
            elif text in ["MC", "MR", "M+", "M-", "MS"]:
                self.memory_operation(text)
            else:
                self.add_to_expression(text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.clear_all()

    def add_to_expression(self, text):
        # Replace symbols for display
        display_text = text
        if text == "×":
            display_text = "*"
        elif text == "÷":
            display_text = "/"
        elif text == "√":
            display_text = "sqrt("
        elif text == "x²":
            display_text = "^2"
        elif text == "xʸ":
            display_text = "^"
        elif text == "π":
            display_text = "pi"
        elif text == "n!":
            display_text = "fact("
        elif text == "ln":
            display_text = "log("  # natural log
        elif text == "log":
            display_text = "log10("

        self.current_expression += display_text
        self.update_display()

    def calculate(self):
        if not self.current_expression:
            return

        try:
            # Replace display symbols with Python equivalents
            expression = self.current_expression
            expression = expression.replace("pi", str(math.pi))
            expression = expression.replace("e", str(math.e))

            # Handle functions
            expression = re.sub(r'sin\(([^)]+)\)', lambda m: f'math.sin(math.radians({m.group(1)}))' if self.angle_mode == "degrees" else f'math.sin({m.group(1)})', expression)
            expression = re.sub(r'cos\(([^)]+)\)', lambda m: f'math.cos(math.radians({m.group(1)}))' if self.angle_mode == "degrees" else f'math.cos({m.group(1)})', expression)
            expression = re.sub(r'tan\(([^)]+)\)', lambda m: f'math.tan(math.radians({m.group(1)}))' if self.angle_mode == "degrees" else f'math.tan({m.group(1)})', expression)
            expression = re.sub(r'log10\(([^)]+)\)', r'math.log10(\1)', expression)
            expression = re.sub(r'log\(([^)]+)\)', r'math.log(\1)', expression)
            expression = re.sub(r'sqrt\(([^)]+)\)', r'math.sqrt(\1)', expression)
            expression = re.sub(r'fact\(([^)]+)\)', lambda m: f'math.factorial(int({m.group(1)}))', expression)

            # Handle power operations
            expression = expression.replace("^", "**")

            # Evaluate the expression
            result = eval(expression, {"__builtins__": None}, {
                "math": math,
                "pi": math.pi,
                "e": math.e
            })

            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            result_str = str(result)

            # Update display
            self.result_label.config(text=result_str)
            self.current_expression = result_str

        except Exception as e:
            messagebox.showerror("Calculation Error", f"Invalid expression: {str(e)}")
            self.result_label.config(text="Error")

    def clear_all(self):
        self.current_expression = ""
        self.result_label.config(text="0")
        self.expression_label.config(text="")

    def clear_entry(self):
        self.current_expression = ""
        self.update_display()

    def backspace(self):
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
            self.update_display()

    def negate(self):
        try:
            if self.current_expression:
                value = float(self.current_expression)
                self.current_expression = str(-value)
                self.update_display()
        except:
            pass

    def memory_operation(self, op):
        try:
            if op == "MC":
                self.memory = 0
            elif op == "MR":
                self.current_expression = str(self.memory)
                self.update_display()
            elif op == "M+":
                if self.current_expression:
                    self.memory += float(self.current_expression)
            elif op == "M-":
                if self.current_expression:
                    self.memory -= float(self.current_expression)
            elif op == "MS":
                if self.current_expression:
                    self.memory = float(self.current_expression)
        except:
            pass


    def update_display(self):
        self.expression_label.config(text=self.current_expression)

    def change_angle_mode(self):
        self.angle_mode = self.angle_var.get()

def main():
    root = tk.Tk()
    app = ComplexCalculator(root)

    # Center the window
    root.update()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()

if __name__ == "__main__":
    main()
