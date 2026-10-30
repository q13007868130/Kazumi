# Kazumi NX for Nintendo Switch — StreamFinEX native experiment (P0)

This is a new proof-of-concept, NOT the completed Flutter Kazumi app port.
Compared to the previous wiliwili experiment, this retains StreamFinEX's
established anime browsing and RemoteView::play full-screen player path.

## Provenance and licenses

- Kazumi: https://github.com/q13007868130/Kazumi (GPL-3.0)
- StreamFinEX: https://github.com/Kirbosh/StreamFinEX (Apache-2.0)
- Base commit: 4ea3cecb3afd91b3b7feff7595b4b74a6e883b4a
- ANIMEX: https://github.com/cuijunhao20000307-web/-ANIMEX-Release
  is CLOSED SOURCE and ONLY a product/UX benchmark. NO ANIMEX executable,
  logo, assets or source code have been copied into this prototype.
- Our integration currently includes no original Kazumi Dart code.
  Future Kazumi rule-engine port must meet GPL-3.0 obligations.
- Preserve upstream license notices and confirm dependencies before publishing.

## P0 features

- Keeps StreamFinEX native Borealis navigation, anime catalog, MPV player.
- Top-bar shortcut "Kazumi NX Sources" opens a direct media test list.
- Reads sdmc:/switch/KazumiNX/streams.txt, format: TITLE|URL.
- Fallback online MP4, HLS/M3U8 plus optional local SD test.mp4.
- Uses existing RemoteView::play() instead of reparenting the video view.
- No Stremio addon required for direct source testing.
- Separate Kazumi NX application title, icon and config folder.
- Disables inherited Google Analytics macros in app compilation.

Not implemented: Kazumi XPath/JSONPath/API rules, anime-to-episode matching,
JavaScript/WebView extraction, importing Kazumi rule JSON, full Chinese UI.

## ANIMEX-inspired test acceptance checklist

- Title discovery + search + episode selection, controller-friendly UI.
- Multiple lines with fallback / errors; video buffering and seeking.
- Poster background caching and memory controls.
- Playback resume and clear diagnostics.

ANIMEX's published notes prove these UX problems matter, but do not reveal
its software design. No permission to copy the closed-source code is implied.

## CI build

Use workflow "Kazumi NX - StreamFinEX Native P0" on
port/switch-streamfinex-mvp. A green Success indicates a compiled
NRO, NOT verified playback.

## Mac Ryujinx smoke test

1. Enable "Enable Guest Internet Access" in Ryujinx settings, System.
2. Set aspect ratio 16:9 (not stretched).
3. Load KazumiNX.nro. Open "Kazumi NX Sources" on home top bar.
4. Check MP4 and HLS videos. For offline test, place H.264 test.mp4 at
   switch/KazumiNX/test.mp4 on the emulator's virtual SD.
5. If online fails but local works, inspect DNS/TLS, not GPU.
6. If audio/clock advances but image stays blank, compare actual Switch.
7. Collect Ryujinx logs and sdmc:/config/KazumiNX/kazuminx.log if available.

On a homebrew Switch, put KazumiNX.nro and streams.txt under
sd:/switch/KazumiNX/ and launch via Homebrew Menu in application
mode (hold R while launching a game).

Previous wiliwili experiment remains available:
https://github.com/q13007868130/Kazumi/tree/port/switch-wiliwili-mvp
