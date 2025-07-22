---
noteId: "a5c433d0669311f0a8d32f47963ec631"
tags: []

---

## deploy chromaDB on GCP

to deploy chromaDB on GCP, i used the steps used on the following repo. https://github.com/HerveMignot/chromadb-on-gcp/tree/main

here is the summary

### create bucket
gsutil mb -p fusion-ai-wil02 -l us-central1  gs://fusion-ai-wil02-bucket/

### set all the necessary variables
* export SERVICE_NAME=""
* export SERVICE_ACCOUNT=""
* export SERVICE_REGION=""
* export API_TOKEN="" --this is used for to authenticate with chromaDB
* export BUCKET_NAME=""
* export MIN_INSTANCES=1  # Set to 1 to keep the service always on
* export project_id=""

### create deploy.yml file and then
run `gcloud run services replace deploy.yaml --project fusion-ai-wil02`

### then allow authenticated access by:
run
 gcloud run services add-iam-policy-binding chroma    --member=allUsers --role=roles/run.invoker --region=us-central1 --project=<project-id>

### test access using python code and API token

import chromadb
from chromadb.config import Settings

### Create a Chroma client with the service URL and API token

client = chromadb.HttpClient(host="<YOUR_SERVICE_URL>", port=443, ssl=True,
        settings=Settings(chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
        chroma_client_auth_credentials="xxyz",
        anonymized_telemetry=False))

