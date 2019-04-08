#!/usr/bin/env python3
import app_builder
import sys
import os

FRONTEND_CHOICES = ['react', 'vue']
BACKEND_CHOICES  = ['go']

frontend_prompt = f"Choose a frontend setup from: ({', '.join(FRONTEND_CHOICES)}): "
backend_prompt  = f"Choose a backend setup from: ({', '.join(BACKEND_CHOICES)}): "

def prompt_for_single_choice(valid_choices, prompt_message):
    user_choice = input(prompt_message)
    while True:
        if user_choice in valid_choices:
            return user_choice
        elif user_choice == 'q':
            exit("User exited Crest.")
        else:
            user_choice = input(f"Please enter a valid choice ({valid_choices}): ")

def prompt_for_multiple_choices(prompt_message):
    return input(prompt_message).split()

if __name__ == "__main__":
    
    print("Crest - a full-stack RESTful project initialiser")

    app_name = input("App name: ")

    frontend_choice = prompt_for_single_choice(FRONTEND_CHOICES, frontend_prompt)
    backend_choice = prompt_for_single_choice(BACKEND_CHOICES, backend_prompt)

    resources = prompt_for_multiple_choices("List the REST resources for this project: ")
    components = prompt_for_multiple_choices("List the frontend components for this project: ")

    items_to_interpolate = { 'resources': resources, 'components': components }

    app_builder.build('client', frontend_choice, items_to_interpolate)
    app_builder.build('server', backend_choice, items_to_interpolate)
