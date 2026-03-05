from utils import csv_utils


def main():
    c = csv_utils.StateConfigCreator()
    c.write_config_to_file()


if __name__ == "__main__":
    main()
