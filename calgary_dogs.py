# calgary_dogs.py
# AUTHOR NAME Riley Martel
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

# Your code should include and use at least one multi-index Pandas DataFrame, at least one IndexSlice object, 
# at least one masking operation, at least one grouping operation, and at least one built-in Pandas or NumPy computational method.

import numpy as np
import pandas as pd


class KeyError(ValueError):
    '''Creates a KeyError of type ValueError, this is used for input checking'''
    pass


def getInput(df,dfIndex):
    '''getInput takes user input for breed, converts it to uppercase to ensure same format as the breed,
    If the breed is not in the dataset then raises a key error and prompts user to input again returns the breed selected in uppercase'''
    error = True
    dogs = df[dfIndex.names[2]].unique()
    breed = ""
    while error:
        value = input("Please enter a dog breed: ").upper()
        try:
            for i in enumerate(dogs):
                if value == dogs[i[0]]:
                    error = False
                    breed = value
            if error == True:
                raise KeyError("[Dog Breed not in dataset]")
        except KeyError:
                print("Dog breed not found in the data. Please try again.")
                error = True
    return breed

def getTotalBreed(df,dfIndex,breed):
    """getTotalBreed takes the imported dataframe containing top 100 dog breeds in calgary for years 2021-2023
    and takes the multi index object and the selected breed. It groups the data by the breed and the total registrations for that breed and sums the totals
    The total is then returned"""
    x = df.groupby(dfIndex.names[2])[dfIndex.names[3]].sum()
    return x.get(breed)

def getYearsBreed(df,dfIndex,breed):
    """getYearsBreed takes the imported dataframe containing top 100 dog breeds in calgary for years 2021-2023
    and takes the multi index object and the selected breed. It groups the data by breed and the year and takes the unique entries
    The years the breed occurs in the dataset is then returned"""
    x = df.groupby(dfIndex.names[2])[dfIndex.names[0]].unique()
    y = np.array2string(x.get(breed))
    return y[1:-1] #String cut off at the beginning and end to remove []
def getPercentBreed(df,breed,year):
    #x = df.pivot_table(dfIndex.names[3],index = dfIndex.names[0],columns= dfIndex.names[2])
    """getPercentBreed takes the imported dataframe containing top 100 dog breeds in calgary for years 2021-2023
    and takes the selected breed and the selected year. It then re arranges the data into a pivot table consisting of the Total
    witht the index being Year and the Breed being the columns, and the totals are summed. The overall total is also calculated (all dogs in the year)
    and the percentage for the selected breed is returned"""
    x = df.pivot_table('Total',index = 'Year', columns = 'Breed', aggfunc = 'sum')
    y = x.T #Transposed
    y = y.sum()
    x = x.get(breed)
    return (x.get(year)/y.get(year))*100 #Percentage calculation
def getTotalPercent(df,breed):
    """getToatlPercent takes the imported dataframe containing top 100 dog breeds in calgary for years 2021-2023
    and the selected breed. It then re arranges the data into a pivot table consisting of the Total
    witht the index being Year and the Breed being the columns, and the totals are summed. It then sums the totals once more and calculates the
    overall percentage the selected breed was registered over all years in the dataset, this is then returned"""
    x = df.pivot_table('Total',index = 'Year', columns = 'Breed', aggfunc = 'sum')
    y = x.T #Transposed
    y = y.sum()
    x = x.get(breed)
    y = y.sum() #Sum previous sums, thus only having one value
    x = x.sum()
    return x/y*100
def getPopularMonths(df,dfIndex,breed):
    """getPopularMonths takes the imported dataframe containing top 100 dog breeds in calgary for years 2021-2023
    and takes the multi index object and the selected breed. It then groups the dataframe by Breed for Months, the entries for
    selected breed are then grabbed and the maximum occurance of a signle month is calculated. All months that occur less than the maximum
    are removed, the months are sorted and converted into a string and returned"""
    x = df.groupby(dfIndex.names[2])[dfIndex.names[1]].value_counts()
    x = x.get(breed)
    m = x.max() #get max amount of months for selected breed
    mask = x[:] >= m #Create the mask for the dataframe
    x.where(mask, inplace=True) #Modify the data with the mask
    x.dropna(inplace=True) #Get rid of NaN
    months = list(x.keys()) #Turn Month indices into list
    months.sort() #Sort into alphabetical order
    monthsString = ""
    for i in months:
        monthsString += (i + " ") #Create one big string containing all the months
    return monthsString[0:-1] #Get rid of extra space at the end


def main():
    # Import data here
    df = pd.read_excel("CalgaryDogBreeds.xlsx")
    dfIndex = pd.MultiIndex.from_frame(df)
    print("ENSF 692 Dogs of Calgary")
    # User input stage
    breed = getInput(df,dfIndex)
    # Data anaylsis stage
    print("The " + breed + " was found in the top breeds for years: "+ str(getYearsBreed(df,dfIndex,breed)))
    print("There have been " + str(getTotalBreed(df,dfIndex,breed)) + " " + breed + " dogs registered total.")
    print("The " + breed + " was {x:.6f}%".format(x = getPercentBreed(df,breed,2021)) + " of top breeds in 2021.")
    print("The " + breed + " was {x:.6f}%".format(x = getPercentBreed(df,breed,2022)) + " of top breeds in 2022.")
    print("The " + breed + " was {x:.6f}%".format(x = getPercentBreed(df,breed,2023)) + " of top breeds in 2023.")
    print("The " + breed + " was {x:.6f}%".format(x = getTotalPercent(df,breed)) + " of top breeds across all years.")
    print("Most popular month(s) for " + breed + " dogs: " + getPopularMonths(df,dfIndex,breed))

if __name__ == '__main__':
    main()
