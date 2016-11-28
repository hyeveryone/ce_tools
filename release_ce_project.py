#!python3
"""
This script combines the required engine and project files into a single directory.
It does not package the assets into .pak files, it simply collects the files that are present.
"""
import os
import shutil
import fnmatch
import subprocess

engine_version = '5.2'
engine_path = r'C:\Program Files (x86)\Crytek\CRYENGINE Launcher\Crytek\CRYENGINE_{}'.format(engine_version)

project_path = os.path.join(engine_path, 'Templates', 'cpp', 'RollingBall')
export_path = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], 'Desktop', 'ce_game')
dll_name = 'Game.dll'

binary_excludes = ['imageformats**',
                   'ToolkitPro*',
                   'platforms**',
                   'Qt*',
                   'mfc*',
                   'CryGame*',
                   'Sandbox*',
                   'ShaderCacheGen*',
                   'smpeg2*',
                   'icu*',
                   'python27*',
                   'LuaCompiler*',
                   'Editor**'
                   ]


def copy_directory(source_dir, rel_dir, excludes):
    """
    Copy a directory to its corresponding location in the export directory.
    :param source_dir: Current location of the files (project_path or engine_path).
    :param rel_dir: Path of the directory to copy, relative to *source_dir*.
    :param excludes: List of filename patterns to exclude from the copying procedure (glob format).
    """
    copypaths = []
    pwd = os.getcwd()
    os.chdir(source_dir)

    for root, _, filenames in os.walk(rel_dir):
        for filename in filenames:
            copypaths.append(os.path.normpath(os.path.join(root, filename)))
    os.chdir(pwd)

    for path in copypaths:
        excluded = False
        for pattern in excludes:
            excluded = excluded or fnmatch.fnmatch(path, os.path.join(rel_dir, pattern))
        if excluded:
            print('Excluding path: {}'.format(path))
            continue
        destpath = os.path.normpath(os.path.join(export_path, path))
        if not os.path.exists(os.path.dirname(destpath)):
            os.makedirs(os.path.dirname(destpath))
        shutil.copy(os.path.join(source_dir, path), destpath)


def copy_levels():
    """
    Copy required level files to the export directory.
    """
    pwd = os.getcwd()
    os.chdir(os.path.join(project_path, 'Assets'))

    level_files = ['filelist.xml', 'terraintexture.pak', 'level.pak']

    for root, _, filenames in os.walk('levels'):
        for filename in filenames:
            if filename not in level_files:
                continue
            path = os.path.normpath(os.path.join(root, filename))
            destpath = os.path.normpath(os.path.join(export_path, 'Assets', path))
            if not os.path.exists(os.path.dirname(destpath)):
                os.makedirs(os.path.dirname(destpath))
            shutil.copy(os.path.join(project_path, 'Assets', path), destpath)

    os.chdir(pwd)
    return


def copy_assets():
    assetpath = os.path.join(project_path, 'Assets')
    for itemname in os.listdir(assetpath):
        itempath = os.path.join(project_path, 'Assets', itemname)
        if 'evels' in itempath:
            continue

        if os.path.isfile(itempath):
            shutil.copyfile(itempath, os.path.join(export_path, 'Assets', itemname))
        else:
            zip_cmd = ['7z',
                       'a',
                       '-r',
                       '-tzip',
                       '-mx0',
                       os.path.join(export_path, 'Assets', '{}.pak'.format(itemname)),
                       os.path.join(assetpath, 'Assets', itempath)]
            print('"{}"'.format(' '.join(zip_cmd)))
            subprocess.check_call(zip_cmd)
    return


def copy_config():
    with open(os.path.join(export_path, 'system.cfg'), 'w') as fd:
        fd.write('sys_game_folder=Assets\n')
        fd.write('sys_dll_game={}\n'.format(dll_name))


def copy_game_dll():
    global dll_name

    binpath = os.path.join(project_path, 'bin', 'win_x64')
    for filename in os.listdir(binpath):
        if not fnmatch.fnmatch(os.path.join(binpath, filename), '*.dll'):
            continue

        dll_name = filename
        shutil.copyfile(os.path.join(binpath, filename),
                        os.path.join(export_path, 'bin', 'win_x64', filename))

# Engine (common) files.
copy_directory(engine_path, 'engine', [])
copy_directory(engine_path, os.path.join('bin', 'win_x64'), binary_excludes)

# Project-specific files.
copy_assets()
copy_levels()
copy_game_dll()
copy_config()
