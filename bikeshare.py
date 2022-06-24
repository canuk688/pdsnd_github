#Carl Evans Udacity Project

import time
import datetime as dt
import pandas as pd
import numpy as np
#Datasets referenced below for which file is queried
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

#This initial function sets up filters on dataset before running statistics
def get_filters():
    MONTH_data = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    DAY_data = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input(
            "Please enter a which of the three cities you would like to explore (chicago, new york city or washington?): ")
        if city not in CITY_DATA:
            print("Oops you may have had a typo or extra space, here try again...")
            continue
        else:
            print("Great, now a few more questions...")
            # get user input for month (all, january, february, ... , june)
            month = input("Which month would you like to look at? (all, january, february, ... , june)?: ")
            while month not in MONTH_data:
                print("Oops you may have had a typo or extra space, here try again...")
                month = input("Which month would you like to look at? (all, january, february, ... , june)?: ")
                continue
            day = input("Which day of the week would you like to look at (all, monday, tuesday, ... sunday)?: ")
            while day not in DAY_data:
                print("Oops you may have had a typo or extra space, here try again...")
                day = input("Which day of the week would you like to look at (all, monday, tuesday, ... sunday)?: ")
                continue

        break

    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    # Print results
    print("The most common month for rentals was:", popular_month)
    print("The most common day for rentals was:", popular_day)
    print("The most common hour for rentals was:", popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['start_end'] = df[['Start Station', 'End Station']].agg(' |--> '.join, axis=1)
    popular_start_end = df['start_end'].mode()[0]

    # Print results

    print("The most commonly used start station was:", popular_start)
    print("The most commonly used end station was:", popular_end)
    print("The most frequent combination of start station and end station trip:", popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['tot_travel_time'] = df['End Time'] - df['Start Time']

    # display mean travel time
    mean_travel_time = df['tot_travel_time'].mean()
    print("The average travel time was:", mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df["User Type"].value_counts()

    # Display counts of gender, earliest, most recent, and most common year of birth
    if city != 'washington':
        gender_counts = df["Gender"].value_counts()
        youngest = df["Birth Year"].min()
        oldest = df["Birth Year"].max()
        commonage = df["Birth Year"].mode()
    else:
        gender_counts = "Not Available"
        youngest = "Not Available"
        oldest = "Not Available"
        commonage = "Not Available"

    print("See counts of typical user types: ", user_counts)
    print("See counts of typical user genders: ", gender_counts)
    print("See bday of youngest user: ", youngest)
    print("See bday of oldest user: ", oldest)
    print("See the most common year of birth: ", commonage)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# Added function to display 5 rows of data per user request, stop if no and starting location cant be greater than the number of rows in the dataframe
def display_data(df, city):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while (view_data == "yes"):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
        if view_data == "no":
            break
        if start_loc > len(df):
            break


def main():
    # Here I added city as an input to user_stats to handle be able to handle washington state not having gender/bdate data available.
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df, city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
