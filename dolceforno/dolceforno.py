import argparse
import importlib
import json
import os
import re
import sys

import requests

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)))
import recipes  # noqa

RECIPES_MAPPING = {
    # Articles on https://medium.com/, for example:
    # https://medium.com/the-mission/the-105-best-tools-to-start-your-business-in-2018-1675a457b4de
    r'medium\.com\/': 'recipes.medium',
    # Articles on https://www.newyorker.com/, for example:
    # https://www.newyorker.com/tech/annals-of-technology/can-indie-social-media-save-us
    # https://www.newyorker.com/magazine/2019/05/20/can-we-live-longer-but-stay-younger
    r'newyorker.com\/': 'recipes.new_yorker',
    # Articles on https://vogue.com/, for example:
    # https://www.vogue.com/article/christian-dior-resort-2020-maria-grazia-chiuri-peter-philips-guido-palau-hair-makeup
    r'vogue\.com\/article\/': 'recipes.vogue_com_article',
    # Articles on https://www.wired.com/<YYYY>/<MM>/, for example:
    # https://www.wired.com/2019/05/geeks-guide-hail-satan/
    r'wired\.com\/\d{4}\/\d{2}\/': 'recipes.wired_com_date',
    # Articles on https://www.wired.com/story/, for example:
    # https://www.wired.com/story/minecraft-earth-wants-to-be-the-next-pokemon-go-but-bigger/
    r'wired\.com\/story\/': 'recipes.wired_com_story',
}


class InvalidURL(Exception):
    """"Raised when the provided URL is not a valid URL."""


def select_appropriate_recipe(url):
    """Selects the most appropriate recipe given a URL.

    Specifically, the function checks against RECIPES_MAPPING to see whether
    the URL matches any of the stored regexes. If yes, than the corresponding
    recipe is retrieved. The function assumes that every URL will only ever
    match a single regex; hence, the first match stops the iteration.

    Args:
        url: str, the URL.

    Returns:
        Either None (if no recipe is retrieved) or a class that inherits from
        _abstract.AbstractRecipe() and that it's expected to have a Parse()
        method.
    """
    recipe_path = None
    for regex, path in RECIPES_MAPPING.items():
        if re.search(regex, url):
            recipe_path = path
            break
    if recipe_path:
        module = importlib.import_module(recipe_path, package=None)
        return module.Recipe()
    return None


class DolceForno(object):
    def __init__(self, url=None):
        self.url = url
        self.recipe = select_appropriate_recipe(url) if url else None
        self.html = requests.get(url).text if url else None

    def cook(self, html=None, recipe=None):
        html = html or self.html
        recipe = recipe or self.recipe
        if recipe:
            return recipe.parse(html)
        raw_message = 'INFO: There was no recipe available to parse {}.'
        message = raw_message.format(self.url)
        print(message)
        return None

    def save(self, output, output_filepath):
        with open(output_filepath, 'w') as output_file:
            json.dump(output, output_file)

    def cook_and_save(self, output_filepath, html=None, recipe=None):
        output = self.cook(html, recipe)
        if output:
            self.save(output, output_filepath)


def ParseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', default='')
    parser.add_argument('--output_filepath', '-o', default='')
    parser.add_argument('--save_html', '-s', action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    args = ParseArgs()
    if args.url:
        filename = (
            args.url.split('/')[-1]
            if args.url.split('/')[-1]
            else args.url.split('/')[-2])
        output_filepath = (
            args.output_filepath
            if args.output_filepath
            else filename+'.json')
        dolce_forno = DolceForno(args.url)
        dolce_forno.cook_and_save(output_filepath)
        if args.save_html:
            html_filepath = output_filepath.replace('.json', '.html')
            with open(html_filepath, 'w') as html_file:
                html_file.write(dolce_forno.html)
