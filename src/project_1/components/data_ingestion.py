import os
import sys
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.project_1.exception import CustomException
from src.project_1.logger import logging

from src.project_1.components.data_transformation import DataTransformation
from src.project_1.components.model_trainer import ModelTrainer


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()


    def initiate_data_ingestion(self):

        logging.info("Entered the Data Ingestion component")

        try:
            # Correct dataset path
            df = pd.read_csv("notebook/StudentsPerformance.csv")

            logging.info("Dataset read successfully as dataframe")

            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path),
                exist_ok=True
            )

            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split started")

            train_set, test_set = train_test_split(
                df,
                test_size=0.2,
                random_state=42
            )

            train_set.to_csv(
                self.ingestion_config.train_data_path,
                index=False,
                header=True
            )

            test_set.to_csv(
                self.ingestion_config.test_data_path,
                index=False,
                header=True
            )

            logging.info("Data ingestion completed successfully")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":

    logging.info("Data pipeline execution started")

    obj = DataIngestion()

    train_data, test_data = obj.initiate_data_ingestion()

    logging.info("Data Transformation started")

    data_transformation = DataTransformation()

    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
        train_data,
        test_data
    )

    logging.info("Model Training started")

    modeltrainer = ModelTrainer()

    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))