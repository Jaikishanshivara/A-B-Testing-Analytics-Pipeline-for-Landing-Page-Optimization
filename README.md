End-to-End A/B Testing Experiment Analytics Pipeline on AWS
Project Overview

This project implements a complete cloud-based analytics pipeline to analyze an A/B test for landing page conversion optimization. The system ingests raw experiment data from AWS S3, processes and cleans it using Python, stores structured datasets in AWS RDS (MySQL), and generates experiment performance metrics for visualization in Power BI.

The goal of this project is to simulate a real-world product analytics workflow, enabling data-driven decision making by evaluating whether a new landing page improves user conversion rates compared to the existing version.

Business Problem

A company launched an experiment to test whether a new landing page design (treatment) improves conversions compared to the current page (control).

The key question:

Does the new landing page increase user conversions?

This project builds a system to:

-Process experiment data
- Compute experiment metrics
- Compare control vs treatment performance
- Provide insights through dashboards

AWS S3 (Raw Experiment Data)
        ↓
Python ELT Pipeline (Data Cleaning & Transformation)
        ↓
AWS RDS MySQL (Cloud Database)
        ↓
SQL Experiment Metrics
        ↓
Power BI Dashboard

Tech Stack
Tool	Purpose
Python	Data pipeline & cleaning
Pandas	Data processing
SQL	Experiment metrics calculation
AWS S3	Raw data storage
AWS RDS (MySQL)	Cloud database
SQLAlchemy	Python database connection
Power BI	Data visualization
Windows Task Scheduler	Pipeline automation
GitHub	Version control & project documentation
Dataset Description

The dataset contains user interaction data from an A/B test experiment.

Columns include:

Column	Description
user_id	Unique identifier for each user
group	Experiment group (control or treatment)
landing_page	Page shown to the user
converted	Whether the user converted (0 or 1)
timestamp	Time of user interaction
Pipeline Workflow
1 Data Ingestion

The raw dataset is uploaded to AWS S3.

S3 Bucket
└── ab_data.csv

The Python pipeline downloads the dataset from S3 automatically.

2 Data Cleaning

The pipeline performs the following preprocessing steps:

Remove duplicate users

Drop missing values

Filter invalid experiment records

Ensure group and landing page consistency

Example rule:

control → old_page
treatment → new_page
3 Data Loading

Cleaned data is loaded into AWS RDS MySQL using SQLAlchemy.

Table created:

ab_test_raw
4 Experiment Metrics Calculation

SQL transformations generate experiment performance metrics.

Example query:

CREATE TABLE experiment_results AS
SELECT
    `group`,
    COUNT(user_id) AS users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted)*100,2) AS conversion_rate
FROM ab_test_raw
GROUP BY `group`;

Output:

group	users	conversions	conversion_rate
control	~145k	~17k	~12.0%
treatment	~145k	~16.8k	~11.8%
Dashboard

The final dataset is connected to Power BI, which visualizes:

Total users

Total conversions

Conversion rate

Control vs treatment comparison

Conversion distribution

Experiment performance summary

This enables quick analysis of experiment outcomes.

Key Insight

The analysis shows:

Control Conversion Rate ≈ 12%
Treatment Conversion Rate ≈ 11.8%

The new landing page did not improve conversions.

Business Recommendation

The company should:

Retain the current landing page (control version)

Conduct additional experiments focusing on:

Call-to-action placement

Page layout

Messaging

User experience improvements

Further experimentation may identify changes that increase conversion performance.

Project Structure
ab-testing-analytics-pipeline
│
├── data
│   └── ab_data.csv
│
├── pipeline
│   └── elt_pipeline.py
│
├── sql
│   └── experiment_metrics.sql
│
├── dashboard
│   └── powerbi_dashboard.pbix
│
├── run_pipeline.bat
│
├── requirements.txt
│
└── README.md
How to Run the Pipeline
1 Install Dependencies
pip install pandas boto3 sqlalchemy pymysql
2 Configure AWS Credentials
aws configure

Provide:

Access Key
Secret Key
Region: ap-south-1
3 Run Pipeline
python pipeline/elt_pipeline.py

The pipeline will:

Download data from S3

Clean and validate data

Load data into AWS RDS

Generate experiment metrics

Automation

The pipeline is automated using Windows Task Scheduler, allowing the system to refresh experiment metrics automatically.

Example Output
File downloaded from S3
Rows loaded: 290584
Data loaded to MySQL
Experiment metrics table created
Pipeline finished successfully
Learning Outcomes

This project demonstrates practical experience with:

Experimentation analytics

A/B testing evaluation

Cloud-based data pipelines

SQL data transformation

Data visualization

Automated analytics workflows

Future Improvements

Possible enhancements:

Add statistical significance testing (Z-test / p-value)

Implement Airflow for orchestration

Store experiment logs in a monitoring system

Expand dashboard with deeper user segmentation

Author

Jai Kishan

AI & Data Science Graduate
Aspiring Data Analyst / Data Scientist


