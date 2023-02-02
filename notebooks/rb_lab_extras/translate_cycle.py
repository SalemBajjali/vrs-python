import json
import json
import csv
from ga4gh.vrs import __version__, models, normalize
from ga4gh.core import ga4gh_digest, ga4gh_identify, ga4gh_serialize
from ga4gh.vrs.dataproxy import SeqRepoRESTDataProxy
from biocommons.seqrepo import SeqRepo
from ga4gh.vrs.extras.variation_normalizer_rest_dp import VariationNormalizerRESTDataProxy
from variation_services_rest_db import VariationServicesRESTDataProxy
from ga4gh.vrs.extras.translator import Translator
import pandas as pd

vnorm = VariationNormalizerRESTDataProxy()
vs = VariationServicesRESTDataProxy()


seqrepo_rest_service_url = "https://services.genomicmedlab.org/seqrepo"
dp = SeqRepoRESTDataProxy(base_url=seqrepo_rest_service_url)


tlr = Translator(data_proxy=dp,
                 translate_sequence_identifiers=True,  # default
                 normalize=True,                       # default
                 identify=True)   



# input the dataset for now we are going to start with SPDI. 
# This is going to be a file with 4 columns. 


# Load the test_spdi table
with open('/infodev1/cim/Salem/ga4ghprojects/vrs-python/notebooks/data/spdi_test_data.csv', 'r') as f:
    reader = csv.reader(f)
    spdi_id_list = []
    for row in reader:
        records = spdi_id_list.append(':'.join(row))

header = spdi_id_list.pop(0)

rshifthgvs = []
for spdi_expr in spdi_id_list:
    try: 
        # Converting a allele in SPDI syntax to the right-shifted HGVS notation
        rshifthgvs.append(vs.spdi2hgvs(spdi_expr))
    except: 
        rshifthgvs.append('{0} {1}'.format('ERROR in the syntext',spdi_expr))

alleles = []
for expr in spdi_id_list:
    try:
        trans = tlr.translate_from(expr)
        alleles.append(trans)
    except:
        alleles.append('{0} {1}'.format('ERROR in the syntext',expr))

vrs_allele_dict = {}

for expr in spdi_id_list:
    try:
        trans = tlr.translate_from(expr)
        # TODO: make sure this json.dumps is actually working
        vrs_allele_dict[ga4gh_identify(trans)] = json.dumps(trans.as_dict())
    except:
        vrs_allele_dict["ERROR in the syntext"] = expr

norm_hgvs_exprs = []

for allele in alleles:
    if isinstance(allele, str):
        norm_hgvs_exprs.append('[{0} {1}]'.format('ERROR in the syntext',expr))
    else: 
        vrs_allele = vnorm.to_hgvs(allele, 'refseq')
        norm_hgvs_exprs.append(vrs_allele)



mydict = {'spdi_expression': spdi_id_list,
          #'ga4gh_identifier': vrs_allele_dict.keys(),
        'rightshift_hgvs_expression': rshifthgvs, 
        'normalized_hgvs_expressions': norm_hgvs_exprs}


df1 = pd.DataFrame(mydict)
df2 = pd.DataFrame(vrs_allele_dict.items(), columns=['ga4gh_id','vrs_allele_obejct'])

frames = [df1, df2]

result = pd.concat(frames,axis = 1)

result.to_csv('/infodev1/cim/Salem/ga4ghprojects/vrs-python/notebooks/data/output_test.csv') 