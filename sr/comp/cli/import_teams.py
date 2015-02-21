import yaml
import os.path

from PIL import Image
from six import BytesIO
from six.moves.urllib.parse import urljoin
import requests

def format_team(entry):
    if 'team_name' in entry:
        name = entry['team_name']
    else:
        name = entry['college']['name']
    rookie = False  # Temporary
    return {'name': name,
            'rookie': rookie}


def download_team_images(server, team_data, compstate):
    team_images_dir = os.path.join(compstate, 'teams', 'images')
    try:
        os.makedirs(team_images_dir)
    except OSError:
        pass

    for tla, team in team_data.items():
        try:
            image_url = team['image']['content']
        except (TypeError, KeyError):
            continue

        req = requests.get(urljoin(server, image_url))
        image = Image.open(BytesIO(req.content))
        image.thumbnail((512, 512), Image.LANCZOS)
        image.save(os.path.join(team_images_dir, '{}.png'.format(tla)))


def command(settings):
    teams_yaml = os.path.join(settings.compstate, 'teams.yaml')
    target = urljoin(settings.server, 'teams-data.php')
    team_data = requests.get(target).json()

    # write out teams.yaml file
    with open(teams_yaml, 'w') as f:
        yaml.dump({'teams': {tla: format_team(team)
                               for tla, team in team_data.items()}},
                  f, default_flow_style=False)

    # download and save team images
    download_team_images(settings.server, team_data, settings.compstate)

def add_subparser(subparsers):
    parser = subparsers.add_parser('import-teams',
                                   help='import a teams.yaml from an SR server')
    parser.add_argument('compstate', help='competition state repository')
    parser.add_argument('-s', '--server', help='srweb instance',
                        default='https://www.studentrobotics.org/')
    parser.set_defaults(func=command)
