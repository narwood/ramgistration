from nicole import bigDictEnergy
import pandas as pd
import csv

#bigDict = bigDictEnergy()
df = pd.read_csv("C:\Users\nsarw\Ramgistration\ramgistration\Spring_2023.csv")

def main():
    print(df.head(5))

if __name__ == "__main__":
    main()
