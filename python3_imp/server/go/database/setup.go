package database

import (
	"database/sql"
	"fmt"
	"os"

	// Required to connect to the Postgres database
	_ "github.com/lib/pq"
)

const (
	host   = "DBHOST"
	name   = "DBNAME"
	port   = "DBPORT"
	user   = "DBUSER"
	pass   = "DBPASS"
	dbtype = "DBTYPE"
)

// Initialise establishes a connection between the app and the database server
func Initialise() {
	config := loadConfig()
	credentials := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		config[host], config[port], config[user], config[pass], config[name])
	var err error
	Connection, err = sql.Open(config[dbtype], credentials)
	if err != nil {
		panic(err)
	}
	err = Connection.Ping()
	if err != nil {
		panic(err)
	}
	fmt.Printf("Successfully connected to database: host=%s name=%s port=%s\n",
		config[host], config[name], config[port])
}

func loadConfig() map[string]string {
	config := make(map[string]string)
	fields := []string{host, user, name, port, pass, pass, dbtype}
	for _, field := range fields {
		value, ok := os.LookupEnv(field)
		if !ok {
			panic(fmt.Sprintf("The %s environment variable is required to set up the database", field))
		}
		config[field] = value
	}
	return config
}
