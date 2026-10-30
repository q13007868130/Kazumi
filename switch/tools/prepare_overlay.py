#!/usr/bin/env python3
"""Apply a small, reviewable Kazumi NX overlay to a pinned wiliwili checkout.

It does not modify the original Kazumi Flutter tree. This is a P0/P1
integration scaffold, NOT a port of Kazumi's search or rule engine.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def apply_overlay(upstream: Path, overlay: Path) -> None:
    main = upstream / "wiliwili" / "source" / "main.cpp"
    if not main.is_file():
        raise FileNotFoundError(f"wiliwili main.cpp not found: {main}")

    source = main.read_text(encoding="utf-8")
    include_anchor = '#include "view/mpv_core.hpp"'
    startup_anchor = "        Intent::openMain();"
    if source.count(include_anchor) != 1 or source.count(startup_anchor) != 1:
        raise RuntimeError("Upstream wiliwili entry changed; inspect before patching.")

    source = source.replace(
        include_anchor,
        include_anchor + '\n#include "kazumi_nx/launcher.hpp"',
        1,
    )
    source = source.replace(startup_anchor, "        KazumiNX::openHome();", 1)
    source = source.replace('createWindow("wiliwili")',
                            'createWindow("Kazumi NX")', 1)

    # Disable wiliwili's startup analytics and Bilibili update check in our MVP.
    analytics_start = source.find('    GA("open_app",')
    update_call = "    APPVersion::instance().checkUpdate();"
    if analytics_start < 0 or source.count(update_call) != 1:
        raise RuntimeError("Upstream analytics block changed; review before patching.")
    analytics_end = source.index(update_call, analytics_start) + len(update_call)
    source = source[:analytics_start] + (
        "    // Kazumi NX does not send wiliwili startup analytics or update checks."
    ) + source[analytics_end:]

    # Update only the pinned wiliwili Switch metadata, not Flutter app.
    cmake = upstream / "CMakeLists.txt"
    if cmake.is_file():
        value = cmake.read_text(encoding="utf-8")
        icon_old = "set(PROJECT_ICON ${CMAKE_CURRENT_SOURCE_DIR}/resources/icon/icon.jpg)"
        icon_new = "set(PROJECT_ICON ${CMAKE_CURRENT_SOURCE_DIR}/resources/icon/kazuminx.jpg)"
        title_old = "COMMAND ${NX_NACPTOOL_EXE} --create ${PROJECT_NAME} ${PROJECT_AUTHOR} ${APP_VERSION} ${PROJECT_NAME}.nacp"
        title_new = 'COMMAND ${NX_NACPTOOL_EXE} --create "Kazumi NX" "Kazumi NX Contributors" ${APP_VERSION} ${PROJECT_NAME}.nacp'
        if value.count(icon_old) != 1 or value.count(title_old) != 1:
            raise RuntimeError("wiliwili CMake metadata changed")
        cmake.write_text(value.replace(icon_old, icon_new).replace(title_old, title_new), encoding="utf-8")
    config = upstream / "wiliwili/source/utils/config_helper.cpp"
    if config.is_file():
        value = config.read_text(encoding="utf-8")
        key = 'return "/config/wiliwili";'
        if value.count(key) != 1:
            raise RuntimeError("wiliwili Switch config path changed")
        config.write_text(value.replace(key, 'return "/config/KazumiNX";'), encoding="utf-8")
    build = upstream / "scripts/build_switch.sh"
    if build.is_file():
        value = build.read_text(encoding="utf-8")
        if value.count("-DBUILTIN_NSP=ON") != 1:
            raise RuntimeError("wiliwili build command changed")
        build.write_text(value.replace("-DBUILTIN_NSP=ON", "-DBUILTIN_NSP=OFF"), encoding="utf-8")
    main.write_text(source, encoding="utf-8")

    dst_cpp = upstream / "wiliwili" / "source" / "kazumi_nx" / "launcher.cpp"
    dst_hpp = upstream / "wiliwili" / "include" / "kazumi_nx" / "launcher.hpp"
    dst_cpp.parent.mkdir(parents=True, exist_ok=True)
    dst_hpp.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(overlay / "launcher.cpp", dst_cpp)
    shutil.copyfile(overlay / "launcher.hpp", dst_hpp)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--overlay", type=Path,
                        default=Path(__file__).resolve().parents[1] / "overlay")
    args = parser.parse_args()
    apply_overlay(args.upstream.resolve(), args.overlay.resolve())
    print("Kazumi NX overlay applied (P0/P1 source only; not yet compiled).")


if __name__ == "__main__":
    main()
