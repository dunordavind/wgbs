# coding=utf-8

from command_line.parse_command_line_args import parse_command_line_args
from config.setup_configs import setup_configs

if __name__ == "__main__":
    args = parse_command_line_args()
    setup_configs(args)
    args.func(args)

