# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Hunter Quarries Quoting Application',
    author='Grant Soper',
    description='A small application to produce quotes.',
    icon='hqcpq\\assets\\hqcpq.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

import os
import shutil
from hqcpq.helpers.io import join_to_project_folder

# Set up sub main folder and include config.ini file
sub_directory_path = join_to_project_folder(os.path.join("dist", "hqcpq"))
if not os.path.exists(sub_directory_path):
    os.mkdir(sub_directory_path)
    shutil.copyfile(
        join_to_project_folder(os.path.join("hqcpq", "config.ini")),
        os.path.join(sub_directory_path, "config.ini"),
    )
    shutil.copyfile(
        join_to_project_folder(os.path.join("hqcpq", "quote_email_body.txt")),
        os.path.join(sub_directory_path, "quote_email_body.txt"),
    )
# Set up db folder and include init.sql file
db_directory_path = join_to_project_folder(os.path.join(sub_directory_path, "db"))
if not os.path.exists(db_directory_path):
    os.mkdir(db_directory_path)
    shutil.copyfile(
        join_to_project_folder(os.path.join("hqcpq", "db", "init.sql")),
        os.path.join(db_directory_path, "init.sql")
    )

# Copy the entire assets folder
assets_directory_path = join_to_project_folder(os.path.join(sub_directory_path, "assets"))
if not os.path.exists(assets_directory_path):
    shutil.copytree(
        join_to_project_folder(os.path.join("hqcpq", "assets")),
        assets_directory_path,
    )
