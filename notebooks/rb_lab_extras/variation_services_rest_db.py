import requests
import json
import sys

# Useful links: 
    # https://ngdc.cncb.ac.cn/gwh/assembly/history
    # https://api.ncbi.nlm.nih.gov/variation/v0/
    # https://github.com/ncbi/dbsnp
    # https://github.com/ncbi/dbsnp/blob/master/tutorials/Variation%20Services/Jupyter_Notebook/spdi_batch.ipynb

class VariationServicesRESTDataProxy:
    """
    Rest data proxy for Variation Services API
    """
    def __init__(self) -> None:
        """
        Initialize class with the API URL
        """
        self.api = 'https://api.ncbi.nlm.nih.gov/variation/v0/'

# TODO: change the name of this function, not the best name 
    def spdi_syntex(self,r):
        reqjson = json.loads(r.text)
        spdiobjs = reqjson['data']['spdis'] #[0] Index at first position for the first spdi object. 
        expr_list = []
        for spdiobj in spdiobjs:
            spdi = ':'.join([
                spdiobj['seq_id'],
                str(spdiobj['position']),
                spdiobj['deleted_sequence'],
                spdiobj['inserted_sequence']])
            expr_list.append(spdi)
        return expr_list

    def spdi2hgvs(self,spdi):
        """
        Converting a allele in SPDI syntax to the right-shifted HGVS notation
        """
    
        r = requests.get(
            url = "{}spdi/{}/hgvs".format(self.api,spdi),
            headers={ "Content-Type": "application/json; charset=utf-8" }
        )

        if r.status_code == 200:
            return json.loads(r.text)['data']['hgvs'] 
        else:
            raise requests.HTTPError(f"Variation Services returned the status code: {r.status_code}.")
        
    def hgvs2spdi(self,expr, assembly ='GCF_000001405.38'):
        """
        Convert HGVS notation to allele in SPDI syntax 
        """
        
        r = requests.get(
            url = "{}hgvs/{}/contextuals?assembly={}".format(self.api,expr,assembly),
            headers={ "Content-Type": "application/json; charset=utf-8" }
        )

        if r.status_code == 200:
            return self.spdi_syntex(r)
        else:
            raise requests.HTTPError(f"Variation Services returned the status code: {r.status_code}.")
