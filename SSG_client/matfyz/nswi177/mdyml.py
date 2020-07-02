#!/usr/bin/env python3

"""
Utilities for Markdown with YAML.
"""

import yaml


def load_markdown_with_yaml_header(lines):
    """
    Splits lines into YAML header and actual contents.

    YAML header is surrounded by triple dash (---) and must be at
    the beginning of the file.

    Returns
    -------
    Tuple of dictionary (parsed YAML header) and contents.
    """

    header = []
    content = []
    header_found = False

    inside_content = False
    for line in lines:
        line = line.rstrip()
        if line == '---':
            if header_found:
                inside_content = True
            header_found = True
            continue
        if inside_content:
            content.append(line)
        else:
            header.append(line)

    if not header_found:
        content = header
        header = []
    header_dict = yaml.load('\n'.join(header), Loader=yaml.FullLoader)
    if not header_dict:
        header_dict = {}
    return (header_dict, '\n'.join(content))


def load_markdown_with_yaml_header_from_file(filename):
    """
    Reads YAML header and contents from file.

    See load_markdown_with_yaml_header for details.
    """

    with open(filename, 'r') as inp:
        return load_markdown_with_yaml_header(inp)
