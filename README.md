# Crest - "create RESTful apps"

## Overview
A utility to generate a quick project skeleton involving REST APIs and reactive frontends whether for a small project or for prototyping.

Frontend:
- React
- Vue
- Angular
- ClojureScript

Backend:
- NodeJS
- Go
- Python
- Clojure

## Description
This command line utility allows you to generate project skeletons from user-provided project templates for client and RESTful server applications. The user provides a list of resources to be used in the backend, and the tool generates all necessary boilerplate pertaining to those resources e.g. database models, schemas, and modules. Similarly, the tool also prompts the user for names of components to be used on the frontend and generates the folders and boilerplate files for each component.

## How it works
The user provides their own templates inside the client and server directories which need to follow a particular naming/extension schema. This is how the tool can identify what folders and files it needs to generate, given the resources and components provided by the user. The tool identifies folders and files marked with a ".crest" suffix. There is also a secondary suffix which precedes the ".crest" extension. Each of these suffixes tells crest what it should generate:

- ".based_on_parent_folder.crest" - generates all files in the current directory, naming them after the current directory
- ".resources.crest" - generate a file or folder for each resource provided by the user
- ".components.crest" - generate a file or folder for each component provided by the user
- ".container.crest" - generates a container file and interpolates all lib imports

Refer to the comments in the code for detailed explanations for each suffix/extension.