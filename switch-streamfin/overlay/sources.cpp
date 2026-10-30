// SPDX-License-Identifier: Apache-2.0
// Native Kazumi NX direct-media smoke test; StreamFinEX handles video playback.
#include "kazumi_nx/sources.hpp"
#include "tab/remote_view.hpp"
#include <borealis.hpp>
#include <algorithm>
#include <cctype>
#include <fstream>
#include <string>
#include <vector>

namespace KazumiNX {
namespace {
struct Source { std::string title, url; };
std::string trim(std::string s) {
    auto nonspace=[](unsigned char c){return !std::isspace(c);};
    s.erase(s.begin(),std::find_if(s.begin(),s.end(),nonspace));
    s.erase(std::find_if(s.rbegin(),s.rend(),nonspace).base(),s.end());
    return s;
}
bool valid(const std::string& s) {
    return s.rfind("https://",0)==0 || s.rfind("http://",0)==0 ||
           s.rfind("sdmc:/",0)==0;
}
std::vector<Source> load() {
    std::ifstream file("sdmc:/switch/KazumiNX/streams.txt");
    std::vector<Source> out;
    std::string line;
    while(std::getline(file,line) && out.size()<30) {
        line=trim(line);
        if(line.empty()||line[0]=='#') continue;
        const auto sep=line.find('|');
        if(sep==std::string::npos) continue;
        auto title=trim(line.substr(0,sep));
        auto url=trim(line.substr(sep+1));
        if(!title.empty() && valid(url)) out.push_back({title,url});
    }
    if(out.empty()) {
        out.push_back({"MP4 demo", "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"});
        out.push_back({"HLS demo", "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"});
        out.push_back({"Local SD test.mp4", "sdmc:/switch/KazumiNX/test.mp4"});
    }
    return out;
}

class SourceScreen: public brls::Box {
public:
    SourceScreen() {
        setAxis(brls::Axis::COLUMN);
        setDimensions(brls::Application::contentWidth,brls::Application::contentHeight);
        setPadding(32,65,30,65);
        auto* title=new brls::Label();
        title->setFontSize(32);
        title->setText("Kazumi NX - Direct Sources");
        title->setMarginBottom(20);
        addView(title);
        auto* scroll=new brls::ScrollingFrame();
        scroll->setGrow(1.0f);
        auto* list=new brls::Box();
        list->setAxis(brls::Axis::COLUMN);
        for(const auto& entry:load()) {
            auto* button=new brls::Box();
            button->setAxis(brls::Axis::COLUMN);
            button->setFocusable(true);
            button->setPadding(14,22,14,22);
            button->setMarginBottom(10);
            button->setCornerRadius(8);
            button->setBackgroundColor(nvgRGBA(52,64,100,175));
            auto* label=new brls::Label();
            label->setFontSize(23);
            label->setText(entry.title);
            button->addView(label);
            button->registerClickAction([entry](brls::View*)->bool{
                brls::Logger::info("[KazumiNX] play {}: {}",entry.title,entry.url);
                RemoteView::play(entry.url,entry.title);
                return true;
            });
            list->addView(button);
        }
        scroll->setContentView(list);
        addView(scroll);
        auto* help=new brls::Label();
        help->setFontSize(17);
        help->setText("B: Back.  SD: switch/KazumiNX/streams.txt");
        help->setMarginTop(15);
        addView(help);
        registerAction("Back",brls::BUTTON_B,[](brls::View*)->bool{
            brls::Application::popActivity();
            return true;
        });
    }
};
}
void openSources(){
    brls::Application::pushActivity(
        new brls::Activity(new SourceScreen()),brls::TransitionAnimation::NONE);
}
}
