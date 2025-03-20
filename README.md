# NYC Airbnb Recommendation System

## Overview

The NYC Airbnb Recommendation System is a project designed to help users find the best Airbnb listings in New York City based on their preferences. By leveraging data analysis and machine learning, the system provides personalized recommendations to enhance the user experience.

**Note**: Due to the limited amount of data available, this recommendation system may not provide the most accurate or comprehensive results. It is intended as a proof of concept and can be improved with access to more extensive datasets.

## Features

- **Data Analysis**: Analyze Airbnb listings data to extract meaningful insights.
- **Recommendation Engine**: Suggests listings based on user preferences and historical data.
- **Interactive Interface**: User-friendly interface for inputting preferences and viewing recommendations.
- **Scalability**: Designed to handle large datasets efficiently.

## Technologies Used

- **Programming Language**: Python
- **Libraries**: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
- **Frameworks**: Flask (for web interface, if applicable)
- **Database**: SQLite or other database systems (if applicable)
- **Visualization**: Plotly, Dash (optional)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/StanleyHe1/nyc_airbnb_rec_sys.git
   ```
2. Navigate to the project directory:
   ```bash
   cd nyc_airbnb_rec_sys
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
5. Install the necessary dependencies manually based on your project setup.

## Usage

1. Prepare the dataset:
   - Place the Airbnb dataset in the `data/` directory.
   - Ensure the dataset is in CSV format and properly cleaned.

2. Run the application:
   ```bash
   python main.py
   ```

3. Input your preferences and view the recommended listings.

## Project Structure

```
nyc_airbnb_rec_sys/
├── Phase1/                 
│   ├── raw/                        # Contains raw, unprocessed data files.
│   ├── cleaning_process/           # Scripts and processes for cleaning and preparing the data.
├── Phase2/                 
│   ├── cleaned/                    # Cleaned data ready for analysis or modeling.
│   ├── models/                     # Machine learning models created during this phase.
├── Phase3/                 
│   ├── cleaned/                    # Cleaned data used for the final phase.
│   ├── AirbnbRecommendation.css/   # CSS file for styling the web interface.
│   ├── AirbnbRecommendation.jsx/   # React JSX file for rendering the website.
│   ├── App.js/                     # Main React application file.
│   ├── kmeans_model.joblib/        # Serialized KMeans model for clustering.
│   ├── project_phase3.py/          # Python script for Phase 3 operations.
│   ├── ridge_regression_model.joblib/ # Serialized Ridge Regression model for predictions.
├── README.md                       # Documentation for the project.
└── LICENSE                         # License file for the project.
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Airbnb for providing the dataset.
- Open-source libraries and tools used in this project.
