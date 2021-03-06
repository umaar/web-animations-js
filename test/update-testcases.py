#!/usr/bin/python

import cStringIO as StringIO
from fnmatch import fnmatch
import difflib
import os
import sys


def get_name(filename):
    return os.path.splitext(filename)[0]


def list_dir(dir_path, filter_func):
    return sorted(filter(filter_func, os.listdir(dir_path)), key=get_name)


def main():
    test_dir = os.path.dirname(os.path.realpath(__file__))
    testcase_dir = os.path.join(test_dir, 'testcases')
    testcase_file = os.path.join(test_dir, 'testcases.js')
    testcases_disabled = os.path.join(test_dir, 'disabled-testcases')

    disabled_tests = [
        x.split("#")[0].strip() for x in file(testcases_disabled).readlines()]

    def is_testcase_file(filename):
        return (
            fnmatch(filename, "*.html") and
            not fnmatch(filename, "manual-test*") and
            filename not in disabled_tests)

    new_testcases = StringIO.StringIO()
    new_testcases.write("""\
// This file is automatically generated by test/update-testcases.py.
// Disable tests by adding them to test/disabled-testcases
""")
    new_testcases.write('var tests = [\n  \'')
    new_testcases.write(
        '\',\n  \''.join(list_dir(testcase_dir, is_testcase_file)))
    new_testcases.write('\',\n];\n')
    new_testcases.seek(0)
    new_testcases_lines = new_testcases.readlines()

    current_testcases_lines = file(testcase_file).readlines()

    lines = list(difflib.unified_diff(
        current_testcases_lines, new_testcases_lines,
        fromfile=testcase_file, tofile=testcase_file))

    if "--update" in sys.argv:
        file(testcase_file, "w").write("".join(new_testcases_lines))

    for line in lines:
        sys.stdout.write(line)

    sys.exit(int(len(list(lines)) > 0))


if __name__ == '__main__':
    main()
