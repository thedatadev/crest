package main

import (
	"fmt"
	"log"
	"net/http"

	"./database"
	"./resources/todo"
)

func main() {

	// ----- Set up data store -------
	database.Initialise()

	// ----- Register handlers -------
	http.HandleFunc("/todo", todo.Handler)

	// ----- Listen for requests -----
	fmt.Println("Server running on http://127.0.0.1:8080/")
	log.Fatal(http.ListenAndServe(":8080", nil))

}
