import os
import requests
import socket
import tarfile

ip = "127.0.0.1"
# root_data_dir = "artifactory-cpp-ce-7.63.12/artifactory"
root_data_dir = "./artifactory"

env_path = os.path.join(os.getcwd(), "artifactory-cpp-ce-7.63.12", ".env")
env_confiuration = {
    "JF_ROOT_DATA_DIR": f"./{root_data_dir}",
    "JF_SHARED_NODE_IP": ip,
    "IS_HA": "n",
    "JF_INSTALL_POSTGRES": "n"
}

system_yaml_path = os.path.join(os.getcwd(), "artifactory-cpp-ce-7.63.12", root_data_dir, "var", "etc", "system.yaml")
system_yaml_configuration = f"""shared:
    node:
        ip: {ip}
        id: {socket.gethostname()}
        name: {socket.gethostname()}
    database:
        allowNonPostgresql: true
        type: derby
router:
    entrypoints:
        externalPort: 8082

"""

# Download sources.
artifactory_url = "https://releases.jfrog.io/artifactory/bintray-artifactory/org/artifactory/cpp/ce/docker/jfrog-artifactory-cpp-ce/7.63.12/jfrog-artifactory-cpp-ce-7.63.12-compose.tar.gz"

compressed_filename = "artifactory.tar.gz"
unpack_directory = "."

response = requests.get(artifactory_url)

with open(compressed_filename, "wb") as file:
    file.write(response.content)

with tarfile.open(compressed_filename, "r:gz") as tar:
    tar.extractall(path=unpack_directory)

os.remove(compressed_filename)

# Modify config files.
with open(env_path, 'a') as file:
    file.write("\n" + "## Injected configuration" + "\n")
    for key, value in env_confiuration.items():
        file.write(f"{key}={value}" + "\n")

os.makedirs(os.path.dirname(system_yaml_path))

with open(system_yaml_path, 'w') as file:
    file.write(system_yaml_configuration)

