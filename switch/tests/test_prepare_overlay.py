import tempfile
import unittest
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location


module_path = Path(__file__).parents[1] / "tools" / "prepare_overlay.py"
spec = spec_from_file_location("prepare_overlay", module_path)
mod = module_from_spec(spec)
spec.loader.exec_module(mod)


class PrepareTests(unittest.TestCase):
    def test_patches_exactly_one_entry_and_disables_analytics(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "upstream" / "wiliwili" / "source"
            src.mkdir(parents=True)
            main = src / "main.cpp"
            main.write_text(
                '#include "view/mpv_core.hpp"\n'
                '    brls::Application::createWindow("wiliwili");\n'
                '        Intent::openMain();\n'
                '    GA("open_app", {{"version", "x"}})\n'
                '    APPVersion::instance().checkUpdate();\n',
                encoding="utf-8",
            )
            mod.apply_overlay(Path(d) / "upstream",
                              Path(__file__).parents[1] / "overlay")
            patched = main.read_text(encoding="utf-8")
            self.assertIn("KazumiNX::openHome();", patched)
            self.assertIn('#include "kazumi_nx/launcher.hpp"', patched)
            self.assertNotIn('GA("open_app"', patched)
            self.assertNotIn("APPVersion::instance().checkUpdate();", patched)
            self.assertTrue((src / "kazumi_nx" / "launcher.cpp").is_file())
            with self.assertRaises(RuntimeError):
                mod.apply_overlay(Path(d) / "upstream",
                                  Path(__file__).parents[1] / "overlay")


if __name__ == "__main__":
    unittest.main()
