/*
 * Crest - create a RESTful project skeleton
 * Written by Edrian Gomez 2019
 */

package main

import (
	"bufio"
	"fmt"
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

func nonCrestHandler() {

}

func customContentHandler(newFilepath string, projectName string, resources []string, components []string) {
	fmt.Println("Injecting project data into the custom content file")
}

func parentFilenameHandler() {
	fmt.Println("Generating file/folder based on parent")
	// Extract the parent dir name

	// Create a new file path based on parent dir name

	// Execute template
}

func resourceFilenameHandler() {
	fmt.Println("Generating file/folder based on resource")

	// If file

	// For each resource

	// Create a new filepath

	// Read the original template

	// Inject resources into template

	// If dir

	// duplicate a new dir for each resource
}

func componentFilenameHandler() {
	fmt.Println("Generating file/folder based on component")

	// If file

	// For each component

	// Create a new filepath

	// Read the original template

	// Inject component info into template

	// If dir

	// duplicate a new dir for each component
}

func customeNameHandler(newFilepath string, projectName string, resources []string, components []string) {
	switch filepath.Ext(newFilepath) {
	case ".parent":
		parentFilenameHandler()
	case ".resources":
		resourceFilenameHandler()
	case ".components":
		componentFilenameHandler()
	default:
		fmt.Printf("Warning: Crest (custom filename) extension %s is not recognised")
	}
}

func crestHandler(newFilepath string, projectName string, resources []string, components []string) {

	switch filepath.Ext(newFilepath) {
	case ".customContent":
		newFilepath = strings.TrimSuffix(newFilepath, ".customContent")
		customContentHandler(newFilepath, projectName, resources, components)
	case ".customeName":
		newFilepath = strings.TrimSuffix(newFilepath, ".customeName")
		customeNameHandler(newFilepath, projectName, resources, components)
	default:
		fmt.Printf("Warning: Crest extension %s is not recognised")
	}

}

func walkFnWrapper(projectName string, sourceBase string, resources []string, components []string) filepath.WalkFunc {
	return func(path string, info os.FileInfo, err error) error {

		cwd, getcwdError := os.Getwd()
		if getcwdError != nil {
			panic(getcwdError)
		}

		// The path in the target directory for the new file or folder
		targetBase := filepath.Join(cwd, projectName)
		targetSuffix := strings.TrimPrefix(path, sourceBase)
		newFilepath := filepath.Join(targetBase, targetSuffix)

		if filepath.Ext(path) == ".crest" {
			fmt.Println(path)
			newFilepath = strings.TrimSuffix(newFilepath, ".crest")
			crestHandler(newFilepath, projectName, resources, components)
		} else {
			nonCrestHandler()
		}

		// if info.IsDir() {
		// 	// fmt.Printf("mkdir %s\n", newFilepath)
		// 	mkdirErr := os.Mkdir(newFilepath, os.ModePerm)
		// 	if mkdirErr != nil {
		// 		panic(mkdirErr)
		// 	}
		// } else {
		// 	// fmt.Printf("write file %s\n", newFilepath)
		// 	data, readFileErr := ioutil.ReadFile(path)
		// 	if readFileErr != nil {
		// 		panic(readFileErr)
		// 	}
		// 	writeFileErr := ioutil.WriteFile(newFilepath, data, os.ModePerm)
		// 	if writeFileErr != nil {
		// 		panic(writeFileErr)
		// 	}
		// }

		return nil
	}
}

func buildProject(name string, frontendChoice string, backendChoice string, resources []string, components []string) {

	exePath, exeErr := os.Executable()
	if exeErr != nil {
		panic(exeErr)
	}
	root := filepath.Join(filepath.Dir(filepath.Dir(exePath)), "templates")

	// Build the frontend skeleton
	frontendPath := filepath.Join(root, "client", frontendChoice)
	frontendWalkErr := filepath.Walk(frontendPath, walkFnWrapper(name, frontendPath, resources, components))
	if frontendWalkErr != nil {
		panic(frontendWalkErr)
	}

	// // Build the backend skeleton
	// backendPath := filepath.Join(root, "backend", backendChoice)
	// backendWalkErr := filepath.Walk(backendPath, walkFnWrapper(name, backendPath, resources, components))
	// if backendWalkErr != nil {
	// 	panic(backendWalkErr)
	// }

}

func main() {

	// fmt.Println("==== Crest - Create a RESTful project base ====")
	// // TODO: validate project name i.e. has legal characters
	// name := promptSingle("What is your project name? ")
	// frontend := promptSingle("What is your project frontend? ", "react", "vue", "reframe")
	// backend := promptSingle("What is your project backend? ", "go", "flask", "clojure")
	// resources := promptMulti("What are your project resources? ")
	// components := promptMulti("What are your project components? ")

	name := "todomvc"
	frontend := "react"
	backend := "go"
	resources := []string{"todo", "user"}
	components := []string{"header", "form", "button"}

	buildProject(name, frontend, backend, resources, components)

}
