## Dependencies installation:

- run pip install -r requirements.txt


## Installation of Dozerdb

- link to dozerdb: http://dozerdb.org/
    - download using this link for windows: https://dist.dozerdb.org/dozerdb-5.19.0.0-alpha.1-windows.zip
- extract the zip file
- Install JDK version (17-21)
- download apoc from https://github.com/neo4j/apoc/releases/download/5.19.0/apoc-5.19.0-core.jar (apoc version should match with neo4j version) and add this file in plugins folder
- go to conf folder and activate all procedures by adding following text in neo4j.conf file: dbms.security.procedures.unrestricted=*
- in conf folder create file named as apoc.conf and add the following text in it for enabling import functionality: apoc.import.file.enabled=true
- Install dozerdb as windows service by typing following command in cmd:
    - bin\neo4j windows-service install
- run dozerdb from cmd as: bin\neo4j-admin server console


## Configuration of dozerdb
- put username as neo4j and password as neo4j
- then create new password as 'password'



## evironment variable

- in .env file change values of following variable
    - your groq api in 'GROQ_API_KEY'
    - pdf file in 'PDF_DIR'
    - dozerdb file path in 'Dozerdb'
    - database name in 'NEO4J_DATABASE'


## Knowledge graph creation

- run 'main.py'


## Retrieval

- run retreivel.py for retrievel depending on the query



