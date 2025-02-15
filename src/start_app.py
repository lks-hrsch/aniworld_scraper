import os
import time

from src.constants import (APP_VERSION, ddos_protection_calc, ddos_wait_timer,
                           language, name, output_path, season_override,
                           site_url, type_of_media, url)
from src.custom_logging import setup_logger
from src.logic.collect_all_seasons_and_episodes import get_episodes, get_season
from src.logic.downloader import already_downloaded, create_new_download_thread
from src.logic.language import LanguageError
from src.logic.search_for_links import (find_cache_url,
                                        get_redirect_link_by_provider)

logger = setup_logger(__name__)

# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #


def main():
    ddos_start_value = 0


    logger.info("------------- AnimeSerienScraper {} started ------------".format(APP_VERSION))

    read_check = os.access('DO_NOT_DELETE.txt', os.R_OK)
    if read_check:
        logger.debug("We have Read Permission")
    else:
        logger.error("No Read Permission. Please check if you own the Folder and/or have "
                                            "permissions to read.")
        exit()
    write_check = os.access('DO_NOT_DELETE.txt', os.W_OK)
    if write_check:
        logger.debug("We have Write Permission")
    else:
        logger.error("No Write Permission. Please check if you own the Folder and/or have "
                                            "permissions to write.")
        exit()

    if name == "Name-Goes-Here":
        logger.error("Name is Default. Please reade readme before starting.")
        exit()

    if season_override == 0:
        logger.info("No Season override detected.")
        seasons = get_season(url)
        logger.info("We have this many seasons: {}".format(seasons))
    else:
        logger.info("Season Override detected. Override set to: {}".format(season_override))
        seasons = 1

    os.makedirs(output_path, exist_ok=True)

    for season in range(int(seasons)):
        season = season + 1 if season_override == 0 else season_override
        season_path = f"{output_path}/Season {season:02}"
        os.makedirs(season_path, exist_ok=True)
        episode_count = get_episodes(url, season)
        logger.info("Season {} has {} Episodes.".format(season, episode_count))

        for episode in range(int(episode_count)):
            episode = episode + 1
            file_name = "{}/{} - s{:02}e{:02} - {}.mp4".format(season_path, name, season, episode, language)
            logger.info("File name will be: " + file_name)
            if not already_downloaded(file_name):
                link = url + "staffel-{}/episode-{}".format(season, episode)
                try:
                    redirect_link, provider = get_redirect_link_by_provider(site_url[type_of_media], link, language)
                except LanguageError:
                    continue
                if ddos_start_value < ddos_protection_calc:
                    logger.debug("Entered DDOS var check and starting new downloader.")
                    ddos_start_value += 1
                else:
                    logger.info("Started {} Downloads. Waiting for {} Seconds to not trigger DDOS"
                                                    "Protection.".format(ddos_protection_calc, ddos_wait_timer))
                    time.sleep(ddos_wait_timer)
                    ddos_start_value = 1
                cache_url = find_cache_url(redirect_link, provider)
                if cache_url == 0:
                    logger.error(f"Could not find cache url for {provider} on {season}, {episode}.")
                    continue
                logger.debug("{} Cache URL is: ".format(provider) + cache_url)
                create_new_download_thread(cache_url, file_name, provider)

