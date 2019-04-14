# Crest - Go REST API Endpoint

## Directory

_ root
    |_ database
    |   |_ connection.go
    |   |_ setup.go
    |_ models
    |   |_ {{for each resource}}.go
    |_ resources
    |   |_ {{for each resource}}
    |       |_ handler.go
    |       |_ get.go
    |       |_ post.go
    |       |_ put.go
    |       |_ delete.go
    |_ main.go
    |_ README.md

## File/folder initialisation

### Database
- The connection.go file stores a global database connection that is shared throughout the application
- The setup.go file contains functions which establish a connection to the database server

### Models
- This contains a model file for each resource

### Resources
- This contains a folder for each resource
- Inside each folder is one file for each major HTTP status method
- Additionally, there is a handler.go file which routes requests by HTTP status method

