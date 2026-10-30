// Kazumi NX P0/P1 launcher.
// Uses wiliwili's Borealis and MPV implementation. SPDX-License-Identifier: GPL-3.0-or-later
#include "kazumi_nx/launcher.hpp"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <cstdio>
#include <sys/stat.h>
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
#include "utils/config_helper.hpp"

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
    return url.rfind("https://", 0) == 0 || url.rfind("http://", 0) == 0 || url.rfind("sdmc:/", 0) == 0;
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
        streams.push_back({"Local SD test.mp4", "sdmc:/switch/KazumiNX/test.mp4"});
    }
    return streams;
}

void openStream(const StreamEntry& stream) {
    MPVCore::HARDWARE_DEC = false; // Ryujinx diagnostic: bypass NVDEC.
    MPVCore::AUTO_PLAY = true;
    // Same full-window geometry as wiliwili's built-in fullscreen path.
    auto* container = new brls::Box();
    const float width = brls::Application::contentWidth;
    const float height = brls::Application::contentHeight;
    container->setDimensions(width, height);
    auto* video = new VideoView();
    video->setDimensions(width, height);
    video->setWidthPercentage(100);
    video->setHeightPercentage(100);
    video->setId("video");
    video->setTitle("Kazumi NX | " + stream.name);
    video->setOnlineCount("");
    video->hideDanmakuButton();
    video->hideDLNAButton();
    video->hideVideoQualityButton();
    video->hideVideoSpeedButton();
    video->hideSkipOpeningCreditsSetting();
    video->hideHistorySetting();
    video->hideVideoRelatedSetting();
    container->addView(video);
    auto* activity = new brls::Activity(container);
    brls::Application::pushActivity(activity, brls::TransitionAnimation::NONE);
    video->registerCommonActions(activity);
    brls::Logger::info("[KazumiNX] Opening {}: {}", stream.name, stream.url);
    video->setUrl(stream.url);
}

void startDiagnosticLog() {
    const auto path = ProgramConfig::instance().getConfigDir();
    mkdir("/config", 0777);
    mkdir(path.c_str(), 0777);
    if (FILE* fp = std::fopen((path + "/kazuminx.log").c_str(), "w")) {
        brls::Logger::setLogLevel(brls::LogLevel::LOG_DEBUG);
        brls::Logger::setLogOutput(fp);
        brls::Logger::info("[KazumiNX] P0.2 software decode / fullscreen");
    } else {
        brls::Logger::warning("[KazumiNX] Cannot open diagnostic log");
    }
}

} // namespace

void openHome() {
    startDiagnosticLog();
    auto* root = new brls::Box(brls::Axis::COLUMN);
    root->setPadding(30, 55, 20, 55);

    auto* heading = new brls::Label();
    heading->setText("Kazumi NX - Fullscreen P0.2");
    heading->setFontSize(28);
    heading->setMargins(4, 0, 12, 0);
    root->addView(heading);

    auto* explanation = new brls::Label();
    explanation->setText("P0.2: Software decoding test. Choose a video.");
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
    tip->setText("Log: /config/KazumiNX/kazuminx.log | stream list: switch/KazumiNX/");
    tip->setFontSize(15);
    tip->setMargins(30, 0, 0, 0);
    root->addView(tip);

    auto* frame = new brls::AppletFrame(root);
    frame->setTitle("Kazumi NX | P0.2");
    brls::Application::pushActivity(new brls::Activity(frame));
}

} // namespace KazumiNX
