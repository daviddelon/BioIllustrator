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
                optionals = match[4]
                callout_numbers = re.findall(r'callout_number="([^"]+)"', optionals)
                callout_xs = re.findall(r'callout_x=(\d+)', optionals)
                callout_ys = re.findall(r'callout_y=(\d+)', optionals)

                # Construction de l'objet data
                data = {
                    "filename": filename,
                    "width": width,
                    "observation": observation,
                    "image_index": image_index,
                }

                if callout_numbers:
                    data["callout_number"] = callout_numbers
                if callout_xs:
                    data["callout_x"] = callout_xs
                if callout_ys:
                    data["callout_y"] = callout_ys

                data_list.append(data)

            print(json.dumps(data_list))
