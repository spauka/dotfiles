#!/usr/bin/env python

import os
from os import readlink
from os.path import (
    dirname, exists, expanduser, islink, join, lexists, realpath, relpath,
)
import re
from subprocess import Popen, PIPE
import sys

install_dir = expanduser('~')

# Get the current version.

version_file = join(install_dir, '.dotfiles-version')
repo_file = join(install_dir, '.dotfiles-repo')

if not exists(version_file):
    print 'Performing initial installation...'
    installed_version = '000000000000'
else:
    f = open(version_file, 'rU')
    installed_version = f.read().strip()
    f.close()
    print 'Currently installed version:', installed_version

# Find changed files between the installed revision and the current revision.

p = Popen(args=['hg', 'root'], stdin=PIPE, stdout=PIPE)
out, _ = p.communicate('')
new_repo = out.strip()

# if this can be expressed relative to install_dir, we want to do that.

def maybe_relpath(path, start):
    rv = relpath(path, realpath(start))
    # TODO: this is a non-portable hack
    if rv.startswith('../'):
        return path
    return join(start, rv)

new_repo = maybe_relpath(new_repo, install_dir)

# get the current revision

p = Popen(args=['hg', 'id', '-i'], stdin=PIPE, stdout=PIPE)
out, _ = p.communicate('')
new_version = out.strip()

if new_version.endswith('+'):
    print 'ERROR: local changes in repository'
    sys.exit(1)

if new_version == installed_version:
    print 'New version %s is already installed.' % new_version
    sys.exit(0)

print 'Installing new version:', new_version

p = Popen(
    args=[
        'hg', 'status',
        '--rev', installed_version,
        '-0', '-a', '-r',
    ],
    stdin=PIPE,
    stdout=PIPE,
)
out, _ = p.communicate('')

# Figure out which files we'll ignore
regexp = None
try:
    f = open(join(new_repo, '.dotfiles-ignore'), 'rU')
except (IOError, OSError), e:
    pass
else:
    regexp = '|'.join(
        '(%s)' % line[:-1]
        for line in f
    )
    regexp = re.compile(regexp)
    f.close()

# Check to see if there are any manually edited files.

queued_links = []
queued_removals = []

errors = False

for line in out.split('\0'):
    if not line: continue
    status, filename = line.split(' ', 1)

    if regexp and regexp.match(filename):
        continue

    install_filename = join(install_dir, filename)
    link_path = relpath(join(new_repo, filename), dirname(install_filename))
#    print install_filename, '->', link_path

    if status == 'A':
        # Sanity checking
        if lexists(install_filename):
            if islink(install_filename):
                target = readlink(install_filename)
                if target == link_path:
                    print 'WARNING: the symlink (%s -> %s) already exists' % (
                        install_filename, target,
                    )
                elif realpath(target) == realpath(link_path):
                    print (
                        'WARNING: the symlink (%s -> %s) already exists '
                        'but is not canonical'
                    ) % (install_filename, target)
                else:
                    print (
                        'ERROR: the symlink %s already exists, and does not '
                        'point somewhere I know about'
                    ) % (install_filename,)
                    errors = True
                    continue
            else:
                print (
                    'ERROR: the file %s already exists, and is not a symlink'
                ) % (install_filename,)
                errors = True
                continue

        # Otherwise, it's fine to make the link.
        queued_links.append((install_filename, link_path))

    else:
        assert status == 'R'

        # Sanity checking
        if not lexists(install_filename):
            print 'WARNING: the file %s has already been deleted' % (
                install_filename,
            )
            continue
        elif not islink(install_filename):
            print 'ERROR: the file %s should have been a symlink' % (
                install_filename,
            )
            errors = True
            continue
        else:
            target = readlink(install_filename)
            if target == link_path:
                pass # expected case
            elif realpath(target) == realpath(link_path):
                print 'WARNING: the symlink (%s -> %s) is not canonical' % (
                    install_filename, target,
                )
            else:
                print (
                    'ERROR: the symlink %s does not point where it should'
                ) % (install_filename,)
                errors = True
                continue

        queued_removals.append(install_filename)

if errors:
    print 'Errors found, exiting...'
    sys.exit(1)

print 'Installing new symlinks...'
for install_filename, link_path in queued_links:
    directory = dirname(install_filename)
    if not exists(directory):
        os.makedirs(directory)
    try:
        os.remove(install_filename)
    except OSError:
        pass # probably the file didn't exist already
    os.symlink(link_path, install_filename)

print 'Removing old symlinks...'
for install_filename in queued_removals:
    os.remove(install_filename)

print 'Writing version number and repo.'
f = open(version_file, 'w')
f.write(new_version)
f.close()

f = open(repo_file, 'w')
f.write(new_repo)
f.close()
