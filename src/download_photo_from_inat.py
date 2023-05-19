import os
import requests
import sys
import json

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python script.py <json_string>\n")
        sys.exit(1)

    json_string = sys.argv[1]

    data_list = json.loads(json_string)

    for data in data_list:
        # Force use of filename provided in asciidoc document
        filename = data['filename'].replace('.jpg', '')
        if os.path.exists('../images/'+filename + '_' + data['id'] + '.jpg'):
            sys.stderr.write(f"L'image {data['id']} existe déjà sur le disque.\n")
        else:
            # Télécharger l'image à partir de l'URL
            response = requests.get(data['url'], stream=True)
            response.raw.decode_content = True

            # Écrire l'image dans un fichier avec le nom de photo_id
            with open('../images/'+filename + '_' + data['id'] + '.jpg', 'wb') as f:
                for chunk in response:
                    f.write(chunk)
            sys.stderr.write(f"L'image {data['id']} a été téléchargée.\n")
    
    print(json.dumps(data_list))
