import json
import os
import subprocess
import sys
from importlib.metadata import distribution

import pytest
from compas.colors import Color
from compas.geometry import Box
from compas.geometry import Translation
from compas.scene import Scene
from compas.scene import SceneItemNotBoundError
from compas_viewer import Viewer
from compas_viewer.scene import ViewerScene

CORE_COMMIT = "f878cd102e87e7859030af96c7871a5b3345cf7d"
VIEWER_COMMIT = "18c87acac907c6d749d95a0e8f56ae2abd021ed2"


def _installed_commit(distribution_name: str) -> str:
    direct_url = distribution(distribution_name).read_text("direct_url.json")
    assert direct_url is not None
    metadata = json.loads(direct_url)
    return metadata["vcs_info"]["commit_id"]


def test_exact_source_candidates_are_installed():
    if os.environ.get("COMPAS_SCENE_SOURCE_CHECKOUTS") == "1":
        pytest.skip("Direct-source local check; exact installed revisions are verified by framework CI.")
    assert _installed_commit("compas") == CORE_COMMIT
    assert _installed_commit("compas_viewer") == VIEWER_COMMIT


def test_plugin_discovery_does_not_import_graphics_modules():
    code = """
import sys

from compas.plugins import PluginManager

manager = PluginManager()
manager.load_plugins()
modules = tuple(sys.modules)
assert "compas_viewer.plugins" in modules
assert not any(name == "PySide6" or name.startswith("PySide6.") for name in modules)
assert not any(name == "OpenGL" or name.startswith("OpenGL.") for name in modules)
"""
    environment = os.environ.copy()
    if os.environ.get("COMPAS_SCENE_SOURCE_CHECKOUTS") != "1":
        environment.pop("PYTHONPATH", None)
    subprocess.run([sys.executable, "-c", code], check=True, env=environment)


def test_reference_scene_roundtrip_and_explicit_binding(tmp_path):
    viewer = Viewer()
    viewer.running = False
    viewer.scene.clear(clear_context=False)

    box = Box(1.0)
    transformation = Translation.from_vector([2.0, 0.0, 0.0])
    original = viewer.scene.add(
        box,
        name="Box",
        is_selected=True,
        show_faces=False,
        facecolor=Color.red(),
        transformation=transformation,
        u=7,
        use_rgba=True,
        v=9,
    )
    original.background = True

    scene_path = tmp_path / "scene.json"
    item_path = tmp_path / "box.json"
    viewer.scene.to_json(scene_path)
    box.to_json(item_path)

    payload = scene_path.read_text()
    assert str(box.guid) in payload
    assert "compas.geometry/Box" not in payload
    assert "is_selected" not in payload
    assert "instance_color" not in payload

    restored_scene = Scene.from_json(scene_path)
    restored_box = Box.from_json(item_path)
    assert isinstance(restored_scene, ViewerScene)
    assert restored_box.guid == box.guid
    assert restored_box.volume() == box.volume()

    node = restored_scene.find_node_by_name("Box")
    assert node is not None
    assert node.guid == original.node.guid
    assert node.item_guid == restored_box.guid
    with pytest.raises(SceneItemNotBoundError, match=str(restored_box.guid)):
        restored_scene.bind_context("Viewer")

    restored_scene.bind(restored_box)
    restored_scene.bind_context("Viewer")
    restored = restored_scene.objects[0]

    assert restored.node.transformation == transformation
    assert restored.show_faces is False
    assert restored.facecolor == Color.red()
    assert restored.u == 7
    assert restored.use_rgba is True
    assert restored.v == 9
    assert restored.background is True
    assert restored.is_selected is False
    assert restored_scene.instance_colors == {}
