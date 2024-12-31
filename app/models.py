import sqlite3
import json

import openpyxl

from .string_utils import extract_ngrams, vectorize_ngrams


class LocalDatabase:

    def __init__(self):
        
        self.connection = sqlite3.connect("annual_population.db")
        self.cursor = self.connection.cursor()
        # Check if empty
        if not self.cursor.execute("SELECT name FROM sqlite_master;").fetchall():
            self.build_database()


    def build_database(self):

        # Create tables
        self.cursor.execute("CREATE TABLE countries(country_code INTEGER, country_name TEXT, country_trigrams TEXT)")
        self.cursor.execute("CREATE TABLE cities(city_code INTEGER, city_name TEXT, city_latitude REAL, city_longitude REAL, country_code INTEGER, city_trigrams TEXT)")
        self.cursor.execute("CREATE TABLE population_records(year INTEGER, annual_population REAL, city_code INTEGER)")

        # Open file
        wb = openpyxl.load_workbook(filename="./data/WUP2018-F22-Cities_Over_300K_Annual.xlsx", read_only=True)
        raw_data = [row for row in wb["Data"].values]

        # Ignore first lines
        while 1:
            row = raw_data.pop(0)
            if row[0]=="Index":
                column_names = row
                break
        
        # Parse data
        countries = []
        cities = []
        records = []

        for row_values in raw_data:
            country = row_values[1:3]
            city = row_values[3:8]
            values = row_values[8:]

            # Countries
            if country not in countries:
                countries.append(country)

            # Cities
            cities.append(city[:2] + city[3:] + tuple([country[0],]))

            # Records
            for year, value in zip(column_names[8:], values):
                records.append((year, value, city[0]))

        # Add trigrams
        for i, country in enumerate(countries):
            trigram = vectorize_ngrams(extract_ngrams(country[1]))
            countries[i] += tuple([json.dumps(trigram),])

        for i, city in enumerate(cities):
            trigram = vectorize_ngrams(extract_ngrams(city[1]))
            cities[i] += tuple([json.dumps(trigram),])


        # Insert into database
        self.cursor.executemany("INSERT INTO countries(country_code, country_name, country_trigrams) VALUES(?, ?, ?)", countries)
        self.cursor.executemany("INSERT INTO cities(city_code, city_name, city_latitude, city_longitude, country_code, city_trigrams) VALUES(?, ?, ?, ?, ?, ?)", cities)
        self.cursor.executemany("INSERT INTO population_records(year, annual_population, city_code) VALUES(?, ?, ?)", records)

        # Save changes
        self.connection.commit()


    def search(self, parameters={}):

        query = """
        SELECT city_name, country_name, year, annual_population FROM population_records 
        JOIN cities ON population_records.city_code = cities.city_code
        JOIN countries ON cities.country_code = countries.country_code
        """

        if parameters.get("year") is not None:

            query += f"WHERE year = {parameters["year"]}"
        
        query += "\nLIMIT 10"

        self.cursor.execute(query)
        
        return self.cursor.fetchall()

