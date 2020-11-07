# microservices
Micro Services for the POC online store orchestration using Camunda


This Repository currently includes 3 dummy Flask APIs.

Stock API
Shipment API
Payment API

Each of these APIs contains a dummy implementation which for now will always approve the requests.

TODO:

Each of the 3 collaborators will implement one of the APIs.
The APIs will be talking to the orchestrator so we need to make sure that the IO information is correctly configured on Both ends. Refer to the orchestration service provided in the other project.

