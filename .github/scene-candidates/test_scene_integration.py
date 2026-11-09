import json
import os
import subprocess
import sys
from importlib import import_module
from importlib.metadata import distribution
from math import pi
from uuid import uuid4

import pytest
from compas.data import json_dumps
from compas.data import json_loads
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.scene import ArrowAnnotation
from compas.scene import ComponentAnchor
from compas.scene import DistanceDimension
from compas.scene import PointAnchor
from compas.scene import Scene
from compas.scene import SceneItemNotBoundError
from compas.scene import SceneObject
from compas.scene import ShapeObject
from compas.scene import TextAnnotation
from compas.scene import register_scene_operation
from compas_viewer import ScaleBarOverlay
from compas_viewer import Viewer
from compas_viewer.commands import builtin_commands
from compas_viewer.config import Config
from compas_viewer.forms import REMOVE_EDITABLE_ATTRIBUTE
from compas_viewer.forms import register_scene_attribute_contribution
from compas_viewer.forms import scene_editable_attributes
from compas_viewer.measurement import DistanceInspection
from compas_viewer.measurement import MeasurementState
from compas_viewer.overlays import _OverlayLayer
from compas_viewer.scene import BufferGeometry
from compas_viewer.scene import ViewerScene
from compas_viewer.scene.annotationobject import ArrowAnnotationRenderObject
from compas_viewer.scene.annotationobject import DistanceDimensionRenderObject
from compas_viewer.scene.annotationobject import TextAnnotationRenderObject
from compas_viewer.selection import Selection
from compas_viewer.snapping import ProjectedPoint
from compas_viewer.snapping import SnapKind
from compas_viewer.snapping import SnapQuery
from compas_viewer.snapping import SnapResult
from compas_viewer.snapping import query_snaps
from compas_viewer.uidefinitions import default_menu_items
from compas_viewer.uidefinitions import default_sidebar_items

CORE_COMMIT = "353cebfd21cd3623f7d950527d71f4770ff2a21c"
VIEWER_COMMIT = "5a25154950be63548928da956ecaff1c2f7e4d3c"


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

assert Config().schema_version == 3
assert any(item.get("type") == "DatastructureAttributes" for item in default_sidebar_items())
assert any(item.get("type") == "MeasurementSetting" for item in default_sidebar_items())
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
            "schema_version": 3,
            "window": {"title": "Framework Viewer"},
            "renderer": {"view": "ortho"},
            "measurement": {"unit": "mm", "precision": 2},
        }
    )
    payload = config.to_dict()

    assert defaults.window.title == "COMPAS Viewer"
    assert defaults.window.icon is None
    assert config.schema_version == 3
    assert config.window.title == "Framework Viewer"
    assert config.window.icon is None
    assert config.renderer.view == "ortho"
    assert config.measurement.unit == "mm"
    assert config.measurement.precision == 2
    assert set(payload) == {"schema_version", "vectorsize", "ui", "window", "renderer", "camera", "measurement"}
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
        "MeasurementSetting",
    ]

    with pytest.raises(ValueError, match=r"window\.about"):
        Config.from_dict({"schema_version": 3, "window": {"about": "retired"}})
    with pytest.raises(ValueError, match=r"window\.icon"):
        Config.from_dict({"schema_version": 3, "window": {"icon": "relative.png"}})
    with pytest.raises(ValueError, match=r"window\.width"):
        Config.from_dict({"schema_version": 3, "window": {"width": 0}})


def test_core_annotations_serialize_and_resolve_without_fallbacks():
    scene = ViewerScene()
    point_object = scene.add(Point(1, 2, 3), transformation=Translation.from_vector([10, 0, 0]))
    line_object = scene.add(Line([0, 0, 0], [4, 0, 0]), transformation=Translation.from_vector([0, 5, 0]))
    mesh = Mesh.from_vertices_and_faces(
        [[0, 0, 0], [4, 0, 0], [0, 4, 0]],
        [[0, 1, 2]],
    )
    mesh_object = scene.add(mesh, transformation=Translation.from_vector([0, 0, 2]))

    point_anchor = PointAnchor([1, 2, 3])
    component_anchor = ComponentAnchor(point_object.guid, "point")
    line_anchor = ComponentAnchor(line_object.guid, "line", parameter=0.25)
    vertex_anchor = ComponentAnchor(mesh_object.guid, "vertex", component=1)
    edge_anchor = ComponentAnchor(mesh_object.guid, "edge", component=(0, 1), parameter=0.5)
    text = TextAnnotation("Origin", [0, 0, 0])
    arrow = ArrowAnnotation([0, 0, 0], [1, 0, 0])
    fixed = DistanceDimension(point_anchor, PointAnchor([4, 6, 3]), unit="mm", precision=2)
    mixed = DistanceDimension(PointAnchor([0, 0, 0]), component_anchor)
    associative = DistanceDimension(line_anchor, edge_anchor)

    for value in (
        point_anchor,
        component_anchor,
        text,
        arrow,
        fixed,
        mixed,
        associative,
    ):
        assert json_loads(json_dumps(value)) == value

    assert fixed.resolve(scene, Translation.from_vector([2, 0, 0])) == (
        Point(3, 2, 3),
        Point(6, 6, 3),
    )
    assert mixed.resolve(scene, Translation.from_vector([2, 0, 0])) == (
        Point(2, 0, 0),
        Point(11, 2, 3),
    )
    assert associative.resolve(scene) == (
        Point(1, 5, 0),
        Point(2, 0, 2),
    )
    assert vertex_anchor.resolve(scene) == Point(4, 0, 2)

    missing_object = DistanceDimension(PointAnchor([0, 0, 0]), ComponentAnchor(uuid4(), "point"))
    missing_vertex = DistanceDimension(PointAnchor([0, 0, 0]), ComponentAnchor(mesh_object.guid, "vertex", component=99))
    assert missing_object.resolve(scene) is None
    assert missing_vertex.resolve(scene) is None


def test_viewer_dispatches_canonical_annotations_without_legacy_types():
    scene = ViewerScene()
    annotations = (
        (TextAnnotation("Note", [0, 0, 0]), TextAnnotationRenderObject),
        (ArrowAnnotation([0, 0, 0], [1, 0, 0]), ArrowAnnotationRenderObject),
        (
            DistanceDimension(PointAnchor([0, 0, 0]), PointAnchor([1, 0, 0])),
            DistanceDimensionRenderObject,
        ),
    )

    for annotation, render_type in annotations:
        sceneobject = scene.add(annotation)
        render_object = scene.render_object(sceneobject)
        assert isinstance(render_object, render_type)
        assert render_object.item is annotation

    with pytest.raises(ModuleNotFoundError):
        import_module("compas_viewer.scene.tagobject")
    with pytest.raises(ModuleNotFoundError):
        import_module("compas_viewer.scene.arrowoverlayobject")


def test_measurement_state_preserves_mode_semantics_and_dimension_settings():
    state = MeasurementState()
    point_guid = uuid4()
    edge_guid = uuid4()
    first = SnapResult(Point(0, 0, 0), point_guid, SnapKind.POINT, 0.0)
    second = SnapResult(Point(3, 4, 0), edge_guid, SnapKind.EDGE, 0.0, component=(1, 2), parameter=0.25)

    state.start("inspection")
    assert state.accept(SnapQuery(first), unit="m", precision=1) is None
    inspection = state.accept(SnapQuery(second), unit="m", precision=1)
    assert isinstance(inspection, DistanceInspection)
    assert inspection.distance == 5.0
    assert state.completed_inspection is inspection
    assert not state.active

    unsupported = SnapResult(
        Point(8, 8, 8),
        uuid4(),
        SnapKind.SURFACE,
        0.0,
        association_error="Surface snaps are not associative.",
    )
    state.start("fixed")
    assert state.accept(SnapQuery(first), unit="mm", precision=4) is None
    fixed = state.accept(SnapQuery(unsupported), unit="mm", precision=4)
    assert isinstance(fixed, DistanceDimension)
    assert fixed.start == PointAnchor(first.point)
    assert fixed.end == PointAnchor(unsupported.point)
    assert (fixed.unit, fixed.precision) == ("mm", 4)

    state.start("associative")
    assert state.accept(SnapQuery(first), unit="cm", precision=3) is None
    assert state.accept(SnapQuery(unsupported), unit="cm", precision=3) is None
    assert state.first_snap is first
    assert state.rejection == "Surface snaps are not associative."
    associative = state.accept(SnapQuery(second), unit="cm", precision=3)
    assert isinstance(associative, DistanceDimension)
    assert associative.start == ComponentAnchor(point_guid, "point")
    assert associative.end == ComponentAnchor(edge_guid, "edge", component=(1, 2), parameter=0.25)
    assert (associative.unit, associative.precision) == ("cm", 3)
    assert not state.active


def test_measurement_hover_exposes_discrete_points_and_one_winner():
    mesh = Mesh.from_vertices_and_faces(
        [[0, 0, 0], [4, 0, 0], [4, 3, 0], [0, 3, 0]],
        [[0, 1, 2, 3]],
    )
    sceneobject = SceneObject(mesh)

    query = query_snaps(
        [sceneobject],
        (0.1, 0.1),
        radius=0.5,
        project=lambda point: ProjectedPoint(point.x, point.y, 0.0),
    )

    assert query.winner is not None
    assert query.winner.kind == SnapKind.VERTEX
    assert query.winner.component == 0
    assert [snap.kind for snap in query.points] == [SnapKind.VERTEX] * 4
    assert [snap.component for snap in query.points] == [0, 1, 2, 3]

    mesh_edge = query_snaps(
        [sceneobject],
        (2.0, 0.0),
        radius=0.1,
        project=lambda point: ProjectedPoint(point.x, point.y, 0.0),
    )

    assert mesh_edge.winner is None
    assert len(mesh_edge.points) == 4


def test_measure_menu_and_commands_have_one_stable_public_path():
    measure_menus = [item for item in default_menu_items() if item.get("title") == "Measure"]
    assert len(measure_menus) == 1
    command_ids = [item["command"] for item in measure_menus[0]["items"] if "command" in item]
    assert command_ids == [
        "viewer.inspect_distance",
        "viewer.add_fixed_distance_dimension",
        "viewer.add_associative_distance_dimension",
        "viewer.cancel_measurement",
    ]
    assert set(command_ids) <= builtin_commands().keys()


def test_viewer_overlays_remain_outside_serialized_scene_data():
    viewer = object.__new__(Viewer)
    viewer._overlay_layer = _OverlayLayer()
    viewer._scene = ViewerScene()
    viewer.running = False
    overlay = ScaleBarOverlay()
    before = viewer.scene.__data__

    viewer.add_overlay(overlay)

    assert viewer.overlays == (overlay,)
    assert viewer.scene.__data__ == before
    assert viewer.scene.objects == []
    assert viewer.remove_overlay(overlay)
    assert viewer.overlays == ()


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


def test_viewer_transform_history_and_refresh_contract():
    viewer = Viewer()

    parent = viewer.scene.add_group(
        "Rotated parent",
        transformation=Rotation.from_axis_and_angle([0, 0, 1], pi / 2),
    )
    child = viewer.scene.add(
        Box(1.0),
        parent=parent,
        transformation=Translation.from_vector([1, 0, 0]),
    )
    previous_local = child.transformation.copy()
    previous_world = child.worldtransformation.copy()
    delta = Translation.from_vector([2, 0, 0])

    viewer.transform_objects([child], delta)

    assert child.worldtransformation == delta * previous_world
    assert child.transformation == parent.worldtransformation.inverse() * delta * previous_world
    viewer.refresh_geometry([child])
    viewer.refresh_appearance([child])
    assert viewer.undo()
    assert child.transformation == previous_local
    assert viewer.redo()

    child.transformation = previous_local
    viewer.refresh_transform([child])
    assert not viewer.undo()


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
        show=False,
        transformation=transformation,
        u=7,
        v=9,
    )
    selection = Selection(scene.object)
    selection.add(original)

    assert type(original) is ShapeObject
    assert selection.objects == (original,)
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
    assert '"selection"' not in payload
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
    assert not Selection(restored_scene.object)
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
