import json
import os
import subprocess
import sys
from importlib.metadata import distribution

import pytest
from compas.data import json_dumps
from compas.data import json_loads
from compas.geometry import Box
from compas.geometry import Translation
from compas.scene import Scene
from compas.scene import SceneItemNotBoundError
from compas.scene import SceneObject
from compas.scene import ShapeObject
from compas.scene import register_scene_operation
from compas_viewer.config import Config
from compas_viewer.forms import REMOVE_EDITABLE_ATTRIBUTE
from compas_viewer.forms import register_scene_attribute_contribution
from compas_viewer.forms import scene_editable_attributes
from compas_viewer.scene import BufferGeometry
from compas_viewer.scene import ViewerScene
from compas_viewer.uidefinitions import default_sidebar_items

CORE_COMMIT = "0b4555c23d570589bf9eab412cfa5a71312e1aa2"
VIEWER_COMMIT = "898d583155ca7782de8365e809ac38acaa68de80"


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
from compas_viewer.config import Config
from compas_viewer.uidefinitions import default_sidebar_items

assert Config().schema_version == 2
assert any(item.get("type") == "DatastructureAttributes" for item in default_sidebar_items())
modules = tuple(sys.modules)
assert "compas_viewer.plugins" in modules
assert not any(name == "PySide6" or name.startswith("PySide6.") for name in modules)
assert not any(name == "OpenGL" or name.startswith("OpenGL.") for name in modules)
"""
    environment = os.environ.copy()
    if os.environ.get("COMPAS_SCENE_SOURCE_CHECKOUTS") != "1":
        environment.pop("PYTHONPATH", None)
    subprocess.run([sys.executable, "-c", code], check=True, env=environment)


def test_viewer_configuration_and_sidebar_contracts():
    defaults = Config()
    config = Config.from_dict(
        {
            "schema_version": 2,
            "window": {"title": "Framework Viewer"},
            "renderer": {"view": "ortho"},
        }
    )
    payload = config.to_dict()

    assert defaults.window.title == "COMPAS Viewer"
    assert defaults.window.icon is None
    assert config.schema_version == 2
    assert config.window.title == "Framework Viewer"
    assert config.window.icon is None
    assert config.renderer.view == "ortho"
    assert set(payload) == {"schema_version", "vectorsize", "ui", "window", "renderer", "camera"}
    assert "about" not in payload["window"]
    assert "opacity" not in payload["renderer"]
    assert "show_widgets" not in payload["ui"]["sidebar"]
    assert "sceneform" not in payload["ui"]["sidebar"]
    assert [item["type"] for item in default_sidebar_items()] == [
        "SceneTree",
        "ObjectSetting",
        "DatastructureAttributes",
        "CameraSetting",
        "DisplaySetting",
    ]

    with pytest.raises(ValueError, match=r"window\.about"):
        Config.from_dict({"schema_version": 2, "window": {"about": "retired"}})
    with pytest.raises(ValueError, match=r"window\.icon"):
        Config.from_dict({"schema_version": 2, "window": {"icon": "relative.png"}})
    with pytest.raises(ValueError, match=r"window\.width"):
        Config.from_dict({"schema_version": 2, "window": {"width": 0}})


def test_indexed_buffer_geometry_stays_indexed_and_roundtrips():
    geometry = BufferGeometry.from_vertices_and_triangles(
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]],
        [[0, 1, 2], [1, 3, 2]],
    )

    restored = json_loads(json_dumps(geometry))

    assert isinstance(restored, BufferGeometry)
    assert restored.vertices.shape == (4, 3)
    assert restored.triangles is not None
    assert restored.triangles.shape == (2, 3)
    assert restored.triangles.tolist() == [[0, 1, 2], [1, 3, 2]]


def test_contextual_editable_scene_state_is_graphics_free_and_not_serialized():
    sceneobject = ShapeObject(item=Box(1.0), u=7, v=9)
    original_payload = sceneobject.to_jsonstring()

    geometry_fields = sceneobject.scene_state_fields()["compas.scene.GeometryObject"]
    editable_state = {field.attribute for field in geometry_fields if field.editable}
    assert editable_state == {
        "linecolor",
        "linewidth",
        "pointcolor",
        "pointsize",
        "show_lines",
        "show_points",
        "show_surfaces",
        "surfacecolor",
    }
    assert editable_state <= sceneobject.editable_attributes().keys()
    assert "u" not in sceneobject.editable_attributes()

    def update_resolution(obj: ShapeObject, value: object) -> None:
        obj.u = int(value)

    register_scene_attribute_contribution(
        "FrameworkIntegration",
        ShapeObject,
        "shape-resolution",
        {
            "name": REMOVE_EDITABLE_ATTRIBUTE,
            "u": update_resolution,
        },
    )
    resolved = scene_editable_attributes("FrameworkIntegration", sceneobject)

    assert "name" not in resolved
    assert resolved["u"] is update_resolution
    assert sceneobject.to_jsonstring() == original_payload

    resolved["u"](sceneobject, 11)
    assert type(sceneobject) is ShapeObject
    assert sceneobject.u == 11
    payload = sceneobject.to_jsonstring()
    assert "shape-resolution" not in payload
    assert "FrameworkIntegration" not in payload
    assert "FormField" not in payload


def test_stable_scene_roundtrip_operations_and_explicit_binding():
    box = Box(1.0)
    transformation = Translation.from_vector([2.0, 0.0, 0.0])
    scene = ViewerScene()
    original = scene.add(
        box,
        name="Box",
        is_selected=True,
        show=False,
        transformation=transformation,
        u=7,
        v=9,
    )

    assert type(original) is ShapeObject
    assert original.node.object_guid == original.guid
    assert original.node.__data__ == {"object": str(original.guid), "children": []}

    calls = []
    runtime = object()

    def draw(scene, sceneobject, active_runtime):
        calls.append(("draw", sceneobject, active_runtime))
        return ["opaque-handle"]

    def clear(scene, sceneobject, active_runtime, resources):
        calls.append(("clear", sceneobject, active_runtime, resources))

    register_scene_operation("FrameworkIntegration", SceneObject, "draw", draw)
    register_scene_operation("FrameworkIntegration", SceneObject, "clear", clear)
    original.show = True
    assert original.draw(context="FrameworkIntegration", runtime=runtime) == ["opaque-handle"]
    assert scene.object(original.guid) is original
    assert type(original) is ShapeObject

    payload = scene.to_jsonstring()
    assert str(box.guid) in payload
    assert "compas.geometry/Box" not in payload
    assert "opaque-handle" not in payload
    assert "FrameworkIntegration" not in payload
    assert "is_selected" not in payload
    assert "render_objects" not in payload
    assert "instance_colors" not in payload

    restored_scene = Scene.from_jsonstring(payload)
    restored_box = Box.from_jsonstring(box.to_jsonstring())
    assert isinstance(restored_scene, ViewerScene)
    assert restored_box.guid == box.guid
    assert restored_box.volume() == box.volume()

    restored = restored_scene.find_by_name("Box")
    assert type(restored) is ShapeObject
    assert restored.guid == original.guid
    assert restored.item_guid == restored_box.guid
    assert restored.transformation == transformation
    assert restored.show is True
    assert (restored.u, restored.v) == (7, 9)
    assert restored_scene.item_store == {}
    assert not restored_scene.is_selected(restored)
    with pytest.raises(SceneItemNotBoundError, match=str(restored_box.guid)):
        _ = restored.item

    restored_scene.bind(restored_box)
    assert restored.item is restored_box
    original.clear(context="FrameworkIntegration")
    assert calls == [
        ("draw", original, runtime),
        ("clear", original, runtime, ("opaque-handle",)),
    ]
    assert restored_scene.instance_colors == {}
