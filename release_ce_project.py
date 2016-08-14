#!python3
"""
This script combines the required engine and project files into a single directory.
It does not package the assets into .pak files, it simply collects the files that are present.
"""
import os
import shutil
import fnmatch

engine_path = r'C:\Program Files (x86)\Crytek\CRYENGINE Launcher\Crytek\CRYENGINE_5.1'
project_path = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], 'Desktop', 'test1')
export_path = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], 'Desktop', 'ce_game')

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


def copy_config():
    """
    Copy the contents of system.cfg and project.cfg to the exported project's system.cfg.
    """
    project_cfg = open(os.path.join(project_path, 'project.cfg')).readlines()
    system_cfg = open(os.path.join(engine_path, 'system.cfg')).readlines()

    with open(os.path.join(export_path, 'system.cfg'), 'w') as fd:
        fd.writelines(system_cfg)
        fd.writelines(project_cfg)


copy_directory(engine_path, 'engine', [])
copy_directory(engine_path, os.path.join('bin', 'win_x64'), binary_excludes)

copy_directory(project_path, 'Assets', ['Levels*'])
copy_directory(project_path, os.path.join('bin', 'win_x64'), binary_excludes)

copy_levels()
copy_config()
