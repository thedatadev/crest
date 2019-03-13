from os.path import basename, dirname, exists, abspath, join, realpath
from os import getcwd, scandir, remove
from string import Template
from shutil import copytree
from sys import exit

def duplicate_template_folder(current_path, folder_name, items_to_interpolate, item_suffix):
    for item in items_to_interpolate[item_suffix]:
        new_folder_path = current_path + '/' + item + folder_name
        copytree(new_folder_path, item)
        perform_templating(items_to_interpolate, new_folder_path)

def duplicate_template_file(template_file, new_file_name, item_to_interpolate):
    with open(template_file, "r") as original_template:
        with open(new_file_name, "w+") as new_file:
            incomplete_template = original_template.read()
            complete_template = Template(incomplete_template).substitute(regular=item_to_interpolate.lowercase(),
                                                                         capital=item_to_interpolate.capitalize())
            new_file.write(complete_template)

def perform_templating(items_to_interpolate, current_path):
    with scandir(current_path) as cwd:
        for entry in cwd:
            if entry.name.endswith('.crest'):
                if entry.is_dir():
                    *folder_prefix, item_suffix, _ = entry.name.split('.')
                    folder_name = '.'.join(folder_prefix)
                    duplicate_template_folder(current_path, folder_name, items_to_interpolate, item_suffix)
                else:
                    *file_prefix, item_suffix, _ = entry.name.split('.')
                    file_name = '.'.join(file_prefix)
                    if item_suffix in ['based_on_parent_folder']:
                        duplicate_template_file(template_file=entry.path, 
                                                new_file_name=abspath(join(entry.path, file_name)),
                                                item_to_interpolate=basename(current_path))
                    else:
                        for item in items_to_interpolate[item_suffix]:
                            file_name = item + file_name
                            duplicate_template_file(template_file=entry.path, 
                                                new_file_name=abspath(join(entry.path, file_name)),
                                                item_to_interpolate=item)
                remove(entry.path)
                                         
def build(api_type, api_choice, items_to_interpolate):
    if exists(api_type) and input(f"The directory '{api_type}' already exists. Enter y to overwrite: ") == 'y':
        exit("Build cancelled.")

    src = join(*[dirname(realpath(__file__)), api_type, api_choice])
    dst = join(getcwd(), api_type)

    print("Copy from:", src)
    print("Copy tp:", dst)

    # copytree(src=join(*[dirname(realpath(__file__)), api_type, api_choice]), dst=join(getcwd(), api_type))
    # perform_templating(items_to_interpolate, current_path=join(getcwd(), api_type))

