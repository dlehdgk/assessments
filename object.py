import pandas as pd
import numpy as np


class Test:
    def __init__(self, filename, parts=True):
        self.__filename = filename
        self.__parts = parts
        self.__df = pd.read_csv(self.__filename)
        # dataframe of the marks available in the exam per question part
        self.__total = self.__df.loc[self.__df["Name"] == "Total"]
        # dataframe of only the total marks per question + overall marks
        self.norm_table = None
        # dataframe of marks in the form of a usual table
        self.mark_table = self.__df[self.__df["Name"] != "Total"]
        # adding columns for total marks per question and total mark for exam
        question_cols = [col for col in self.mark_table.columns if col.startswith("Q")]
        if self.__parts == True:
            # Extract unique question numbers
            self.__question_nos = sorted(
                set(col.split("_")[0] for col in question_cols)
            )
        else:
            self.__question_nos = question_cols

        # extracting marks per questions by summing over parts per question
        total_marks = {}
        for q_num in self.__question_nos:
            question_parts = [
                col for col in self.__total.columns if col.startswith(q_num)
            ]
            self.__total[q_num + "Total"] = (
                self.__total[question_parts].sum(axis=1).sum()
            )
        total_marks["Total"] = sum(
            self.__total[self.__total.columns.str.contains("Total")].values()
        )
        self.available_marks = pd.DataFrame(
            list(total_marks.items()), columns=["Question", "Marks_Available"]
        )
        # print(self.available_marks)

    def add_total_mark(self):
        # adding columns for total marks per question and total mark for exam
        question_cols = [col for col in self.mark_table.columns if col.startswith("Q")]
        # print(question_cols)
        if self.__parts == True:
            # want to add columns for the total marks per question and the total mark to the mark table
            # Extract unique question numbers
            self.__question_nos = sorted(
                set(col.split("_")[0] for col in question_cols)
            )
            # print(question_numbers)
            # Sum marks for each question
            for q_num in self.__question_nos:
                question_parts = [
                    col for col in self.mark_table.columns if col.startswith(q_num)
                ]
                self.mark_table[q_num + "_Total"] = self.mark_table[question_parts].sum(
                    axis=1
                )

            # Add a new column with total marks for each student
            total_cols = [
                col for col in self.mark_table.columns if col.endswith("_Total")
            ]
            self.mark_table["Total"] = self.mark_table[total_cols].sum(axis=1)
        else:
            # Add a new column with total marks for each student
            self.__question_nos = question_cols
            self.mark_table["Total"] = self.mark_table[self.__question_nos].sum(axis=1)
        return self

    # return dataframe for total marks so that it turns into a dataframe containing only the total marks for each question and total
    def get_total_marks(self):
        # print(self.__question_nos)
        if self.__parts == True:
            columns = ["Name"] + [q + "_Total" for q in self.__question_nos] + ["Total"]
            mt = self.add_total_mark().mark_table
            total = mt.loc[:, columns]
        else:
            total = self.add_total_mark().mark_table
        return total

    # melt marks to dataframe suitable for seaborn plotting
    def marks(self, norm=False):
        df = self.mark_table
        if norm == True:
            df = self.normalise_marks().norm_table
        else:
            df = self.mark_table
        # if the database contains questions and parts of questions divide them separately
        if self.__parts == True:
            df_melted = df.melt(
                id_vars=["Name"], var_name="Question_Part", value_name="Mark"
            )
            df_melted[["Question", "Part"]] = df_melted["Question_Part"].str.split(
                "_", expand=True
            )
            df_melted = df_melted.drop(columns=["Question_Part"])
            marks_df = df_melted[["Name", "Question", "Part", "Mark"]]
        else:
            df_melted = df.melt(
                id_vars=["Name"], var_name="Question", value_name="Mark"
            )
            marks_df = df_melted[["Name", "Question", "Mark"]]
        return marks_df

    def normalise_marks(self):
        # Create a copy of the mark table for normalisation
        self.norm_table = self.mark_table.copy()
        for q_num in self.__total.columns:
            if "Q" in q_num:
                self.norm_table[q_num] = self.norm_table[q_num] / self.__total[q_num]
        if col in self.norm_table.columns == "Total":
            self.norm_table[col] = (
                self.mark_table[col] / self.available_marks["Marks_Available"].iloc[-1]
            )

        return self

