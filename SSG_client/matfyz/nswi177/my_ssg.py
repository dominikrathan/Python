#!/usr/bin/env python3

"""
my_ssg - My simple static site generator for
the NSWI177 course at MFF CUNI.
"""

import argparse
import os
import pathlib
import sys
import shutil
import jinja2
import markdown

import matfyz.nswi177.mdyml as mdyml
import matfyz.nswi177.files as files

VERSION = "1.1"

def generate_one_file(template, all_pages, base_dir, input_filename, destination_filename):
    """
    Generate one HTML file from Markdown source.

    Parameters
    ----------
    template
        Templating engine object.
    all_pages: list
        List of all pages (already pre-parsed).
    base_dir: str
        Base directory with content
    input_filename: str
        Filename to process.
    destination_filename: str
        Where to store the converted file.
    """

    print("{} => {}".format(input_filename, destination_filename))
    (meta, content) = mdyml.load_markdown_with_yaml_header_from_file(input_filename)

    SITE = setup_site(base_dir, input_filename, all_pages)

    rendered = template.render(
        title = meta['title'],
        content = content,
        SITE = SITE,
        home = True if 'home' in meta else False
    )

    tidied = tidy_html(rendered)

    with open(destination_filename, 'w') as out:
        out.write(tidied)


def setup_site(base_dir, input_filename, all_pages):
    """
    Sets up site variable with path to root and list of all pages

    Parameters
    ----------
    base_dir: str
        Base directory with content
    input_filename: str
        Filename to process.
    destination_filename: str
        Where to store the converted file.
    """

    path_to_root = os.path.relpath(base_dir, pathlib.Path(input_filename).parent) + '/'

    SITE = {
        'path_to_root': path_to_root,
        'pages': all_pages
        }

    return SITE

def get_html_filename(relative_markdown_filename):
    """
    Get HTML filename from given Markdown filename.
    """

    return os.path.splitext(relative_markdown_filename)[0] + '.html'


def get_template_filename(templates_dir):
    """
    Get template filename in a given directory
    Returns either the only template present or if multiple are present the main one named 'main.j2'
    """

    templates_dir_content = [template for template in os.listdir(templates_dir) if template.endswith('.j2')]
    templates_count = len(templates_dir_content)

    if (templates_count == 1):
        return templates_dir_content[0]
    elif (templates_count > 1):
        for file in templates_dir_content:
            if (file == "main.j2"):
                return file

    raise Exception('Template not found. Please ensure there is \'main.j2\' template present in /templates')


def get_markdownify_template(templates_dir):
    """
    Sets jinja2 template with markdownify filter
    """
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))

    from markdown import markdown
    environment.filters['markdownify'] = markdown

    template_filename = get_template_filename(templates_dir)
    return environment.get_template(template_filename)

def tidy_html(html):
    """
    Tidy html string with proper indentation, omit doctype and limit number of chars per line to 80
    """
    from tidylib import tidy_document
    return tidy_document(html, options = {'doctype': 'omit', 'wrap':80})[0]

def action_generate(content_dir, templates_dir, static_dir, destination_dir):
    """
    Callback for the `generate` action.

    Parameters
    ----------
    content_dir: str
        Path to directory with input Markdown files.
    templates_dir: str
        Path to directory with Jinja templates.
    static_dir: str
        Path to directory with static files (CSS, images etc.).
    destinatation_dir: str
        Path to directory where to put the generated files.
    """

    from distutils.dir_util import copy_tree
    if (os.path.isdir(static_dir)):
        copy_tree(static_dir, destination_dir)

    template = get_markdownify_template(templates_dir)
    all_pages = get_all_pages(content_dir)

    for (file_in, file_in_rel, relative_dirname) in files.relative_paths_walk(content_dir, '*.md'):
        dir_out = os.path.join(destination_dir, relative_dirname)
        file_out = os.path.join(destination_dir, get_html_filename(file_in_rel))

        pathlib.Path(dir_out).mkdir(parents=True, exist_ok=True)
        generate_one_file(template, all_pages, content_dir, file_in, file_out)

class page:
    def __init__(self, meta, link):
        self.meta = meta
        self.link = link

def get_all_pages(content_dir):
    """
    Get list of all pages present in the given directory
    """
    files_in = files.relative_paths_walk(content_dir, '*.md')
    all_pages = []

    for file in files_in:
        (meta, content) = mdyml.load_markdown_with_yaml_header_from_file(file[0])
        all_pages.append(page(meta, get_html_filename(file[1])))

    return all_pages


def action_version():
    """
    Prints current version
    """
    print(VERSION)

def main():
    """
    Entry point of the whole program.

    Only parses command-line arguments and executes the right callback.
    """
    args = argparse.ArgumentParser(description='My SSG')
    args_sub = args.add_subparsers(help='Select what to do')
    args.set_defaults(action='help')
    args_help = args_sub.add_parser('help', help='Show this help.')
    args_help.set_defaults(action='help')

    args_version = args_sub.add_parser(
        'version',
        help='Show version of this tool.'
    )
    args_version.set_defaults(action='version')

    args_generate = args_sub.add_parser(
        'generate',
        help='Generate the web.'
    )
    args_generate.set_defaults(action='generate')
    args_generate.add_argument(
        '--content',
        dest='content_dir',
        default='content/',
        metavar='PATH',
        help='Directory with source (content) files.'
    )
    args_generate.add_argument(
        '--templates',
        dest='templates_dir',
        default='templates/',
        metavar='PATH',
        help='Directory with Jinja templates.'
    )
    args_generate.add_argument(
        '--static',
        dest='static_dir',
        default='static/',
        metavar='PATH',
        help='Directory with static files (images, styles, ...).'
    )
    args_generate.add_argument(
        '--destination',
        dest='destination_dir',
        default='out/',
        metavar='PATH',
        help='Directory where to store the result.'
    )

    if len(sys.argv) < 2:
        # pylint: disable=too-few-public-methods,missing-class-docstring
        class HelpConfig:
            def __init__(self):
                self.action = 'help'
        config = HelpConfig()
    else:
        config = args.parse_args()

    if config.action == 'help':
        args.print_help()
    elif config.action == 'generate':
        action_generate(
            config.content_dir,
            config.templates_dir,
            config.static_dir,
            config.destination_dir
        )
    elif config.action == 'version':
        action_version()
    else:
        raise Exception("Internal error, unknown action")

if __name__ == '__main__':
    main()
