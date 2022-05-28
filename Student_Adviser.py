import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
from tkinter import *
from datetime import date

SEASONS = ('Summer', 'Fall', 'Spring')

class StudentAdviser():

    # CONSTRUCTOR
    def __init__(self, master):
        self.master = master
        self.file_contents = []
        self.file_contents_hash = {}
        # self.frame = tk.Frame(self.master)
        tabControl = ttk.Notebook(self.master)
  
        self.tab1 = ttk.Frame(tabControl)
        s = ttk.Style()
        s.configure('new.TFrame', background='#FFFFFF')
        self.tab2 = ttk.Frame(tabControl, style='new.TFrame')
        
        tabControl.add(self.tab1, text ='Course Data')
        tabControl.add(self.tab2, text ='Course Schema')
        tabControl.grid(row=1, column=1, sticky='nesw')
        
        ttk.Label(self.tab1, 
                text ="Welcome to Student Adviser").grid(row=2, column=1, sticky='nesw')

        ttk.Button(self.tab1, text='Load File', command=self.openFile).grid(row=1, column=2, sticky='nesw', pady=30)

        label = ttk.Label(self.tab1, text="Please select a Start Term:")
        # label.configure(background='#33BBFF')
        label.grid(row=3, column=1, pady=(20,0))

        label = ttk.Label(self.tab1, text="Please select a Start semester:")
        # label.configure(background='#33BBFF')
        label.grid(row=3, column=2, pady=(20,0))

        self.start_term = StringVar()
        self.start_term_cb = ttk.Combobox(self.tab1, textvariable=self.start_term)
        self.start_term_cb.bind("<<ComboboxSelected>>", self.set_period)

        self.start_term_cb['values'] = SEASONS
        self.start_term_cb.grid(row=4, column=1, pady=(0,20), padx=20)

        self.start_year = StringVar()
        self.start_year_cb = ttk.Combobox(self.tab1, textvariable=self.start_year)
        self.start_year_cb['values'] = [date.today().year - i for i in range(0, 5)]
        self.start_year_cb.bind("<<ComboboxSelected>>", self.set_period)
        self.start_year_cb.grid(row=4, column=2, pady=(0,20), padx=20,)

        label = ttk.Label(self.tab1, text="Please select a Course:")
        # label.configure(background='#33BBFF')
        label.grid(row=7, column=1)

        label = ttk.Label(self.tab1, text="Please select a Period:")
        # label.configure(background='#33BBFF')
        label.grid(row=7, column=2)


        label = ttk.Label(self.tab1, text="Please select a Grade:")
        # label.configure(background='#33BBFF')
        label.grid(row=7, column=3)
        
        self.course_drop_value = StringVar()
        self.course_drop = ttk.Combobox(self.tab1, textvariable=self.course_drop_value)
        self.course_drop.bind("<<ComboboxSelected>>", self.set_period)
        self.course_drop['values'] = []
        self.course_drop.grid(row=8, column=1, padx=20, pady=(0,20))
       
        self.seleted_year_term = tk.StringVar()
        self.seleted_year_term_cb = ttk.Combobox(self.tab1, textvariable=self.seleted_year_term)
        self.seleted_year_term_cb['values'] = self.get_period_options()
        self.seleted_year_term_cb.grid(row=8, column=2, sticky='nesw', pady=(0,20), padx=20)

        self.seleted_grade = tk.StringVar()
        self.seleted_grade_cb = ttk.Combobox(self.tab1, textvariable=self.seleted_grade)
        self.seleted_grade_cb['values'] = ['A', 'B', 'C', 'F']
        self.seleted_grade_cb.grid(row=8, column=3, pady=(0,20), padx=20)

        self.master.style = ttk.Style()
        #root.style.theme_use("clam")
        self.master.style.configure('TButton', background='white')
        self.master.style.configure('TButton', foreground='green')

        self.cgpa_label = ttk.Label(self.tab1, text="CGPA = " + str(self.calculate_cgpa()))
        self.cgpa_label.grid(row=9, column=1, padx=20, sticky='nesw', pady=20)

        ttk.Button(self.tab1, text='Update and Save File', command=self.complete_course).grid(row=9, column=3, padx=20, sticky='nesw', pady=20)

    def set_period(self, e):
        self.seleted_year_term_cb['values'] = self.get_period_options()

    def calculate_cgpa(self):
        cgpa= 0;
        course_count = 0
        grades = {
            "A": 4,
            "B": 3,
            "C": 2,
            "F": 0,
        }
        for course in self.file_contents:
            try:
                if grades[course[4]]:
                    cgpa = cgpa + grades[course[4]]
                    course_count = course_count+1
            except:
                pass
        if course_count > 0:
            return "{:.2f}".format(cgpa/course_count)
        return 0

    def get_period_options(self):
        completed_at = None
        if self.course_drop_value.get():
            print(self.file_contents_hash)
            try:
                completed_at = self.file_contents_hash[self.file_contents_hash[self.course_drop_value.get()]["dependent"][len(self.file_contents_hash[self.course_drop_value.get()]["dependent"]) - 1]]["completed_at"] # USE CATCH to handle DICT ERROR
            except:
                pass
                # print(e)
        if completed_at:
            print(completed_at.split(" "))
            start_term, year = completed_at.split(" ")
            year = int(year)
        else:
            year = date.today().year
            start_term = self.start_term.get()

        if start_term == 'Spring' and completed_at:
            return ['Summer ' + str(year), 'Fall ' + str(year), 'Spring ' + str(year+1)]
        elif start_term == 'Summer' and completed_at:
            return ['Fall ' + str(year), 'Spring ' + str(year+1), 'Summer ' + str(year+1)]
        elif start_term == 'Fall' and completed_at:
            return ['Spring ' + str(year+1), 'Summer ' + str(year+1), 'Fall ' + str(year+1)]

        if start_term == 'Spring':
            if self.start_year.get().isdigit() and int(self.start_year.get()) < year:
                return ['Spring ' + str(year), 'Summer ' + str(year), 'Fall ' + str(year)]
            else:
                return ['Spring ' + str(year), 'Summer ' + str(year), 'Fall ' + str(year)]
        elif start_term == 'Summer':
            if self.start_year.get().isdigit() and int(self.start_year.get()) < year:
                return ['Spring ' + str(year), 'Summer ' + str(year), 'Fall ' + str(year)]
            else:
                return ['Summer ' + str(year), 'Fall ' + str(year), 'Spring ' + str(year+1)]
        elif start_term == 'Fall':
            if self.start_year.get().isdigit() and int(self.start_year.get()) < year:
                return ['Spring ' + str(year), 'Summer ' + str(year), 'Fall ' + str(year)]
            else:
                return ['Fall ' + str(year), 'Spring ' + str(year+1), 'Summer ' + str(year+1)]
        return []

    def create_schema(self):
         self.tab2_content = ttk.Label(self.tab2,
                text =self.write_get_courses(False)).grid(row=1, column=1, sticky='nesw')
        
    def get_grade(self, course):
        if(len(course) > 4):
            return course[4]
        else:
            return ''

    def openFile(self):
        file = filedialog.askopenfile(mode='r')
        if file is not None:
            content = file.read()
            try:
                self.file_contents = content.split("\n")
                self.file_contents = [list(map(str.strip, x.split("|"))) for x in self.file_contents]
                self.file_contents_hash = {}
                for course in self.file_contents:
                    self.file_contents_hash[course[0]] = {
                        "course": course[0],
                        "grade": self.get_grade(course),
                        "dependent": self.get_dependent_courses(course),
                        "completed_at": course[3],
                        "code": course[1],
                    }
                self.course_drop['values'] = self.get_avaialbel_courses()
                self.create_schema()
            except:
                tk.messagebox.showerror(title="File Error", message="There is a problem in schema uploaded.")

    def get_dependent_courses(self, course):
        try:
            dependent = course[2].split(",")
        except Exception as e:
            print(e)
            dependent = []
            tk.messagebox.showerror(title="File Error", message="The dependent courses should be comma seperated")
        if len(dependent) == 1:
            dep_with_spaces = course[2].split(" ")
            if len(dep_with_spaces) > 1 and dep_with_spaces[len(dep_with_spaces)-1][-3].isdigit():
                return dep_with_spaces
        return dependent

    def write_get_courses(self, is_write = True):
        txt = "\n".join(["|".join(arr) for arr in self.file_contents])
        if is_write:
            file = open("studentadviser.txt","w")
            file.write(txt)
            file.close()
        else:
            return txt

    def complete_course(self):
        for i,course in enumerate(self.file_contents):
            if course[0] == self.course_drop_value.get():
                self.file_contents[i][4] = self.seleted_grade.get()
                self.file_contents[i][3] = self.seleted_year_term.get()
                self.file_contents_hash[course[0]]["grade"] = self.seleted_grade.get()
                self.file_contents_hash[course[0]]["completed_at"] = self.seleted_year_term.get()
                self.write_get_courses()
                self.course_drop['values'] = self.get_avaialbel_courses()
                self.create_schema()
                self.cgpa_label = ttk.Label(self.tab1, text="CGPA = " + str(self.calculate_cgpa())).grid(row=9, column=1, padx=20, sticky='nesw', pady=20)
                self.seleted_grade.set('')
                self.seleted_year_term.set('')
                self.course_drop_value.set('')
                return

    def get_avaialbel_courses(self):
        return [i[0] for i in filter(self.filter_courses, self.file_contents)]

    def filter_courses(self, arr):
        try:
            if arr[2] == '' and arr[4] == '':
                return True
            elif arr[2]:
                for i in self.file_contents_hash[arr[0]]["dependent"]:
                    if i and self.file_contents_hash[i]["grade"] == '' or self.file_contents_hash[i]["grade"] == 'F' or self.file_contents_hash[arr[0]]["grade"] in ['A', 'B', 'C']:
                        return False
                return True
        except:
            return True


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Student Advisor")
    root.geometry("800x500")
    root.grid_columnconfigure(4, minsize=200)  # Here
    app = StudentAdviser(root)
    root.mainloop()