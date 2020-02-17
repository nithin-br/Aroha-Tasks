# importing the necessary modules
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=Warning)

# loading the tables
holidays = pd.read_csv('holiday.csv')
shift_type = pd.read_csv('shift_type.csv')
shift = pd.read_csv('shift_table.csv',
                    dtype={'shift_id': 'int32', 'Date': 'str', 'start_time': 'str', 'end_time': 'str'},
                    parse_dates=['Date'])

# dropping the manually added row (in csv file) from the dataframe
shift = shift.drop(shift.index[0])

'''function which takes in one input parameter:
1. month and year in the format mon_yy. example: FEB_20/feb_20 (february 2020)
and returns the populated table of shifts for that month and year as per the bussiness rules mentioned in the 
scenario'''


def populate_shift_table(mon_yy):
    # getting month and year details from input
    month_year = mon_yy.split('_')
    user_month = month_year[0].lower()
    year = month_year[1]
    full_year = '20' + year

    # making the date column in the holidays table to datetime dtype
    holidays['Date'] = pd.to_datetime(holidays['Date'], errors='coerce')
    '''replacing the year in the date col of holidays table to the year given by user 
    (default year in this table is 2015)'''
    for i, j in enumerate(holidays.Date):
        holidays['Date'].loc[i] = j.replace(year=int(full_year))

    '''creating a Series of date ranges for the year given by user along with leap Year Check and 
    assign value for the periods parameter accordingly'''
    if (int(full_year) % 4) == 0:
        if (int(full_year) % 100) == 0:
            if (int(full_year) % 400) == 0:
                date_range = pd.date_range(start='01/01/' + full_year, periods=366)
            else:
                date_range = pd.date_range(start='01/01/' + full_year, periods=365)
        else:
            date_range = pd.date_range(start='01/01/' + full_year, periods=366)
    else:
        date_range = pd.date_range(start='01/01/' + full_year, periods=365)

    '''creating duplicates of the values in the array. we want every date/value to occur twice in the date 
    column of the shift table as per scenario.
    making use of the series method repeat()'''

    date_range_duplicate = date_range.repeat(2)

    # adding this duplicated Series to the Date column of the shift table
    shift['Date'] = date_range_duplicate

    '''the shift_id column should have values 1 and 2. 1 for morning shift and 2 for night shift for 
    each and every date.creating a list of 1 and 2 and then appending it to shift_id column of the dataframe'''
    shift_id = []
    for i in range(shift.shape[0]):
        if (i % 2) == 0:
            shift_id.append(1)
        else:
            shift_id.append(2)

    # adding the created list as column to the dataframe
    shift['shift_id'] = shift_id

    # making a list of holiday_dates
    holiday_date_list = list(holidays.Date)

    '''if a date entry in the shift table is holiday as per dates in the holidays table and if a particular 
    day is sunday then append holiday/sunday for entries in the start_time and end_time'''
    for i, j in enumerate(shift.Date):
        if j in (holiday_date_list):
            shift['start_time'].loc[i] = 'Holiday'
            shift['end_time'].loc[i] = 'Holiday'
        elif j.day_name() == 'Sunday':
            shift['start_time'].loc[i] = j.day_name()
            shift['end_time'].loc[i] = j.day_name()

    '''if day is sturday then assign only morning shift (shift_id=1=morning shift and shift_id=2=evening shift)
    and append no shift for the evening shift'''
    for i, j in enumerate(shift.Date):
        if (j.day_name() == 'Saturday') and (shift['shift_id'].loc[i] == 1):
            shift['start_time'].loc[i] = '6:00 AM'
            shift['end_time'].loc[i] = '2:00 PM'
        elif (j.day_name() == 'Saturday') and (shift['shift_id'].loc[i] == 2):
            shift['start_time'].loc[i] = 'No shift'
            shift['end_time'].loc[i] = 'No shift'

    '''filling rest of the entries for the columns start_shift and end_shift. if shift_id=1 and either one 
    of the columns(start_shift/end_shift) is nan then fill time for morning shift.if shift_id=2 and either one 
    of the columns(start_shift/end_shift) is nan then fill time for evening shift'''
    for i in range(shift.shape[0]):
        if (shift['shift_id'].loc[i] == 1) and (pd.isna(shift['start_time'].loc[i])):
            shift['start_time'].loc[i] = '6:00 AM'
            shift['end_time'].loc[i] = '2:00 PM'
        elif (shift['shift_id'].loc[i] == 2) and (pd.isna(shift['start_time'].loc[i])):
            shift['start_time'].loc[i] = '2:00 PM'
            shift['end_time'].loc[i] = '10:00 PM'

    # adding a new column with months abbreviated name for being able to filter the shift table month wise
    month_name = []
    for val in (shift.Date):
        month_name.append(val.month_name()[0:3].lower())
    shift['Month'] = month_name

    # filtering the data as per user input
    month_shift = shift[shift['Month'] == user_month]
    month_shift = month_shift.drop(columns=['Month'], axis=1)
    month_shift = month_shift.reset_index(drop=True)
    return(month_shift)


# calling the function
month_shift = populate_shift_table('JAN_24')

# converting the dataframe to csv to show result
month_shift.to_csv('month_shift.csv', index=False)
