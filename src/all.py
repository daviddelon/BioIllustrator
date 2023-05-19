import subprocess
import json
import sys

if len(sys.argv) != 3:
    print("Usage: python script.py <filename> <script_name>")
    sys.exit(1)

filename = sys.argv[1]
script_name = sys.argv[2]

# Premier script : extract_image_reference_from_asciidoc.py
if script_name == "extract_image_reference_from_asciidoc.py" or script_name=="all":
    cmd = ["python", "extract_image_reference_from_asciidoc.py", filename]
    print("Exécution de extract_image_reference_from_asciidoc.py...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    output1 = result.stdout.strip()
    with open("output1.json", "w") as f:
        f.write(output1)
    print("Terminé.")

# Deuxième script : get_photo_information_from_inat.py
if script_name == "get_photo_information_from_inat.py" or script_name=="all":
    with open("output1.json", "r") as f:
        output1 = f.read().strip()
    cmd = ["python", "get_photo_information_from_inat.py", output1]
    print("Exécution de get_photo_information_from_inat.py...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    output2 = result.stdout.strip()
    with open("output2.json", "w") as f:
        f.write(output2)
    print("Terminé.")

# Troisième script : download_photo_from_inat.py
if script_name == "download_photo_from_inat.py" or script_name=="all":
    with open("output2.json", "r") as f:
        output2 = f.read().strip()
    cmd = ["python", "download_photo_from_inat.py", output2]
    print("Exécution de download_photo_from_inat.py...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    output3 = result.stdout.strip()
    with open("output3.json", "w") as f:
        f.write(output3)
    print("Terminé.")

# Quatrième script : crop_photo_and_add.mention.py
if script_name == "crop_photo_and_add.mention.py" or script_name=="all":
    with open("output3.json", "r") as f:
        output3 = f.read().strip()
    cmd = ["python", "crop_photo_and_add.mention.py", output3]
    print("Exécution de crop_photo_and_add.mention.py...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    output4 = result.stdout.strip()
    with open("output4.json", "w") as f:
        f.write(output4)


# Cinquième script : asciidoctor-pdf
if script_name == "asciidoctor" or script_name=="all":
    print("Exécution de asciidoctor-pdf ...")
    subprocess.call(["asciidoctor-pdf", "-a", "pdf-theme=key-theme.yml", "-a", "pdf-themesdir=themes", filename])
    print("Terminé.")
