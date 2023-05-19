import sys
import json
from pyinaturalist.node_api import get_observation


def process_observation(observation_num, image_index):
    # Récupére l'observation correspondant au numéro d'observation
    # All API requests are cached by default. These expire in 30 minutes for most endpoints, and 1 day for some infrequently-changing data (like taxa and places). See requests-cache: Expiration for details on cache expiration behavior.
    observation = get_observation(observation_num)

    imgurl = observation['photos'][image_index]['url']
    imgurl = imgurl.replace("square", "original")

    attribution = observation['photos'][image_index]['attribution']
    id = observation['photos'][image_index]['id']
    name = observation['taxon']['name']

    image_dict = {'url': imgurl, 'attribution': attribution, 'id': str(id), 'name': name}

    return image_dict


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python script.py <json_string>\n")
        sys.exit(1)

    json_string = sys.argv[1]

    data_list = json.loads(json_string)


    images_list = []

    for data in data_list:
        observation_num = int(data['observation'])
        image_index = int(data['image_index'])
        image_dict = process_observation(observation_num, image_index)
        image_dict ['width']=data['width']
        image_dict ['filename']=data['filename']
        if 'callout_number' in data:
            image_dict ['callout_number']=data['callout_number']
            image_dict ['callout_x']=data['callout_x']
            image_dict ['callout_y']=data['callout_y']
        images_list.append(image_dict)

    images_json = json.dumps(images_list)

    print(images_json)
