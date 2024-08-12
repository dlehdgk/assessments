import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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
        self.total_marks_table = None  # New dataframe to store total marks
        self.norm_total = None  # New dataframe to store normalized total marks
        question_cols = [col for col in self.mark_table.columns if col.startswith("Q")]

        # Determine question numbers based on the presence of parts
        if self.__parts:
            self.__question_nos = sorted(
                set(col.split("_")[0] for col in question_cols)
            )
        else:
            self.__question_nos = question_cols

        # Calculate total marks available for each question part and overall total
        total_marks = {}
        for q_num in self.__question_nos:
            question_parts = [
                col for col in self.__total.columns if col.startswith(q_num)
            ]
            q_total = self.__total[question_parts].sum(axis=1).sum()
            total_marks[q_num + "_Total"] = q_total
            self.__total[q_num + "_Total"] = q_total

            for part in question_parts:
                total_marks[part] = self.__total[part].values[0]

        total_marks["Total"] = self.__total.filter(like="_Total").sum(axis=1).values[0]

        # Store available marks in a dataframe
        self.available_marks = pd.DataFrame(
            list(total_marks.items()), columns=["Question", "Marks_Available"]
        )

        # Initialize total_marks_table with total marks
        self._initialize_total_marks_table()

        # Normalize the total marks table
        self._initialize_norm_total()

    def _initialize_total_marks_table(self):
        if self.__parts:
            columns = ["Name"] + [q + "_Total" for q in self.__question_nos] + ["Total"]
            self.total_marks_table = self.mark_table.copy()
            for q_num in self.__question_nos:
                question_parts = [
                    col for col in self.mark_table.columns if col.startswith(q_num)
                ]
                self.total_marks_table[q_num + "_Total"] = self.mark_table[
                    question_parts
                ].sum(axis=1)

            # Add a new column with total marks for each student
            total_cols = [q + "_Total" for q in self.__question_nos]
            self.total_marks_table["Total"] = self.total_marks_table[total_cols].sum(
                axis=1
            )
            self.total_marks_table = self.total_marks_table.loc[:, columns]
        else:
            self.total_marks_table = self.mark_table.copy()
            self.total_marks_table["Total"] = self.total_marks_table[
                self.__question_nos
            ].sum(axis=1)

    def _initialize_norm_total(self):
        # Create a normalized version of the total_marks_table
        self.norm_total = self.total_marks_table.copy()

        for q_num in self.__question_nos:
            total_column = q_num + "_Total"
            max_marks = self.available_marks[
                self.available_marks["Question"] == total_column
            ]["Marks_Available"].values[0]

            # Normalize each question total
            self.norm_total[total_column] = self.norm_total[total_column] / max_marks

        # Normalize the overall total
        total_max_marks = self.available_marks[
            self.available_marks["Question"] == "Total"
        ]["Marks_Available"].values[0]
        self.norm_total["Total"] = self.norm_total["Total"] / total_max_marks

    def marks(self, norm=False, to_one=False):
        df = self.mark_table
        if norm:
            df = self.normalise_marks(to_one=to_one).norm_table
        if self.__parts:
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

    def normalise_marks(self, to_one=False):
        self.norm_table = self.mark_table.copy()
        for q_num in self.__question_nos:
            question_parts = [
                col for col in self.norm_table.columns if col.startswith(q_num)
            ]
            if to_one:
                total_max_marks = self.available_marks[
                    self.available_marks["Question"] == q_num + "_Total"
                ]["Marks_Available"].values[0]
                for part in question_parts:
                    self.norm_table[part] = self.norm_table[part] / total_max_marks
            else:
                for part in question_parts:
                    self.norm_table[part] = (
                        self.norm_table[part]
                        / self.available_marks[
                            self.available_marks["Question"] == part
                        ]["Marks_Available"].values[0]
                    )
            total_column_name = q_num + "_Total"
            if total_column_name in self.norm_table.columns:
                self.norm_table[total_column_name] = (
                    self.norm_table[total_column_name]
                    / self.available_marks[
                        self.available_marks["Question"] == total_column_name
                    ]["Marks_Available"].values[0]
                )
        if "Total" in self.norm_table.columns:
            self.norm_table["Total"] = (
                self.norm_table["Total"]
                / self.available_marks[self.available_marks["Question"] == "Total"][
                    "Marks_Available"
                ].values[0]
            )
        return self

    def total_marks_analysis(self, file_path):
        # Create a figure with subplots
        fig, axes = plt.subplots(3, 1, figsize=(14, 18))
        plt.subplots_adjust(hspace=0.5)

        # Plot 1: Heatmap of Student Scores
        heatmap_data = self.mark_table.set_index("Name")
        sns.heatmap(
            heatmap_data, annot=True, cmap="coolwarm", linewidths=0.5, ax=axes[0]
        )
        axes[0].set_title("Heatmap of Student Scores")

        # Plot 2: Annotated Histogram of Total Marks
        hist = sns.histplot(data=self.norm_total, x="Total", kde=True, ax=axes[1])
        mean_total = np.mean(self.norm_total["Total"])
        std_total = np.std(self.norm_total["Total"])
        data = f"mean: {mean_total:.3f}, standard deviation: {std_total:.3f}"
        axes[1].set_title("Distribution of Normalized Total Marks")
        axes[1].annotate(data, xy=(0.6, 0.8), xycoords="axes fraction")

        # Plot 3: Stacked Bar Plot of Average Normalized Scores
        df_avg = (
            self.marks(norm=True, to_one=True)
            .groupby(["Question", "Part"])["Mark"]
            .mean()
            .unstack()
            .fillna(0)
        )
        df_avg.plot(kind="bar", stacked=True, ax=axes[2])
        axes[2].set_title("Average Normalized Scores for Each Question Part")
        axes[2].set_ylabel("Average Normalized Mark")
        axes[2].set_xlabel("Questions")
        axes[2].legend(title="Part", bbox_to_anchor=(1.05, 1), loc="upper left")

        # Save the figure to a file
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return self


# Create an instance of Test
# p3_mock = Test("example.csv")
# p3_mock.total_marks_analysis("Output/test_analyser.png")
# Inspect the total marks DataFrame
# print(p3_mock.normalise_marks(to_one=False).norm_table)
