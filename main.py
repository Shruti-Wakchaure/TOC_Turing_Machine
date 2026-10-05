import tkinter as tk
from tkinter import messagebox


# ============================================================
# TURING MACHINE
# ============================================================

class TuringMachine:

    def __init__(self, token):

        self.token = token
        self.tape = list(token) + ["□"]

        self.head = 0
        self.state = "q0"

        self.step_number = 0
        self.transitions = []

        self.finished = False

    # --------------------------------------------------------
    # Check Letter
    # --------------------------------------------------------

    def is_letter(self, ch):
        return ch.isalpha()

    # --------------------------------------------------------
    # Check remaining valid character
    # --------------------------------------------------------

    def is_valid_remaining(self, ch):
        return ch.isalpha() or ch.isdigit() or ch == "_"

    # --------------------------------------------------------
    # Perform one TM transition
    # --------------------------------------------------------

    def step(self):

        if self.finished:
            return None

        current_symbol = self.tape[self.head]

        old_state = self.state
        action = ""
        movement = "-"

        # ====================================================
        # STATE q0
        # First character
        # ====================================================

        if self.state == "q0":

            if self.is_letter(current_symbol) or current_symbol == "_":

                self.head += 1
                self.state = "q1"

                action = "Valid first character"
                movement = "R"

            else:

                self.state = "q_reject"
                self.finished = True

                action = "Invalid first character"
                movement = "-"

        # ====================================================
        # STATE q1
        # Remaining characters
        # ====================================================

        elif self.state == "q1":

            # Blank reached
            if current_symbol == "□":

                self.state = "q_accept"
                self.finished = True

                action = "End of input"
                movement = "-"

            # Valid character
            elif self.is_valid_remaining(current_symbol):

                self.head += 1

                action = "Valid character"
                movement = "R"

            # Invalid character
            else:

                self.state = "q_reject"
                self.finished = True

                action = "Invalid character"
                movement = "-"

        # ====================================================
        # ACCEPT
        # ====================================================

        elif self.state == "q_accept":

            self.finished = True
            return None

        # ====================================================
        # REJECT
        # ====================================================

        elif self.state == "q_reject":

            self.finished = True
            return None

        # ----------------------------------------------------
        # Save transition
        # ----------------------------------------------------

        self.step_number += 1

        transition = {
            "step": self.step_number,
            "old_state": old_state,
            "symbol": current_symbol,
            "new_state": self.state,
            "movement": movement,
            "action": action
        }

        self.transitions.append(transition)

        return transition


# ============================================================
# GUI
# ============================================================

class TuringMachineGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Compiler Token Verification - Turing Machine"
        )

        self.root.geometry("1200x800")

        self.root.configure(
            bg="#eef3f8"
        )

        self.tm = None

        self.running = False

        self.create_widgets()

    # ========================================================
    # CREATE GUI
    # ========================================================

    def create_widgets(self):

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = tk.Label(
            self.root,
            text="COMPILER TOKEN VERIFICATION",
            font=("Arial", 25, "bold"),
            bg="#173f6f",
            fg="white",
            pady=15
        )

        title.pack(fill="x")

        subtitle = tk.Label(
            self.root,
            text="Turing Machine Simulator",
            font=("Arial", 14, "bold"),
            bg="#eef3f8",
            fg="#173f6f"
        )

        subtitle.pack(pady=8)

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        input_frame = tk.Frame(
            self.root,
            bg="#eef3f8"
        )

        input_frame.pack(pady=8)

        tk.Label(
            input_frame,
            text="Enter Identifier:",
            font=("Arial", 14, "bold"),
            bg="#eef3f8"
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        self.input_entry = tk.Entry(
            input_frame,
            width=35,
            font=("Arial", 14)
        )

        self.input_entry.grid(
            row=0,
            column=1,
            padx=10
        )

        verify_button = tk.Button(
            input_frame,
            text="VERIFY",
            font=("Arial", 12, "bold"),
            bg="#2878b5",
            fg="white",
            width=12,
            command=self.start_machine
        )

        verify_button.grid(
            row=0,
            column=2,
            padx=10
        )

        # ----------------------------------------------------
        # INFORMATION PANEL
        # ----------------------------------------------------

        info_frame = tk.Frame(
            self.root,
            bg="#eef3f8"
        )

        info_frame.pack(pady=5)

        self.step_label = tk.Label(
            info_frame,
            text="Step: 0",
            font=("Arial", 13, "bold"),
            bg="#eef3f8"
        )

        self.step_label.grid(
            row=0,
            column=0,
            padx=30
        )

        self.symbol_label = tk.Label(
            info_frame,
            text="Current Symbol: --",
            font=("Arial", 13, "bold"),
            bg="#eef3f8"
        )

        self.symbol_label.grid(
            row=0,
            column=1,
            padx=30
        )

        self.state_label = tk.Label(
            info_frame,
            text="Current State: --",
            font=("Arial", 13, "bold"),
            bg="#eef3f8"
        )

        self.state_label.grid(
            row=0,
            column=2,
            padx=30
        )

        # ----------------------------------------------------
        # TAPE
        # ----------------------------------------------------

        tk.Label(
            self.root,
            text="TURING MACHINE TAPE",
            font=("Arial", 16, "bold"),
            bg="#eef3f8",
            fg="#173f6f"
        ).pack(pady=(10, 5))

        self.tape_canvas = tk.Canvas(
            self.root,
            width=1100,
            height=130,
            bg="white",
            highlightthickness=1,
            highlightbackground="#9aaabd"
        )

        self.tape_canvas.pack(
            padx=20
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        button_frame = tk.Frame(
            self.root,
            bg="#eef3f8"
        )

        button_frame.pack(pady=10)

        self.step_button = tk.Button(
            button_frame,
            text="STEP",
            font=("Arial", 12, "bold"),
            width=12,
            bg="#f0ad4e",
            fg="white",
            command=self.perform_step
        )

        self.step_button.grid(
            row=0,
            column=0,
            padx=8
        )

        self.run_button = tk.Button(
            button_frame,
            text="RUN",
            font=("Arial", 12, "bold"),
            width=12,
            bg="#3c9d5d",
            fg="white",
            command=self.run_machine
        )

        self.run_button.grid(
            row=0,
            column=1,
            padx=8
        )

        self.reset_button = tk.Button(
            button_frame,
            text="RESET",
            font=("Arial", 12, "bold"),
            width=12,
            bg="#d9534f",
            fg="white",
            command=self.reset_machine
        )

        self.reset_button.grid(
            row=0,
            column=2,
            padx=8
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 18, "bold"),
            bg="#eef3f8"
        )

        self.result_label.pack(
            pady=5
        )

        # ----------------------------------------------------
        # LOWER FRAME
        # ----------------------------------------------------

        lower_frame = tk.Frame(
            self.root,
            bg="#eef3f8"
        )

        lower_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=5
        )

        # ====================================================
        # TRANSITION TABLE
        # ====================================================

        table_frame = tk.Frame(
            lower_frame,
            bg="white",
            bd=2,
            relief="groove"
        )

        table_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            table_frame,
            text="TURING MACHINE TRANSITION TABLE",
            font=("Arial", 13, "bold"),
            bg="#173f6f",
            fg="white",
            pady=6
        ).pack(
            fill="x"
        )

        columns = (
            "State",
            "Read",
            "Next State",
            "Move"
        )

        self.transition_table = tk.Listbox(
            table_frame,
            font=("Consolas", 11),
            height=10
        )

        self.transition_table.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ----------------------------------------------------
        # Add transition rules
        # ----------------------------------------------------

        rules = [
            "q0     Letter       q1          R",
            "q0     _            q1          R",
            "q0     Digit        qReject     -",
            "q0     Special      qReject     -",
            "q1     Letter       q1          R",
            "q1     Digit        q1          R",
            "q1     _            q1          R",
            "q1     □            qAccept     -",
            "q1     Special      qReject     -"
        ]

        for rule in rules:

            self.transition_table.insert(
                tk.END,
                rule
            )

        # ====================================================
        # TRANSITION HISTORY
        # ====================================================

        history_frame = tk.Frame(
            lower_frame,
            bg="white",
            bd=2,
            relief="groove"
        )

        history_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            history_frame,
            text="EXECUTION HISTORY",
            font=("Arial", 13, "bold"),
            bg="#173f6f",
            fg="white",
            pady=6
        ).pack(
            fill="x"
        )

        self.history_list = tk.Listbox(
            history_frame,
            font=("Consolas", 10),
            height=10
        )

        self.history_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    # ========================================================
    # START MACHINE
    # ========================================================

    def start_machine(self):

        token = self.input_entry.get()

        if token == "":

            messagebox.showwarning(
                "Input Error",
                "Please enter an identifier."
            )

            return

        self.tm = TuringMachine(token)

        self.running = False

        self.history_list.delete(
            0,
            tk.END
        )

        self.result_label.config(
            text=""
        )

        self.step_label.config(
            text="Step: 0"
        )

        self.symbol_label.config(
            text=f"Current Symbol: {self.tm.tape[0]}"
        )

        self.state_label.config(
            text="Current State: q0"
        )

        self.draw_tape()

    # ========================================================
    # DRAW TAPE
    # ========================================================

    def draw_tape(self):

        self.tape_canvas.delete(
            "all"
        )

        if self.tm is None:
            return

        cell_width = 65

        total_width = len(
            self.tm.tape
        ) * cell_width

        start_x = max(
            20,
            (1100 - total_width) // 2
        )

        y1 = 30
        y2 = 85

        for i, symbol in enumerate(
            self.tm.tape
        ):

            x1 = start_x + i * cell_width
            x2 = x1 + cell_width

            # Highlight tape head
            if i == self.tm.head:

                self.tape_canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#ffd966",
                    outline="#173f6f",
                    width=3
                )

            else:

                self.tape_canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="white",
                    outline="#173f6f",
                    width=2
                )

            self.tape_canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=symbol,
                font=("Arial", 18, "bold")
            )

            if i == self.tm.head:

                self.tape_canvas.create_text(
                    (x1 + x2) / 2,
                    105,
                    text="▲ HEAD",
                    font=("Arial", 10, "bold"),
                    fill="#d9534f"
                )

    # ========================================================
    # STEP
    # ========================================================

    def perform_step(self):

        if self.tm is None:

            messagebox.showwarning(
                "Machine Not Started",
                "Click VERIFY first."
            )

            return

        if self.tm.finished:

            self.show_final_result()

            return

        transition = self.tm.step()

        if transition is None:
            return

        history_text = (
            f"Step {transition['step']} | "
            f"{transition['old_state']} → "
            f"{transition['new_state']} | "
            f"Read: {transition['symbol']} | "
            f"Move: {transition['movement']} | "
            f"{transition['action']}"
        )

        self.history_list.insert(
            tk.END,
            history_text
        )

        self.history_list.see(
            tk.END
        )

        self.step_label.config(
            text=f"Step: {transition['step']}"
        )

        self.state_label.config(
            text=f"Current State: {self.tm.state}"
        )

        # Current symbol
        if self.tm.head < len(self.tm.tape):

            current = self.tm.tape[
                self.tm.head
            ]

            self.symbol_label.config(
                text=f"Current Symbol: {current}"
            )

        else:

            self.symbol_label.config(
                text="Current Symbol: □"
            )

        self.draw_tape()

        if self.tm.finished:

            self.show_final_result()

    # ========================================================
    # RUN
    # ========================================================

    def run_machine(self):

        if self.tm is None:
            return

        if self.tm.finished:
            return

        self.running = True

        self.perform_step()

        if self.running and not self.tm.finished:

            self.root.after(
                600,
                self.run_machine
            )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    def show_final_result(self):

        self.running = False

        if self.tm.state == "q_accept":

            self.result_label.config(
                text="✓ ACCEPTED — VALID IDENTIFIER",
                fg="#218838"
            )

        elif self.tm.state == "q_reject":

            self.result_label.config(
                text="✗ REJECTED — INVALID IDENTIFIER",
                fg="#d9534f"
            )

    # ========================================================
    # RESET
    # ========================================================

    def reset_machine(self):

        self.running = False

        self.tm = None

        self.tape_canvas.delete(
            "all"
        )

        self.history_list.delete(
            0,
            tk.END
        )

        self.result_label.config(
            text=""
        )

        self.step_label.config(
            text="Step: 0"
        )

        self.symbol_label.config(
            text="Current Symbol: --"
        )

        self.state_label.config(
            text="Current State: --"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TuringMachineGUI(root)

    root.mainloop()