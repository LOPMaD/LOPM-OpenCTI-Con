import requests
from pydantic import HttpUrl


class LopmConnectorClient:

    def get_entities(self, params=None) -> dict:
        
        # If params is None, retrieve all CVEs in National Vulnerability Database
        # :param params: Optional Params to filter what list to return
        # :return: A list of dicts of the complete collection of CVE from NVD

        try:
            
            r = requests.request('GET', "https://phishing.army/download/phishing_army_blocklist.txt")
            start_index = 446
            raw_text = r.text[start_index:]
            block_list = [
            line.strip()                     
            for line in raw_text.splitlines()
            ]


            return block_list

            raise NotImplementedError
        
        except:
            print("LopmClient")
        # except Exception as err:
        #     self.helper.connector_logger.error(err)