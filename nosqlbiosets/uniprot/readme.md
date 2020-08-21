
# Index/query scripts for UniProtKB datasets

* [index.py](index.py): Index UniProtKB xml files

  _Tested with Swiss-Prot dataset only, (December 2019 release)_
  
    ```
    ./nosqlbiosets/uniprot/index.py --help
    usage: index.py [-h] [--index INDEX] [--doctype DOCTYPE] [--host HOST]
                    [--port PORT] [--db DB]
                    infile
    
    Index UniProt xml files, with MongoDB
    
    positional arguments:
      infile             Input file name for UniProt Swiss-Prot compressed xml
                         dataset
    
    optional arguments:
      -h, --help         show this help message and exit
      --index INDEX      Name of MongoDB database
      --doctype DOCTYPE  Document type name for collection name for MongoDB
      --host HOST        MongoDB server hostname
      --port PORT        MongoDB server port number
      --db DB            Database: 'MongoDB'
    ```

* [query.py](query.py): Query API, at its early stages of development

* [../../tests/test_uniprot_queries.py](test_uniprot_queries.py):
 Tests for the query API

                                      
## Usage

Example command lines for downloading `uniprot_sprot.xml` file and for indexing:

#### Download UniProt/Swiss-Prot data set

```bash
mkdir -p data
# ~720M(compressed), ~165.6 million lines, ~560,500 entries
wget -nc -P ./data ftp://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/\
knowledgebase/complete/uniprot_sprot.xml.gz
```

#### Index with MongoDB
If you have not already installed nosqlbiosets project see the Installation
section of the [readme.md](../../readme.md) file on project main folder._

Server default connection settings are read from [../../conf/dbservers.json](
../../conf/dbservers.json
)

```bash
# Index with MongoDB, typically requires about 1 to 2 hours
./nosqlbiosets/uniprot/index.py ./data/uniprot_sprot.xml.gz\
 --host localhost --db MongoDB --index biosets
```

