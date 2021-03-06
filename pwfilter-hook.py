#!/usr/bin/env python

import os
import shutil
import subprocess as sub

FILTER_FILE = "filter"
FILTER_BASE = "gitfilter"


def files_to_filter():
    with open(FILTER_FILE, 'r') as filters:
        return filters.readlines()


def filters_for_file(fname):
    d = {}
    for f in filters_from_passdb(fname):
        add_filter_rule(d, f)
    return d


def filters_from_passdb(rel_path):
    filter_pass = os.path.join(FILTER_BASE, rel_path)
    cmd = ['pass', filter_pass]
    out = sub.Popen(cmd, stdout=sub.PIPE).communicate()[0]
    filters = sanitize_popen_output(out)
    return filters.splitlines()


def add_filter_rule(filter_rules, rule):
    if current_hook() == "pre-commit":
        cipher, secret = rule.split(':', 1)
    elif current_hook() in ["post-commit", "post-merge"]:
        secret, cipher = rule.split(':', 1)
    filter_rules[secret] = cipher


def current_hook():
    return os.path.basename(__file__)


def filter_file(fname, filters):
    with open(fname, 'r') as infile, open(fname+'tmp', 'w') as outfile:
        for line in infile:
            line = filter_line(line, filters)
            outfile.write("%s" % line)
    os.remove(fname)
    shutil.move(fname+'tmp', fname)


def filter_line(line, filters):
    for token, subst in filters.items():
        line = line.replace(token, subst)
    return line


def file_is_staged(fname):
    cmd = ['git', 'diff', '--name-only', '--cached']
    out = sub.Popen(cmd, stdout=sub.PIPE).communicate()[0]
    staged_files = sanitize_popen_output(out)
    return fname in staged_files


def sanitize_popen_output(output):
    return output.strip().decode('utf-8')


def stage_file(fname):
    cmd = ['git', 'add', fname]
    sub.Popen(cmd).wait()


if __name__ == "__main__":

    for fname in files_to_filter():
        fname = fname.strip()
        filters = filters_for_file(fname)
        filter_file(fname, filters)
        if current_hook() == "pre-commit" and file_is_staged(fname):
            stage_file(fname)
