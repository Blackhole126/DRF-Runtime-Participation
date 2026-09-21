"""E2E proof: SVACS runtime adapter -> canonical Capability Registry REST contract -> discovery."""
import json, os, sys
import requests
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')); sys.path.insert(0,ROOT)
from runtime_participation import registration_payload, register_runtime, discover_self
url=os.getenv('CAPABILITY_REGISTRY_URL','http://127.0.0.1:18001').rstrip('/')
# Keep adapter pointed at the actual test registry process.
import runtime_participation as rp
rp.REGISTRY_URL=url
payload=registration_payload()
result=register_runtime(); discovered=discover_self()
checks={'registration_status': result.get('status') in {'REGISTERED','DUPLICATE_ALREADY_REGISTERED'},
        'canonical_fields': set(payload)=={'name','description','category','version','author'},
        'discovered_identity': isinstance(discovered,dict) and discovered.get('name')==payload['name']}
report={'phase':'2','verification':'runtime-to-registry E2E','checks':checks,'passed':all(checks.values()),
        'registration_status':result.get('status'),'response_status':result.get('response_status'),
        'discovered':discovered}
os.makedirs(os.path.join(ROOT,'reports','phase2'),exist_ok=True)
with open(os.path.join(ROOT,'reports','phase2','REGISTRY_RUNTIME_E2E.json'),'w') as f: json.dump(report,f,indent=2)
print(json.dumps(report,indent=2)); raise SystemExit(0 if report['passed'] else 1)
