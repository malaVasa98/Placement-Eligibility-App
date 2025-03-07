# Importing the necessary packages
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
st.markdown(
    """
    <style>
    .centered-title {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 48px;
        font-weight: bold;
        color: blue;
    }
    </style>
    <div class="centered-title">PLACEMENT ELIGIBILITY APP</div>
    """,
    unsafe_allow_html=True
)
with st.sidebar:
    selected = option_menu("Menu",["About","Eligible for Placement","SQL Queries and Insights"])
    
if selected=='About':
    st.write("This app focuses on the eligibility criteria for placement. The app has two sections: Eligible for Placement, and SQL Queries and Insights. In the 'Eligible for Placement' section, the user gets the students' data eligible for placement based on the filters provided. Some sql queries are performed and insights can be observed in the 'SQL Queries and Insights' section.")
    
# Establish connection with MySQL
# Use your own connection
connection = mysql.connector.connect(
            host = 'localhost',
            user='root',
            #password='',
            database='Placement_database'
)
cursor = connection.cursor()
#cursor.close()
#connection.close()

if selected == 'SQL Queries and Insights':
    sql_qns = {
                "Q1":"What are the total number of students enrolled in each year?",
                "Q2":"""Display the student names along with their programming performance 
                        and rank the students based on the problems solved in each language.""",
                "Q3":"""Display the students along with their soft skill scores who have high leadership and communication skills""",
                "Q4":'Who are the students who got placed before 2024?',
                "Q5":'Display the students who cleared more than 2 interview rounds and their placement status.',
                "Q6":'What are the top 5 highest placement packages obtained by the students of each batch?',
                "Q7":'Which students have both high soft skills and strong programming skills?',
                "Q8":'What is the placement status and mock interview score of the students who have cleared atleast 2 internships?',
                "Q9":'What is the most common programming among students?',
                "Q10":'''Which students are not yet placed?
                         Also, display their certifications earned, latest project score and mock interview score.'''
              }
    option = st.selectbox("Select an SQL query",tuple(sql_qns.values()),index=None)
    if option==sql_qns["Q1"]:
        query = """select enrollment_year, count(*) as count
           from students_table
           group by enrollment_year order by enrollment_year"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query1 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query1)
    if option==sql_qns["Q2"]:
        query = """SELECT 
                    s.name, 
                    p.language, 
                    p.Problems_solved, 
                    p.assessments_completed, 
                    p.mini_projects, 
                    p.certifications_earned, 
                    p.latest_project_score, 
                    RANK() OVER (PARTITION BY p.language ORDER BY p.problems_solved DESC) AS `rank`
                  FROM students_table s
                  JOIN programming_table p ON s.student_id = p.student_id
                  ORDER BY p.language, `rank`;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query2 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query2)
    if option == sql_qns["Q3"]:
        query = """select 
            s.name,
            sk.communication,
            sk.leadership,
            sk.teamwork,
            sk.presentation,
            sk.critical_thinking,
            sk.interpersonal_skills
           from students_table s
           join soft_skills_table sk on s.student_id = sk.student_id
           where sk.communication > 80 and sk.leadership > 80;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query3 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query3)
        df_query33 = df_query3.drop('name',axis=1)
        selected_skill = st.selectbox("Select a skill to visualise:",tuple(df_query33.columns),index=None)
        if selected_skill!=None:
            fig, ax = plt.subplots()
            ax.hist(df_query3[selected_skill], bins=10, color="red", edgecolor="black")
            ax.set_xlabel(selected_skill.replace('_',' ') if '_' in selected_skill else selected_skill)
            ax.set_ylabel("Frequency")
            ax.set_title(f"Histogram of {selected_skill.replace('_',' ') if '_' in selected_skill else selected_skill}")
            st.pyplot(fig)
    if option == sql_qns["Q4"]:
        query = """select
            s.name,
            s.email,
            s.course_batch,
            s.phone_number,
            s.city,
            p.placement_date,
            p.Placement_package_in_LPA
           from students_table s
           join placements_table p on s.student_id = p.student_id
           where YEAR(placement_date)<2024 and s.enrollment_year<=2022;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query4 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query4)
    if option == sql_qns["Q5"]:
        query = """select
             s.name,
             p.interview_rounds_cleared,
             p.placement_status
           from students_table s
           join placements_table p on s.student_id = p.student_id
           where p.interview_rounds_cleared > 2"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query5 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query5)
        query = """select place_table.placement_status, count(*) as Count
            from
            (select
             s.name,
             p.interview_rounds_cleared,
             p.placement_status
           from students_table s
           join placements_table p on s.student_id = p.student_id
           where p.interview_rounds_cleared > 2) as place_table
           group by place_table.placement_status"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query51 = pd.DataFrame(rows,columns=cols)
        fig, ax = plt.subplots()
        sns.barplot(x="placement_status", y="Count", data=df_query51, ax=ax, palette="rocket")
        ax.set_xlabel('Placement Status')
        st.pyplot(fig)
    if option==sql_qns["Q6"]:
        query = """WITH Ranked_Placements as (select 
            s.name,
            s.Course_batch,
            p.placement_package_in_LPA,
            RANK() OVER(PARTITION BY s.Course_batch ORDER BY p.placement_package_in_LPA desc) as `rank`
           from students_table s
           join placements_table p on s.student_id = p.student_id 
           where p.placement_status = 'Placed')
           select name,course_batch,placement_package_in_LPA
           from Ranked_Placements
           where `rank`<=5;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query6 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query6)
        df_query61 = df_query6.groupby('course_batch')['placement_package_in_LPA'].mean()
        df_query61 = pd.DataFrame(df_query61)
        df_query61.reset_index(inplace=True)
        fig = px.bar(df_query61,
                     x="course_batch",
                     y="placement_package_in_LPA",
                     title="Average of top 5 highest placement pacakges",
                     labels={"course_batch":"Course batch","placement_package_in_LPA": "Average Placement Package (LPA)"})
        st.plotly_chart(fig)
    if option==sql_qns["Q7"]:
        query = """select s.name
           from students_table s
           join soft_skills_table sk on s.student_id = sk.student_id
           join programming_table p on s.student_id = p.student_id
           where (sk.communication + sk.teamwork + sk.presentation + sk.leadership + sk.critical_thinking + sk.interpersonal_skills)/6 > 75
           and p.problems_solved > 60;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query7 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query7)
    if option==sql_qns["Q8"]:
        query = """select
            s.name,
            p.placement_status,
            p.mock_interview_score
           from students_table s
           join placements_table p on s.student_id = p.student_id
           where p.Internships_completed >=2;"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query8 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query8)
    if option==sql_qns["Q9"]:
        query = "select language, COUNT(*) as count from programming_table group by language;"
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query9 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query9)
        fig, ax = plt.subplots()
        ax.bar(df_query9['language'],df_query9['count'],color='blue')
        ax.set_xlabel('Programming Language')
        ax.set_ylabel('Count')
        st.pyplot(fig)
    if option==sql_qns["Q10"]:
        query =  """select s.name,s.email,p.placement_status,pp.certifications_earned,
           pp.Latest_project_score, p.mock_interview_score
           from students_table s
           join placements_table p on s.student_id = p.student_id
           join programming_table pp on s.student_id = p.student_id
           where p.placement_status != 'Placed'"""
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [x[0] for x in cursor.description]
        df_query10 = pd.DataFrame(rows,columns=cols)
        st.dataframe(df_query10)
        selected_opt = st.selectbox("Select a skill to visualise:",tuple(df_query10[['placement_status','certifications_earned','Latest_project_score','mock_interview_score']].columns),index=None)
        if selected_opt!=None:
            if selected_opt!='placement_status':
                fig, ax = plt.subplots()
                ax.hist(df_query10[selected_opt], bins=10, color="#42F135", edgecolor="black")
                ax.set_xlabel(selected_opt.replace('_',' '))
                ax.set_ylabel("Frequency")
                ax.set_title(f"Histogram of {selected_opt.replace('_',' ')}")
                st.pyplot(fig)
            else:
                df_query100 = df_query10.groupby('placement_status')['placement_status'].count()
                df_query100 = pd.DataFrame(df_query100)
                df_query100.rename(columns={'placement_status':'Frequency'},inplace=True)
                df_query100.reset_index(inplace=True)
                fig, ax = plt.subplots()
                sns.barplot(x="placement_status", y="Frequency", data=df_query100, ax=ax, palette="deep")
                ax.set_xlabel('Placement Status')
                st.pyplot(fig)

if selected == "Eligible for Placement":
    # Get Students table
    query = "select * from students_table"
    cursor.execute(query)
    rows = cursor.fetchall()
    col = [x[0] for x in cursor.description]
    df_students_table = pd.DataFrame(rows,columns=col)
    
    # Get Programming table
    query = "select * from programming_table"
    cursor.execute(query)
    rows = cursor.fetchall()
    col = [x[0] for x in cursor.description]
    df_programming_table = pd.DataFrame(rows,columns=col)
    
    # Get Soft Skills Table
    query = "select * from soft_skills_table"
    cursor.execute(query)
    rows = cursor.fetchall()
    col = [x[0] for x in cursor.description]
    df_soft_skills_table = pd.DataFrame(rows,columns=col)
    # Add a column for average score
    df_soft_skills_table['Average_soft_skill_score'] = (df_soft_skills_table['Communication'] + df_soft_skills_table['Teamwork'] + df_soft_skills_table['Presentation'] + df_soft_skills_table['Leadership'] + df_soft_skills_table['Critical_thinking'] + df_soft_skills_table['Interpersonal_skills'])/6 
    df_soft_skills_table['Average_soft_skill_score'] = round(df_soft_skills_table['Average_soft_skill_score'],2)
    
    # Get Placements Table
    query = "select * from placements_table"
    cursor.execute(query)
    rows = cursor.fetchall()
    col = [x[0] for x in cursor.description]
    df_placements_table = pd.DataFrame(rows,columns=col)
    
    merged_df = df_students_table.merge(df_programming_table,on='Student_id',how='inner').merge(df_soft_skills_table,on='Student_id',how='inner').merge(df_placements_table,on='Student_id',how='inner')
    col1, col2 = st.columns(2)
    with col1:
        pbms_solved = st.slider('Problems Solved',10,500,key='pbm')
        mini_proj = st.slider('Mini Projects',1,5,key='mini')
        cert = st.slider('Certifications Earned',0,3,key='certi')
        lat_proj = st.slider('Latest Project Score',40,100,key='proj')
        languages = df_programming_table['Language'].unique().tolist()
        lan = st.multiselect("Language",languages)
    with col2:
        min_sk = df_soft_skills_table['Average_soft_skill_score'].min()
        max_sk =  df_soft_skills_table['Average_soft_skill_score'].max()
        mskc = st.slider('Average Soft Skills Score',int(min_sk)-1,int(max_sk),key='soft')
        mock = st.slider('Mock Interview Score',30,100,key='mock')
        intern = st.slider('Internships Completed',0,3,key='intern')
        interview = st.slider('Interview Rounds Cleared',0,4,key='interv')
        pc = df_placements_table['Placement_status'].unique().tolist()
        place = st.selectbox('Placement Status',tuple(pc),index=None)
    
    if lan!=[] and place!=None and st.button('Get Students'):
        cond1 = merged_df['Language'].isin(lan)
        cond2 = merged_df['Problems_solved'] >= pbms_solved
        cond3 = merged_df['Mini_projects']>=mini_proj
        cond4 = merged_df['Certifications_earned']>=cert
        cond5 = merged_df['Latest_project_score']>=lat_proj
        cond6 = merged_df['Average_soft_skill_score']>=mskc
        cond7 = merged_df['Mock_interview_score']>=mock
        cond8 = merged_df['Internships_completed']>=intern
        cond9 = merged_df['Interview_rounds_cleared']>=interview
        cond10 = merged_df['Placement_status'] == place
        stud_df = merged_df[(cond1)&(cond2)&(cond3)&(cond4)&(cond5)&(cond6)&(cond7)&(cond8)&(cond9)&(cond10)]
        eligible_students = stud_df[['Name','Age','Gender','Email','Phone_number','City','Language']]
        if stud_df.empty:
            st.write('No Data Available')
        else:
            st.dataframe(eligible_students)
       
        