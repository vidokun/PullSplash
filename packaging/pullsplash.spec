# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

datas = (
    collect_data_files("fastapi")
    + [("../backend/templates", "backend/templates")]
    + collect_data_files("webview", subdir="js")
)

hiddenimports = (
    [
        "PIL", "PIL._webp", "PIL._imaging", "PIL.Image",
        "uvicorn.logging", "uvicorn.loops.auto", "uvicorn.loops.asyncio",
        "uvicorn.protocols.http.auto", "uvicorn.protocols.http.h11_impl",
        "uvicorn.lifespan.on",
        "fastapi", "pydantic", "pydantic.deprecated.decorator",
        "anyio", "anyio._backends._asyncio",
        "webview", "webview.platforms.cocoa", "webview.js",
        "webview.guilib", "webview.http",
        "bottle", "proxy_tools",
        "Foundation", "AppKit", "WebKit", "Quartz",
        "objc", "objc._objc", "objc._bridges",
        "PyObjCTools", "PyObjCTools.AppHelper",
    ]
    + collect_submodules("backend")
)

a = Analysis(
    ["../launcher.py"],
    pathex=[".."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy", "pandas", "scipy", "IPython", "jupyter", "notebook", "sqlalchemy", "tensorflow", "torch"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name="PullSplash", debug=False, strip=False, upx=True,
    console=True, icon="../branding/icon.icns",
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name="PullSplash.app",
    icon="../branding/icon.icns",
    bundle_identifier="com.pullsplash.app",
    info_plist={
        "NSHighResolutionCapable": True,
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleName": "PullSplash",
        "CFBundleExecutable": "PullSplash",
    },
)
