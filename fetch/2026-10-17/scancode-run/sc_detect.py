import sys,types,json
m=types.ModuleType('typecode.magic2'); m.file_type=lambda *a,**k:'ASCII text'; m.mime_type=lambda *a,**k:'text/plain'; m.libmagic_version=lambda *a,**k:'stub'
class _E(Exception): pass
m.NoMagicLibError=_E; sys.modules['typecode.magic2']=m
from scancode.api import get_licenses
for p in sys.argv[1:]:
  r=get_licenses(p, include_text=False)
  ld=r.get('license_detections',[])
  print('==',p,'| detected_license_expression:',r.get('detected_license_expression'),'| spdx:',r.get('detected_license_expression_spdx'))
  for d in ld:
    print('   det:',d.get('license_expression'),'|',d.get('detection_log'),'| n_matches',len(d.get('matches',[])))
  print('   clues:',[ (c.get('license_expression'),c.get('start_line')) for c in r.get('license_clues',[])])
