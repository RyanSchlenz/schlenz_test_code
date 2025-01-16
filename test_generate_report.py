import unittest
import pandas as pd
from datetime import datetime
import json 
from generate_report import calculate_age, load_data, clean_data, generate_report

class TestGenerateReport(unittest.TestCase):
    def test_calculate_age_valid_date(self):
        # Test valid date formats
        current_year = datetime.today().year
        expected_age = current_year - 1989 - ((datetime.today().month, datetime.today().day) < (6, 15))
        self.assertEqual(calculate_age("1989-06-15"), expected_age)

    def test_calculate_age_invalid_date(self):
        # Test invalid date formats
        self.assertIsNone(calculate_age("invalid-date"))
        self.assertIsNone(calculate_age("1234"))

    def test_load_data(self):
        # Test loading valid XML data
        xml_data = """<people>
            <person>
                <id>1</id>
                <name>John Doe</name>
                <dob>1989-06-15</dob>
                <address>
                    <city>Springfield</city>
                    <country>USA</country>
                </address>
            </person>
            <person>
                <id>2</id>
                <name>Jane Doe</name>
                <dob>2010-04-03</dob>
                <address>
                    <city>SLC</city>
                    <country>USA</country>
                </address>
            </person>
        </people>"""
        with open("test_data.xml", "w") as f:
            f.write(xml_data)

        df = load_data("test_data.xml")
        self.assertEqual(len(df), 2)
        self.assertIn("John Doe", df["name"].values)

    def test_clean_data(self):
        # Test cleaning the data
        data = {
            "id": [1, 2],
            "name": ["John Doe", "Jane Doe"],
            "dob": ["1989-06-15", "invalid-date"],
            "city": ["Springfield", "SLC"],
            "country": ["USA", "USA"],
        }
        df = pd.DataFrame(data)
        cleaned_df = clean_data(df)
        self.assertEqual(len(cleaned_df), 1)  # Only valid row should remain
        self.assertEqual(cleaned_df.iloc[0]["name"], "John Doe")

    def test_generate_report(self):
        # Test report generation
        data = {
            "id": [1, 2],
            "name": ["John Doe", "Jane Doe"],
            "dob": ["1989-06-15", "2010-04-03"],
            "city": ["Springfield", "SLC"],
            "country": ["USA", "USA"],
            "age": [35, 13],
        }
        df = pd.DataFrame(data)
        report_file = "test_report.json"
        generate_report(df, report_file)

        with open(report_file, "r") as f:
            report = json.load(f)

        self.assertIn("Springfield", report)
        self.assertEqual(report["Springfield"]["adults"], 1)
        self.assertEqual(report["SLC"]["children"], 1)

if __name__ == "__main__":
    unittest.main()
