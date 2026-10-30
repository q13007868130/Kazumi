// Kazumi NX P0/P1 launcher.
// Uses wiliwili's Borealis and MPV implementation. SPDX-License-Identifier: GPL-3.0-or-later
#include "kazumi_nx/launcher.hpp"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <string>
#include <utility>
#include <vector>

#include <borealis/core/application.hpp>
#include <borealis/core/box.hpp>
#include <borealis/views/applet_frame.hpp>
#include <borealis/views/label.hpp>
#include <borealis/views/cells/cell_radio.hpp>

#include "view/video_view.hpp"
#include "view/mpv_core.hpp"

namespace KazumiNX {
namespace {

struct StreamEntry {
    std::string name;
    std::string url;
};

std::string trim(std::string value) {
    auto notSpace = [](unsigned char c) { return !std::isspace(c); };
    value.erase(value.begin(), std::find_if(value.begin(), value.end(), notSpace));
    value.erase(std::find_if(value.rbegin(), value.rend(), notSpace).base(), value.end());
    return value;
}

bool isAllowedUrl(const std::string& url) {
    return url.rfind("https://", 0) == 0 || url.rfind("http://", 0) == 0;
}

std::vector<StreamEntry> readStreams() {
    // SD card path is intentional: this MVP does not parse arbitrary websites.
    std::ifstream file("sdmc:/switch/KazumiNX/streams.txt");
    std::vector<StreamEntry> streams;
    std::string line;
    while (std::getline(file, line) && streams.size() < 20) {
        line = trim(line);
        if (line.empty() || line[0] == '#') continue;
        auto separator = line.find('|');
        if (separator == std::string::npos) continue;
        std::string name = trim(line.substr(0, separator));
        std::string url = trim(line.substr(separator + 1));
        if (!name.empty() && isAllowedUrl(url)) {
            streams.push_back({std::move(name), std::move(url)});
        }
    }
    if (streams.empty()) {
        streams.push_back({"Big Buck Bunny (MP4 demo)",
            "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"});
        streams.push_back({"HLS test stream",
            "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"});
    }
    return streams;
}

void openStream(const StreamEntry& stream) {
    // Keep the player view from wiliwili: includes controller focus, OSD and MPV rendering.
    auto* video = new VideoView();
    auto* frame = new brls::AppletFrame(video);
    frame->setTitle("Kazumi NX | " + stream.name);
    brls::Application::pushActivity(
        new brls::Activity(frame), brls::TransitionAnimation::NONE);
    video->setUrl(stream.url);
}

} // namespace

void openHome() {
    auto* root = new brls::Box(brls::Axis::COLUMN);
    root->setPadding(30, 55, 20, 55);

    auto* heading = new brls::Label();
    heading->setText("Kazumi NX - Native Switch MVP");
    heading->setFontSize(28);
    heading->setMargins(4, 0, 12, 0);
    root->addView(heading);

    auto* explanation = new brls::Label();
    explanation->setText("P0/P1: Choose a video to test networking and MPV playback.");
    explanation->setFontSize(17);
    explanation->setMargins(0, 0, 24, 0);
    root->addView(explanation);

    for (const auto& entry : readStreams()) {
        auto* item = new brls::RadioCell();
        item->title->setText(entry.name);
        item->registerClickAction([entry](brls::View*) -> bool {
            openStream(entry);
            return true;
        });
        root->addView(item);
    }

    auto* tip = new brls::Label();
    tip->setText("Custom streams: sdmc:/switch/KazumiNX/streams.txt (Title|URL).");
    tip->setFontSize(15);
    tip->setMargins(30, 0, 0, 0);
    root->addView(tip);

    auto* frame = new brls::AppletFrame(root);
    frame->setTitle("Kazumi NX | Build P0.1");
    brls::Application::pushActivity(new brls::Activity(frame));
}

} // namespace KazumiNX
