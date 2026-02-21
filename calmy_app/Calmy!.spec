# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['calmy.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('data/data.db', 'data'), ('pre-splash.kv', '.'), ('welcome.kv', '.'), ('about.kv', '.'), ('info.kv', '.'), ('signup1.kv', '.'), ('signup2.kv', '.'), ('signup3.kv', '.'), ('signup4.kv', '.'), ('signup5.kv', '.'), ('signup6.kv', '.'), ('login.kv', '.'), ('profil.kv', '.'), ('notif.kv', '.'), ('main.kv', '.'), ('bmi.kv', '.'), ('bmr.kv', '.'), ('program.kv', '.'), ('daily.kv', '.'), ('recap.kv', '.'), ('update.kv', '.'), ('verif.kv', '.'), ('change.kv', '.'), ('food.kv', '.')],
    hiddenimports=['kivymd.uix.button', 'kivymd.uix.card', 'kivymd.uix.dialog', 'kivymd.uix.dropdownitem', 'kivymd.uix.divider', 'kivymd.uix.label', 'kivymd.uix.list', 'kivymd.uix.menu', 'kivymd.uix.navigationdrawer', 'kivymd.uix.pickers', 'kivymd.uix.progressbar', 'kivymd.uix.selectioncontrol', 'kivymd.uix.slider', 'kivymd.uix.snackbar', 'kivymd.uix.textfield', 'kivymd.uix.toolbar', 'kivymd.uix.tab', 'kivymd.uix.tooltip', 'kivymd.uix.behaviors', 'kivymd.uix.spinner', 'kivymd.uix.chip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Calmy!',
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
    icon=['assets\\logoapk.ico'],
)
