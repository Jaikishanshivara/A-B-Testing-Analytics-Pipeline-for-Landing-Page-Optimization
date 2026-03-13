import boto3
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

import logging

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("pipeline started")

try:
    # ---------- S3 DOWNLOAD ----------
    bucket_name = "ab-testing-data-jai"
    file_key = "ab_data.csv"
    local_file = "ab_data.csv"

    s3 = boto3.client("s3")
    s3.download_file(bucket_name, file_key, local_file)

    logging.info("File downloaded from S3")

    # ---------- LOAD DATA ----------
    df = pd.read_csv(local_file)
    logging.info(f"Rows loaded: {len(df)}")

    # ---------- CLEAN DATA ----------
    df = df.drop_duplicates(subset='user_id')
    df = df.dropna()

    df = df[((df['group']=='control') & (df['landing_page']=='old_page')) |
            ((df['group']=='treatment') & (df['landing_page']=='new_page'))]

    # ---------- DATABASE CONNECTION ----------
    username = "root"
    password = quote_plus("J@ikishan08")

    engine = create_engine(
        f"mysql+pymysql://{username}:{password}@localhost:3306/ab_testing"
    )

    # ---------- LOAD RAW TABLE ----------
    df.to_sql("ab_test_raw", engine, if_exists="replace", index=False)

    logging.info("Data loaded to MySQL")

    # ---------- CREATE METRICS ----------
    with engine.connect() as conn:

        conn.execute(text("DROP TABLE IF EXISTS experiment_results"))

        conn.execute(text("""
            CREATE TABLE experiment_results AS
            SELECT
                `group`,
                COUNT(user_id) AS users,
                SUM(converted) AS conversions,
                ROUND(AVG(converted)*100,2) AS conversion_rate
            FROM ab_test_raw
            GROUP BY `group`
        """))

        conn.commit()

    logging.info("Experiment metrics table created")
    logging.info("Pipeline finished successfully")

except Exception as e:

    logging.error(f"Pipeline failed: {e}")