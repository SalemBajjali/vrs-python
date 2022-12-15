import requests
from pprint import pp

allele_info = {'q':['NC_000007.13:g.140453136A>T'],'untranslatable_returns_text': False}
# r = requests.get("https://normalize.cancervariants.org/variation")
r = requests.get("https://normalize.cancervariants.org/variation/to_vrs",params= allele_info) 

r_dict = r.json()
print(r_dict['variations'])
pp(r.json())
#print(r.url)

