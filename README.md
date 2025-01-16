*XML Medical Data Processor*

This project processes patient data from an XML file, cleans the data, and generates a report summarizing adults and children by city. It also creates a bar chart displaying the average age by city.

*Features*
Data Loading: Loads XML data and converts it into a pandas DataFrame.

Data Cleaning: Handles missing or malformed records and calculates ages from dates of birth.

Report Generation: Creates a JSON report summarizing the number of adults and children for each city.

Visualization: Generates a bar chart showing the average age by city and saves it as an image file.

*Prerequisites*
Ensure you have Python installed (>= 3.7). Install the required libraries using:

pip install -r requirements.txt

Usage
Prepare the Input Data:
Place the XML file (people_data.xml) in the project directory.

Run the Main Script:
Execute the main script to process the data and generate the outputs:
python main.py

Output Files:
report.json: A JSON file summarizing adults and children by city.
age_by_city.png: A bar chart image showing the average age by city.

*File Structure*
project/
├── main.py                # Orchestrates the workflow
├── generate_report.py      # Handles data loading, cleaning, and reporting
├── visualization.py        # Generates bar charts
├── requirements.txt        # Python dependencies
├── README.md               # Project instructions
└── people_data.xml         # Input XML data (sample data provided by the user)

License
This project is licensed under the MIT License.

Author
Ryan Schlenz