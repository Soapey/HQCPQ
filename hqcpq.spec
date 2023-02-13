# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['hqcpq\\hqcpq.py'],
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
    name='HQCPQ_1.0.0',
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
from hqcpq.helpers import resource_path


attachment_directory_path = resource_path("dist\\hqcpq\\")

if not os.path.exists(attachment_directory_path):
    os.mkdir(attachment_directory_path)

shutil.copyfile(
    resource_path("hqcpq\\hq_keq_logos.jpg"),
    os.path.join(attachment_directory_path, "hq_keq_logos.jpg"),
)
shutil.copyfile(
    resource_path("hqcpq\\config.ini"),
    os.path.join(attachment_directory_path, "config.ini"),
)
