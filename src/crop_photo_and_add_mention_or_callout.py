import json
import subprocess
import sys
import re
from PIL import Image, ImageDraw, ImageFont

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python script.py <json_string>\n")
        sys.exit(1)

    json_string = sys.argv[1]

    data_list = json.loads(json_string)

    for data in data_list:
        filename = '../images/' + data['filename'].replace('.jpg', '')

        input_file = filename + '_' + str(data['id']) + ".jpg"
        cropped_file = input_file + "_cropped.jpg"
        cropped_with_attribution = filename + ".jpg"

        width = data.get('width', 300)
        height = width

        subprocess.call(["smartcroppy", "--width=" + str(width), "--height=" + str(height), input_file, cropped_file])

        # Ajout du texte d'attribution en bas de l'image
        m = re.search("\(c\) (.+),", data['attribution'])
        if m:
            author = m.group(1)
        else:
            author = "Auteur inconnu"

        # Recherche du type de licence entre parenthèses à la fin de la chaîne
        m = re.search("\((CC .+)\)$", data['attribution'])
        if m:
            license_type = m.group(1)
        else:
            license_type = "Licence inconnue"

        img = Image.open(cropped_file)
        draw = ImageDraw.Draw(img)
        text = author + ' ' + license_type
        font = ImageFont.truetype("../font/LiberationSans-Regular.ttf", 12)
        text_size = draw.textsize(text, font=font)
        text_x = img.width - text_size[0] - 5
        text_y = img.height - text_size[1] - 5
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

        # Ajout des annotations (callouts) si les champs correspondants sont renseignés
        callout_numbers = data.get('callout_number', [])
        callout_xs = data.get('callout_x', [])
        callout_ys = data.get('callout_y', [])

        for i in range(len(callout_numbers)):
            callout_number = callout_numbers[i]
            callout_x = int(callout_xs[i]) if i < len(callout_xs) else 10
            callout_y = int(callout_ys[i]) if i < len(callout_ys) else 10

            callout_value = str(callout_number)

            # Position et taille du cercle du callout
            circle_radius = 15

            # Dessin du cercle noir
            draw.ellipse([(callout_x - circle_radius, callout_y - circle_radius),
                          (callout_x + circle_radius, callout_y + circle_radius)],
                         fill=(0, 0, 0))

            # Position et taille du texte du callout
            callout_font = ImageFont.truetype("../font/LiberationSans-Bold.ttf", 14)
            text_width, text_height = draw.textsize(callout_value, font=callout_font)

            # Calcul des coordonnées pour centrer le texte dans le cercle
            text_x = callout_x - text_width // 2
            text_y = callout_y - text_height // 2 - 2  # Déplacer le texte un peu plus haut

            # Dessin du texte du callout
            draw.text((text_x, text_y), callout_value, font=callout_font, fill=(255, 255, 255))

        img.save(cropped_with_attribution)
