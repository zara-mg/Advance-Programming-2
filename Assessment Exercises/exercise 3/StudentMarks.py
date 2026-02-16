import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1000x600")
        self.root.configure(bg="#A9566B")
        self.students = []
        self.load_students()
        self.create_widgets()
        
    def load_students(self):
        file_path = os.path.join(os.path.dirname(__file__), 'Marks.txt')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                num_students = int(lines[0].strip())
                for i in range(1, num_students + 1):
                    parts = [p.strip() for p in lines[i].split(',')]
                    student = {
                        'code': parts[0],
                        'name': parts[1],
                        'coursework': [int(parts[2]), int(parts[3]), int(parts[4])],
                        'exam': int(parts[5])
                    }
                    self.students.append(student)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading student data: {e}\nTried: {file_path}")
    
    def calculate_stats(self, student):
        total_coursework = sum(student['coursework'])
        total_marks = total_coursework + student['exam']
        percentage = (total_marks / 160) * 100
        if percentage >= 70:
            grade = 'A'
        elif percentage >= 60:
            grade = 'B'
        elif percentage >= 50:
            grade = 'C'
        elif percentage >= 40:
            grade = 'D'
        else:
            grade = 'F'
        return total_coursework, total_marks, percentage, grade
    
    def create_widgets(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        header = tk.Frame(self.root, bg="Pink", height=60)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        tk.Label(header, text="Student Manager", font=("Arial", 24, "bold"), 
                bg="Pink", fg="white", pady=15).pack()
        
        nav_frame = tk.Frame(self.root, bg="Pink", width=220)
        nav_frame.grid(row=1, column=0, sticky="ns")
        nav_frame.grid_propagate(False)
        
        tk.Button(nav_frame, text="View All Students", command=self.view_all, 
                 font=("Arial", 12), bg="#A9566B", fg="white", 
                 width=20, height=2, relief=tk.FLAT, cursor="hand2").pack(pady=15, padx=10)
        tk.Button(nav_frame, text="View Individual", command=self.view_individual, 
                 font=("Arial", 12), bg="#A9566B", fg="white", 
                 width=20, height=2, relief=tk.FLAT, cursor="hand2").pack(pady=15, padx=10)
        tk.Button(nav_frame, text="Highest Score", command=self.show_highest, 
                 font=("Arial", 12), bg="#A9566B", fg="white", 
                 width=20, height=2, relief=tk.FLAT, cursor="hand2").pack(pady=15, padx=10)
        tk.Button(nav_frame, text="Lowest Score", command=self.show_lowest, 
                 font=("Arial", 12), bg="#A9566B", fg="white", 
                 width=20, height=2, relief=tk.FLAT, cursor="hand2").pack(pady=15, padx=10)
        
        content_frame = tk.Frame(self.root, bg="white")
        content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, 
                                                   font=("Courier New", 11), bg="white",
                                                   relief=tk.SOLID, borderwidth=1)
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.text_area.insert(tk.END, f"\n\n  Welcome to Student Manager\n\n")
        self.text_area.insert(tk.END, f"  Loaded {len(self.students)} students from database.\n\n")
        self.text_area.insert(tk.END, "  Please select an option from the menu.")
        self.text_area.config(state=tk.DISABLED)
        
    def format_student(self, student):
        course_work, total, percentage, grade = self.calculate_stats(student)
        output = f"\n  Student Name          : {student['name']}\n"
        output += f"  Student Number        : {student['code']}\n"
        output += f"  Total Coursework Mark : {course_work}/60\n"
        output += f"  Exam Mark             : {student['exam']}/100\n"
        output += f"  Overall Percentage    : {percentage:.2f}%\n"
        output += f"  Grade                 : {grade}\n"
        return output
    
    def view_all(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "\n")
        self.text_area.insert(tk.END, "  " + "=" * 75 + "\n")
        self.text_area.insert(tk.END, "  ALL STUDENT RECORDS\n")
        self.text_area.insert(tk.END, "  " + "=" * 75 + "\n")
        
        total_percentage = 0
        for i, student in enumerate(self.students, 1):
            self.text_area.insert(tk.END, self.format_student(student))
            if i < len(self.students):
                self.text_area.insert(tk.END, "  " + "-" * 75 + "\n")
            _, _, percentage, _ = self.calculate_stats(student)
            total_percentage += percentage
        
        avg_percentage = total_percentage / len(self.students) if self.students else 0
        self.text_area.insert(tk.END, "\n  " + "=" * 75 + "\n")
        self.text_area.insert(tk.END, "  SUMMARY\n")
        self.text_area.insert(tk.END, "  " + "=" * 75 + "\n\n")
        self.text_area.insert(tk.END, f"  Total Students       : {len(self.students)}\n")
        self.text_area.insert(tk.END, f"  Average Percentage   : {avg_percentage:.2f}%\n\n")
        self.text_area.config(state=tk.DISABLED)
    
    def view_individual(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Student")
        dialog.geometry("450x550")
        dialog.configure(bg="white")
        
        tk.Label(dialog, text="Select a Student", font=("Arial", 14, "bold"), 
                bg="white", pady=15).pack()
        
        frame = tk.Frame(dialog, bg="white")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, font=("Arial", 11), height=20, 
                            yscrollcommand=scrollbar.set, relief=tk.SOLID, borderwidth=1)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        for i, student in enumerate(self.students, 1):
            listbox.insert(tk.END, f"{i}. {student['name']} ({student['code']})")
        
        def show_selected():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                self.text_area.config(state=tk.NORMAL)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, "\n")
                self.text_area.insert(tk.END, "  " + "=" * 75 + "\n")
                self.text_area.insert(tk.END, "  INDIVIDUAL STUDENT RECORD\n")
                self.text_area.insert(tk.END, "  " + "=" * 75 + "\n")
                self.text_area.insert(tk.END, self.format_student(self.students[idx]))
                self.text_area.insert(tk.END, "\n")
                self.text_area.config(state=tk.DISABLED)
                dialog.destroy()
        
        tk.Button(dialog, text="View Student", command=show_selected, 
                 font=("Arial", 11), bg="#A9566B", fg="white", 
                 padx=30, pady=10, cursor="hand2").pack(pady=15)
    
    def show_highest(self):
        if not self.students:
            return
        highest = max(self.students, key=lambda s: sum(s['coursework']) + s['exam'])
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "\n")
        self.text_area.insert(tk.END, "  " + "=" * 75 + "\n")
        self.text_area.insert(tk.END, "  STUDENT WITH HIGHEST TOTAL SCORE\n")
        self.text_area.insert(tk.END, "  " + "=" * 75 + "\n")
        self.text_area.insert(tk.END, self.format_student(highest))
        self.text_area.insert(tk.END, "\n")
        self.text_area.config(state=tk.DISABLED)
    
    def show_lowest(self):
        if not self.students:
            return
        lowest = min(self.students, key=lambda s: sum(s['coursework']) + s['exam'])
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, "\n")
        self.text_area.insert(tk.END, "  " + "=" * 75 + "\n")
        self.text_area.insert(tk.END, "  STUDENT WITH LOWEST TOTAL SCORE\n")
        self.text_area.insert(tk.END, "  " + "=" * 75 + "\n")
        self.text_area.insert(tk.END, self.format_student(lowest))
        self.text_area.insert(tk.END, "\n")
        self.text_area.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()