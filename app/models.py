import sqlite3
import json

import openpyxl

from .string_utils import extract_ngrams, vectorize_ngrams, cosine_similarity, is_year, preprocess


class LocalDatabase:

    def __init__(self):
        
        self.connection = sqlite3.connect("annual_population.db")
        self.cursor = self.connection.cursor()
        # Check if empty
        if not self.cursor.execute("SELECT name FROM sqlite_master;").fetchall():
            self.build_database()
        # Custom function used to compute similarity between strings
        self.connection.create_function("similarity_score", 2, cosine_similarity,
                                        deterministic=True)


    def build_database(self):
        """Populate database with data from the Excel file in the data folder"""

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

        # Compute trigrams (with some preprocessing before)
        for i, country in enumerate(countries):
            trigram = vectorize_ngrams(extract_ngrams(preprocess(country[1])))
            countries[i] += tuple([json.dumps(trigram),])

        for i, city in enumerate(cities):
            trigram = vectorize_ngrams(extract_ngrams(preprocess(city[1])))
            cities[i] += tuple([json.dumps(trigram),])


        # Insert into database
        self.cursor.executemany("INSERT INTO countries(country_code, country_name, country_trigrams) VALUES(?, ?, ?)", countries)
        self.cursor.executemany("INSERT INTO cities(city_code, city_name, city_latitude, city_longitude, country_code, city_trigrams) VALUES(?, ?, ?, ?, ?, ?)", cities)
        self.cursor.executemany("INSERT INTO population_records(year, annual_population, city_code) VALUES(?, ?, ?)", records)

        # Save changes
        self.connection.commit()


    def search(self, raw_input):
        """Check for records that match user's input (in GUI seach bar)"""

        # Convert user's input (in seach bar) to searchable parameters
        parameters = parse_input(raw_input)

        query = """
        SELECT city_name, country_name, year, annual_population FROM population_records 
        JOIN cities ON population_records.city_code = cities.city_code
        JOIN countries ON cities.country_code = countries.country_code
        WHERE similarity_score(cities.city_trigrams, :trigram) > 0.333
        """

        if parameters.get("year") is not None:
            query += " AND year=:year"

        query += "\n ORDER BY similarity_score(cities.city_trigrams, :trigram) DESC"

        self.cursor.execute(query, parameters)
        
        return self.cursor.fetchall()

    def search_autofill(self, raw_input):
        """Provide suggestions (city names) based on the user's input"""

        parameters = {"name":raw_input}

        query = """
        SELECT city_name FROM cities 
        WHERE city_name LIKE :name || '%'
        LIMIT 5
        """

        self.cursor.execute(query, parameters)

        return self.cursor.fetchall()


def parse_input(raw_input):
    """Parse user input and return a set of parameters for database search."""
    
    parameters = {}

    # Lowercase and separate words
    clean_input = preprocess(raw_input)
    words = clean_input.split()

    # Check if year is provided
    for word in words:
        if is_year(word):
            parameters["year"] = int(word)
            words.remove(word)

    # Use the rest for string similarity
    name = " ".join(words)
    name_vector = json.dumps(vectorize_ngrams(extract_ngrams(name)))
    parameters["trigram"] = name_vector

    return parameters

