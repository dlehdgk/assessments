import pandas as pd
import numpy as np

class Test:
    def __init__(self, filename, parts=True):
        self.__filename = filename
        self.__parts = parts
        self.__df = pd.read_csv(self.__filename)
        
        # Separate total marks row from student marks
        self.__total = self.__df[self.__df["Name"] == "Total"].copy()
        self.mark_table = self.__df[self.__df["Name"] != "Total"].copy()
        
        # Initialize additional dataframes and variables
        self.norm_table = None
        question_cols = [col for col in self.mark_table.columns if col.startswith("Q")]
        
        # Determine question numbers based on the presence of parts
        if self.__parts:
            self.__question_nos = sorted(set(col.split("_")[0] for col in question_cols))
        else:
            self.__question_nos = question_cols
        
        # Calculate total marks available for each question part and overall total
        total_marks = {}
        for q_num in self.__question_nos:
            question_parts = [col for col in self.__total.columns if col.startswith(q_num)]
            self.__total.loc[:, q_num + "_Total"] = self.__total[question_parts].sum(axis=1).sum()
            for part in question_parts:
                total_marks[part] = self.__total[part].values[0]
            total_marks[q_num + "_Total"] = self.__total[q_num + "_Total"].values[0]
        
        total_marks["Total"] = self.__total.filter(like="_Total").sum(axis=1).values[0]
        
        # Store available marks in a dataframe
        self.available_marks = pd.DataFrame(list(total_marks.items()), columns=["Question", "Marks_Available"])

    def add_total_mark(self):
        # Adding total marks per question and overall total to mark_table
        question_cols = [col for col in self.mark_table.columns if col.startswith("Q")]
        
        if self.__parts:
            for q_num in self.__question_nos:
                question_parts = [col for col in self.mark_table.columns if col.startswith(q_num)]
                self.mark_table[q_num + "_Total"] = self.mark_table[question_parts].sum(axis=1)
            total_cols = [col for col in self.mark_table.columns if col.endswith("_Total")]
            self.mark_table["Total"] = self.mark_table[total_cols].sum(axis=1)
        else:
            self.__question_nos = question_cols
            self.mark_table["Total"] = self.mark_table[self.__question_nos].sum(axis=1)
        
        return self

    def get_total_marks(self):
        if self.__parts:
            columns = ["Name"] + [q + "_Total" for q in self.__question_nos] + ["Total"]
            mt = self.add_total_mark().mark_table
            total = mt.loc[:, columns]
        else:
            total = self.add_total_mark().mark_table
        return total

    def marks(self, norm=False):
        df = self.mark_table
        if norm:
            df = self.normalise_marks().norm_table
        if self.__parts:
            df_melted = df.melt(id_vars=["Name"], var_name="Question_Part", value_name="Mark")
            df_melted[["Question", "Part"]] = df_melted["Question_Part"].str.split("_", expand=True)
            df_melted = df_melted.drop(columns=["Question_Part"])
            marks_df = df_melted[["Name", "Question", "Part", "Mark"]]
        else:
            df_melted = df.melt(id_vars=["Name"], var_name="Question", value_name="Mark")
            marks_df = df_melted[["Name", "Question", "Mark"]]
        return marks_df

    def normalise_marks(self):
        self.norm_table = self.mark_table.copy()
        for q_num in self.__question_nos:
            question_parts = [col for col in self.norm_table.columns if col.startswith(q_num)]
            for part in question_parts:
                self.norm_table[part] = self.norm_table[part] / self.available_marks[self.available_marks["Question"] == part]["Marks_Available"].values[0]
            total_column_name = q_num + "_Total"
            if total_column_name in self.norm_table.columns:
                self.norm_table[total_column_name] = self.norm_table[total_column_name] / self.available_marks[self.available_marks["Question"] == total_column_name]["Marks_Available"].values[0]
        if "Total" in self.norm_table.columns:
            self.norm_table["Total"] = self.mark_table["Total"] / self.available_marks[self.available_marks["Question"] == "Total"]["Marks_Available"].values[0]
        return self

# Example usage
p3_mock = Test("example.csv")
print(p3_mock.marks(norm=False))