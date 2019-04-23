from os.path import basename, dirname, exists, abspath, join, realpath, isfile, isdir
from os import getcwd, scandir, remove
from jinja2 import Template
from shutil import copytree, rmtree
from sys import exit
                                         
def build(api_type, api_choice, items_to_interpolate):
    # Verify if user would like to overwrite client or server directories if they alrady exist
    if exists(api_type) and input(f"The directory '{api_type}' already exists. Enter y to overwrite: ") == 'y':
        exit("Build cancelled.")
    # Construct the file path to the template files and folders
    src = join(*[dirname(realpath(__file__)), api_type, api_choice])
    # Construct the filepath to the directory where the crest.py file is run
    dst = join(getcwd(), api_type)
    # Copy over all the template files and folders from src to dst
    copytree(src=src, dst=dst)
    # Run the templating on the retrieved templates
    perform_templating(items_to_interpolate, current_path=dst)

def perform_templating(items_to_interpolate, current_path):

    # Enumerate all files and folders in the current directory
    with scandir(current_path) as cwd:
        for entry in cwd:
            # Only look out for .crest templates
            if entry.name.endswith('.crest'):
                # Handle .crest template folder
                if entry.is_dir():
                    handle_directory(entry, current_path, items_to_interpolate)
                # Handle .crest template file
                else:
                    handle_file(entry, current_path, items_to_interpolate)
            # If just a regular folder, recurse into it to see if there are .crest files or folders
            else:
                if entry.is_dir():
                    perform_templating(items_to_interpolate, entry.path)

def handle_directory(entry, current_path, items_to_interpolate):
    # Extract the folder prefix and item suffix (the third unpacked value is the ".crest" extension which we don't need now)
    # The directory name is split by "."
    # The item suffix is the extension which comes before ".crest"
    # The folder prefix becomes a list of any additional extensions preceding the item suffix
    # 
    # Example:
    #   entry = "components.crest"
    #   *folder_prefix, item_suffix, _ = entry.name.split('.')
    #   >> *folder_prefix = []
    #   >> item_suffix = "components"
    #   >> _ = ".crest"
    #
    # The folder prefix is generally empty. It's only there if you want to give a special suffix
    # to the directories you generate. It's a suffix because whatever you make as the folder_prefix
    # later gets prepended onto the eventual folder name
    # 
    # Example:
    #   entry = "rest.components.crest"
    #   This eventually becomes a folder named "<folder_name>.rest"
    *folder_prefix, item_suffix, _ = entry.name.split('.')
    folder_name = '.'.join(folder_prefix)
    duplicate_template_folder(current_path, entry.path, folder_name, items_to_interpolate, item_suffix)
    # Finally, discard the template folder from the repo
    rmtree(entry.path)

def handle_file(entry, current_path, items_to_interpolate):
    # Extract the file prefix and item suffix (the third unpacked value is the ".crest" extension which we don't need now)
    # The directory name is split by "."
    # The item suffix is the extension which comes before ".crest"
    # The file prefix becomes a list of any additional extensions preceding the item suffix
    # 
    # Example:
    #   entry = ".js.resources.crest"
    #   *folder_prefix, item_suffix, _ = entry.name.split('.')
    #   >> *folder_prefix = ["js"]
    #   >> item_suffix = "resources"
    #   >> _ = ".crest"
    #
    # The file prefix is preserved especially when you want to retain a particular file extension such as .js or .py
    # Example:
    #   entry = ".js.resources.crest"
    #   This eventually becomes a file named "<file_name>.js"
    #   e.g. ".api.js.resources.crest" with the resource name "user" becomes "user.api.js"
    #
    # The item suffix determines the method used to template the file
    #
    *file_prefix, item_suffix, _ = entry.name.split('.')
    file_name =  '.'.join(file_prefix)
    if item_suffix == 'based_on_parent_folder':
        file_is_based_on_parent_folder(entry, current_path, file_name)
    elif item_suffix == 'resources':
        file_is_based_on_item(entry, items_to_interpolate, item_suffix, file_name, current_path)
    elif item_suffix == 'components':
        file_is_based_on_item(entry, items_to_interpolate, item_suffix, file_name, current_path)
    elif item_suffix == 'container':
        file_is_item_container(entry, items_to_interpolate, file_name, current_path)
    elif item_suffix == 'inherit':
        file_inherits_item(entry, items_to_interpolate, file_name, current_path)
    else:
        exit(f"The item suffix '{item_suffix}' is not supported. Crest terminated.")
    # Finally, discard the template file from the repo
    remove(entry.path)

def file_is_based_on_parent_folder(entry, current_path, file_name):
    # If a file is marked with the extension "based_on_parent_folder",
    # it results in the file being named after the directory
    # Example:
    #   If we have a dir named "Navbar", all .crest files in it are named after it
    #   e.g. "Navbar.js", "Navbar.css", "Navbar.test.js"
    file_name = basename(current_path) + file_name
    duplicate_template_file(template_file=entry.path, # entry.path ends with dir name
                            new_file_name=abspath(join(current_path, file_name)),
                            item_to_interpolate=basename(current_path)) # just dir name

def file_is_based_on_item(entry, items_to_interpolate, item_suffix, file_name, current_path):
    # If a file is marked with the extension "resources",
    # it results in the file being named after a given resource in items_to_interpolate["resources"]
    # Example:
    #   If we have a .crest file named ".go.resources.crest", 
    #   and items_to_interpolate["resources"] = ["todo", "user"]
    #   then the resulting files are "todo.go" and "user.go"
    for item in items_to_interpolate[item_suffix]:
        item_file_name = item + file_name
        duplicate_template_file(template_file=entry.path, 
                                new_file_name=abspath(join(current_path, item_file_name)),
                                item_to_interpolate=item)

def file_is_item_container(entry, items_to_interpolate, file_name, current_path):
    # If a file is marked with the extension "container",
    # it contains information about resources or components etc. but its name is unaffected
    # Example:
    #   If we have a file that needs to import multiple components because
    #   it serves as a main entry point such as App.vue or app.py then it needs
    #   to import all its dependencies such as modules and libraries
    container_file_path = abspath(join(current_path, file_name))
    template_file = entry.path
    with open(template_file, "r") as original_template:
        with open(container_file_path, "w+") as new_file:
            incomplete_template = original_template.read()
            complete_template = Template(incomplete_template)
            new_file.write(complete_template.render(resources=items_to_interpolate['resources'],
                                                    components=items_to_interpolate['components']))

def file_inherits_item(entry, items_to_interpolate, file_name, current_path):
    # Same as based_on_parent_folder except that it only inherits 
    # the item, not the name from parent folder
    duplicate_template_file(template_file=entry.path, # entry.path ends with dir name
                            new_file_name=abspath(join(current_path, file_name)),
                            item_to_interpolate=basename(current_path)) # just dir name

def duplicate_template_folder(current_path, template_folder_path, folder_name, items_to_interpolate, item_suffix):
    # Generates a new folder based on the template folder and the item suffix of the template folder
    # For example, if the item_suffix is "components", then the entry for "components" is looked up
    # in the items_to_interpolate dict. The corresponding value is a list of strings.
    #
    # Example:
    #   item_suffix = "components"
    #   items_to_interpolate = ["header", "form", "button"]
    #
    # The template folder and its contents are duplicated and named after each "item" in the list
    # Then the perform_templating algorithm is called to template any additional .crest template
    # files or folders recursively
    for item in items_to_interpolate[item_suffix]:
        new_folder_path = current_path + '/' + item + folder_name
        copytree(template_folder_path, new_folder_path)
        perform_templating(items_to_interpolate, new_folder_path)

def duplicate_template_file(template_file, new_file_name, item_to_interpolate):
    with open(template_file, "r") as original_template:
        with open(new_file_name, "w+") as new_file:
            incomplete_template = original_template.read()
            complete_template = Template(incomplete_template)
            new_file.write(complete_template.render(regular=item_to_interpolate.lower(),
                                                    capital=item_to_interpolate.capitalize()))