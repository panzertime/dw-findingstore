# Dark Web Findingstore 

A tool for threat intelligence researchers to store, search, and share findings from the dark web. 

Findingstore is an Elasticsearch-backed Flask application that stores "finding cards," which package full-text and binary artifacts with metadata useful to threat researchers. Findingstore users can search cards, download artifacts, and import and export cards. Exported cards can be shared with other threat research teams, to be imported into private Findingstore instances.

## An example use case

A threat researcher digging through a particular Russian-language dark web marketplace may discover stolen credit cards for sale. The researcher could take a screenshot of the listing, create a new card in Findingstore, upload the screenshot, attach an English translation of the listing, and add tags and other data to connect the found listing to prior findings.

This card can then be exported and shared, or simply left in Findingstore to contextualize future findings.

## Running Findingstore

The "tools" directory contains scripts which prepare an environment and run the app.
1. `setup.sh` locally installs a compatible Elasticsearch instance via Docker. Useful for development
2. `start_elastic.sh` runs the ES instance installed by `setup.sh`. Useful for development
3. `prep_elastic.sh` creates Findingstore's index and mapping in ES. Must be run before Findingstore can be used
4. `start_frontend.sh` loads Findingstore's dependencies (by activating a virtualenv) and runs a development WSGI server. Useful for development, not appropriate for production use
