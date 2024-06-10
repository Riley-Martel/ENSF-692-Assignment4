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




def main():

    # Import data here

    df = pd.read_excel("CalgaryDogBreeds.xlsx")
    dfIndex = pd.MultiIndex.from_frame(df)
    #dogs = df[dfIndex.names[2]].unique()
    print(df.head)
    #print(dfIndex.names)
    #print(dogs[3])
    #print(df.info)
    #print(df.index.names)

    print("ENSF 692 Dogs of Calgary")
    # User input stage
    breed = getInput(df,dfIndex)
    print(breed)
    # Data anaylsis stage
    

if __name__ == '__main__':
    main()
