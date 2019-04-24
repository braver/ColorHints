"""
Return the RGB value of a Pantone color code

"""
import json
import sublime
from .rgba import round_int, clamp

pantone_name_map = {}
pantone_code_map = {}
pantone_books = [
    'pantoneCmykCoated.json',
    'pantoneCmykUncoated.json',
    'pantoneColorBridgeCoatedV3.json',
    'pantoneColorBridgeUncoatedV3.json',
    'pantoneExtendedGamutCoatedM2.json',
    'pantoneFhCottonTcx.json',
    'pantoneFhiMetallicShimmersTpmM2.json',
    'pantoneFhiPaperTpg210NewColorsM2.json',
    'pantoneFhiPaperTpgM2.json',
    'pantoneFhiPolyesterTsx.json',
    'pantoneFhNylonBrightsTn.json',
    'pantoneMetallicsSolidCoatedM2.json',
    'pantonePastelsNeonsCoatedM2.json',
    'pantoneSkinToneGuideM2.json',
    'pantoneSolidCoatedV3M2.json',
    'pantoneSolidUncoatedV3M2.json',
]


def load():
    """Load Pantone books into memory."""

    for book in pantone_books:
        locations = sublime.find_resources(book)
        if locations:
            data = sublime.load_resource(locations[0])
            colors = json.loads(data)['data']['getBook']['colors']
            for color in colors:
                code = color['code']
                name = color['name']
                hex_value = "#%02x%02x%02x" % (
                    clamp(round_int(float(color['rgb']['r'])), 0, 255),
                    clamp(round_int(float(color['rgb']['g'])), 0, 255),
                    clamp(round_int(float(color['rgb']['b'])), 0, 255)
                )
                pantone_code_map[code.lower()] = hex_value
                if name:
                    pantone_name_map[name.lower()] = hex_value


def code2hex(code):
    """Convert Pantone color code to CSS hex."""

    return pantone_code_map.get(code.lower(), None)


def name2hex(name):
    """Convert Pantone color name to CSS hex."""

    return pantone_name_map.get(name.lower(), None)
