import requests
from pydantic import HttpUrl


class LopmConnectorClient:

    duplicate_set = set() 
    def get_entities(self, params=None) -> dict:
        
        # If params is None, retrieve all CVEs in National Vulnerability Database
        # :param params: Optional Params to filter what list to return
        # :return: A list of dicts of the complete collection of CVE from NVD

        try:
            
            r = requests.request('GET', "https://phishing.army/download/phishing_army_blocklist.txt")
            lines = r.text[446:].splitlines()
            
            block_list = []
            for line in lines:
                clean_line = line.strip()
                if clean_line and clean_line not in self.duplicate_set:
                    block_list.append(clean_line)
                    self.duplicate_set.add(clean_line)

            return block_list

            raise NotImplementedError
        
        except:
            print("LopmClient")
        # except Exception as err:
        #     self.helper.connector_logger.error(err)