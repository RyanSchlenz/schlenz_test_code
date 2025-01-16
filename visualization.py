import matplotlib.pyplot as plt

def generate_chart(df, output_path):
    """
    Generates a bar chart showing the average age by city and saves it as an image.

    Parameters:
        df (DataFrame): The cleaned DataFrame containing the data.
        output_path (str): The file path to save the chart image.

    Returns:
        None
    """
    avg_age_by_city = df.groupby("city")["age"].mean()
    avg_age_by_city.plot(kind="bar")
    plt.title("Average Age by City")
    plt.xlabel("City")
    plt.ylabel("Average Age")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Chart saved to {output_path}")
