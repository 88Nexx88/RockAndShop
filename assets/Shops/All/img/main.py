import os

# List of file extensions to delete
extensions_to_delete = ['.jpg']

# Get a list of all files in the current directory
files = os.listdir()

# Delete files with specified extensions
for file in files:
    for ext in extensions_to_delete:
        if file.endswith(ext):
            try:
                os.remove(file)
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Error while removing {file}: {e}")

print("Files with specified extensions have been removed.")