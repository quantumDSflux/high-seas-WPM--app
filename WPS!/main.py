import tkinter as tk
import time
import random
from tkinter import font


class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Speed Typing Test")
        
        # Set the window to full-screen by default
        self.is_fullscreen = True
        self.root.attributes('-fullscreen', True)
        self.root.config(bg="#1e1e1e")  # Dark background color

        # Custom fonts and colors
        self.letter_font = font.Font(family="Consolas", size=30, weight="bold")  # Larger font for letters
        self.dot_font = font.Font(family="Consolas", size=20)  # Smaller font for dots
        self.correct_color = "#5a5a5a"  # Dark gray for correct text (simulates transparency)
        self.wrong_color = "#f44747"   # Red for incorrect text
        self.cursor_color = "#ffffff"  # White for cursor
        self.glowing_color = "#ff0"  # Bright yellow for glowing effect
        self.normal_color = "#d4d4d4"  # Default gray color for timer

        # Create a canvas for background and text display
        self.text_canvas = tk.Canvas(self.root, bg="#1e1e1e", highlightthickness=0)
        self.text_canvas.pack(fill="both", expand=True, padx=20, pady=20)

        # Add a gradient background (optional enhancement)
        self.add_gradient_background()

        # UI Elements
        self.entry_text = tk.Entry(self.root, font=self.letter_font, bg="#252526", fg="#d4d4d4", insertbackground="#d4d4d4",
                                   bd=0, highlightthickness=1, highlightbackground="#444444", width=50)
        self.entry_text.pack(pady=20)
        self.entry_text.bind("<KeyRelease>", self.check_typing)

        # WPM Label with a nice glowing effect
        self.label_wpm = tk.Label(self.root, text="WPM: 0", font=("Helvetica", 20), fg="#d4d4d4", bg="#1e1e1e")
        self.label_wpm.pack()

        # Timer Label for countdown
        self.label_timer = tk.Label(self.root, text="Next in: 3s", font=("Helvetica", 20), fg=self.normal_color, bg="#1e1e1e")
        self.label_timer.pack()

        # Restart Button with a stylish hover effect
        self.button_restart = tk.Button(self.root, text="Restart", command=self.restart, bg="#444444", fg="#d4d4d4",
                                        font=("Helvetica", 14), bd=0, activebackground="#5a5a5a", padx=10, pady=5)
        self.button_restart.pack(pady=10)
        self.button_restart.bind("<Enter>", self.on_button_hover)
        self.button_restart.bind("<Leave>", self.on_button_leave)

        # Test Variables
        self.target_text = ""
        self.start_time = None
        self.running = False
        self.countdown = 3  # 3 seconds for the timer

        self.load_new_test()

        # Bind F11 and ESC to toggle full-screen/windowed mode
        self.root.bind("<F11>", self.toggle_full_screen)
        self.root.bind("<Escape>", self.toggle_full_screen)

    def add_gradient_background(self):
        """Optional function to add a gradient background effect."""
        for i in range(0, 300, 10):  # Gradually changing the background color
            self.text_canvas.create_line(0, i, self.root.winfo_width(), i,
                                         fill=f"#{int(255 - i*0.7):02x}{int(255 - i*0.3):02x}33", width=2)

    def load_new_test(self):
        """Load a new test."""
        self.target_text = self.load_text().replace(" ", "•")  # Replace spaces with dots
        self.entry_text.delete(0, tk.END)
        self.text_canvas.delete("all")
        self.start_time = None
        self.running = True
        self.label_wpm.config(text="WPM: 0")  # Reset WPM display
        self.label_timer.config(text="Next in: 3s", fg=self.normal_color)  # Reset the timer display
        self.display_text(self.target_text, [])
        self.update_wpm()  # Start updating WPM periodically

    def load_text(self):
        """Load a random line from text.txt."""
        try:
            with open("text.txt", "r") as f:
                lines = f.readlines()
                return random.choice(lines).strip()
        except FileNotFoundError:
            return "Error: Could not find 'text.txt'. Please create the file with sample texts."

    def display_text(self, target, current):
        """Display the target text with highlighting for typed characters."""
        self.text_canvas.delete("all")  # Clear the canvas
        x = 20
        y = 50
        spacing = 25  # Letter spacing

        for i, char in enumerate(target):
            if char == "•":
                font_to_use = self.dot_font  # Use smaller font for dots
            else:
                font_to_use = self.letter_font  # Use larger font for letters

            color = self.correct_color
            if i < len(current):
                if char != current[i]:  # Incorrect character
                    color = self.wrong_color
            elif i == len(current):  # Cursor position
                color = self.cursor_color

            self.text_canvas.create_text(x, y, text=char, fill=color, font=font_to_use, anchor="nw")
            x += spacing  # Add spacing for the next character

            # Wrap to a new line if the text exceeds the canvas width
            if x > self.root.winfo_width() - 40:
                x = 20
                y += 50  # Adjust line height for larger font

    def check_typing(self, event):
        """Check typing progress."""
        if not self.running:
            return

        if self.start_time is None:
            self.start_time = time.time()

        entered_text = self.entry_text.get().replace(" ", "•")  # Replace spaces with dots for checking
        target_text = self.target_text

        if entered_text == target_text:
            self.running = False
            self.label_wpm.config(text=f"WPM: {self.calculate_wpm(len(entered_text))}")
            self.entry_text.config(state="disabled")  # Disable entry during delay
            self.start_next_sentence_timer()  # Start the 3-second timer before next sentence
            return

        self.display_text(target_text, entered_text)

    def calculate_wpm(self, char_count):
        """Calculate words per minute."""
        elapsed_time = max(time.time() - self.start_time, 1)  # Avoid division by zero
        return round((char_count / 5) / (elapsed_time / 60))

    def update_wpm(self):
        """Update WPM periodically while typing."""
        if self.running and self.start_time:
            entered_text = self.entry_text.get().replace(" ", "•")
            wpm = self.calculate_wpm(len(entered_text))
            self.label_wpm.config(text=f"WPM: {wpm}")

        # Schedule the next WPM update after 500ms (half a second)
        if self.running:
            self.root.after(500, self.update_wpm)

    def start_next_sentence_timer(self):
        """Start a 3-second timer before loading the next sentence."""
        self.countdown = 3  # Reset the countdown to 3 seconds
        self.update_timer()  # Start updating the timer
        self.glow_timer()  # Start the glowing effect
        self.root.after(1000, self.decrement_timer)  # Start the countdown after 1 second

    def glow_timer(self):
        """Glow the timer text by alternating its color."""
        current_color = self.normal_color
        if self.countdown % 2 == 0:
            current_color = self.glowing_color
        self.label_timer.config(fg=current_color)
        self.root.after(500, self.glow_timer)  # Update color every 500ms to create the glow effect

    def decrement_timer(self):
        """Decrement the timer every second."""
        self.countdown -= 1
        self.label_timer.config(text=f"Next in: {self.countdown}s")
        if self.countdown > 0:
            # Keep decrementing the timer every second
            self.root.after(1000, self.decrement_timer)
        else:
            # Timer finished, load the next sentence
            self.next_sentence()

    def update_timer(self):
        """Update the timer display immediately."""
        self.label_timer.config(text=f"Next in: {self.countdown}s")

    def next_sentence(self):
        """Load the next sentence after the timer ends."""
        self.load_new_test()

    def restart(self):
        """Restart the typing test."""
        self.load_new_test()

    def toggle_full_screen(self, event=None):
        """Toggle fullscreen/windowed mode."""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

    def on_button_hover(self, event):
        """Change button color on hover."""
        self.button_restart.config(bg="#666666")

    def on_button_leave(self, event):
        """Reset button color when hover ends."""
        self.button_restart.config(bg="#444444")


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()

