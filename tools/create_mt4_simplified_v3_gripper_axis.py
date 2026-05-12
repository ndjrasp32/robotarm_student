from pathlib import Path
import shutil

try:
    from isaacsim import SimulationApp
except Exception:
    from omni.isaac.kit import SimulationApp

simulation_app = SimulationApp({"headless": True})

from pxr import Gf, Sdf, Usd, UsdGeom, UsdPhysics


PROJECT_DIR = Path.home() / "work/robotarm/mt4_isaac_lab_task"
SRC = PROJECT_DIR / "assets/usd/mt4_simplified_v2.usd"
DST = PROJECT_DIR / "assets/usd/mt4_simplified_v3.usd"
ROOT = "/mt4_simplified_v2"


def set_attr(prim, name, type_name, value):
    attr = prim.GetAttribute(name)
    if not attr:
        attr = prim.CreateAttribute(name, type_name)
    attr.Set(value)


def main():
    if not SRC.exists():
        raise SystemExit(f"[ERROR] source USD not found: {SRC}")

    shutil.copy2(SRC, DST)
    stage = Usd.Stage.Open(str(DST))
    if stage is None:
        raise SystemExit(f"[ERROR] could not open copied USD: {DST}")

    root = stage.GetPrimAtPath(ROOT)
    if not root:
        raise SystemExit(f"[ERROR] root prim not found: {ROOT}")

    gripper = UsdGeom.Xform.Define(stage, f"{ROOT}/gripper_link")
    gripper_prim = gripper.GetPrim()
    gripper.ClearXformOpOrder()
    gripper.AddTranslateOp().Set(Gf.Vec3f(0.38, 0.0, 0.09))
    gripper.AddOrientOp().Set(Gf.Quatf(1.0, 0.0, 0.0, 0.0))
    gripper.AddScaleOp().Set(Gf.Vec3f(1.0, 1.0, 1.0))

    UsdPhysics.RigidBodyAPI.Apply(gripper_prim)
    UsdPhysics.MassAPI.Apply(gripper_prim)
    set_attr(gripper_prim, "physics:rigidBodyEnabled", Sdf.ValueTypeNames.Bool, True)
    set_attr(gripper_prim, "physics:kinematicEnabled", Sdf.ValueTypeNames.Bool, False)
    set_attr(gripper_prim, "physics:mass", Sdf.ValueTypeNames.Float, 0.08)
    set_attr(gripper_prim, "physics:centerOfMass", Sdf.ValueTypeNames.Point3f, Gf.Vec3f(0.035, 0.0, 0.0))
    set_attr(gripper_prim, "physics:diagonalInertia", Sdf.ValueTypeNames.Vector3f, Gf.Vec3f(0.0002, 0.0003, 0.0003))
    set_attr(gripper_prim, "physics:principalAxes", Sdf.ValueTypeNames.Quatf, Gf.Quatf(1.0, 0.0, 0.0, 0.0))

    visuals = UsdGeom.Xform.Define(stage, f"{ROOT}/gripper_link/visuals")
    collisions = UsdGeom.Xform.Define(stage, f"{ROOT}/gripper_link/collisions")
    visuals.GetPrim().CreateAttribute("purpose", Sdf.ValueTypeNames.Token).Set("default")
    collisions.GetPrim().CreateAttribute("purpose", Sdf.ValueTypeNames.Token).Set("default")

    visual_cube = UsdGeom.Cube.Define(stage, f"{ROOT}/gripper_link/visuals/gripper_tip")
    visual_cube.CreateSizeAttr(1.0)
    visual_cube.ClearXformOpOrder()
    visual_cube.AddTranslateOp().Set(Gf.Vec3f(0.035, 0.0, 0.0))
    visual_cube.AddScaleOp().Set(Gf.Vec3f(0.035, 0.012, 0.012))
    visual_cube.CreateDisplayColorAttr([Gf.Vec3f(0.05, 0.05, 0.05)])

    collision_cube = UsdGeom.Cube.Define(stage, f"{ROOT}/gripper_link/collisions/gripper_tip")
    collision_cube.CreateSizeAttr(1.0)
    collision_cube.ClearXformOpOrder()
    collision_cube.AddTranslateOp().Set(Gf.Vec3f(0.035, 0.0, 0.0))
    collision_cube.AddScaleOp().Set(Gf.Vec3f(0.035, 0.012, 0.012))
    UsdPhysics.CollisionAPI.Apply(collision_cube.GetPrim())
    set_attr(collision_cube.GetPrim(), "physics:collisionEnabled", Sdf.ValueTypeNames.Bool, True)

    joint = UsdPhysics.RevoluteJoint.Define(stage, f"{ROOT}/joints/gripper_pitch")
    joint_prim = joint.GetPrim()
    joint.CreateBody0Rel().SetTargets([Sdf.Path(f"{ROOT}/wrist_link")])
    joint.CreateBody1Rel().SetTargets([Sdf.Path(f"{ROOT}/gripper_link")])
    joint.CreateAxisAttr("Y")
    joint.CreateLocalPos0Attr(Gf.Vec3f(0.06, 0.0, 0.0))
    joint.CreateLocalPos1Attr(Gf.Vec3f(0.0, 0.0, 0.0))
    joint.CreateLocalRot0Attr(Gf.Quatf(0.0, 1.0, 0.0, 0.0))
    joint.CreateLocalRot1Attr(Gf.Quatf(0.0, 1.0, 0.0, 0.0))
    joint.CreateLowerLimitAttr(-68.75493621826172)
    joint.CreateUpperLimitAttr(68.75493621826172)
    set_attr(joint_prim, "physics:collisionEnabled", Sdf.ValueTypeNames.Bool, False)
    set_attr(joint_prim, "physics:jointEnabled", Sdf.ValueTypeNames.Bool, True)
    set_attr(joint_prim, "drive:angular:physics:targetPosition", Sdf.ValueTypeNames.Float, 0.0)
    set_attr(joint_prim, "drive:angular:physics:stiffness", Sdf.ValueTypeNames.Float, 625.0)
    set_attr(joint_prim, "drive:angular:physics:damping", Sdf.ValueTypeNames.Float, 0.0)
    set_attr(joint_prim, "drive:angular:physics:maxForce", Sdf.ValueTypeNames.Float, 120.0)

    stage.GetRootLayer().Save()
    print(f"[OK] wrote {DST}")


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
