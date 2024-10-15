import argparse
import os

def replace_line_in_file(file_path, search_string, new_line):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    replacement_made = False

    for i, line in enumerate(lines):
        if search_string in line:
            lines[i] = new_line + '\n'
            replacement_made = True

    if replacement_made:
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print("File updated successfully by replacing existing line.")
    else:
        with open(file_path, 'a') as file:
            file.write(new_line + '\n')
        print("File updated successfully by adding new line.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conan_global_conf_path', type=str, required=True, help="Path to the conan global configuration.")
    parser.add_argument('--port', type=int, required=True, help="The port to serve the webserver on.")

    args = parser.parse_args()

    search_string = 'core.sources:download_urls'
    new_line = f'core.sources:download_urls=["https://localhost:{args.port}", "origin"]'

    replace_line_in_file(args.conan_global_conf_path, search_string, new_line)

if __name__ == "__main__":
    main()