from numpy import PINF, promote_types
import pandas as pd
from pandas.core.algorithms import unique


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")
    
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = pd.Series(df["race"].value_counts())

    # What is the average age of men?
    males = df["sex"] == "Male"
    average_age_men = round(df[males]["age"].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    bachelors = df["education"] == "Bachelors"
    percentage_bachelors = round((df[bachelors].__len__() / df.__len__()) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    highDegrees = (df["education"] == "Bachelors") | (df["education"] == "Masters") | (df["education"] == "Doctorate")
    higher_education = df[highDegrees]
    lower_education = df[~highDegrees]

    # percentage with salary >50K
    largeIncome = df["salary"] == ">50K"
    higher_education_rich = round((higher_education[largeIncome].__len__() / higher_education.__len__()) * 100, 1)
    lower_education_rich = round((lower_education[largeIncome].__len__() / lower_education.__len__()) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    minHours = (df["hours-per-week"] == min_work_hours)
    num_min_workers = df[largeIncome][minHours]

    rich_percentage = round((num_min_workers.__len__() / df[minHours].__len__()) * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    highest_earning_country = ""
    highest_earning_country_percentage = 0

    for country, value in df["native-country"].value_counts().items():
        countryFilter = df["native-country"] == country
        salary = df[largeIncome][countryFilter]["salary"].value_counts()
        
        try:
            percentage = round((salary[0] / value) * 100, 1)
        except:
            continue

        if percentage > highest_earning_country_percentage:
            highest_earning_country_percentage = percentage
            highest_earning_country = country
  

    # Identify the most popular occupation for those who earn >50K in India.
    fromIndia = df["native-country"] == "India"
    top_IN_occupation = df[largeIncome][fromIndia]["occupation"].value_counts()[:1].index.tolist()[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
