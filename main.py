from tkinter import *

settings = {"pawn": "⚫",
            "pawn_color": "darkorange",
            "empty_color": "gainsboro",
            "default_background": "skyblue",
            "default_button_background": "#6CB8FF",
            "possible_selected_button_background": "#A4F1AE",
            "impossible_selected_button_background": "dimgray",
            "possible_case_background": "#166172",
            "bar_background":"lightblue",
            "bar_text_color":"navy",
            "bar_font":60
            }

game = {"situation": "nothing_selected"}


class Cell:
    def __init__(self, row_no, column_no):
        self.situation = "pawn"  # can be "pawn" or "empty"
        self.row_no = row_no
        self.column_no = column_no
        self.button = Button(board, text=settings["pawn"], font=40, width=3, relief="flat",
                             bg=settings["default_button_background"], fg=settings["pawn_color"],
                             command=self.clicked)
        self.button.grid(row=self.row_no, column=self.column_no)

    def situation_change(self):
        if self.situation == "pawn":
            self.situation = "empty"
            self.button["fg"] = settings["empty_color"]
        else:
            self.situation = "pawn"
            self.button["fg"] = settings["pawn_color"]

    def possible_moves(self):
        if self.button["fg"] == settings["empty_color"]:
            return None
        cases = []
        # Look for left right up and down
        for side in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            first_step = matrix[self.row_no + side[0]][self.column_no + side[1]]
            if first_step is not None and first_step.situation == "pawn":
                second_step = matrix[self.row_no + 2 * side[0]][self.column_no + 2 * side[1]]
                if second_step is not None and second_step.situation == "empty":
                    cases.append(second_step)
        if not cases:
            return None
        return cases

    def clicked(self):
        if game["situation"] in ("nothing_selected", "impossible_selected", "possible_selected") and \
                self.button["fg"] == settings["pawn_color"] and self.button["bg"] == settings["default_button_background"]:
            clear_colored()
            self.button["bg"] = settings["impossible_selected_button_background"]
            game["situation"] = "impossible_selected"
            colored.append(matrix[self.row_no][self.column_no])
            possible_cases = self.possible_moves()
            if possible_cases is not None:
                self.button["bg"] = settings["possible_selected_button_background"]
                game["situation"] = "possible_selected"
                for poss in possible_cases:
                    poss.button["bg"] = settings["possible_case_background"]
                    colored.append(poss)
        elif game["situation"] == "possible_selected" and self.button["bg"] == settings["possible_case_background"]:
            colored[0].situation_change()
            self.situation_change()
            matrix[(colored[0].row_no + self.row_no) // 2][
                (colored[0].column_no + self.column_no) // 2].situation_change()
            clear_colored()
            game["situation"] = "nothing_selected"
            pawn_number["text"] = str(int(pawn_number["text"]) - 1)
            check_game_continues()
        else:
            game["situation"] = "nothing_selected"
            clear_colored()

def clear_colored():
    while len(colored) > 0:
        colored[0].button["bg"] = settings["default_button_background"]
        colored.pop(0)


def check_game_continues():
    for row in matrix:
        for cell in row:
            if cell is not None:
                if cell.possible_moves() is not None:
                    return 0  # The game continues.
    game_over()


def game_over():
    message_box["text"]="Game Over!"

def restart():
    message_box["text"] = ""
    pawn_number["text"] = "32"
    for row in matrix:
        for cell in row:
            if cell is not None and cell.situation == "empty":
                cell.situation_change()
    matrix[4][4].situation_change()

root = Tk()
root.title("Solo Test")
root.iconbitmap("images/solotest.ico")
root.configure(bg=settings["default_background"])
root.resizable(False,False)
bar = Frame(root, bg=settings["bar_background"])
bar.pack(padx=20, pady=20, anchor="w",fill="x")
pawn_number = Label(bar, text="32", font=settings["bar_font"], width=2,
                    bg=settings["bar_background"], fg=settings["bar_text_color"])
pawn_number.grid(row=0, column=0,padx=10)
message_box=Label(bar, text="", font=settings["bar_font"], width=20,
                  bg=settings["bar_background"], fg=settings["bar_text_color"])
message_box.grid(row=0, column=1)
retry_button=Button(bar, text="R", width=3, relief= "flat",font=settings["bar_font"], command=restart,
                    bg=settings["bar_background"], fg=settings["bar_text_color"])
retry_button.grid(row=0, column=2)
board = Frame(root, bg=settings["default_background"])
board.pack(padx=20, pady=(0, 20))
colored = []
# Creating buttons
matrix = []
for y in range(9):
    matrix_row = []
    for x in range(9):
        if (x not in (1, 2, 6, 7) or y not in (1, 2, 6, 7)) and x not in (0, 8) and y not in (0, 8):
            matrix_row.append(Cell(y, x))
        else:
            matrix_row.append(None)
    matrix.append(matrix_row)
# Empty middle
matrix[4][4].situation_change()

root.mainloop()
