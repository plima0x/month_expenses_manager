from expense_manager import ExpenseManager

csv_file = input("Enter the csv file path: ")

em = ExpenseManager(csv_file)

# Convert types:
em.convert_all_cols()

em.summary()

