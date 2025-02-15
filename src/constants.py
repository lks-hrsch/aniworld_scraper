import sys

from src.custom_logging import setup_logger

logger = setup_logger(__name__)


def parse_cli_arguments(default: str | int, position: int) -> str | int:
    try:
        cli_argument: str = sys.argv[position]
        logger.debug(f"cli argument detected on position:{position} with value:{cli_argument}")
        if type(default) is int:
            cli_argument: int = int(cli_argument)
        return cli_argument
    except IndexError:
        return default


# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
APP_VERSION = "v01-10-00"

# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #
type_of_media = parse_cli_arguments("anime", 1)  # choose 'serie' or 'anime'
name = parse_cli_arguments("Name-Goes-Here", 2)
language = parse_cli_arguments("Deutsch", 3)
season_override = parse_cli_arguments(0, 4)  # 0 = no override. 1 = season 1. etc...
episode_override = 0  # 0 = no override. 1 = episode 1. etc...
ddos_protection_calc = 5
ddos_wait_timer = 180  # in seconds
output_path = name
site_url = {
    "serie": "https://s.to",  # maybe you need another dns to be able to use this site
    "anime": "https://aniworld.to"
}

url = "{}/{}/stream/{}/".format(site_url[type_of_media], type_of_media, name)