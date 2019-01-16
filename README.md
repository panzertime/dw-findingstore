# Dark Web Findingstore 

A tool for threat intelligence researchers to store, search, and share findings from the dark web. 

Findingstore is an Elasticsearch-backed Flask application that stores "finding cards," which package full-text and binary artifacts with metadata useful to threat researchers. Findingstore users can search cards, download artifacts, and import and export cards. Exported cards can be shared with other threat research teams, to be imported into private Findingstore instances.

## An example use case

A threat researcher digging through a particular Russian-language dark web marketplace may discover stolen credit cards for sale. The researcher could take a screenshot of the listing, create a new card in Findingstore, upload the screenshot, attach an English translation of the listing, and add tags and other data to connect the found listing to prior findings.

This card can then be exported and shared, or simply left in Findingstore to contextualize future findings.

## Running Findingstore

Application works in a Docker container environment.

### Project Setup

##### Create a Docker Instance in VirtualBox

1. Use Docker Machine to create a Docker instance.
`docker-machine create -d "virtualbox" findingstore`
2. Connect to the Docker daemon.
`eval $(docker-machine eval findingstore)`
3. ES requires a memory bump, so update the Docker service manually.
`docker-machine ssh findingstore sudo sysctl -w vm.max_map_count=262144`
4. Use Docker Compose to build and start the application.
`docker-compose up --build`
5. After the ES service comes up, run `tools/prep_elastic.sh` to create the FindingStore Index.
