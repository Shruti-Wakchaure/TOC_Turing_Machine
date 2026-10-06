import tkinter as tk
from tkinter import messagebox


# ============================================================
# C / C++ RESERVED KEYWORDS
# ============================================================

KEYWORDS = {
    # ---------------- C KEYWORDS ----------------
    "auto",
    "break",
    "case",
    "char",
    "const",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "float",
    "for",
    "goto",
    "if",
    "inline",
    "int",
    "long",
    "register",
    "restrict",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "typedef",
    "union",
    "unsigned",
    "void",
    "volatile",
    "while",
    "_Alignas",
    "_Alignof",
    "_Atomic",
    "_Bool",
    "_Complex",
    "_Generic",
    "_Imaginary",
    "_Noreturn",
    "_Static_assert",
    "_Thread_local",

    # ---------------- C++ KEYWORDS ----------------
    "alignas",
    "alignof",
    "and",
    "and_eq",
    "asm",
    "atomic_cancel",
    "atomic_commit",
    "atomic_noexcept",
    "bitand",
    "bitor",
    "bool",
    "catch",
    "class",
    "compl",
    "concept",
    "const_cast",
    "consteval",
    "constexpr",
    "constinit",
    "decltype",
    "delete",
    "do",
    "dynamic_cast",
    "explicit",
    "export",
    "extern",
    "false",
    "friend",
    "inline",
    "mutable",
    "namespace",
    "new",
    "noexcept",
    "not",
    "not_eq",
    "nullptr",
    "operator",
    "or",
    "or_eq",
    "private",
    "protected",
    "public",
    "reflexpr",
    "reinterpret_cast",
    "requires",
    "static_assert",
    "static_cast",
    "synchronized",
    "template",
    "this",
    "thread_local",
    "throw",
    "true",
    "try",
    "typedef",
    "typeid",
    "typename",
    "using",
    "virtual",
    "wchar_t",
    "xor",
    "xor_eq",

    # ---------------- MODERN C++ ----------------
    "char8_t",
    "char16_t",
    "char32_t",
    "co_await",
    "co_return",
    "co_yield",
    "override",
    "final"
}


# ============================================================
# TURING MACHINE
# ============================================================

class TuringMachine:

    def __init__(self, token):

        self.token = token

        # Tape contains input + blank symbol
        self.tape = list(token) + ["□"]

        # Head starts at first character
        self.head = 0

        # Initial state
        self.state = "q0"

        # Step counter
        self.step_number = 0

        # Store all transitions
        self.transitions = []

        # Machine completion flag
        self.finished = False

    # ========================================================
    # CHECK LETTER
    # ========================================================

    def is_letter(self, ch):

        # Strict ASCII letters only
        return (
            ("A" <= ch <= "Z") or
            ("a" <= ch <= "z")
        )

    # ========================================================
    # CHECK REMAINING VALID CHARACTER
    # ========================================================

    def is_valid_remaining(self, ch):

        return (
            self.is_letter(ch)
            or
            ("0" <= ch <= "9")
            or
            ch == "_"
        )

    # ========================================================
    # CHECK RESERVED KEYWORD
    # ========================================================

    def is_keyword(self):

        return self.token in KEYWORDS

    # ========================================================
    # PERFORM ONE TM TRANSITION
    # ========================================================

    def step(self):

        if self.finished:
            return None

        current_symbol = self.tape[self.head]

        old_state = self.state

        action = ""

        movement = "-"

        # ====================================================
        # KEYWORD CHECK
        # ====================================================

        # Check only at the beginning.
        # If complete input is a reserved keyword,
        # reject it immediately.

        if self.step_number == 0 and self.is_keyword():

            self.state = "q_keyword_reject"

            self.finished = True

            action = "Reserved keyword"

            movement = "-"

        # ====================================================
        # STATE q0
        # First character
        # ====================================================

        elif self.state == "q0":

            # First character must be letter or underscore
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

            # ------------------------------------------------
            # Blank reached
            # ------------------------------------------------

            if current_symbol == "□":

                self.state = "q_accept"

                self.finished = True

                action = "End of input"

                movement = "-"

            # ------------------------------------------------
            # Valid character
            # ------------------------------------------------

            elif self.is_valid_remaining(current_symbol):

                self.head += 1

                action = "Valid character"

                movement = "R"

            # ------------------------------------------------
            # Invalid character
            # ------------------------------------------------

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
        # NORMAL REJECT
        # ====================================================

        elif self.state == "q_reject":

            self.finished = True

            return None

        # ====================================================
        # KEYWORD REJECT
        # ====================================================

        elif self.state == "q_keyword_reject":

            self.finished = True

            return None

        # ====================================================
        # SAVE TRANSITION
        # ====================================================

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

        # Turing Machine object
        self.tm = None

        # Running flag
        self.running = False

        # Scheduled RUN callback
        self.after_id = None

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
            text="Enter Token:",
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

        self.transition_table = tk.Listbox(
            table_frame,
            font=("Consolas", 10),
            height=13
        )

        self.transition_table.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ----------------------------------------------------
        # Transition Rules
        # ----------------------------------------------------

        rules = [

            "KEYWORD CHECK",
            "Any Keyword → qKeywordReject",

            "",
            "IDENTIFIER CHECK",

            "q0     Letter       q1              R",
            "q0     _            q1              R",
            "q0     Digit        qReject         -",
            "q0     Special      qReject         -",

            "q1     Letter       q1              R",
            "q1     Digit        q1              R",
            "q1     _            q1              R",
            "q1     □            qAccept         -",
            "q1     Special      qReject         -"
        ]

        for rule in rules:

            self.transition_table.insert(
                tk.END,
                rule
            )

        # ====================================================
        # EXECUTION HISTORY
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
            height=13
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

        # Stop previous RUN
        self.running = False

        if self.after_id is not None:

            try:
                self.root.after_cancel(self.after_id)

            except Exception:
                pass

            self.after_id = None

        token = self.input_entry.get()

        # Remove accidental spaces at beginning/end
        token = token.strip()

        if token == "":

            messagebox.showwarning(
                "Input Error",
                "Please enter an identifier."
            )

            return

        # Create new TM
        self.tm = TuringMachine(token)

        # Clear history
        self.history_list.delete(
            0,
            tk.END
        )

        # Clear result
        self.result_label.config(
            text=""
        )

        # Reset information
        self.step_label.config(
            text="Step: 0"
        )

        self.symbol_label.config(
            text=f"Current Symbol: {self.tm.tape[0]}"
        )

        self.state_label.config(
            text="Current State: q0"
        )

        # Show tape
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

        total_width = (
            len(self.tm.tape) * cell_width
        )

        # Keep tape inside canvas for normal inputs
        if total_width <= 1100:

            start_x = max(
                20,
                (1100 - total_width) // 2
            )

        else:

            start_x = 20

        y1 = 30
        y2 = 85

        for i, symbol in enumerate(
            self.tm.tape
        ):

            x1 = start_x + i * cell_width
            x2 = x1 + cell_width

            # ------------------------------------------------
            # Highlight current head
            # ------------------------------------------------

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

            # ------------------------------------------------
            # Symbol
            # ------------------------------------------------

            self.tape_canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=symbol,
                font=("Arial", 18, "bold")
            )

            # ------------------------------------------------
            # Head indicator
            # ------------------------------------------------

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

        # ----------------------------------------------------
        # Execution history
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Update step
        # ----------------------------------------------------

        self.step_label.config(
            text=f"Step: {transition['step']}"
        )

        # ----------------------------------------------------
        # Update state
        # ----------------------------------------------------

        self.state_label.config(
            text=f"Current State: {self.tm.state}"
        )

        # ----------------------------------------------------
        # Update current symbol
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Redraw tape
        # ----------------------------------------------------

        self.draw_tape()

        # ----------------------------------------------------
        # Final result
        # ----------------------------------------------------

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

            self.after_id = self.root.after(
                600,
                self.run_machine
            )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    def show_final_result(self):

        self.running = False

        # ----------------------------------------------------
        # VALID IDENTIFIER
        # ----------------------------------------------------

        if self.tm.state == "q_accept":

            self.result_label.config(
                text="✓ ACCEPTED — VALID IDENTIFIER",
                fg="#218838"
            )

        # ----------------------------------------------------
        # RESERVED KEYWORD
        # ----------------------------------------------------

        elif self.tm.state == "q_keyword_reject":

            self.result_label.config(
                text="✗ REJECTED — RESERVED KEYWORD",
                fg="#d9534f"
            )

        # ----------------------------------------------------
        # INVALID IDENTIFIER
        # ----------------------------------------------------

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

        # Cancel scheduled RUN
        if self.after_id is not None:

            try:
                self.root.after_cancel(
                    self.after_id
                )

            except Exception:
                pass

            self.after_id = None

        # Remove TM
        self.tm = None

        # Clear tape
        self.tape_canvas.delete(
            "all"
        )

        # Clear history
        self.history_list.delete(
            0,
            tk.END
        )

        # Clear result
        self.result_label.config(
            text=""
        )

        # Reset information
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