from pathlib import Path

root = Path(SPECPATH)

a = Analysis(
    [str(root / "scripts" / "launcher.py")],
    pathex=[str(root / "src")],
    datas=[
        (str(root / "README.md"), "."),
        (str(root / "SECURITY.md"), "."),
        (str(root / "rules.md"), "."),
        (str(root / "assets" / "senpai_bot.ico"), "assets"),
    ],
    hiddenimports=[],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True,
    name="Senpai_Bot", icon=str(root / "assets" / "senpai_bot.ico"),
    console=False, debug=False,
)
coll = COLLECT(exe, a.binaries, a.datas, name="Senpai_Bot")
