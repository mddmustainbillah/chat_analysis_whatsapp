import re
import pandas as pd


def preprocess(data):
    # Define the regular expression pattern to extract the date, time, and message
    pattern = r'(\[\d{1,2}/\d{1,2}/\d{2,4} \d{2}:\d{2}:\d{2}\])'

    # Split the data using the regular expression pattern
    split_data = re.split(pattern, data)[1:]

    # Extract the matched groups and store them in lists
    date_time = [split_data[i].strip() for i in range(0, len(split_data), 2)]
    messages = [split_data[i + 1].strip() for i in range(0, len(split_data), 2)]

    # Create a DataFrame
    df = pd.DataFrame({'Date_Time': date_time, 'Message': messages})

    # Remove '[' and ']' from Date_Time column
    df['Date_Time'] = df['Date_Time'].str.replace(r'[\[\]]', '')

    # Remove '~ ' from Message column
    df['Message'] = df['Message'].str.replace(r'~', '')

    # Convert into datetime format
    df['Date_Time'] = pd.to_datetime(df['Date_Time'], format='%d/%m/%y %H:%M:%S')

    # Remove the white space from message column
    df['Message'] = df['Message'].str.strip()

    # Rename the columns name
    df.rename(columns={'Date_Time': 'date', 'Message': 'user_message'}, inplace=True)


    # Separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    # Droping the user_message column
    df.drop(columns='user_message', inplace=True)

    # Extracting year, month, day, hour, minute for date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day 
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute



    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    # Sort values by Date_Time in ascending order
    df = df.sort_values(by='date', ascending=True)


    return df