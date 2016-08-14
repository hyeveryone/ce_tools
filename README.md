# ce_tools
Small scripts to simplify and automate working with CRYENGINE, it is hoped that these scripts can be pushed upstream.
Only Python 3.5 has been used in development, earlier versions of Python 3 are likely, but not guaranteed, to work.

## release_ce_project.py
This script combines the required engine and project files into a single directory.
It does not package the assets into .pak files, it simply collects the files that are present.
In order to set the paths, it is necessary to edit the <name>_path variables at the top of the script.
