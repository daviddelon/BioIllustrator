import sys
import re
import json

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python script.py <filename>\n")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, 'r') as f:
        content = f.read()

        matches = re.findall(r'.+image::(.+\.jpg).+width="(.+)mm".+observation=(\d+),image_index=(\d+)(.+)', content)

        if matches:
            data_list = []

            for match in matches:
                filename = match[0]
                width = match[1]
                observation = match[2]
                image_index = match[3]

                # Extraction des champs optionnels
                callout_number = None
                callout_x = None
                callout_y = None

                optionals = match[4]
                callout_match = re.search(r'callout_number="([^"]+)"', optionals)
                if callout_match:
                    callout_number = callout_match.group(1)

                callout_x_match = re.search(r'callout_x=(\d+)', optionals)
                if callout_x_match:
                    callout_x = callout_x_match.group(1)

                callout_y_match = re.search(r'callout_y=(\d+)', optionals)
                if callout_y_match:
                    callout_y = callout_y_match.group(1)

                # Construction de l'objet data
                data = {
                    "filename": filename,
                    "width": width,
                    "observation": observation,
                    "image_index": image_index,
                }

                if callout_number != None:
                    data["callout_number"] = callout_number
                    data["callout_x"] = callout_x
                    data["callout_y"] =  callout_y

                data_list.append(data)

            print(json.dumps(data_list))
