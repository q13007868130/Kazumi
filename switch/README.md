# Kazumi NX P0.2 - Mac Ryujinx / Switch diagnostic build

Status: second experimental test version. A successful compilation does not yet
prove playback or correct rendering on Ryujinx or physical Switch.

## Fixes after first Ryujinx screenshots

- Use wiliwili's full-window Box(VideoView) geometry instead of placing
  VideoView into AppletFrame; this addresses the large white/black split.
- NRO metadata now says Kazumi NX and includes a newly generated original icon.
- Disable mpv hardware decode in this diagnosis build to isolate Ryujinx NVDEC.
- Keep configuration under /config/KazumiNX rather than /config/wiliwili.
- Write logs to /config/KazumiNX/kazuminx.log when accessible.
- Hide Bilibili-specific video controls and do not bundle its NSP forwarder.

## Test P0.2

Get artifact KazumiNX-P0.2 from the latest successful GitHub Actions build.
Open KazumiNX.nro using Ryujinx File > Load Application From File.

1. Confirm the launch banner says Kazumi NX with the new icon.
2. Enter the MP4 demo and check fullscreen video, audio and progress.
3. Try the HLS demo and compare results.
4. Optional: place a small H.264 test.mp4 in the emulator's virtual SD
   directory switch/KazumiNX and select Local SD test.mp4.
5. Share the emulator's log and /config/KazumiNX/kazuminx.log if the video
   is still blank.

If local MP4 works but remote media does not, check HTTP and TLS.
If time/audio advances without a visible picture, suspect GPU video drawing.
If file loading fails, inspect mpv/FFmpeg error details.
The Ryujinx virtual SD mapping depends on the emulator build.

For real Switch hardware, put the NRO and streams.txt under
sd:/switch/KazumiNX and run in Homebrew Menu Application Mode (hold R
when starting a game). Software decoding may be slower on actual hardware.

## Provenance

The original Kazumi app is Flutter/Dart; this test does not yet include its
anime catalogs, XPath/JSONPath/API rule engine, browser extraction, or history.
The Switch integration reuses the GPL-3.0 wiliwili player/backend and is
based on upstream commit 88e5876bea9502d06f46a8656e3530684d3aaf7d.
Preserve the GPL notices and obligations when sharing source or binaries.
