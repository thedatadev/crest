package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
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

func walkFnWrapper(name string) filepath.WalkFunc {
	return func(path string, info os.FileInfo, err error) error {

		// The directory where all the template files and folders are from
		sourceBase := "/Users/developer/dev/code/projects/crest/go_imp/src"

		cwd, getcwdError := os.Getwd()
		if getcwdError != nil {
			panic(getcwdError)
		}

		// The directory where all the template files and folders are going
		targetBase := filepath.Join(cwd, name)

		targetSuffix := strings.TrimPrefix(path, sourceBase)

		// The path in the target directory for the new file or folder
		newFilepath := filepath.Join(targetBase, targetSuffix)

		if info.IsDir() {
			fmt.Printf("mkdir %s\n", newFilepath)
			mkdirErr := os.Mkdir(newFilepath, os.ModePerm)
			if mkdirErr != nil {
				panic(mkdirErr)
			}
		} else {
			fmt.Printf("write file %s\n", newFilepath)
			data, readFileErr := ioutil.ReadFile(path)
			if readFileErr != nil {
				panic(readFileErr)
			}
			writeFileErr := ioutil.WriteFile(newFilepath, data, os.ModePerm)
			if writeFileErr != nil {
				panic(writeFileErr)
			}
		}

		return nil
	}
}

func walkDir() {

	// TODO: change this to be dynamic; build an executable and use os.executable's path
	root := "/Users/developer/dev/code/projects/crest/go_imp/src"

	walkErr := filepath.Walk(root, walkFnWrapper("myApp"))

	if walkErr != nil {
		panic(walkErr)
	}

}

func main() {

	// fmt.Println("==== Crest - Create a RESTful project base ====")
	//// TODO: validate project name i.e. has legal characters
	// name := promptSingle("What is your project name? ")
	// frontend := promptSingle("What is your project frontend? ", "react", "vue", "reframe", "angular")
	// backend := promptSingle("What is your project backend? ", "go", "flask", "node", "clojure")
	// resources := promptMulti("What are your project resources? ")
	// components := promptMulti("What are your project components? ")

	// buildProject(name, frontend, backend, resources, components)

	walkDir()

}
