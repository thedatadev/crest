package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func prompt() string {
	reader := bufio.NewReader(os.Stdin)
	// Receive user's answer
	answer, promptError := reader.ReadString('\n')
	if promptError != nil {
		panic(promptError)
	}
	// Remove trailing '\n'
	answer = strings.Replace(answer, "\n", "", -1)
	return answer
}

func getAnswer(choices []string) string {

	// Present user with options
	if choices != nil {
		fmt.Print("[ ")
		for _, choice := range choices {
			fmt.Printf("%s ", choice)
		}
		fmt.Print("] ")
	}

	answer := prompt()

	// Return answer if valid
	if choices == nil {
		return answer
	}
	for _, choice := range choices {
		fmt.Printf("Comapring %s with %s.\n", answer, choice)
		if answer == choice {
			// To remove the trailing line break \n
			return answer
		}
	}
	return ""
}

func promptSingle(question string, choices ...string) string {

	fmt.Print(question)
	answer := getAnswer(choices)
	for {
		if answer != "" {
			break
		}
		if choices != nil {
			fmt.Print("Please choose a valid option: ")
		}
		answer = getAnswer(choices)
	}
	return answer
}

func promptMulti(question string) []string {

	fmt.Print(question)
	reader := bufio.NewReader(os.Stdin)
	// Receive user's answer
	answer, promptError := reader.ReadString('\n')
	if promptError != nil {
		panic(promptError)
	}
	// Remove trailing '\n'
	answer = strings.Replace(answer, "\n", "", -1)
	// Split answers
	return strings.Split(answer, " ")
}

func buildProject(name string, frontend string, backend string, resources []string, components []string) {
	fmt.Printf("%v %v %v %v %v\n", name, frontend, backend, resources, components)
}

func main() {

	fmt.Println("==== Crest - Create a RESTful project base ====")
	name := promptSingle("What is your project name? ")
	frontend := promptSingle("What is your project frontend? ", "react", "vue", "reframe", "angular")
	backend := promptSingle("What is your project backend? ", "go", "flask", "node", "clojure")
	resources := promptMulti("What are your project resources? ")
	components := promptMulti("What are your project components? ")

	buildProject(name, frontend, backend, resources, components)

}
