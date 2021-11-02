
# sorts the pandas dataframe by Column: Salary
def sort_by_salary(df):
    return df.sort_values(by=['Salary'], ascending=False)

# returns the average value of Salary among all players in the dataframe
def average_salary(df):
    return int(df["Salary"].sum(axis=0))/(len(df))

# reduces the number of rows in the dataframe to the top n values
def nth_largest(df, n):
    return df.head(n)

