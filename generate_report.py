import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import logging

# Set up a logger for discarded records only
logger = logging.getLogger("discarded_records")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("discarded_files.txt", mode="w")
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

def calculate_age(dob):
    """ 
    Calculates the age based on the given date of birth.

    Parameters:
        dob (str): Date of birth in "YYYY-MM-DD" or "YYYYMMDD" format.

    Returns:
        int: The calculated age, or None if the date is invalid.
    """
    try:
        dob = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        try:
            dob = datetime.strptime(dob, "%Y%m%d")
        except ValueError:
            return None
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def load_data(file_path):
    """
    Parses the XML file and loads valid data into a pandas DataFrame.

    Parameters:
        file_path (str): Path to the XML file containing the data.

    Returns:
        DataFrame: A pandas DataFrame containing the valid records from the XML file.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []

    for person in root.findall("person"):
        try:
            person_data = {
                "id": person.find("id").text,
                "name": person.find("name").text,
                "dob": person.find("dob").text,
                "city": person.find("address/city").text,
                "country": person.find("address/country").text,
            }
            data.append(person_data)
        except AttributeError:
            logger.info(f"Invalid record: {ET.tostring(person, encoding='unicode')}")
            continue

    return pd.DataFrame(data)

def clean_data(df):
    """
    Cleans the data by calculating ages and removing invalid records.

    Parameters:
        df (DataFrame): The DataFrame containing the raw data.

    Returns:
        DataFrame: A cleaned DataFrame with valid records and calculated ages.
    """
    df["age"] = df["dob"].apply(calculate_age)
    df = df.dropna(subset=["age", "city", "country"])
    df.loc[:, "age"] = df["age"].astype(int)
    return df

def generate_report(df, output_path):
    """
    Generates a JSON report summarizing adults and children by city.

    Parameters:
        df (DataFrame): The cleaned DataFrame containing the data.
        output_path (str): The file path where the JSON report will be saved.

    Returns:
        None
    """
    report = {}

    grouped = df.groupby("city")
    for city, group in grouped:
        adults = group[group["age"] > 18].shape[0]
        children = group[group["age"] <= 18].shape[0]

        report[city] = {
            "adults": adults,
            "children": children
        }

    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)
