import pandas as pd

'''takes two input params: 
1. sales_data_file_name in quotes (eg:'table.csv')  
2. date in the format yyyymmdd (eg:20200220 which is 2020-02-20) 
and returns the sales transaction data for given date in .txt format with naming convention: Sales_DD_MM_YY'''


def get_day_trns(sale_data_file_name, date):
    # the date entered will be in integer format
    dt = pd.to_datetime(str(date), format='%Y%m%d')

    # reading the .csv file, located in the current working directory, using pandas
    sales = pd.read_csv(sale_data_file_name, engine='python')

    # if the entries in sale_date column are in string format then convert the entries to datatime format
    if type(sales.sale_date.loc[0]) == str:
        sales['sale_date'] = pd.to_datetime(sales['sale_date'], errors='coerce')
    else:
        sales = sales

    # getting the list of unique date entries in the
    dates = list(sales.sale_date.unique())

    # following string operations are done for naming the .txt file
    string_date = str(date)
    year = string_date[2:4]
    month = string_date[4:6]
    day = string_date[6:]

    # if the sales transaction exists for the entered date then return the sales for the day in .txt else return error message
    if dt in dates:
        tab = sales[sales['sale_date'] == dt].reset_index(drop=True)
        return (tab.to_csv(str.format('Sales_{0}_{1}_{2}.txt', day, month, year), index=None, sep=',', mode='a'))
    return ('Sales transaction for this date is not available')


# calling the function
get_day_trns('sales.csv', 20130725)
