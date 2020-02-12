import pandas as pd

'''takes one input params: 
1. sales_data_file_name in quotes (eg:'table.csv')  
and returns daily sales transaction data in .txt format, with naming convention: Sales_DD_MM_YY,for the 
last few dates in the entire sales data'''


def get_day_trns(sale_data_file_name):
    # reading the .csv file, located in the current working directory, using pandas
    sales = pd.read_csv(sale_data_file_name, engine='python')

    # if the entries in sale_date column are in string format then convert the entries to datatime format
    if type(sales.sale_date.loc[0]) == str:
        sales['sale_date'] = pd.to_datetime(sales['sale_date'], errors='coerce')
    else:
        sales = sales

    # getting the list of sorted unique date entries and getting only the last few dates for which .txt file has to be generated
    dates = list(sorted(sales.sale_date.unique()))
    last_dates = dates[len(dates) - 5:]

    for i in last_dates:
        # converting the numpy.datetime object to pandas datatime object for being able to use some functions
        d = pd.to_datetime(i)
        dd = str(d.date())  # strips off the timestamp and gives only the date and then convert to string
        date = dd.split('-')
        year = date[0][2:]  # slicing the year in order to get it in yy format
        month = date[1]
        day = date[2]
        tab = sales[sales['sale_date'] == i].reset_index(drop=True)
        tab.to_csv(str.format('Sales_{0}_{1}_{2}.txt', day, month, year), index=None, sep=',', mode='a')


# calling the function
get_day_trns('sales.csv')
