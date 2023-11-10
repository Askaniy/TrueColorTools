from argparse import ArgumentParser
from src.main import launch_window

# CLI parsing
parser = ArgumentParser(description='See ReadMe on the GitHub page: https://github.com/Askaniy/TrueColorTools#readme')
parser.add_argument('-v', '--verbose', '--verbosity', action='count', help='increase level of output verbosity (-v, -vv, etc.)')
parser.add_argument('-l', '--lang', '--language', type=str, default='en', help='set startup language, editable in GUI (en, de, ru)')
args = parser.parse_args()

launch_window(args.lang)