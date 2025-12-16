#!/usr/bin/env python3
# vim: ts=4 sts=4 sw=4 et

from os import chdir, mkdir, makedirs, symlink, rmdir, walk
from os.path import (
    basename, exists, expanduser, isdir, join, relpath, realpath, samefile,
)
from shutil import copy, copyfile, move
import re
from subprocess import CalledProcessError, run
import sys
from typing import Union

def run_command(command: Union[list[str], str]):
    """
    Run the command and return the output
    """
    shell = isinstance(command, str)
    result = subprocess.run(command, shell=shell, capture_output=True, text=True)
    return result.stdout

def get_output(command):
    """ Run the given command and return the output of the command. """
    try:
        from subprocess import check_output
    except ImportError:
        def check_output(popen_args, **kwargs):
            from subprocess import Popen, PIPE
            p = Popen(popen_args, stdout=PIPE, **kwargs)
            out, _ = p.communicate()
            p.poll()
            return out
    return check_output(command.split(), universal_newlines=True)

def inst_and_back(src, dest, bak):
    """ Copy files from src to dest, backing up existing files to bak. """
    # Walk the directory structure
    for d, _, fs in walk(src):
        # Calculate paths
        rel_path = relpath(d, src)
        src_path = join(src, rel_path)
        dest_path = join(dest, rel_path)
        bak_path = join(bak, rel_path)

        for f in fs:
            # Calculate file paths
            f_src_path = join(src_path, f)
            f_dest_path = join(dest_path, f)
            f_bak_path = join(bak_path, f)

            # If the file exists, we need to make a backup of it
            if exists(f_dest_path):
                # Create the directory structure if it doesn't already exists
                if not exists(bak_path):
                    makedirs(bak_path)
                # Move the previous file to the new location
                move(f_dest_path, f_bak_path)

            # Finally, try to install the new file. Ensure that the installation
            # path exists and create the directory structure, then copy the file
            # over.
            if exists(dest_path) and not isdir(dest_path):
                unlink(dest_path)
            if not isdir(dest_path):
                makedirs(dest_path)
            copy(f_src_path, f_dest_path)

install_dir = realpath(expanduser('~'))

version_file = join(install_dir, '.dotfiles-version')
repo_file = join(install_dir, '.dotfiles-repo')

# Move into the repo directory. If it doesn't exist
# it is expected that the cwd is the repo location.
if exists(repo_file):
    with open(repo_file, 'r') as f:
        repo_path = f.read().strip()
    if not repo_path or not isdir(repo_path):
        print('Repo path "%s" is not a directory.' % repo_path)
        exit(1)
    repo_path = realpath(repo_path)
    chdir(repo_path)
else:
    try:
        repo_path = get_output("git rev-parse --show-toplevel").strip()
        chdir(repo_path)
    except CalledProcessError:
        print("Unable to find .dotfiles repository.")
        exit(1)

# Read the version
if not exists(version_file):
    print('Performing initial installation...')
    installed_version = '000000000000'
    initial_install = True
else:
    with open(version_file, 'r') as f:
        installed_version = f.read().strip()
    initial_install = False
    print('Currently installed version:', installed_version)

# Check for changes
changes = get_output("git status -s").strip()
if changes:
    print("Error: local changes in repository")
    sys.exit(1)

# get the current revision
new_version = get_output("git rev-parse HEAD").strip()
if new_version == installed_version:
    print('New version %s is already installed.' % new_version)
    sys.exit(0)

# Start the installation process
print('Installing new version:', new_version)

# Figure out which files which are candidates for installation
files = get_output("find . -maxdepth 1 -print0")

# Figure out which files we'll ignore. Initially create a regexp which
# will never match.
try:
    with open(join(repo_path, '.dotfiles-ignore'), 'r') as f:
        ignore = '|'.join(
            '(%s)' % (line[:-1])
            for line in f
            if line.strip() and not line.startswith('#')
        )
        if ignore:
            ignore = re.compile(ignore)
        else:
            ignore = re.compile("$x")
except (IOError, OSError):
    ignore = re.compile("$x")

# Figure out which files only need to be installed once
# and then should NOT be version controlled.
try:
    with open(join(repo_path, '.dotfiles-once'), 'r') as f:
        install_once = '|'.join(
            '(%s)' % (line[:-1])
            for line in f
            if line.strip() and not line.startswith('#')
        )
        if install_once:
            install_once = re.compile(install_once)
        else:
            install_once = re.compile("$x")
except (IOError, OSError):
    install_once = re.compile("$x")

# Create a backup folder incase we encounter any conflicts
tmp_dir = join(install_dir, new_version)
if exists(tmp_dir):
    print("Error: Temporary directory already exists.")
    exit(1)
mkdir(tmp_dir)

for line in files.split('\0'):
    # Strip the leading ./
    line = line[2:]
    if not line:
        continue

    # Determine the install path
    inst = join(install_dir, line)
    source = join(repo_path, line)

    # Try installing things that should only be installed once
    # if this is an initial installation
    if install_once.match(line):
        if not initial_install:
            continue
        if isdir(source):
            inst_and_back(source, inst, tmp_dir)
        else:
            if exists(inst):
                move(inst, tmp_dir)
            copyfile(source, inst)
            # Set the path to ignored in git
            get_output("git update-index --assume-unchanged {}".format(line))
        continue

    # Ignore files which do not need to be installed
    if ignore.match(line):
        continue

    # Otherwise, make sure that a symlink exists. If it doesn't, make one
    if exists(inst):
        # Check if the symlink is installed
        if samefile(inst, source):
            continue
        # Otherwise make a backup of the existing file
        move(inst, tmp_dir)
    path = relpath(source, install_dir)
    print(path)
    # Finally, make a symlink to the location
    symlink(path, inst)

# Write out the new version details
print('Writing version number and repo.')
f = open(version_file, 'w')
f.write(new_version)
f.close()

f = open(repo_file, 'w')
f.write(repo_path)
f.close()

# Finally we check if the temp-directory was needed. If not, we remove it.
try:
    rmdir(tmp_dir)
except OSError:
    print("Backed up some files into ~/%s" % (basename(tmp_dir)))
