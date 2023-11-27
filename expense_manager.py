import pandas as pd


def show_bars():
    print("=" * 50)


class ExpenseManager:
    """
    Class that manage the csv file with expenses, extracting valuable metrics.
    """

    # Formats used in type conversion.
    NUM_FORMAT = "numeric"
    DATE_FORMAT = "date"
    STR_FORMAT = "string"
    BOOL_FORMAT = "bool"

    # Csv delimiter.
    DELIMITER = ";"
    # Date format used in conversion to timestamp data type.
    DATE_STR_FMT = "%m/%d/%Y"

    # Columns representing the columns in the csv file.
    DT_COL = "date"
    PROD_COL = "product"
    VAL_COL = "value"
    CATEG_COL = "category"
    PAY_COL = "payment_method"
    PRIOR_COL = "priority"
    MY_EXP_COL = "my_expense"
    FIX_EXP_COL = "fixed_expense"
    DETAILS_COL = "details"

    def __init__(self, csv_file: str):
        """
        :param csv_file: csv file path with the standardized.
        """
        self.csv_file = csv_file
        self.df_exp = pd.read_csv(self.csv_file, delimiter=self.DELIMITER)

    def convert_col(self, col_name: str, data_type: str):
        """
        Convert the column col_name to the data type specified in data_type.

        :param col_name: column to convert.
        :param data_type: column type to convert to.
        :return:
        """
        if data_type == self.NUM_FORMAT:
            # First replace all the comma to dots to avoid value error.
            self.df_exp[col_name] = self.df_exp[col_name].str.replace(",", ".")
            # Convert to a numeric value:
            self.df_exp[col_name] = pd.to_numeric(self.df_exp[col_name])
        elif data_type == self.DATE_FORMAT:
            # Convert to a timestamp using the format specified.
            self.df_exp[col_name] = pd.to_datetime(self.df_exp[col_name],
                                                   format=self.DATE_STR_FMT)
        elif data_type == self.STR_FORMAT:
            # Convert to string.
            self.df_exp[col_name] = self.df_exp[col_name].astype(str)
        elif data_type == self.BOOL_FORMAT:
            # Convert to a boolean column using the following rule:
            # Replace all 'no' values to a empty string ''.
            # When converting to boolean, the empty strings will be treated as False and
            # non-empty strings will be treated as True.

            self.df_exp[col_name] = self.df_exp[col_name].str.replace("no", "")
            self.df_exp[col_name] = self.df_exp[col_name].astype(bool)
        else:
            raise Exception(f"[!] Invalid format {data_type}!")

    def convert_all_cols(self):
        """
        Convert all columns in the pandas data frame self.df_exp to a valid data type.
        """
        col_dict = {
            self.DT_COL: self.DATE_FORMAT,
            self.PROD_COL: self.STR_FORMAT,
            self.VAL_COL: self.NUM_FORMAT,
            self.CATEG_COL: self.STR_FORMAT,
            self.PAY_COL: self.STR_FORMAT,
            self.PRIOR_COL: self.BOOL_FORMAT,
            self.MY_EXP_COL: self.BOOL_FORMAT,
            self.FIX_EXP_COL: self.BOOL_FORMAT,
            self.DETAILS_COL: self.STR_FORMAT
        }
        for col, col_type in col_dict.items():
            self.convert_col(col, col_type)

    def get_sum(self, df_filtered: pandas.DataFrame) -> float:
        """
        Sum the value column(self.VAL_COL) of the data frame df_filtered.

        :param df_filtered: pandas dataframe to be used in the sum.
        :return: the total sum of the column values(self.VAL_COL) of the data frame df_filtered.
        """

        sum_col_val = df_filtered[self.VAL_COL].sum()
        return round(sum_col_val, 2)

    def get_sum_by_date(self, df_base: pd.DataFrame, filter_date: str) -> float:
        """
        Filter the data frame df_base by the data specified in filter_date and sums the values column(self.VAL_COL)

        :param df_base: pandas dataframe to be used in the sum.
        :param filter_date: the date value to use in the filter before the sum.
        :return: the total sum of the column values(self.VAL_COL) of the data frame df_filtered.
        """
        dt_time = pd.Timestamp(filter_date)
        df_filter_dt = df_base[df_base[self.DT_COL] >= dt_time]

        return self.get_sum(df_filter_dt)

    def get_filtered_df(self, filter_col: str = None, filter_val: str = None, my_own_exp: bool = True):
        """
        Returns a data frame with the filters specified.

        :param filter_col: column to be used in the filter.
        :param filter_val: value to compare with the desired column filter_col.
        :param my_own_exp: if True, the data frame returned will not contain third-party expenses.
        :return: a data frame with the filters applied.
        """
        df_my_exp = self.df_exp[self.df_exp[self.MY_EXP_COL] == my_own_exp]
        df_filtered = df_my_exp[df_my_exp[filter_col] == filter_val]
        return df_filtered

    def summary(self):
        df_debit = self.get_filtered_df(self.PAY_COL, "debit")
        sum_debit = self.get_sum(df_debit)

        df_credit = self.get_filtered_df(self.PAY_COL, "credit")
        filter_credit_date = "2023-10-01"
        sum_credit = self.get_sum_by_date(df_credit, filter_credit_date)

        show_bars()
        filter_cols = [self.DT_COL, self.PROD_COL, self.VAL_COL, self.CATEG_COL]
        sort_col = self.VAL_COL

        print(f"Sum of all debit expenses:  ${sum_debit}")
        print("\nMost expensive items paid in debit: ")
        print(df_debit[filter_cols].sort_values(sort_col, ascending=False)[:3])
        print("\nMost expensive categories paid in debit: ")

        grp_cols = [self.CATEG_COL, self.VAL_COL]
        df_debit_summed = df_debit[grp_cols].groupby(self.CATEG_COL).sum()
        print(df_debit_summed.sort_values(self.VAL_COL, ascending=False)[:3])
        show_bars()

        show_bars()
        print(f"Sum of all credit expenses: ${sum_credit}")
        print("\nMost expensive items paid in credit: ")
        print(df_credit[filter_cols].sort_values(sort_col, ascending=False)[:3])
        print("\nMost expensive categories paid in credit: ")
        df_credit_summed = df_credit[grp_cols].groupby(self.CATEG_COL).sum()
        print(df_credit_summed.sort_values(self.VAL_COL, ascending=False)[:3])
        show_bars()
