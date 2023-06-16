import sys
import re
import json

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python script.py <filename>\n")
        sys.exit(1)

    asciidoc = sys.argv[1]

    with open(asciidoc, 'r') as f:
        content = f.read()

        matches = re.findall(r'.+image::(.+\.jpg)\["(.+)".+width="(.+)mm".+observation=(\d+),image_index=(\d+)(.+)', content)

        if matches:
            data_list = []

            for match in matches:
                filename = match[0]
                name = match[1]
                width = match[2]
                observation = match[3]
                image_index = match[4]

                # Extraction des champs optionnels
                optionals = match[5]
                callout_numbers = re.findall(r'callout_number="([^"]+)"', optionals)
                callout_xs = re.findall(r'callout_x=(\d+)', optionals)
                callout_ys = re.findall(r'callout_y=(\d+)', optionals)

                # Construction de l'objet data
                data = {
                    "filename": filename,
                    "name": name,
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

            # Génération du code HTML avec des images et leurs noms
            html_code = """
            <script>
                function FindPosition(oElement) {
                    var posX = 0, posY = 0;
                    while (oElement) {
                        posX += (oElement.offsetLeft - oElement.scrollLeft + oElement.clientLeft);
                        posY += (oElement.offsetTop - oElement.scrollTop + oElement.clientTop);
                        oElement = oElement.offsetParent;
                    }
                    return { x: posX, y: posY };
                }


                function getCoordinates(event) {
                    var x = event.clientX;
                    var y = event.clientY;
                    var imgPos = FindPosition(this);
                    var posX = x - imgPos.x;
                    var posY = y - imgPos.y;
                    var coordinates = 'callout_number="' + this.getAttribute('data-callout-number') + '",callout_x=' + posX + ',callout_y=' + posY;
                    navigator.clipboard.writeText(coordinates)
                        .then(function() {
                            console.log("Coordinates copied to clipboard: " + coordinates);
                        })
                        .catch(function(error) {
                            console.error("Error copying coordinates to clipboard:", error);
                        });
                }

                document.addEventListener('DOMContentLoaded', function() {
                    var images = document.querySelectorAll('img');
                    for (var i = 0; i < images.length; i++) {
                        var image = images[i];
                        image.addEventListener('click', getCoordinates);
                    }
                });
            </script>
            """

            for data in data_list:
                image_source = data["filename"]
                name = data["name"]
                callout_numbers = data.get("callout_number", [])
                html_code += f"<div style='display: flex;'>\n"
                html_code += f"  <img src='../images/{image_source}' data-callout-number='{','.join(callout_numbers)}'>\n"
                html_code += f"  <span style='margin-left: 10px;'>{name}</span>\n"
                html_code += f"</div><br>\n"

            # Écriture dans le fichier HTML
            output_filename = asciidoc.rsplit('.', 1)[0] + ".html"
            with open(output_filename, 'w') as output_file:
                output_file.write(html_code)
