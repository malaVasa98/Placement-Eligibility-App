# Import the necessary packages
from faker import Faker
import random
import mysql.connector

# Create classes to generate data using faker and random
fake = Faker()
class Student:
    student_counter = 1  # Auto-incrementing student ID

    def __init__(self):
        self.student_id = Student.student_counter  # Assign unique ID
        
        # Generate gender first
        self.gender = random.choice(["Male", "Female"])

        # Generate name based on gender
        self.first_name = fake.first_name_male() if self.gender == "Male" else fake.first_name_female()
        self.last_name = fake.last_name()
        self.name = f"{self.first_name} {self.last_name}"

        # Generate email in a realistic format
        self.email = f"{self.first_name.lower()}.{self.last_name.lower()}@{fake.free_email_domain()}"

        # Generate other attributes
        self.age = random.randint(20, 25)  # Age between 20 and 25
        self.phone = fake.phone_number()
        self.enrollment_year = random.randint(2020, 2024)  
        self.course_batch = f"Batch-{self.enrollment_year}"
        self.city = fake.city()
        self.graduation_year = self.enrollment_year + random.randint(2,4)

        Student.student_counter += 1  # Increment student ID

class Programming:
    # To maintain unique Programming IDs
    prog_ctr = 1
    def __init__(self,student_id):
        self.programming_id = Programming.prog_ctr
        # Foreign key reference to student 
        self.student_id = student_id
        self.language = random.choice(["Python", "SQL", "Java", "C++", "JavaScript"])
        self.problems_solved = random.randint(50, 500)
        self.assessments_completed = random.randint(5, 20)
        self.mini_projects = random.randint(1, 5)
        self.certifications_earned = random.randint(0, 3)
        self.latest_project_score = random.randint(50, 100)
        
        Programming.prog_ctr += 1

class Soft_Skills:
    soft_skill_ctr = 1
    def __init__(self,student_id):
        self.soft_skill_id = Soft_Skills.soft_skill_ctr
        self.student_id = student_id
        self.communication = random.randint(40,100)
        self.teamwork = random.randint(40,100)
        self.presentation = random.randint(40,100)
        self.leadership = random.randint(40,100)
        self.critical_thinking = random.randint(40,100)
        self.interpersonal_skills = random.randint(40,100)
        
        Soft_Skills.soft_skill_ctr += 1

class Placements:
    placement_ctr = 1
    def __init__(self,student_id):
        self.placement_id = Placements.placement_ctr
        self.student_id = student_id
        self.mock_interview_score = random.randint(35,100)
        self.internships_completed = random.randint(0, 3)
        self.placement_status = random.choice(['Ready','Not Ready','Placed'])
        if self.placement_status == 'Placed':
            self.company_name = fake.company()
            # Package in LPA (Lakhs Per Annum)
            self.placement_package = round(random.uniform(3, 50), 2)  
            self.placement_date = fake.date_between(start_date='-2y', end_date='today')
            self.interview_rounds_cleared = 4
        else:
            self.company_name = None
            self.placement_package = None
            self.placement_date = None
            self.interview_rounds_cleared = random.randint(0,4)
        
        Placements.placement_ctr += 1

# Establish connection with MySQL
# Use your own connection
connection = mysql.connector.connect(
            host = 'localhost',
            user='root',
            #password='',
            database='Placement_database'
)
cursor = connection.cursor()
# If Placement_database doesn't exist, use the command below to create the database
#query = "Create Database if not exists Placement_database"
#cursor.execute(query)

# Generate Students table
query = """create table if not exists Students_table(Student_id INT primary key,
                                                     Name varchar(100) not null,
                                                     Age int,
                                                     Gender varchar(100),
                                                     Email varchar(100),
                                                     Phone_number varchar(100),
                                                     Enrollment_year varchar(100),
                                                     Course_batch varchar(100),
                                                     City varchar(100),
                                                     Graduation_year int)"""
cursor.execute(query)
query = "Insert into Students_table values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
stud_data = []
stud_id = []
query = "Insert into Students_table values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
stud_data = []
stud_id = []
for i in range(1000):
    student = Student()
    stud_id.append(student.student_id)
    gender = student.gender
    fn = student.first_name
    ln = student.last_name
    tup_stud = (student.student_id,
                student.name,
                student.age,
                gender,
                student.email,
                student.phone,
                student.enrollment_year,
                student.course_batch,
                student.city,
                student.graduation_year)
    stud_data.append(tup_stud)
cursor.executemany(query,stud_data)
connection.commit()

# Generate Programming Table
query = """create table if not exists Programming_table(Programming_id int primary key,
                                                        Student_id int,
                                                        foreign key(Student_id) references Students_table(Student_id),
                                                        Language varchar(100),
                                                        Problems_solved int,
                                                        Assessments_completed int,
                                                        Mini_projects int,
                                                        Certifications_earned int,
                                                        Latest_project_score int)"""
cursor.execute(query)
query = """insert into Programming_table values(%s,%s,%s,%s,%s,%s,%s,%s)"""
prog_data = []
for i in range(1000):
    prog = Programming(stud_id[i])
    tup = (prog.programming_id,
           prog.student_id,
           prog.language,
           prog.problems_solved,
           prog.assessments_completed,
           prog.mini_projects,
           prog.certifications_earned,
           prog.latest_project_score)
    prog_data.append(tup)
cursor.executemany(query,prog_data)
connection.commit()

# Generate Soft Skills Table
query = """create table if not exists Soft_Skills_table(Soft_skill_id int primary key,
                                                        Student_id int,
                                                        foreign key(Student_id) references Students_table(student_id),
                                                        Communication int,
                                                        Teamwork int,
                                                        Presentation int,
                                                        Leadership int,
                                                        Critical_thinking int,
                                                        Interpersonal_skills int)"""
cursor.execute(query)
query = "insert into soft_skills_table values(%s,%s,%s,%s,%s,%s,%s,%s)"
soft_sk_data = []
for i in range(1000):
    sfsk = Soft_Skills(stud_id[i])
    tup = (sfsk.soft_skill_id,
           sfsk.student_id,
           sfsk.communication,
           sfsk.teamwork,
           sfsk.presentation,
           sfsk.leadership,
           sfsk.critical_thinking,
           sfsk.interpersonal_skills)
    soft_sk_data.append(tup)
cursor.executemany(query,soft_sk_data)
connection.commit()

# Generate Placements table
query = """create table if not exists Placements_table(Placement_id int primary key,
                                                       Student_id int,
                                                       foreign key(Student_id) references Students_table(student_id),
                                                       Mock_interview_score int,
                                                       Internships_completed int,
                                                       Placement_status varchar(100),
                                                       Company_name varchar(100),
                                                       Placement_package_in_LPA float,
                                                       Placement_date date,
                                                       Interview_rounds_cleared int)"""
cursor.execute(query)
query = "insert into placements_table values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
plac_data = []
for i in range(1000):
    place = Placements(stud_id[i])
    tup = (place.placement_id,
           place.student_id,
           place.mock_interview_score,
           place.internships_completed,
           place.placement_status,
           place.company_name,
           place.placement_package,
           place.placement_date,
           place.interview_rounds_cleared)
    plac_data.append(tup)
cursor.executemany(query,plac_data)
connection.commit()

# Close the connection after saving changes
cursor.close()
connection.close()
        
