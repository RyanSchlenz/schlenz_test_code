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

# Function to calculate age based on date of birth
def calculate_age(dob):
    try:
        dob = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        try:
            dob = datetime.strptime(dob, "%Y%m%d")
        except ValueError:
            return None
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# Load XML data
def load_data(file_path):
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

# Data cleaning and processing
def clean_data(df):
    df["age"] = df["dob"].apply(calculate_age)
    df = df.dropna(subset=["age", "city", "country"])
    df["age"] = df["age"].astype(int)
    return df

# Generate report as JSON
def generate_report(df, output_path):
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
