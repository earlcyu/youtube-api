import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account



class BigQuery:
    '''
    A class that represents a BigQuery instance

    Attributes
    ----------
    service_account_file : str
        the file path of the service account credentials

    Methods
    -------
    load_data(load_type: str, job_schema: str, data: pd.DataFrame, target_dataset: str, target_table: str)
        Loads a given dataframe into a table; overwrites existing data
    '''

    def __init__(self, service_account_file: str) -> None:
        # Construct a BigQuery client object.
        self.client = bigquery.Client()
        self.service_account_file = service_account_file

    def connect(self):
        '''Connects to the BigQuery destination'''
        self.connection = service_account.Credentials.from_service_account_file(
            self.service_account_file
        )
        
    def disconnect(self) -> bool:
        '''Disconnects from the BigQuery destination'''
        self.connection = None

    def load_data(
        self, 
        load_type: str,
        job_schema: str, 
        data: pd.DataFrame, 
        target_dataset: str, 
        target_table: str
    ):
        '''
        Loads a given dataframe into a table; overwrites existing data
        
        Parameters
        ----------
        load_type : str
            WRITE_TRUNCATE or WRITE_APPEND
        job_schema : str
            a string of columns and their data types 
            e.g., first_name:STRING,birthday:DATE,salary:FLOAT
        data : pd.DataFrame
            the dataframe to load into BigQuery
        target_dataset : str
            the destination dataset of where to load the given dataframe
        target_table : str
            the destination table of where to load the given dataframe
        '''
        
        # Define load parameter
        if load_type == 'overwrite':
            load_parameter = 'WRITE_TRUNCATE'
        elif load_type == 'append':
            load_parameter = 'WRITE_APPEND'
        
        # Specify the job configuration
        job_config = bigquery.LoadJobConfig(
            autodetect=True, # Autodetect the schema
            write_disposition=load_parameter
        )

        # Set the provided schema if it has been provided
        if job_schema:
            columns = [column.split(':') for column in job_schema.split(',')]
            schema = [bigquery.SchemaField(col_name, dtype) for col_name, dtype in columns]
            print(columns)
            print(schema)
            job_config.schema = schema 

        # Define table ID
        table_id = f'{target_dataset}.{target_table}'

        # Make an API request.
        job = self.client.load_table_from_dataframe(
            dataframe=data, 
            destination=table_id, 
            job_config=job_config
        )
        
        # Wait for the job to complete
        job.result()
        print(
            f'Loaded {len(data)} rows and {len(data.columns)} columns to {table_id}'
        )
