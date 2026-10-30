#!/usr/bin/env python3
"""Integrate Kazumi NX direct-source screen into pinned StreamFinEX sources.

Fail closed if upstream source changes. This is a playback/UI P0 experiment,
not an implementation of Kazumi's XPath/WebView rules.
"""
import argparse
from pathlib import Path
import shutil

def once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError("%s: expected 1 anchor, found %s" % (label, count))
    return text.replace(old, new, 1)

def apply(base, overlay):
    cmake = base / "CMakeLists.txt"
    home = base / "app/src/activity/stremio_home.cpp"
    main = base / "app/src/main.cpp"
    analytics = base / "app/include/api/analytics.hpp"
    for path in [cmake, home, main, analytics]:
        if not path.is_file():
            raise FileNotFoundError(str(path))

    c = cmake.read_text(encoding="utf-8")
    c = once(c, "project(StreamFin)", "project(KazumiNX)", "project")
    c = once(c, 'set(PROJECT_AUTHOR "Kirbosh")',
             'set(PROJECT_AUTHOR "Kazumi NX Contributors")', "author")
    c = once(c, "resources/icon/icon.jpg",
             "resources/icon/kazuminx.jpg", "icon")

    h = home.read_text(encoding="utf-8")
    h = once(h, '#include "activity/stremio_anime.hpp"',
             '#include "activity/stremio_anime.hpp"\n#include "kazumi_nx/sources.hpp"', "include")
    extra = """    // Kazumi NX direct-source browser; reuse existing working UI & player.
    auto* kz = new brls::Box();
    kz->setFocusable(true);
    kz->setPadding(9, 16, 9, 16);
    kz->setCornerRadius(8);
    kz->setBackgroundColor(nvgRGBA(55, 100, 135, 200));
    auto* kzLabel = new brls::Label();
    kzLabel->setText("Kazumi NX Sources");
    kzLabel->setFontSize(21);
    kz->addView(kzLabel);
    kz->registerClickAction([](brls::View*) -> bool {
        KazumiNX::openSources();
        return true;
    });
    kz->addGestureRecognizer(new brls::TapGestureRecognizer(kz));
    bar->addView(kz);
    this->boxHome->addView(bar);"""
    h = once(h, "    this->boxHome->addView(bar);", extra, "navigation")
    h = once(h,
             '    if (stremio::STREAM_ADDON.empty())\n        brls::sync([]() { promptForAddon(""); });',
             "    // No addon is required for Kazumi NX direct playback.",
             "initial addon prompt")

    m = main.read_text(encoding="utf-8")
    m = once(m, "#include <borealis.hpp>",
             "#include <borealis.hpp>\n#include <cstdio>\n#include <sys/stat.h>",
             "main header")
    m = once(m, "    // Init the app and i18n",
             """    // Best-effort diagnostic log in a separate Kazumi NX config folder.
    mkdir("sdmc:/config", 0777);
    mkdir(conf.configDir().c_str(), 0777);
    if (FILE* logfile = std::fopen((conf.configDir() + "/kazuminx.log").c_str(), "w")) {
        brls::Logger::setLogLevel(brls::LogLevel::LOG_DEBUG);
        brls::Logger::setLogOutput(logfile);
        brls::Logger::info("[KazumiNX] StreamFinEX-based native P0");
    }

    // Init the app and i18n""", "log initialization")
    a = analytics.read_text(encoding="utf-8")
    a = once(a,
        '#define GA(a, ...) analytics::Analytics::instance().report(a, ##__VA_ARGS__);',
        '#define GA(a, ...) ((void)0)', "disable analytics")

    # Write validated files only after all anchors have been checked.
    cmake.write_text(c, encoding="utf-8")
    home.write_text(h, encoding="utf-8")
    main.write_text(m, encoding="utf-8")
    analytics.write_text(a, encoding="utf-8")
    cpp = base / "app/src/kazumi_nx/sources.cpp"
    hpp = base / "app/include/kazumi_nx/sources.hpp"
    cpp.parent.mkdir(parents=True, exist_ok=True)
    hpp.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(overlay / "sources.cpp", cpp)
    shutil.copyfile(overlay / "sources.hpp", hpp)

def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, default=Path(__file__).resolve().parents[1] / "overlay")
    args = parser.parse_args()
    apply(args.upstream.resolve(), args.overlay.resolve())
    print("Applied Kazumi NX StreamFinEX P0 overlay; compile & hardware validation still required.")

if __name__ == "__main__":
    main_cli()
