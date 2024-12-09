import os
import re

# Define the input file and the directory containing target files
input_file = "home/linux_playground/output.txt"
target_directory = "/home/linux_playground/dir_one/"  # Directory containing the files to process

# Read the words from the input file
with open(input_file, "r") as f:
    words_to_replace = [line.strip() for line in f if line.strip().startswith("de_")]

# Create a regex pattern to match any of the words in the list
pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in words_to_replace) + r')\b')

# Function to remove the prefix
def remove_prefix(match):
    return match.group(1)[3:]

# Process each file in the target directory
for filename in os.listdir(target_directory):
    print(f"processing file {filename}")
    file_path = os.path.join(target_directory, filename)
    
    # Check if it's a file
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            content = file.read()

        # Replace words matching the pattern
        updated_content = pattern.sub(remove_prefix, content)

        # Write the updated content back to the file
        with open(file_path, "w") as file:
            file.write(updated_content)

print("Processing complete. All matching words have been updated.")