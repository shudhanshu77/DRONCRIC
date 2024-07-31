import tkinter as tk
from tkinter import messagebox
import time


class CricketQuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cricket Quiz")
        self.master.geometry("400x400")  # Reduced dimensions for a smaller screen

        # Set background color to light blue
        self.master.configure(bg="#87CEEB")

        self.quiz = CricketQuiz()

        # Quiz title label
        self.title_label = tk.Label(self.master, text="Cricket Quiz", font=("Helvetica", 16, "bold"), bg="#87CEEB")
        self.title_label.pack(pady=10)

        self.start_button = tk.Button(self.master, text="Start Quiz", command=self.start_quiz, bg="#3498db", fg="white",
                                      font=("Helvetica", 12, "bold"))
        self.start_button.pack(pady=20)

        # Question label
        self.question_label = tk.Label(self.master, text="", font=("Helvetica", 14), bg="#87CEEB")
        self.question_label.pack(pady=10)

        # Option buttons
        self.option_buttons = []
        for i in range(4):
            option_button = tk.Button(self.master, text="", command=lambda i=i: self.check_answer(i + 1),
                                      bg="#3498db", fg="white", font=("Helvetica", 10, "bold"))
            option_button.pack(pady=5, padx=20, fill=tk.X)
            self.option_buttons.append(option_button)

        self.timer_label = tk.Label(self.master, text="", font=("Helvetica", 12), bg="#87CEEB")
        self.timer_label.pack(pady=10)

        self.result_label = tk.Label(self.master, text="", font=("Helvetica", 12), bg="#87CEEB")
        self.result_label.pack(pady=10)

        self.next_button = tk.Button(self.master, text="Next", command=self.next_question, bg="#2ecc71", fg="white",
                                     font=("Helvetica", 12, "bold"))
        self.next_button.pack(pady=10)
        self.next_button.config(state=tk.DISABLED)  # Disable "Next" button initially

        self.current_question = 0
        self.quiz_duration = 300  # 5 minutes in seconds
        self.start_time = None

    def start_quiz(self):
        self.start_button.config(state=tk.DISABLED)  # Disable "Start" button after starting the quiz
        self.next_button.config(state=tk.NORMAL)  # Enable "Next" button
        self.current_question = 0
        self.quiz.score = 0
        self.start_time = time.time()
        self.update_question()
        self.update_timer()

    def update_question(self):
        if self.current_question < len(self.quiz.questions):
            question_data = self.quiz.questions[self.current_question]
            self.question_label.config(text=f"{self.current_question + 1}. {question_data['question']}")
            for i, option_button in enumerate(self.option_buttons):
                option_button.config(text=question_data['options'][i], state=tk.NORMAL)

    def check_answer(self, user_answer):
        self.quiz.check_answer(self.current_question, user_answer)
        for option_button in self.option_buttons:
            option_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question += 1

        if self.current_question < len(self.quiz.questions):
            self.update_question()
            for option_button in self.option_buttons:
                option_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)
        else:
            elapsed_time = int(time.time() - self.start_time)
            self.show_result(elapsed_time)

    def update_timer(self):
        remaining_time = max(0, self.quiz_duration - int(time.time() - self.start_time))
        minutes, seconds = divmod(remaining_time, 60)
        timer_text = f"Time Left: {minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=timer_text)

        if remaining_time > 0:
            self.master.after(1000, self.update_timer)
        else:
            self.show_result(0)

    def show_result(self, elapsed_time):
        result_text = f"Quiz completed!\nYour score is: {self.quiz.score}/{len(self.quiz.questions)}\nElapsed Time: {elapsed_time} seconds."
        self.result_label.config(text=result_text)
        self.current_question = 0
        self.quiz.score = 0
        self.update_question()
        self.start_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)


class CricketQuiz:
    def __init__(self):
        self.questions = [
            {
                "question": "Who is known as the 'Little Master' in cricket?",
                "options": ["Sachin Tendulkar", "Virat Kohli", "Ricky Ponting", "Brian Lara"],
                "correct_answer": "Sachin Tendulkar",
            },
            # Add more questions as needed
        ]
        self.score = 0

    def check_answer(self, question_number, user_answer):
        correct_answer = self.questions[question_number]["correct_answer"]
        if user_answer == self.questions[question_number]["options"].index(correct_answer) + 1:
            messagebox.showinfo("Result", "Correct!")
            self.score += 1
        else:
            correct_option = self.questions[question_number]["options"].index(correct_answer) + 1
            messagebox.showinfo("Result", f"Wrong! The correct answer is Option {correct_option}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CricketQuizApp(root)
    root.mainloop()
