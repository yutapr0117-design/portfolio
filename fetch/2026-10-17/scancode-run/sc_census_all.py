import sys,types,json,os
m=types.ModuleType('typecode.magic2'); m.file_type=lambda *a,**k:''; m.mime_type=lambda *a,**k:''; m.libmagic_version=lambda *a,**k:'stub'
class _E(Exception): pass
m.NoMagicLibError=_E; sys.modules['typecode.magic2']=m
from licensedcode.cache import get_index
idx=get_index()
L=json.load(open('lld2/json/licenses.json'))['licenses']
osi=[x for x in L if not x.get('isDeprecatedLicenseId')]
out=[]
for x in osi:
  p=f"lld2/text/{x['licenseId']}.txt"
  if not os.path.exists(p): out.append({'id':x['licenseId'],'osi':x.get('isOsiApproved'),'fsf':x.get('isFsfLibre'),'missing':True}); continue
  ms=idx.match(query_string=open(p,encoding='utf-8',errors='replace').read())
  out.append({'id':x['licenseId'],'osi':x.get('isOsiApproved'),'fsf':x.get('isFsfLibre'),'n':len(ms),'exprs':sorted(set(m.rule.license_expression for m in ms)),
   'spdx_keys':sorted(set(k for m in ms for k in [m.rule.license_expression])),
   'max_cov':max([round(m.coverage(),1) for m in ms] or [0]),
   'proprietary':[m.start_line for m in ms if 'proprietary' in m.rule.license_expression]})
json.dump(out,open('sc_all_census.json','w'),indent=1)
print(len(out))
