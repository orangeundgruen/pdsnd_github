import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Would you like to see data for Chicago, New York, or Washington?\n').title()
    cities =['Chicago', 'New York', 'Washington']

    while city not in cities:
        city = input('Please enter one of the following cities you want to explore: Chicago, New York or Washington\n').title()
    
    print('Looks like you want to hear about {}! If this is not true, please restart the program.\n'.format(city))

    time_filter = input('Would you like to filter the data by month, day, or not at all? Type "none" for no time filter.\n')
    time_filters = ['Month', 'Day', 'None']

    while time_filter.title() not in time_filters:
        time_filter = input('Please type in month, day, or "none" depending on your preffered filter option.\n')

    print('We will make sure to filter by {}!\n'.format(time_filter.title()))

    if time_filter.title() == 'Month':  
            # get user input for month (all, january, february, ... , june)
        month = input('Which month? January, February, March, April, May, or June? Please type out the full month name or "all" for all month.\n').title()
        months = ['None', 'January', 'February', 'March', 'April', 'May', 'June']

        while month.title() not in months:
            month = input('Please enter one of the following month as filter: January, February, March, April, May, June, or All\n')
        
        print('We will make sure to filter by {}!\n'.format(month))

        day = 'None'
    
    elif time_filter.title() == 'Day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Which day? Please type the day as full name of the day (e.g. Sunday)\n')
        days = ['None', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        while day.title() not in days:
            day = input('Please type the day as full name of the day (e.g. Sunday)\n')
        
        print('We will make sure to filter by {}!\n'.format(day))

        month = 'None'

    else:
        print('We will not filter the data by month or day.\n')

        month = 'None'
        day = 'None'


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # transform the column Sart Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Duration'] = df['End Time'] - df['Start Time']

    # create columns with month, day and hour
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter for the month
    if month != 'None':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month
        df = df[df['month'] == month]
    
    # filter for the day
    if day != 'None':
        # use the index of the days list to get the corresponding int
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = days.index(day) + 1
        # filter by day
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('The most popular Start Month: ', months[popular_month-1])

    # display the most common day of week
    popular_day = df['weekday'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('The most popular Start Day: ', days[popular_day-1])

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_st = df['Start Station'].mode()[0]
    print('The most commonly used Start Station is: ', popular_start_st)

    # display most commonly used end station
    popular_end_st = df['End Station'].mode()[0]
    print('The most commonly used End Station is: ', popular_end_st)

    # display most frequent combination of start station and end station trip
    df['to'] = ' to '
    df['Trip'] = df['Start Station'] + df['to'] + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('The most commonly used trip realtion is: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_tt = df['Trip Duration'].sum()
    print('The total travel time is ', total_tt)

    # display mean travel time
    average_tt = df['Trip Duration'].mean()
    print('The average travel time is ', average_tt)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The number of customers breaks down as follows:\n', user_types.to_string())

    # Display counts of gender
    gender = df['Gender'].value_counts()
    print(gender.to_string())

    # Display earliest year of birth
    year_of_birth_earliest = df['Birth Year'].value_counts().idxmin()
    print('Earliest birth year:', int(year_of_birth_earliest))

    # Display most recent year of birth
    year_of_birth_recent = df['Birth Year'].value_counts().idxmax()
    print('Most recent birth year:', int(year_of_birth_recent))

    # Display most common year of birth
    year_of_birth_common = df['Birth Year'].mode()[0]
    print('Most common birth year:', int(year_of_birth_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
