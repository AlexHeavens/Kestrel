import argparse

import paths
from data import get_all_data_by_ward
from visualize import generate_interactive_map


def main():
    args = parse_args()
    ward_data = get_all_data_by_ward()
    map_obj = generate_interactive_map(ward_data)
    map_obj.save(f"{args.build_dir}/index.html")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--build-dir",
        default=paths.default_build_dir,
        help="directory to build files in",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
