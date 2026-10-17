import sys,types
m=types.ModuleType('typecode.magic2')
m.file_type=lambda *a,**k:''; m.mime_type=lambda *a,**k:''; m.libmagic_version=lambda *a,**k:'stub'
class _E(Exception): pass
m.NoMagicLibError=_E
sys.modules['typecode.magic2']=m
import sys,json
from licensedcode.cache import get_index
idx=get_index()
out={}
for p in sys.argv[1:]:
  t=open(p,encoding='utf-8').read()
  ms=idx.match(query_string=t)
  out[p]=[{'license_expression':m.rule.license_expression,'rule':m.rule.identifier,'score':round(m.score(),2),'coverage':round(m.coverage(),2),'matcher':m.matcher,'start_line':m.start_line,'end_line':m.end_line} for m in ms]
print(json.dumps(out,indent=1,ensure_ascii=False))
