import pandas as pd
from google.cloud import bigquery



class BigQuery:
    '''
    A class that represents a BigQuery instance

    Attributes
    ----------

    Methods
    -------
    load_data(df: pd.DataFrame, table_id: str)
        Loads a given dataframe into a table; overwrites existing data
    '''

    def __init__(self) -> None:
        # Construct a BigQuery client object.
        self.client = bigquery.Client()

    def load_data(self, df: pd.DataFrame, table_id: str):
        '''
        Loads a given dataframe into a table; overwrites existing data
        
        Parameters
        ----------
        df : pd.DataFrame
            the dataframe to load into BigQuery
        table_id : str
            the destination table of where to load the given dataframe
        '''
        # Specify the job configuration
        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("title", bigquery.enums.SqlTypeNames.STRING),
                bigquery.SchemaField("wikidata_id", bigquery.enums.SqlTypeNames.STRING),
            ],
            write_disposition="WRITE_TRUNCATE",
        )

        # Make an API request.
        job = self.client.load_table_from_dataframe(
            dataframe=df, 
            destination=table_id, 
            job_config=job_config
        )
        
        # Wait for the job to complete
        job.result()
        print(
            f'Loaded {len(df)} rows and {len(df.columns)} columns to {table_id}'
        )