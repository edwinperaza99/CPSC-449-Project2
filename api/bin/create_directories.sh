#!/bin/bash

# Define the root directory
root_dir="api/var"

# Function to create a directory structure
create_directory_structure() {
    mkdir -p "$root_dir/$1/data" "$root_dir/$1/fuse"
}

# Function to remove a directory structure if it exists
remove_directory_structure() {
    if [ -d "$root_dir/$1" ]; then
        rm -r "$root_dir/$1"
    fi
}

# Remove the existing directory structures if they exist
remove_directory_structure "primary"
remove_directory_structure "secondary-1"
remove_directory_structure "secondary-2"

# Create the directory structures
create_directory_structure "primary"
create_directory_structure "secondary-1"
create_directory_structure "secondary-2"
