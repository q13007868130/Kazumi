import tempfile
import unittest
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

root = Path(__file__).resolve().parents[1]
spec = spec_from_file_location("kazumi_prepare", root/"tools/prepare.py")
module = module_from_spec(spec)
spec.loader.exec_module(module)

class OverlayTest(unittest.TestCase):
    def populate(self, folder):
        files = {
            "CMakeLists.txt": 'project(StreamFin)\nset(PROJECT_AUTHOR "Kirbosh")\nresources/icon/icon.jpg\n',
            "app/src/activity/stremio_home.cpp": (
                '#include "activity/stremio_anime.hpp"\n'
                '    this->boxHome->addView(bar);\n'
                '    if (stremio::STREAM_ADDON.empty())\n'
                '        brls::sync([]() { promptForAddon(""); });\n'
            ),
            "app/src/main.cpp": '#include <borealis.hpp>\n    // Init the app and i18n\n',
            "app/include/api/analytics.hpp":
                '#define GA(a, ...) analytics::Analytics::instance().report(a, ##__VA_ARGS__);\n',
        }
        for relative, content in files.items():
            target = folder/relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    def test_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            self.populate(base)
            module.apply(base, root/"overlay")
            self.assertIn("project(KazumiNX)",(base/"CMakeLists.txt").read_text())
            self.assertIn("kazuminx.jpg",(base/"CMakeLists.txt").read_text())
            self.assertIn("KazumiNX::openSources()", (base/"app/src/activity/stremio_home.cpp").read_text())
            self.assertNotIn("brls::sync([]() { promptForAddon", (base/"app/src/activity/stremio_home.cpp").read_text())
            self.assertIn("kazuminx.log", (base/"app/src/main.cpp").read_text())
            self.assertIn("#define GA(a, ...) ((void)0);", (base/"app/include/api/analytics.hpp").read_text())
            self.assertTrue((base/"app/src/kazumi_nx/sources.cpp").is_file())
            with self.assertRaises(RuntimeError):
                module.apply(base, root/"overlay")

    def test_invalid_upstream_does_not_modify(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            self.populate(base)
            (base/"app/src/main.cpp").write_text("unexpected change", encoding="utf-8")
            original=(base/"CMakeLists.txt").read_text()
            with self.assertRaises(RuntimeError):
                module.apply(base, root/"overlay")
            self.assertEqual((base/"CMakeLists.txt").read_text(), original)

    def test_reuses_native_player(self):
        content=(root/"overlay/sources.cpp").read_text(encoding="utf-8")
        self.assertIn("RemoteView::play(entry.url,entry.title)",content)
        self.assertIn('std::ifstream file("sdmc:/switch/KazumiNX/streams.txt")',content)
        self.assertNotIn("new VideoView()",content)

if __name__=="__main__":
    unittest.main()
