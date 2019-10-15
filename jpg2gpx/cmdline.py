
import argparse
import importlib
import sys

from . import processor
from . import sorters

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Simple tool to convert a series of JPG files to a GPX route")

    parser.add_argument(
        "-d", "--input-dir", 
        type=str, required=True,
        help="directory to process")

    parser.add_argument(
        "-r", "--recoursive", 
        action="store_true",
        help="search input directory recoursive")

    parser.add_argument(
        "-s", "--sort-mode", 
        choices=sorters.SortModes, 
        default=sorters.SortModes[0],
        help="Sort order of processed image files")

    parser.add_argument(
        "-o", "--output-name",
        help="Output path",
        default=".")

    parser.add_argument(
        "-g", "--group-by-date",
        action="store_true",
        help="Group track segments by (GPS) date")

    return parser.parse_args()

def main():
    ns = parse_args()
    proc = processor.Processor()
    proc.process(
        ns.input_dir, ns.recoursive, ns.sort_mode, 
        ns.output_name, ns.group_by_date)