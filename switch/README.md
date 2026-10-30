# Kazumi NX — P0/P1 native Switch proof of concept

A **very early** Nintendo Switch homebrew experiment that borrows the battle-tested
Borealis UI, video view, FFmpeg and mpv integration from [wiliwili]
(https://github.com/xfangfang/wiliwili), and provides a small Kazumi NX launcher.

**Status: source scaffold committed; it is not yet verified to compile or play on hardware.**
This does **not** yet implement Kazumi's Flutter UI, anime metadata, XPath/API rules,
WebView extraction, favourites, or subtitles. Do not confuse this with a completed port.

## Source / provenance

- Original app: https://github.com/Predidit/Kazumi
- This experiment: Kazumi repository branch port/switch-wiliwili-mvp
- Base player/UI: https://github.com/xfangfang/wiliwili
- Upstream wiliwili ref pinned to 88e5876bea9502d06f46a8656e3530684d3aaf7d
- Existing Borealis, libnx, mpv, FFmpeg and other libraries remain third-party
  components with their respective licenses.
- This overlay has not copied Kazumi artwork or Mi Sans fonts, whose use requires
  separate permission/licence review.
- Both Kazumi and wiliwili are GPL-3.0 licensed. Distributions of a combined
  executable must comply with the relevant obligations including source offers
  and notices. **Do not distribute a binary without checking dependencies.**

## What the test build does

- Launches a native .nro with Borealis and Switch controller support.
- Shows a minimal video list: either entries from SD card or two public test URLs.
- Uses wiliwili VideoView/MPVCore to open MP4 or HLS/M3U8 HTTP(S) streams.
- Keeps the wiliwili resource/layout tree for this exploratory build.
- Disables wiliwili startup analytics and its Bilibili update check.
- Does not send user information to a new Kazumi NX server.

## How to build (GitHub Actions)

Run the "Kazumi NX Switch P0/P1" workflow on branch port/switch-wiliwili-mvp.
It clones the pinned wiliwili revision including its git submodules, adds this
overlay, and invokes upstream's Switch Docker build script. If compilation works,
download the uploaded artifact KazumiNX-P0 from the Actions run.

If the workflow fails, collect the log. Do **not** treat an uploaded file as
hardware-validated until it boots on your Switch.

## SD card layout

    sdmc:/switch/KazumiNX/KazumiNX.nro
    sdmc:/switch/KazumiNX/streams.txt

Example streams.txt:

    MP4 demo|https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4
    HLS demo|https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8

Line format: Title|https://direct-video-url. Blank and # comment lines are
ignored. First 20 valid entries are listed. Only direct HTTP(S) URLs are
supported at this stage. The list falls back to built-in test URLs if no valid
configuration file exists. No bypass of DRM or paywalls is implemented.

Launch via **Application Mode**: hold R while starting a game, open hbmenu,
and start KazumiNX.nro. The applet/Album mode may not have enough memory.

## Development milestones

- P0: obtain a reproducible CI compilation and test basic UI/controller/exit.
- P1: verify MP4 and HLS on real hardware, including 30-minute stability.
- P2: port subset of Kazumi API/JSONPath and XPath rules into C++.
- P3: address sites requiring JavaScript/WebView with an optional helper.
- P4: history, catalogue, subtitles and deeper feature compatibility.

## Limitations

The overlay is intentionally thin and wiliwili's full application code still
compiles and links. A later cleanup should remove Bilibili-only modules, strip
unused telemetry, replace wiliwili branding and move to a dedicated repository.
No network-enabled dependency graph has been built locally in this environment.
