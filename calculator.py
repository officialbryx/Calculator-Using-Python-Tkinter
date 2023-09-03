# imported tkinter for gui creation
import tkinter as tk

# Define font styles
LARGE_FONT_STYLE = ("Segoe", 40, "bold")
SMALL_FONT_STYLE = ("Segoe", 16)
DIGITS_FONT_STYLE = ("Segoe", 24, "bold")
DEFAULT_FONT_STYLE = ("Segoe", 20)

# Define color constants
OPERATOR_GREY = "#323232"
WHITE = "#3b3b3b"
EQUAL_LIGHTGREY = "#595959"
DISPLAY_GRAY = "#202020"
LABEL_COLOR = "#FFFFFF"


class Calculator:
    def __init__(self):
        # Initialize the tkinter window
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        # Set the window icon
        self.window.iconbitmap(r"calculator.ico")

        # Initialize expression variables
        self.total_expression = ""
        self.current_expression = ""

        # Create the frame for displaying the expressions
        self.display_frame = self.create_display_frame()

        # Create labels for displaying expressions
        self.total_label, self.label = self.create_display_labels()

        # Define the layout of digits and operators on the calculator
        self.digits = {
            7: (1, 1),
            8: (1, 2),
            9: (1, 3),
            4: (2, 1),
            5: (2, 2),
            6: (2, 3),
            1: (3, 1),
            2: (3, 2),
            3: (3, 3),
            0: (4, 2),
            ".": (4, 1),
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        # Create a frame to hold calculator buttons
        self.buttons_frame = self.create_buttons_frame()

        # Configure the grid layout for buttons
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        # Create digit, operator, and special buttons
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

        # Bind keys for keyboard input
        self.bind_keys()

    def bind_keys(self):
        # Bind the Enter key to evaluate the expression
        self.window.bind("<Return>", lambda event: self.evaluate())

        # Bind digit keys to add corresponding digits to the expression
        for key in self.digits:
            self.window.bind(
                str(key), lambda event, digit=key: self.add_to_expression(digit)
            )

        # Bind operator keys to append corresponding operators to the expression
        for key in self.operations:
            self.window.bind(
                key, lambda event, operator=key: self.append_operator(operator)
            )

    def create_special_buttons(self):
        # Create special buttons (Clear, Equals, Square, Square Root)
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        # Create labels for displaying the total and current expressions
        total_label = tk.Label(
            self.display_frame,
            text=self.total_expression,
            anchor=tk.E,
            bg=DISPLAY_GRAY,
            fg=LABEL_COLOR,
            padx=24,
            font=SMALL_FONT_STYLE,
        )
        total_label.pack(expand=True, fill="both")

        label = tk.Label(
            self.display_frame,
            text=self.current_expression,
            anchor=tk.E,
            bg=DISPLAY_GRAY,
            fg=LABEL_COLOR,
            padx=24,
            font=LARGE_FONT_STYLE,
        )
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        # Create a frame for displaying expressions with a specified height and background color
        frame = tk.Frame(self.window, height=221, bg=DISPLAY_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        # Add the given value (digit) to the current expression
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        # Create buttons for digits and place them in the grid
        for digit, grid_value in self.digits.items():
            button = tk.Button(
                self.buttons_frame,
                text=str(digit),
                bg=WHITE,
                fg=LABEL_COLOR,
                font=DIGITS_FONT_STYLE,
                borderwidth=0,
                command=lambda x=digit: self.add_to_expression(x),
            )
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        # Append the given operator to the current expression and update total expression
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        # Create buttons for operators and place them in the grid
        for operator, symbol in self.operations.items():
            button = tk.Button(
                self.buttons_frame,
                text=symbol,
                bg=OPERATOR_GREY,
                fg=LABEL_COLOR,
                font=DEFAULT_FONT_STYLE,
                borderwidth=0,
                command=lambda x=operator: self.append_operator(x),
            )
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        # Clear both the current and total expressions, and update the labels
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        # Create a "C" button for clearing the current expression
        button = tk.Button(
            self.buttons_frame,
            text="C",
            bg=OPERATOR_GREY,
            fg=LABEL_COLOR,
            font=DEFAULT_FONT_STYLE,
            borderwidth=0,
            command=self.clear,
        )
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        # Square the current expression and update the label
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        # Create a button for squaring the current expression
        button = tk.Button(
            self.buttons_frame,
            text="x\u00b2",  # Unicode character for superscript 2
            bg=OPERATOR_GREY,
            fg=LABEL_COLOR,
            font=DEFAULT_FONT_STYLE,
            borderwidth=0,
            command=self.square,
        )
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        # Calculate the square root of the current expression and update the label
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        # Create a button for calculating the square root of the current expression
        button = tk.Button(
            self.buttons_frame,
            text="\u221ax",  # Unicode character for square root symbol
            bg=OPERATOR_GREY,
            fg=LABEL_COLOR,
            font=DEFAULT_FONT_STYLE,
            borderwidth=0,
            command=self.sqrt,
        )
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        # Evaluate the total expression, update the current expression, and clear the total expression
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            # If an error occurs, set the current expression to blank
            self.current_expression = ""
        finally:
            self.update_label()

    def create_equals_button(self):
        # Create an "=" button for evaluating the expression
        button = tk.Button(
            self.buttons_frame,
            text="=",
            bg=EQUAL_LIGHTGREY,
            fg=LABEL_COLOR,
            font=DEFAULT_FONT_STYLE,
            borderwidth=0,
            command=self.evaluate,
        )
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        # Create a frame to hold calculator buttons
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        # Update the total expression label with proper formatting
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.total_label.config(text=expression)

    def update_label(self):
        # Update the current expression label, truncating it if it's too long
        self.label.config(text=self.current_expression[:11])

    def run(self):
        # Start the main event loop of the tkinter application
        self.window.mainloop()


# Entry point of the application
if __name__ == "__main__":
    calc = Calculator()
    calc.run()
