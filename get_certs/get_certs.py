import yaml
import subprocess
import base64


def get_certificate_secret():
    process = subprocess.run([
        'kubectl', '-n', 'infra-prod', 'get', 'secret', 'kafka-certificate', '-o', 'yaml'
    ], capture_output=True, text=True)

    return process.stdout


def extract_certs(yaml_string):
    yaml_object = yaml.safe_load(yaml_string)
    return yaml_object['data']


def write_to_file(file_name, content):
    decoded_content = base64.b64decode(content)
    with open(file_name, 'wb') as file:
        file.write(decoded_content)


def write_certs(certs):
    for file_name, content in certs.items():
        write_to_file(file_name, content)


secret_yaml_string = get_certificate_secret()
secret_certs = extract_certs(secret_yaml_string)
write_certs(secret_certs)
