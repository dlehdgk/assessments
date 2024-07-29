import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data (you can replace these with your actual data)
students = [
    "Freddie", "Elliot", "Lee", "Seoyeong", "Daeun",
    "Sungjae", "Youngjae", "Jay", "Yunjeong", "Young",
    "Taeun", "Benji"
]

# Define questions and their parts with the total marks for each part
questions = {
    "Q1": {"a": 2, "b": 2, "c":2},
    "Q2": {"a": 3, "b": 4},
    "Q3": {"a": 3, "b": 3},
    "Q4": {"a": 3,"b":3,"c":3},
    "Q5": {"a": 2, "b": 3,"c":3,"d":2},
    "Q6": {"a": 5, "b": 4},
    "Q7": {"a": 4, "b": 4},
    "Q8": {"a": 3, "b":4, "c":3},
    "Q9": {"a": 1, "b": 6, "c":3}
}

# Define marks for each student and each part of each question
# You can manually input these marks or use any method to fill them in
marks_data = {
    "Freddie": {"Q1_a": 2, "Q1_b": 1, "Q1_c": 0, "Q2_a": 2, "Q2_b": 0, "Q3_a": 3, "Q3_b": 3, "Q4_a": 1, "Q4_b": 3, "Q4_c": 0, "Q5_a": 2, "Q5_b": 3, "Q5_c": 3, "Q5_d": 0, "Q6_a": 3, "Q6_b": 0, "Q7_a": 3, "Q7_b": 0, "Q8_a": 3, "Q8_b": 0,"Q8_c": 0,"Q9_a": 1, "Q9_b": 2, "Q9_c": 0, "Finish_Time": 85},
    "Elliot": {"Q1_a": 2, "Q1_b": 2, "Q1_c": 2, "Q2_a": 3, "Q2_b": 4, "Q3_a": 3, "Q3_b": 3, "Q4_a": 3, "Q4_b": 1, "Q4_c": 3, "Q5_a": 2, "Q5_b": 3, "Q5_c": 0, "Q5_d": 0, "Q6_a": 5, "Q6_b": 4, "Q7_a": 4, "Q7_b": 4, "Q8_a": 3, "Q8_b": 4,"Q8_c": 2,"Q9_a": 1, "Q9_b": 6, "Q9_c": 3, "Finish_Time": 90},
    "Lee": {"Q1_a": 2, "Q1_b": 2, "Q1_c": 2, "Q2_a": 3, "Q2_b": 4, "Q3_a": 3, "Q3_b": 3, "Q4_a": 3, "Q4_b": 3, "Q4_c": 3, "Q5_a": 2, "Q5_b": 3, "Q5_c": 3, "Q5_d": 2, "Q6_a": 5, "Q6_b": 4, "Q7_a": 4, "Q7_b": 4, "Q8_a": 3, "Q8_b": 4,"Q8_c": 2,"Q9_a": 1, "Q9_b": 6, "Q9_c": 3, "Finish_Time": 88},
    "Seoyeong": {"Q1_a": 2, "Q1_b": 2, "Q1_c": 0, "Q2_a": 3, "Q2_b": 2, "Q3_a": 1, "Q3_b": 3, "Q4_a": 2, "Q4_b": 2, "Q4_c": 1, "Q5_a": 2, "Q5_b": 3, "Q5_c": 2, "Q5_d": 0, "Q6_a": 5, "Q6_b": 2, "Q7_a": 4, "Q7_b": 0, "Q8_a": 3, "Q8_b": 0,"Q8_c": 2,"Q9_a": 1, "Q9_b": 0, "Q9_c": 0, "Finish_Time": 90},
    "Daeun": {"Q1_a": 2, "Q1_b": 2, "Q1_c": 2, "Q2_a": 3, "Q2_b": 4, "Q3_a": 3, "Q3_b": 3, "Q4_a": 3, "Q4_b": 3, "Q4_c": 3, "Q5_a": 2, "Q5_b": 3, "Q5_c": 2, "Q5_d": 0, "Q6_a": 4, "Q6_b": 4, "Q7_a": 4, "Q7_b": 4, "Q8_a": 0, "Q8_b": 3,"Q8_c": 0,"Q9_a": 0, "Q9_b": 0, "Q9_c": 0, "Finish_Time": 90},
    "Sungjae": {"Q1_a": 2, "Q1_b": 2, "Q1_c": 0, "Q2_a": 3, "Q2_b": 3, "Q3_a": 0, "Q3_b": 1, "Q4_a": 3, "Q4_b": 1, "Q4_c": 0, "Q5_a": 0, "Q5_b": 3, "Q5_c": 2, "Q5_d": 0, "Q6_a": 5, "Q6_b": 4, "Q7_a": 4, "Q7_b": 0, "Q8_a": 3, "Q8_b": 4,"Q8_c": 2,"Q9_a": 0, "Q9_b": 0, "Q9_c": 3, "Finish_Time": 90},
    "Youngjae": {"Q1_a": 2, "Q1_b": 0, "Q1_c": 0, "Q2_a": 3, "Q2_b": 0, "Q3_a": 0, "Q3_b": 0, "Q4_a": 0, "Q4_b": 0, "Q4_c": 0, "Q5_a": 0, "Q5_b": 0, "Q5_c": 0, "Q5_d": 0, "Q6_a": 0, "Q6_b": 0, "Q7_a": 0, "Q7_b": 0, "Q8_a": 0, "Q8_b": 0,"Q8_c": 0,"Q9_a": 0, "Q9_b": 0, "Q9_c": 0, "Finish_Time": 60},
    "Jay": {"Q1_a": 2, "Q1_b": 2, "Q1_c": 2, "Q2_a": 3, "Q2_b": 3, "Q3_a": 2, "Q3_b": 3, "Q4_a": 3, "Q4_b": 3, "Q4_c": 1, "Q5_a": 2, "Q5_b": 3, "Q5_c": 2, "Q5_d": 0, "Q6_a": 5, "Q6_b": 2, "Q7_a": 4, "Q7_b": 3, "Q8_a": 3, "Q8_b": 0,"Q8_c": 2,"Q9_a": 1, "Q9_b": 0, "Q9_c": 0, "Finish_Time": 90},
    "Yunjeong": {"Q1_a": 2, "Q1_b": 2, "Q1_c": 2, "Q2_a": 2, "Q2_b": 1, "Q3_a": 3, "Q3_b": 3, "Q4_a": 3, "Q4_b": 1, "Q4_c": 3, "Q5_a": 2, "Q5_b": 3, "Q5_c": 2, "Q5_d": 0, "Q6_a": 5, "Q6_b": 2, "Q7_a": 4, "Q7_b": 3, "Q8_a": 2, "Q8_b": 4,"Q8_c": 2,"Q9_a": 1, "Q9_b": 6, "Q9_c": 3, "Finish_Time": 80},
    "Young": {"Q1_a": 0, "Q1_b": 0, "Q1_c": 0, "Q2_a": 0, "Q2_b": 0, "Q3_a": 0, "Q3_b": 0, "Q4_a": 0, "Q4_b": 0, "Q4_c": 0, "Q5_a": 0, "Q5_b": 1, "Q5_c": 1, "Q5_d": 0, "Q6_a": 0, "Q6_b": 0, "Q7_a": 0, "Q7_b": 0, "Q8_a": 0, "Q8_b": 0,"Q8_c": 0,"Q9_a": 0, "Q9_b": 0, "Q9_c": 0, "Finish_Time": 25},
    "Taeun": {"Q1_a": 2, "Q1_b": 2, "Q1_c": 0, "Q2_a": 3, "Q2_b": 1, "Q3_a": 3, "Q3_b": 3, "Q4_a": 0, "Q4_b": 0, "Q4_c": 0, "Q5_a": 0, "Q5_b": 3, "Q5_c": 2, "Q5_d": 0, "Q6_a": 5, "Q6_b": 0, "Q7_a": 0, "Q7_b": 0, "Q8_a": 3, "Q8_b": 0,"Q8_c": 2,"Q9_a": 1, "Q9_b": 0, "Q9_c": 0, "Finish_Time": 35},
    "Benji": {"Q1_a": 2, "Q1_b": 2, "Q1_c": 2, "Q2_a": 3, "Q2_b": 3, "Q3_a": 0, "Q3_b": 2, "Q4_a": 2, "Q4_b": 0, "Q4_c": 0, "Q5_a": 0, "Q5_b": 3, "Q5_c": 2, "Q5_d": 0, "Q6_a": 5, "Q6_b": 2, "Q7_a": 4, "Q7_b": 2, "Q8_a": 3, "Q8_b": 0,"Q8_c": 2,"Q9_a": 1, "Q9_b": 0, "Q9_c": 2, "Finish_Time": 90},
    # Add more students similarly
}

# Create a DataFrame
columns = ["Student"] + [f"{q}_{p}" for q in questions for p in questions[q]] + ["Finish_Time"]
df = pd.DataFrame(columns=columns)

# Fill in the DataFrame with the marks data
rows = []
for student in students:
    if student in marks_data:
        student_data = marks_data[student]
        row = {"Student": student, **student_data}
        rows.append(row)
df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

# Calculate total marks for each question and add to DataFrame
for question, parts in questions.items():
    part_columns = [f"{question}_{part}" for part in parts]
    df[f"{question}_Total"] = df[part_columns].sum(axis=1)

# Calculate overall total marks for each student
df["Total_Marks"] = df[[f"{question}_Total" for question in questions]].sum(axis=1)

# Save to CSV
file_path = 'Exam_Results.csv'
df.to_csv(file_path, index=False)

# Display the DataFrame
print(df)
