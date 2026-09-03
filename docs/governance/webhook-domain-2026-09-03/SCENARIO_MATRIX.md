# Scenario Matrix

| Scenario | Result | Status |
|---|---|---|
| n8n container after recreation | healthy | passed |
| Container webhook base URL | requested hydrogen domain | passed |
| Container editor base URL | requested hydrogen domain | passed |
| Workflow remains active | true | passed |
| GET registration | intellicad | passed |
| POST registration | intellicad | passed |
| Editor workflow URL | HTTP 200 | passed |
| Direct n8n webhook GET | HTTP 200 | passed |
| Public valid verification challenge | HTTP 200 and exact match | passed |
| Secret disclosure | none in evidence/Git | passed |
