import time
import pandas as pd
import os
from entsoe import EntsoePandasClient
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_fixed


class EUZOnalInput():
    '''
    All EU_Zonal inputs.
    '''

    def __init__(self, file, header='infer', col_names=None):
        self.file = file
        self.df = None
        self.header = header
        self.col_names = col_names
        
    def get_data(self, *args, **kwargs):
        if self.df is None:
            self.read_data(*args, **kwargs)
        return self.df.copy()


class CSVInput(EUZOnalInput):
    '''
    ReEDS EU_Zonal .csv input files.
    '''
    def read_data(self, *args, **kwargs):
        if self.df is None:
            self.df = pd.read_csv(
                        os.path.join(
                            self.file
                        ),
                        header=self.header,
                        **kwargs
            )
            if self.col_names is not None:
                self.df.columns = self.col_names


class EntsoePandasClient():
    """ Client to perform API calls and return the data parsed
    as a Pandas Series or DataFrame
    """
    def __init__(
        self,
        api_key: str,
    ):
        if api_key is None:
            raise TypeError("API key cannot be None")
        self.api_key = api_key
        self.client = EntsoePandasClient(api_key=api_key)

    @retry(ConnectionError, tries=5, delay=1)
    def _base_query(
        self,
        query_func,
        *args,
        **kwargs
    ):
        """
        Queries the ENTSO-E TP by the query function and parameters.
        Retries on a connection error or if too many requests are made.
        Returns the response content as a string.
        """
        try:
            response = query_func(self.client, **kwargs)
            response.raise_for_status()
        except ConnectionError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to query data: {str(e)}")
        # Return the response content as a string
        return response.text

    def query_crossborder_flows(
        self,
        country_from,
        country_to,
        start_date,
        end_date,
    ):
        crossborder_flows = self._base_query(
            self.client.query_crossborder_flows,
            country_from=country_from,
            country_to=country_to,
            start=start_date,
            end=end_date,
        )

        return crossborder_flows

    def query_scheduled_exchanges(
        self,
        country_from,
        country_to,
        start_date,
        end_date,
    ):
        scheduled_exchanges = self._base_query(
            self.client.scheduled_exchanges,
            country_from=country_from,
            country_to=country_to,
            start=start_date,
            end=end_date,
        )
        return scheduled_exchanges


# All inputs for the India Zonal PCM based on ReEDS-India data
INPUTS = {
    'nodes': CSVInput(
        os.path.join(
            'io',
            'inputs',
            'zones.csv')
        )
}
