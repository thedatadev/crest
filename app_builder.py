from os.path import basename, dirname, exists, abspath, join, realpath
from os import getcwd, scandir, remove
from string import Template
from shutil import copytree
from sys import exit
                                         
def build(api_type, api_choice, items_to_interpolate):
    if exists(api_type) and input(f"The directory '{api_type}' already exists. Enter y to overwrite: ") == 'y':
        exit("Build cancelled.")
    src = join(*[dirname(realpath(__file__)), api_type, api_choice])
    dst = join(getcwd(), api_type)
    copytree(src=src, dst=dst)
    perform_templating(items_to_interpolate, current_path=dst)

def perform_templating(items_to_interpolate, current_path):
    with scandir(current_path) as cwd:
        for entry in cwd:
            if entry.name.endswith('.crest'):
                if entry.is_dir():
                    handle_directory(entry, current_path, items_to_interpolate)
                else:
                    handle_file(entry, current_path, items_to_interpolate)
            else:
                if entry.is_dir():
                    perform_templating(items_to_interpolate, entry.path)
    # TODO: perform another scan to remove all .crest files and folders

def handle_directory(entry, current_path, items_to_interpolate):
    *folder_prefix, item_suffix, _ = entry.name.split('.')
    folder_name = '.'.join(folder_prefix)
    duplicate_template_folder(current_path, entry.path, folder_name, items_to_interpolate, item_suffix)

def handle_file(entry, current_path, items_to_interpolate):
    *file_prefix, item_suffix, _ = entry.name.split('.')
    file_name =  '.'.join(file_prefix)
    if item_suffix == 'based_on_parent_folder':
        file_is_based_on_parent_folder(entry, current_path, file_name)
    elif item_suffix == 'resources':
        file_is_based_on_resource(entry, items_to_interpolate, item_suffix, file_name, current_path)
    else:
        exit(f"The item suffix '{item_suffix}' is not supported. Crest terminated.")

def file_is_based_on_parent_folder(entry, current_path, file_name):
    file_name = basename(current_path) + file_name
    duplicate_template_file(template_file=entry.path, # entry.path ends with dir name
                            new_file_name=abspath(join(current_path, file_name)),
                            item_to_interpolate=basename(current_path)) # just dir name

def file_is_based_on_resource(entry, items_to_interpolate, item_suffix, file_name, current_path):
    for item in items_to_interpolate[item_suffix]:
        item_file_name = item + file_name
        duplicate_template_file(template_file=entry.path, 
                                new_file_name=abspath(join(current_path, item_file_name)),
                                item_to_interpolate=item)

def duplicate_template_folder(current_path, template_folder_path, folder_name, items_to_interpolate, item_suffix):
    for item in items_to_interpolate[item_suffix]:
        new_folder_path = current_path + '/' + item + folder_name
        copytree(template_folder_path, new_folder_path)
        perform_templating(items_to_interpolate, new_folder_path)

def duplicate_template_file(template_file, new_file_name, item_to_interpolate):
    with open(template_file, "r") as original_template:
        with open(new_file_name, "w+") as new_file:
            incomplete_template = original_template.read()
            complete_template = Template(incomplete_template).substitute(regular=item_to_interpolate.lower(),
                                                                         capital=item_to_interpolate.upper())
            new_file.write(complete_template)