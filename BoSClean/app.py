import customtkinter as ctk
from tkinter import messagebox

from income import clean_income
from disability import clean_disability
from homelessness import clean_homelessness
from housing_timelines import process_length_and_movein
from permanent_housing import calculate_permanent_exit

# Set theme and color settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BoSDataCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.title("BoS Data Cleaner")

        # Set fixed size
        window_width = 600
        window_height = 600

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate center position
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # Set geometry with position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Optional: make column stretchable
        self.grid_columnconfigure(0, weight=1)

    def run_task(self, func, description):
        try:
            func()
            messagebox.showinfo(
                "Success", f"{description} completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def create_widgets(self):
        # Header
        header = ctk.CTkLabel(
            self,
            text="BoS Data Cleaner",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        header.grid(row=0, column=0, pady=(20, 20), padx=20)

        # Subheader
        subheader = ctk.CTkLabel(
            self,
            text="Select a cleaning option:",
            font=ctk.CTkFont(size=16)
        )
        subheader.grid(row=1, column=0, pady=(0, 20))

        # Cleaning options
        options = [
            ("1 → Disability", "Clean 'DISABILITY ENT' and 'DISABILITY EXT' tabs",
             lambda: self.run_task(clean_disability, "Disability cleaning")),

            ("2 → Homelessness", "Clean 'EE UDES' tab\n(prior living, times homeless, months homeless)",
             lambda: self.run_task(clean_homelessness, "Homelessness cleaning")),

            ("3 → Income", "Clean 'INCOME ENT' and 'INCOME EXT' tabs",
             lambda: self.run_task(clean_income, "Income cleaning")),

            ("4 → Housing Timelines", "Clean 'ENTRY-EXIT' tab\n(length of stay and days to move-in)",
             lambda: self.run_task(process_length_and_movein, "Housing Timelines cleaning")),

            ("5 → Housing Exit Type", "Clean 'ENTRY-EXIT' tab\nClassify permanent vs. non-permanent exits",
             lambda: self.run_task(calculate_permanent_exit, "Housing Exit Type classification"))
        ]

        # Create buttons for each option
        for i, (title, description, command) in enumerate(options, start=2):
            # Frame for each option
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=i, column=0, padx=20, pady=10, sticky="ew")
            frame.grid_columnconfigure(0, weight=1)

            # Button with title and description
            btn = ctk.CTkButton(
                frame,
                text=f"{title}\n{description}",
                font=ctk.CTkFont(size=14),
                height=50,
                command=command
            )
            btn.grid(row=0, column=0, sticky="ew")

        # Exit button
        exit_btn = ctk.CTkButton(
            self,
            text="6 → Exit",
            font=ctk.CTkFont(size=14),
            height=50,
            fg_color="#D35B58",
            hover_color="#C83632",
            command=self.quit
        )
        exit_btn.grid(row=len(options)+2, column=0,
                      padx=20, pady=(30, 30), sticky="ew")


def main():
    app = BoSDataCleanerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
