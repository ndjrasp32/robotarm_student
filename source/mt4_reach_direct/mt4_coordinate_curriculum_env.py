from __future__ import annotations

from pathlib import Path

import torch

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import Articulation, ArticulationCfg
from isaaclab.envs import DirectRLEnv, DirectRLEnvCfg
from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.utils import configclass
from isaaclab.utils import math as math_utils


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MT4_USD_PATH = str(PROJECT_ROOT / "assets/usd/mt4_simplified_v3.usd")

JOINT_NAMES = ("base_yaw", "shoulder", "elbow", "wrist_pitch", "gripper_pitch")
HOME_JOINT_POS = (0.0, 1.44, -1.19, 1.19, 0.0)
JOINT_LOWER = (-1.57, 0.05, -1.20, -1.20, -1.20)
JOINT_UPPER = (1.57, 1.45, 1.40, 1.20, 1.20)


@configclass
class MT4CoordinateCurriculumEnvCfg(DirectRLEnvCfg):
    decimation = 2
    episode_length_s = 6.0

    action_space = 5
    observation_space = 54
    state_space = 0

    curriculum_stage = "plane_localization"

    sim: sim_utils.SimulationCfg = sim_utils.SimulationCfg(
        dt=1 / 120,
        render_interval=decimation,
    )

    scene: InteractiveSceneCfg = InteractiveSceneCfg(
        num_envs=64,
        env_spacing=0.85,
        replicate_physics=True,
    )

    robot_cfg: ArticulationCfg = ArticulationCfg(
        prim_path="/World/envs/env_.*/Robot",
        spawn=sim_utils.UsdFileCfg(
            usd_path=MT4_USD_PATH,
            activate_contact_sensors=False,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
                max_depenetration_velocity=5.0,
            ),
            articulation_props=sim_utils.ArticulationRootPropertiesCfg(
                enabled_self_collisions=False,
                solver_position_iteration_count=8,
                solver_velocity_iteration_count=1,
            ),
        ),
        init_state=ArticulationCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.0),
            joint_pos={
                "base_yaw": 0.0,
                "shoulder": 1.44,
                "elbow": -1.19,
                "wrist_pitch": 1.19,
                "gripper_pitch": 0.0,
            },
        ),
        actuators={
            "arm": ImplicitActuatorCfg(
                joint_names_expr=list(JOINT_NAMES),
                stiffness=2200.0,
                damping=280.0,
                effort_limit=1500.0,
                velocity_limit=1.5,
            )
        },
    )

    target_marker_cfg = VisualizationMarkersCfg(
        prim_path="/Visuals/MT4CoordinateTargets",
        markers={
            "target": sim_utils.SphereCfg(
                radius=0.018,
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(0.05, 1.0, 0.15),
                    emissive_color=(0.0, 0.25, 0.02),
                ),
            ),
        },
    )

    success_marker_cfg = VisualizationMarkersCfg(
        prim_path="/Visuals/MT4CoordinateSuccess",
        markers={
            "success": sim_utils.SphereCfg(
                radius=0.024,
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(0.05, 0.35, 1.0),
                    emissive_color=(0.0, 0.05, 0.30),
                ),
            ),
        },
    )

    action_scale = 0.040
    success_radius = 0.040
    plane_success_radius = 0.075
    workspace_entry_success_radius = 0.065
    camera_region_success_radius = 0.80
    center_success_radius = 0.010
    region_success_margin_fraction = 0.20
    master_regions_sequentially = False
    region_mastery_successes = 10
    camera_alignment_success = 0.95
    workspace_center = (0.27, 0.0, 0.14)
    workspace_size = (0.18, 0.22, 0.16)
    min_target_base_radius = 0.17

    gripper_center_offset_b = (0.158, 0.0, 0.0)
    gripper_forward_axis_b = (1.0, 0.0, 0.0)

    left_camera_pos = (0.035, -0.255, 0.225)
    right_camera_pos = (0.035, 0.255, 0.225)
    camera_look_at = (0.27, 0.0, 0.14)
    camera_fov_deg = 72.0
    gripper_camera_offset_b = (-0.035, 0.0, 0.018)
    gripper_camera_fov_deg = 78.0
    gripper_camera_min_depth = 0.020
    gripper_camera_max_depth = 0.45
    face_region_shape = (3, 3)
    volume_region_shape = (3, 3, 3)
    front_face_region_targets = False
    sequential_region_targets = True
    region_target_jitter_fraction = 0.20

    reach_weight = 3.0
    plane_weight = 0.0
    region_center_weight = 3.0
    reach_exp_scale = 70.0
    plane_exp_scale = 120.0
    workspace_entry_exp_scale = 80.0
    region_center_exp_scale = 20.0
    region_entry_weight = 5.0
    near_center_radius = 0.070
    near_center_weight = 0.0
    target_tracking_weight = 0.0
    target_tracking_exp_scale = 450.0
    precision_center_exp_scale = 3500.0
    target_overshoot_penalty_weight = 0.0
    preferred_approach_weight = 0.0
    preferred_approach_margin = 0.030
    preferred_approach_exp_scale = 1500.0
    workspace_entry_weight = 0.0
    camera_alignment_weight = 2.5
    camera_alignment_exp_scale = 5.0
    gripper_camera_alignment_weight = 1.2
    gripper_camera_alignment_exp_scale = 2.0
    gripper_camera_visibility_weight = 0.8
    inside_workspace_weight = 0.8
    stereo_visibility_weight = 1.2
    success_bonus_weight = 18.0
    action_penalty_weight = 0.012
    joint_velocity_penalty_weight = 0.0004
    time_penalty_weight = 0.003


@configclass
class MT4CoordinatePlaneEnvCfg(MT4CoordinateCurriculumEnvCfg):
    curriculum_stage = "plane_localization"
    front_face_region_targets = True
    master_regions_sequentially = True
    region_mastery_successes = 10
    camera_region_success_radius = 1.35
    center_success_radius = 0.010
    reach_weight = 5.0
    plane_weight = 3.0
    reach_exp_scale = 18.0
    plane_exp_scale = 12.0
    workspace_entry_weight = 3.0
    region_center_exp_scale = 2.0
    region_entry_weight = 8.0
    near_center_radius = 0.070
    near_center_weight = 12.0
    target_tracking_weight = 18.0
    target_tracking_exp_scale = 450.0
    precision_center_exp_scale = 3500.0
    target_overshoot_penalty_weight = 45.0
    preferred_approach_weight = 3.0
    preferred_approach_margin = 0.030
    preferred_approach_exp_scale = 1500.0
    camera_alignment_weight = 5.0
    camera_alignment_exp_scale = 2.0
    gripper_camera_alignment_weight = 1.5
    gripper_camera_visibility_weight = 1.0
    inside_workspace_weight = 3.0
    stereo_visibility_weight = 0.5
    success_bonus_weight = 35.0
    time_penalty_weight = 0.03


@configclass
class MT4CoordinateVolumeEnvCfg(MT4CoordinatePlaneEnvCfg):
    front_face_region_targets = False
    volume_region_shape = (3, 3, 3)
    workspace_center = (0.30, 0.0, 0.21)
    workspace_size = (0.12, 0.16, 0.12)
    camera_look_at = (0.30, 0.0, 0.21)
    episode_length_s = 7.0
    plane_weight = 0.0
    workspace_entry_weight = 2.0
    region_entry_weight = 6.0
    near_center_weight = 10.0
    target_tracking_weight = 20.0
    target_overshoot_penalty_weight = 45.0
    preferred_approach_weight = 3.0


@configclass
class MT4CoordinateWorkspaceEntryEnvCfg(MT4CoordinateCurriculumEnvCfg):
    curriculum_stage = "workspace_entry"
    episode_length_s = 5.0
    reach_weight = 1.0
    plane_weight = 0.0
    region_center_weight = 0.0
    region_entry_weight = 0.0
    workspace_entry_weight = 8.0
    camera_alignment_weight = 0.0
    inside_workspace_weight = 4.0
    stereo_visibility_weight = 2.0
    success_bonus_weight = 20.0


@configclass
class MT4CoordinateSphereEnvCfg(MT4CoordinateCurriculumEnvCfg):
    curriculum_stage = "sphere_reach"
    episode_length_s = 5.0
    reach_weight = 4.0
    plane_weight = 0.6
    camera_alignment_weight = 0.8
    success_bonus_weight = 22.0


class MT4CoordinateCurriculumEnv(DirectRLEnv):
    cfg: MT4CoordinateCurriculumEnvCfg

    def __init__(self, cfg: MT4CoordinateCurriculumEnvCfg, render_mode: str | None = None, **kwargs):
        super().__init__(cfg, render_mode, **kwargs)

        self.joint_names = list(JOINT_NAMES)
        self.joint_ids, _ = self.robot.find_joints(self.joint_names)
        self.ee_body_id = self.robot.find_bodies("gripper_link")[0][0]

        self.joint_lower = torch.tensor(JOINT_LOWER, device=self.device)
        self.joint_upper = torch.tensor(JOINT_UPPER, device=self.device)
        self.home_joint_pos = torch.tensor(HOME_JOINT_POS, device=self.device)

        self.actions = torch.zeros((self.num_envs, self.cfg.action_space), device=self.device)
        self.joint_targets = self.home_joint_pos.repeat(self.num_envs, 1)

        self.workspace_center = torch.tensor(self.cfg.workspace_center, device=self.device)
        self.workspace_half_size = 0.5 * torch.tensor(self.cfg.workspace_size, device=self.device)
        self.workspace_min = self.workspace_center - self.workspace_half_size
        self.workspace_max = self.workspace_center + self.workspace_half_size
        if self.cfg.front_face_region_targets:
            self.region_cols = int(self.cfg.face_region_shape[0])
            self.region_rows = int(self.cfg.face_region_shape[1])
            self.region_depth = 1
        else:
            self.region_cols = int(self.cfg.volume_region_shape[0])
            self.region_rows = int(self.cfg.volume_region_shape[1])
            self.region_depth = int(self.cfg.volume_region_shape[2])
        self.regions_per_face = self.region_cols * self.region_rows
        self.total_regions = self.region_cols * self.region_rows * self.region_depth
        self.next_region_id = 0
        self.active_region_id = 0
        self.region_success_counts = torch.zeros((self.total_regions,), dtype=torch.long, device=self.device)
        self.region_best_episode_reward = torch.full((self.total_regions,), -float("inf"), device=self.device)
        self.region_mastered = torch.zeros((self.total_regions,), dtype=torch.bool, device=self.device)
        self.region_mastery_snapshot_writes = 0

        self.target_pos = torch.zeros((self.num_envs, 3), device=self.device)
        self.face_ids = torch.zeros((self.num_envs,), dtype=torch.long, device=self.device)
        self.region_ids = torch.zeros((self.num_envs,), dtype=torch.long, device=self.device)
        self.camera_estimated_target_pos = torch.zeros((self.num_envs, 3), device=self.device)
        self.camera_estimated_face_ids = torch.zeros((self.num_envs,), dtype=torch.long, device=self.device)
        self.camera_estimated_region_ids = torch.zeros((self.num_envs,), dtype=torch.long, device=self.device)
        self.camera_region_matches = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.face_one_hot = torch.zeros((self.num_envs, 6), device=self.device)
        self.region_features = torch.zeros((self.num_envs, 4), device=self.device)
        self.gripper_center_pos = torch.zeros((self.num_envs, 3), device=self.device)
        self.gripper_forward = torch.zeros((self.num_envs, 3), device=self.device)
        self.to_target = torch.zeros((self.num_envs, 3), device=self.device)
        self.distance = torch.zeros((self.num_envs,), device=self.device)
        self.plane_error = torch.zeros((self.num_envs,), device=self.device)
        self.region_uv_error = torch.zeros((self.num_envs,), device=self.device)
        self.in_target_region = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.workspace_entry_error = torch.zeros((self.num_envs,), device=self.device)
        self.camera_alignment_error = torch.zeros((self.num_envs,), device=self.device)
        self.target_estimate_error = torch.zeros((self.num_envs,), device=self.device)
        self.gripper_camera_target_error = torch.zeros((self.num_envs,), device=self.device)
        self.gripper_camera_target_depth = torch.zeros((self.num_envs,), device=self.device)
        self.target_overshoot = torch.zeros((self.num_envs,), device=self.device)
        self.preferred_approach_error = torch.zeros((self.num_envs,), device=self.device)
        self.inside_workspace = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.target_stereo_visible = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.target_three_camera_visible = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.target_gripper_camera_visible = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.gripper_stereo_visible = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.target_left_visible = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.target_right_visible = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.gripper_left_visible = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.gripper_right_visible = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        self.target_camera_features = torch.zeros((self.num_envs, 6), device=self.device)
        self.gripper_camera_features = torch.zeros((self.num_envs, 6), device=self.device)
        self.target_gripper_camera_features = torch.zeros((self.num_envs, 4), device=self.device)
        self.episode_rewards = torch.zeros((self.num_envs,), device=self.device)

        self.target_markers = VisualizationMarkers(self.cfg.target_marker_cfg)
        self.success_markers = VisualizationMarkers(self.cfg.success_marker_cfg)

        self._sample_targets(torch.arange(self.num_envs, device=self.device))

    def _setup_scene(self):
        self.robot = Articulation(self.cfg.robot_cfg)
        self.scene.articulations["robot"] = self.robot

        ground_cfg = sim_utils.GroundPlaneCfg()
        ground_cfg.func("/World/defaultGroundPlane", ground_cfg)

        light_cfg = sim_utils.DomeLightCfg(intensity=1800.0, color=(0.85, 0.85, 0.85))
        light_cfg.func("/World/Light", light_cfg)

        self.scene.clone_environments(copy_from_source=False)
        self.scene.filter_collisions(global_prim_paths=["/World/defaultGroundPlane"])

    def _pre_physics_step(self, actions: torch.Tensor):
        self.actions = actions.clamp(-1.0, 1.0)
        self.joint_targets = self.joint_targets + self.cfg.action_scale * self.actions
        self.joint_targets = torch.max(torch.min(self.joint_targets, self.joint_upper), self.joint_lower)

    def _apply_action(self):
        self.robot.set_joint_position_target(self.joint_targets, joint_ids=self.joint_ids)

    def _get_observations(self):
        self._compute_intermediate_values()

        joint_pos = self.robot.data.joint_pos[:, self.joint_ids]
        joint_vel = self.robot.data.joint_vel[:, self.joint_ids]
        gripper_in_cube = (self.gripper_center_pos - self.workspace_center) / self.workspace_half_size
        camera_estimated_to_target = (
            (self.camera_estimated_target_pos - self.gripper_center_pos) / self.workspace_half_size
        ).clamp(-2.0, 2.0)
        stage_flag = torch.full(
            (self.num_envs, 1),
            0.0 if self.cfg.curriculum_stage == "plane_localization" else 1.0,
            device=self.device,
        )

        obs = torch.cat(
            [
                joint_pos,
                0.1 * joint_vel,
                self.gripper_center_pos,
                self.gripper_forward,
                self.target_camera_features,
                self.gripper_camera_features,
                self.target_gripper_camera_features,
                camera_estimated_to_target,
                self.face_one_hot,
                self.region_features,
                self.actions,
                stage_flag,
                gripper_in_cube.clamp(-2.0, 2.0),
            ],
            dim=-1,
        )
        return {"policy": obs}

    def _get_rewards(self):
        self._compute_intermediate_values()

        success = self._success()
        reach_reward = torch.exp(-self.cfg.reach_exp_scale * self.distance * self.distance)
        plane_reward = torch.exp(-self.cfg.plane_exp_scale * self.plane_error * self.plane_error)
        region_center_reward = torch.exp(
            -self.cfg.region_center_exp_scale * self.region_uv_error * self.region_uv_error
        )
        workspace_entry_reward = torch.exp(
            -self.cfg.workspace_entry_exp_scale * self.workspace_entry_error * self.workspace_entry_error
        )
        target_tracking_reward = torch.exp(
            -self.cfg.target_tracking_exp_scale * self.distance * self.distance
        )
        camera_alignment_reward = torch.exp(
            -self.cfg.camera_alignment_exp_scale * self.camera_alignment_error * self.camera_alignment_error
        )
        gripper_camera_alignment_reward = torch.exp(
            -self.cfg.gripper_camera_alignment_exp_scale
            * self.gripper_camera_target_error
            * self.gripper_camera_target_error
        )
        stereo_visible = self.target_stereo_visible & self.gripper_stereo_visible
        action_penalty = torch.sum(self.actions * self.actions, dim=-1)
        joint_vel = self.robot.data.joint_vel[:, self.joint_ids]
        joint_velocity_penalty = torch.sum(joint_vel * joint_vel, dim=-1)

        if self.cfg.front_face_region_targets:
            center_reward = torch.exp(-self.cfg.precision_center_exp_scale * self.distance * self.distance)
            near_center_progress = (
                (self.cfg.near_center_radius - self.distance)
                / max(self.cfg.near_center_radius - self.cfg.center_success_radius, 1.0e-6)
            ).clamp(0.0, 1.0)
            near_center_reward = near_center_progress * near_center_progress * self.in_target_region.float()
            preferred_approach_reward = torch.exp(
                -self.cfg.preferred_approach_exp_scale
                * self.preferred_approach_error
                * self.preferred_approach_error
            )
            rewards = (
                -4.0 * self.distance
                -3.0 * self.plane_error
                -1.2 * self.camera_alignment_error
                -0.8 * self.gripper_camera_target_error
                -2.0 * self.workspace_entry_error
                + 4.0 * center_reward
                + self.cfg.target_tracking_weight * target_tracking_reward
                + 8.0 * self.in_target_region.float()
                + self.cfg.near_center_weight * near_center_reward
                + self.cfg.preferred_approach_weight * preferred_approach_reward
                + 3.0 * self.inside_workspace.float()
                + 0.5 * stereo_visible.float()
                + self.cfg.gripper_camera_visibility_weight * self.target_gripper_camera_visible.float()
                + self.cfg.success_bonus_weight * success.float()
                - self.cfg.target_overshoot_penalty_weight * self.target_overshoot
                - self.cfg.action_penalty_weight * action_penalty
                - self.cfg.joint_velocity_penalty_weight * joint_velocity_penalty
                - self.cfg.time_penalty_weight
            )
            self.episode_rewards += rewards.detach()
            return rewards

        if self.cfg.curriculum_stage == "plane_localization":
            center_reward = torch.exp(-self.cfg.precision_center_exp_scale * self.distance * self.distance)
            near_center_progress = (
                (self.cfg.near_center_radius - self.distance)
                / max(self.cfg.near_center_radius - self.cfg.center_success_radius, 1.0e-6)
            ).clamp(0.0, 1.0)
            near_center_reward = near_center_progress * near_center_progress
            preferred_approach_reward = torch.exp(
                -self.cfg.preferred_approach_exp_scale
                * self.preferred_approach_error
                * self.preferred_approach_error
            )
            center_reward_weight = 4.0
        else:
            center_reward = torch.zeros_like(self.distance)
            near_center_reward = torch.zeros_like(self.distance)
            preferred_approach_reward = torch.zeros_like(self.distance)
            center_reward_weight = 0.0

        rewards = (
            self.cfg.reach_weight * reach_reward
            + self.cfg.plane_weight * plane_reward
            + self.cfg.region_center_weight * region_center_reward
            + self.cfg.region_entry_weight * self.in_target_region.float()
            + self.cfg.workspace_entry_weight * workspace_entry_reward
            + self.cfg.target_tracking_weight * target_tracking_reward
            + center_reward_weight * center_reward
            + self.cfg.near_center_weight * near_center_reward
            + self.cfg.preferred_approach_weight * preferred_approach_reward
            + self.cfg.camera_alignment_weight * camera_alignment_reward
            + self.cfg.gripper_camera_alignment_weight * gripper_camera_alignment_reward
            + self.cfg.inside_workspace_weight * self.inside_workspace.float()
            + self.cfg.stereo_visibility_weight * stereo_visible.float()
            + self.cfg.gripper_camera_visibility_weight * self.target_gripper_camera_visible.float()
            + self.cfg.success_bonus_weight * success.float()
            - self.cfg.target_overshoot_penalty_weight * self.target_overshoot
            - self.cfg.action_penalty_weight * action_penalty
            - self.cfg.joint_velocity_penalty_weight * joint_velocity_penalty
            - self.cfg.time_penalty_weight
        )
        self.episode_rewards += rewards.detach()
        return rewards

    def _get_dones(self):
        self._compute_intermediate_values()

        success = self._success()
        self._update_region_mastery(success)
        time_out = self.episode_length_buf >= self.max_episode_length - 1

        prefix = f"coordinate_curriculum/{self.cfg.curriculum_stage}"
        log_data = {
            f"{prefix}_success_rate": success.float().mean(),
            f"{prefix}_mean_distance": self.distance.mean(),
            f"{prefix}_mean_plane_error": self.plane_error.mean(),
            f"{prefix}_mean_camera_region_error": self.region_uv_error.mean(),
            f"{prefix}_camera_region_entry_rate": self.in_target_region.float().mean(),
            f"{prefix}_camera_region_match_rate": self.camera_region_matches.float().mean(),
            f"{prefix}_mean_workspace_entry_error": self.workspace_entry_error.mean(),
            f"{prefix}_mean_camera_alignment_error": self.camera_alignment_error.mean(),
            f"{prefix}_mean_target_estimate_error": self.target_estimate_error.mean(),
            f"{prefix}_mean_gripper_camera_target_error": self.gripper_camera_target_error.mean(),
            f"{prefix}_mean_gripper_camera_target_depth": self.gripper_camera_target_depth.mean(),
            f"{prefix}_mean_target_overshoot": self.target_overshoot.mean(),
            f"{prefix}_mean_preferred_approach_error": self.preferred_approach_error.mean(),
            f"{prefix}_inside_workspace_rate": self.inside_workspace.float().mean(),
            f"{prefix}_target_left_visible_rate": self.target_left_visible.float().mean(),
            f"{prefix}_target_right_visible_rate": self.target_right_visible.float().mean(),
            f"{prefix}_target_stereo_visible_rate": self.target_stereo_visible.float().mean(),
            f"{prefix}_target_gripper_camera_visible_rate": self.target_gripper_camera_visible.float().mean(),
            f"{prefix}_target_three_camera_visible_rate": self.target_three_camera_visible.float().mean(),
            f"{prefix}_gripper_left_visible_rate": self.gripper_left_visible.float().mean(),
            f"{prefix}_gripper_right_visible_rate": self.gripper_right_visible.float().mean(),
            f"{prefix}_gripper_stereo_visible_rate": self.gripper_stereo_visible.float().mean(),
            f"{prefix}_mean_region_number": (self.region_ids.float() + 1.0).mean(),
            f"{prefix}_min_region_number": (self.region_ids.float() + 1.0).min(),
            f"{prefix}_max_region_number": (self.region_ids.float() + 1.0).max(),
            f"{prefix}_mean_camera_estimated_region_number": (
                self.camera_estimated_region_ids.float() + 1.0
            ).mean(),
            f"{prefix}_min_camera_estimated_region_number": (
                self.camera_estimated_region_ids.float() + 1.0
            ).min(),
            f"{prefix}_max_camera_estimated_region_number": (
                self.camera_estimated_region_ids.float() + 1.0
            ).max(),
            f"{prefix}_center_1cm_rate": (self.distance < self.cfg.center_success_radius).float().mean(),
            f"{prefix}_near_center_7cm_rate": (self.distance < self.cfg.near_center_radius).float().mean(),
            f"{prefix}_strict_region_center_success_rate": (
                success.float() if self.cfg.curriculum_stage == "plane_localization" else torch.zeros_like(success.float())
            ).mean(),
            f"{prefix}_active_region_number": torch.tensor(float(self.active_region_id + 1), device=self.device),
            f"{prefix}_mastered_region_count": self.region_mastered.float().sum(),
        }
        for region_id in range(self.total_regions):
            region_mask = self.region_ids == region_id
            region_count = region_mask.float().sum().clamp(min=1.0)
            region_success = (success.float() * region_mask.float()).sum() / region_count
            best_reward = self.region_best_episode_reward[region_id]
            if not torch.isfinite(best_reward):
                best_reward = torch.tensor(0.0, device=self.device)
            log_data[f"{prefix}_region_{region_id + 1:02d}_batch_success_rate"] = region_success
            log_data[f"{prefix}_region_{region_id + 1:02d}_success_count"] = self.region_success_counts[
                region_id
            ].float()
            log_data[f"{prefix}_region_{region_id + 1:02d}_best_episode_reward"] = best_reward
            log_data[f"{prefix}_region_{region_id + 1:02d}_mastered"] = self.region_mastered[region_id].float()
        for face_id, face_name in enumerate(("x_min", "x_max", "y_min", "y_max", "z_min", "z_max")):
            face_mask = self.face_ids == face_id
            face_count = face_mask.float().sum().clamp(min=1.0)
            log_data[f"{prefix}_{face_name}_sample_rate"] = face_mask.float().mean()
            log_data[f"{prefix}_{face_name}_success_rate"] = (success.float() * face_mask.float()).sum() / face_count
        self.extras["log"] = log_data

        self._update_markers(success)
        return success, time_out

    def _reset_idx(self, env_ids: torch.Tensor | None):
        if env_ids is None:
            env_ids = self.robot._ALL_INDICES

        super()._reset_idx(env_ids)
        self.robot.reset(env_ids)

        self.joint_targets[env_ids] = self.home_joint_pos
        joint_pos = self.robot.data.default_joint_pos[env_ids].clone()
        joint_vel = self.robot.data.default_joint_vel[env_ids].clone()
        joint_pos[:, self.joint_ids] = self.joint_targets[env_ids]
        joint_vel[:, self.joint_ids] = 0.0
        self.robot.write_joint_state_to_sim(joint_pos, joint_vel, env_ids=env_ids)

        self.episode_rewards[env_ids] = 0.0
        self._sample_targets(env_ids)

    def _sample_targets(self, env_ids: torch.Tensor):
        n = len(env_ids)
        workspace_span = self.workspace_max - self.workspace_min
        if self.cfg.curriculum_stage in ("plane_localization", "workspace_entry"):
            region_ids = self._next_region_ids(n)
            if self.cfg.front_face_region_targets:
                target = self._front_face_region_centers(region_ids)
            else:
                target = self._region_centers(region_ids)
            jitter_fraction = float(self.cfg.region_target_jitter_fraction)
            if jitter_fraction > 0.0:
                if self.cfg.front_face_region_targets:
                    target = self._jitter_front_face_region_targets(target, region_ids, jitter_fraction)
                else:
                    target = self._jitter_region_targets(target, region_ids, jitter_fraction)
            if self.cfg.front_face_region_targets:
                face_ids = torch.zeros((n,), dtype=torch.long, device=self.device)
            else:
                face_ids = self._nearest_face_ids(target)
        else:
            target = self.workspace_min + torch.rand((n, 3), device=self.device) * workspace_span

            for _ in range(4):
                radial = torch.linalg.norm(target[:, :2], dim=-1)
                too_close = radial < self.cfg.min_target_base_radius
                if not torch.any(too_close):
                    break
                count = int(too_close.sum().item())
                target[too_close] = self.workspace_min + torch.rand((count, 3), device=self.device) * workspace_span

            region_ids, face_ids = self._nearest_region_ids(target)

        self.target_pos[env_ids] = target
        self.face_ids[env_ids] = face_ids
        self.region_ids[env_ids] = region_ids
        self.camera_estimated_target_pos[env_ids] = target
        self.camera_estimated_face_ids[env_ids] = face_ids
        self.camera_estimated_region_ids[env_ids] = region_ids
        self.face_one_hot[env_ids] = torch.nn.functional.one_hot(face_ids, num_classes=6).float()
        self.region_features[env_ids] = self._region_features(region_ids)
        self._update_markers()

    def _next_region_ids(self, n: int) -> torch.Tensor:
        if self._uses_region_mastery():
            return torch.full((n,), self.active_region_id, dtype=torch.long, device=self.device)
        if self.cfg.sequential_region_targets:
            region_ids = (torch.arange(n, device=self.device) + self.next_region_id) % self.total_regions
            self.next_region_id = (self.next_region_id + n) % self.total_regions
            return region_ids.long()
        return torch.randint(0, self.total_regions, (n,), device=self.device)

    def _region_centers(self, region_ids: torch.Tensor) -> torch.Tensor:
        col_ids, row_ids, depth_ids = self._volume_cell_indices(region_ids)
        cell = torch.stack(
            [
                (col_ids.float() + 0.5) / float(self.region_cols),
                (row_ids.float() + 0.5) / float(self.region_rows),
                (depth_ids.float() + 0.5) / float(self.region_depth),
            ],
            dim=-1,
        )
        return self.workspace_min + cell * (self.workspace_max - self.workspace_min)

    def _front_face_region_centers(self, region_ids: torch.Tensor) -> torch.Tensor:
        col_ids, row_ids, _ = self._volume_cell_indices(region_ids)
        span = self.workspace_max - self.workspace_min
        target = torch.zeros((region_ids.shape[0], 3), device=self.device)
        target[:, 0] = self.workspace_center[0]
        target[:, 1] = self.workspace_min[1] + ((col_ids.float() + 0.5) / float(self.region_cols)) * span[1]
        target[:, 2] = self.workspace_min[2] + ((row_ids.float() + 0.5) / float(self.region_rows)) * span[2]
        return target

    def _jitter_region_targets(
        self,
        target: torch.Tensor,
        region_ids: torch.Tensor,
        jitter_fraction: float,
    ) -> torch.Tensor:
        col_ids, row_ids, depth_ids = self._volume_cell_indices(region_ids)
        cell_size = torch.tensor(
            [
                1.0 / float(self.region_cols),
                1.0 / float(self.region_rows),
                1.0 / float(self.region_depth),
            ],
            device=self.device,
        )
        base = torch.stack(
            [
                (col_ids.float() + 0.5) * cell_size[0],
                (row_ids.float() + 0.5) * cell_size[1],
                (depth_ids.float() + 0.5) * cell_size[2],
            ],
            dim=-1,
        )
        jitter = (torch.rand((target.shape[0], 3), device=self.device) - 0.5) * jitter_fraction * cell_size
        cell = (base + jitter).clamp(0.0, 1.0)
        return self.workspace_min + cell * (self.workspace_max - self.workspace_min)

    def _jitter_front_face_region_targets(
        self,
        target: torch.Tensor,
        region_ids: torch.Tensor,
        jitter_fraction: float,
    ) -> torch.Tensor:
        col_ids, row_ids, _ = self._volume_cell_indices(region_ids)
        span = self.workspace_max - self.workspace_min
        cell_size = torch.tensor(
            [
                1.0 / float(self.region_cols),
                1.0 / float(self.region_rows),
            ],
            device=self.device,
        )
        base = torch.stack(
            [
                (col_ids.float() + 0.5) * cell_size[0],
                (row_ids.float() + 0.5) * cell_size[1],
            ],
            dim=-1,
        )
        jitter = (torch.rand((target.shape[0], 2), device=self.device) - 0.5) * jitter_fraction * cell_size
        face_cell = (base + jitter).clamp(0.0, 1.0)
        jittered = target.clone()
        jittered[:, 0] = self.workspace_center[0]
        jittered[:, 1] = self.workspace_min[1] + face_cell[:, 0] * span[1]
        jittered[:, 2] = self.workspace_min[2] + face_cell[:, 1] * span[2]
        return jittered

    def _write_face_uv_to_targets(
        self,
        target: torch.Tensor,
        face_ids: torch.Tensor,
        u: torch.Tensor,
        v: torch.Tensor,
    ):
        span = self.workspace_max - self.workspace_min

        x_min = face_ids == 0
        x_max = face_ids == 1
        y_min = face_ids == 2
        y_max = face_ids == 3
        z_min = face_ids == 4
        z_max = face_ids == 5

        x_from_u = self.workspace_min[0] + u * span[0]
        y_from_u = self.workspace_min[1] + u * span[1]
        z_from_v = self.workspace_min[2] + v * span[2]
        y_from_v = self.workspace_min[1] + v * span[1]

        target[x_min, 0] = self.workspace_min[0]
        target[x_min, 1] = y_from_u[x_min]
        target[x_min, 2] = z_from_v[x_min]

        target[x_max, 0] = self.workspace_max[0]
        target[x_max, 1] = y_from_u[x_max]
        target[x_max, 2] = z_from_v[x_max]

        target[y_min, 0] = x_from_u[y_min]
        target[y_min, 1] = self.workspace_min[1]
        target[y_min, 2] = z_from_v[y_min]

        target[y_max, 0] = x_from_u[y_max]
        target[y_max, 1] = self.workspace_max[1]
        target[y_max, 2] = z_from_v[y_max]

        target[z_min, 0] = x_from_u[z_min]
        target[z_min, 1] = y_from_v[z_min]
        target[z_min, 2] = self.workspace_min[2]

        target[z_max, 0] = x_from_u[z_max]
        target[z_max, 1] = y_from_v[z_max]
        target[z_max, 2] = self.workspace_max[2]

    def _nearest_region_ids(self, target: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        span = torch.clamp(self.workspace_max - self.workspace_min, min=1e-6)
        norm = ((target - self.workspace_min) / span).clamp(0.0, 0.999999)

        col_ids = torch.clamp((norm[:, 0] * self.region_cols).long(), max=self.region_cols - 1)
        row_ids = torch.clamp((norm[:, 1] * self.region_rows).long(), max=self.region_rows - 1)
        depth_ids = torch.clamp((norm[:, 2] * self.region_depth).long(), max=self.region_depth - 1)
        region_ids = depth_ids * self.region_rows * self.region_cols + row_ids * self.region_cols + col_ids
        return region_ids.long(), self._nearest_face_ids(target)

    def _region_features(self, region_ids: torch.Tensor) -> torch.Tensor:
        col_ids, row_ids, depth_ids = self._volume_cell_indices(region_ids)
        denom = max(float(self.total_regions - 1), 1.0)
        col_denom = max(float(self.region_cols - 1), 1.0)
        row_denom = max(float(self.region_rows - 1), 1.0)
        depth_denom = max(float(self.region_depth - 1), 1.0)
        return torch.stack(
            [
                (region_ids.float() / denom) * 2.0 - 1.0,
                (col_ids.float() / col_denom) * 2.0 - 1.0,
                (row_ids.float() / row_denom) * 2.0 - 1.0,
                (depth_ids.float() / depth_denom) * 2.0 - 1.0,
            ],
            dim=-1,
        )

    def _volume_cell_indices(self, region_ids: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        plane_cells = self.region_cols * self.region_rows
        depth_ids = region_ids // plane_cells
        cell_ids = region_ids % plane_cells
        row_ids = cell_ids // self.region_cols
        col_ids = cell_ids % self.region_cols
        return col_ids.long(), row_ids.long(), depth_ids.long()

    def _nearest_face_ids(self, target: torch.Tensor) -> torch.Tensor:
        distances = torch.stack(
            [
                torch.abs(target[:, 0] - self.workspace_min[0]),
                torch.abs(target[:, 0] - self.workspace_max[0]),
                torch.abs(target[:, 1] - self.workspace_min[1]),
                torch.abs(target[:, 1] - self.workspace_max[1]),
                torch.abs(target[:, 2] - self.workspace_min[2]),
                torch.abs(target[:, 2] - self.workspace_max[2]),
            ],
            dim=-1,
        )
        return torch.argmin(distances, dim=-1).long()

    def _front_face_region_ids_from_points(self, points: torch.Tensor) -> torch.Tensor:
        span = torch.clamp(self.workspace_max - self.workspace_min, min=1e-6)
        norm_y = ((points[:, 1] - self.workspace_min[1]) / span[1]).clamp(0.0, 0.999999)
        norm_z = ((points[:, 2] - self.workspace_min[2]) / span[2]).clamp(0.0, 0.999999)
        col_ids = torch.clamp((norm_y * self.region_cols).long(), max=self.region_cols - 1)
        row_ids = torch.clamp((norm_z * self.region_rows).long(), max=self.region_rows - 1)
        return (row_ids * self.region_cols + col_ids).long()

    def _camera_basis(self, camera_pos: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        look_at = torch.tensor(self.cfg.camera_look_at, device=self.device)
        forward = look_at - camera_pos
        forward = forward / torch.clamp(torch.linalg.norm(forward), min=1e-6)
        world_up = torch.tensor((0.0, 0.0, 1.0), device=self.device)
        right = torch.cross(forward, world_up, dim=0)
        right = right / torch.clamp(torch.linalg.norm(right), min=1e-6)
        up = torch.cross(right, forward, dim=0)
        up = up / torch.clamp(torch.linalg.norm(up), min=1e-6)
        return forward, right, up

    def _camera_rays_from_uv(self, uv: torch.Tensor, camera_pos: torch.Tensor) -> torch.Tensor:
        forward, right, up = self._camera_basis(camera_pos)
        focal = 1.0 / torch.tan(torch.deg2rad(torch.tensor(self.cfg.camera_fov_deg * 0.5, device=self.device)))
        rays = forward.unsqueeze(0) + (uv[:, 0:1] / focal) * right.unsqueeze(0) + (uv[:, 1:2] / focal) * up.unsqueeze(0)
        return rays / torch.clamp(torch.linalg.norm(rays, dim=-1, keepdim=True), min=1e-6)

    def _dynamic_camera_basis(self, forward: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        forward = forward / torch.clamp(torch.linalg.norm(forward, dim=-1, keepdim=True), min=1e-6)
        world_up = torch.tensor((0.0, 0.0, 1.0), device=self.device).repeat(self.num_envs, 1)
        fallback_up = torch.tensor((0.0, 1.0, 0.0), device=self.device).repeat(self.num_envs, 1)
        near_parallel = torch.abs(torch.sum(forward * world_up, dim=-1, keepdim=True)) > 0.95
        up_ref = torch.where(near_parallel, fallback_up, world_up)
        right = torch.cross(forward, up_ref, dim=-1)
        right = right / torch.clamp(torch.linalg.norm(right, dim=-1, keepdim=True), min=1e-6)
        up = torch.cross(right, forward, dim=-1)
        up = up / torch.clamp(torch.linalg.norm(up, dim=-1, keepdim=True), min=1e-6)
        return forward, right, up

    def _triangulate_stereo_points(self, stereo_features: torch.Tensor) -> torch.Tensor:
        left_pos = torch.tensor(self.cfg.left_camera_pos, device=self.device)
        right_pos = torch.tensor(self.cfg.right_camera_pos, device=self.device)
        left_ray = self._camera_rays_from_uv(stereo_features[:, 0:2], left_pos)
        right_ray = self._camera_rays_from_uv(stereo_features[:, 3:5], right_pos)

        w0 = left_pos.unsqueeze(0) - right_pos.unsqueeze(0)
        a = torch.sum(left_ray * left_ray, dim=-1)
        b = torch.sum(left_ray * right_ray, dim=-1)
        c = torch.sum(right_ray * right_ray, dim=-1)
        d = torch.sum(left_ray * w0, dim=-1)
        e = torch.sum(right_ray * w0, dim=-1)
        denom = torch.clamp(a * c - b * b, min=1e-6)
        left_t = (b * e - c * d) / denom
        right_t = (a * e - b * d) / denom
        left_point = left_pos.unsqueeze(0) + left_t.unsqueeze(-1) * left_ray
        right_point = right_pos.unsqueeze(0) + right_t.unsqueeze(-1) * right_ray
        return 0.5 * (left_point + right_point)

    def _estimate_regions_from_target_cameras(self) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        target_estimate = self._triangulate_stereo_points(self.target_camera_features)
        visible = torch.all(self.target_camera_features[:, [2, 5]] > 0.5, dim=-1)
        fallback_region = min(self.total_regions // 2, self.total_regions - 1)

        if self.cfg.front_face_region_targets:
            target_estimate[:, 0] = self.workspace_center[0]
            target_estimate = torch.max(torch.min(target_estimate, self.workspace_max), self.workspace_min)
            region_ids = self._front_face_region_ids_from_points(target_estimate)
            face_ids = torch.zeros((self.num_envs,), dtype=torch.long, device=self.device)
            region_centers = self._front_face_region_centers(region_ids)
        else:
            target_estimate = torch.max(torch.min(target_estimate, self.workspace_max), self.workspace_min)
            region_ids, face_ids = self._nearest_region_ids(target_estimate)
            region_centers = self._region_centers(region_ids)

        fallback_ids = torch.full((self.num_envs,), fallback_region, dtype=torch.long, device=self.device)
        fallback_faces = torch.zeros((self.num_envs,), dtype=torch.long, device=self.device)
        region_ids = torch.where(visible, region_ids, fallback_ids)
        face_ids = torch.where(visible, face_ids, fallback_faces)
        if self.cfg.front_face_region_targets:
            region_centers = self._front_face_region_centers(region_ids)
        else:
            region_centers = self._region_centers(region_ids)
        estimated_targets = torch.where(visible.unsqueeze(-1), target_estimate, region_centers)
        return estimated_targets, face_ids, region_ids, visible

    def _compute_intermediate_values(self):
        ee_pos_w = self.robot.data.body_pos_w[:, self.ee_body_id, :]
        ee_quat_w = self.robot.data.body_quat_w[:, self.ee_body_id, :]
        ee_pos = ee_pos_w - self.scene.env_origins

        center_offset_b = torch.tensor(self.cfg.gripper_center_offset_b, device=self.device).repeat(self.num_envs, 1)
        forward_axis_b = torch.tensor(self.cfg.gripper_forward_axis_b, device=self.device).repeat(self.num_envs, 1)
        self.gripper_center_pos = ee_pos + math_utils.quat_apply(ee_quat_w, center_offset_b)
        self.gripper_forward = math_utils.quat_apply(ee_quat_w, forward_axis_b)
        self.gripper_forward = self.gripper_forward / torch.clamp(
            torch.linalg.norm(self.gripper_forward, dim=-1, keepdim=True), min=1e-6
        )

        self.to_target = self.target_pos - self.gripper_center_pos
        self.distance = torch.linalg.norm(self.to_target, dim=-1)
        self.plane_error = self._compute_plane_error(self.gripper_center_pos)
        closest_workspace_point = torch.max(torch.min(self.gripper_center_pos, self.workspace_max), self.workspace_min)
        self.workspace_entry_error = torch.linalg.norm(self.gripper_center_pos - closest_workspace_point, dim=-1)
        inside_min = self.gripper_center_pos >= self.workspace_min
        inside_max = self.gripper_center_pos <= self.workspace_max
        self.inside_workspace = torch.all(inside_min & inside_max, dim=-1)
        self.target_camera_features = self._project_to_stereo(self.target_pos)
        self.gripper_camera_features = self._project_to_stereo(self.gripper_center_pos)
        self.target_gripper_camera_features = self._project_to_gripper_camera(self.target_pos)
        (
            self.camera_estimated_target_pos,
            self.camera_estimated_face_ids,
            self.camera_estimated_region_ids,
            self.target_stereo_visible,
        ) = self._estimate_regions_from_target_cameras()
        self.face_one_hot = torch.nn.functional.one_hot(self.camera_estimated_face_ids, num_classes=6).float()
        self.region_features = self._region_features(self.camera_estimated_region_ids)
        self.camera_region_matches = self.target_stereo_visible & (self.camera_estimated_region_ids == self.region_ids)
        self.target_estimate_error = torch.linalg.norm(self.camera_estimated_target_pos - self.target_pos, dim=-1)
        self.region_uv_error, self.in_target_region = self._compute_region_entry(self.gripper_center_pos)
        self.target_overshoot, self.preferred_approach_error = self._compute_target_approach_terms()
        camera_delta = self.target_camera_features[:, [0, 1, 3, 4]] - self.gripper_camera_features[:, [0, 1, 3, 4]]
        self.camera_alignment_error = torch.linalg.norm(camera_delta, dim=-1)
        self.gripper_camera_target_error = torch.linalg.norm(self.target_gripper_camera_features[:, 0:2], dim=-1)
        self.gripper_camera_target_depth = self.target_gripper_camera_features[:, 3]
        self.target_left_visible = self.target_camera_features[:, 2] > 0.5
        self.target_right_visible = self.target_camera_features[:, 5] > 0.5
        self.target_gripper_camera_visible = self.target_gripper_camera_features[:, 2] > 0.5
        self.gripper_left_visible = self.gripper_camera_features[:, 2] > 0.5
        self.gripper_right_visible = self.gripper_camera_features[:, 5] > 0.5
        self.target_stereo_visible = self.target_left_visible & self.target_right_visible
        self.target_three_camera_visible = self.target_stereo_visible & self.target_gripper_camera_visible
        self.gripper_stereo_visible = self.gripper_left_visible & self.gripper_right_visible

    def _compute_plane_error(self, points: torch.Tensor) -> torch.Tensor:
        if self.cfg.front_face_region_targets:
            return torch.abs(points[:, 0] - self.target_pos[:, 0])

        errors = torch.zeros((self.num_envs,), device=self.device)
        errors[self.face_ids == 0] = torch.abs(points[self.face_ids == 0, 0] - self.workspace_min[0])
        errors[self.face_ids == 1] = torch.abs(points[self.face_ids == 1, 0] - self.workspace_max[0])
        errors[self.face_ids == 2] = torch.abs(points[self.face_ids == 2, 1] - self.workspace_min[1])
        errors[self.face_ids == 3] = torch.abs(points[self.face_ids == 3, 1] - self.workspace_max[1])
        errors[self.face_ids == 4] = torch.abs(points[self.face_ids == 4, 2] - self.workspace_min[2])
        errors[self.face_ids == 5] = torch.abs(points[self.face_ids == 5, 2] - self.workspace_max[2])
        return errors

    def _compute_region_entry(self, points: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        estimated_target_camera_features = self._project_to_stereo(self.camera_estimated_target_pos)
        target_uv = estimated_target_camera_features[:, [0, 1, 3, 4]]
        gripper_uv = self.gripper_camera_features[:, [0, 1, 3, 4]]
        camera_region_error = torch.linalg.norm(target_uv - gripper_uv, dim=-1)

        left_entry = self._same_camera_cell(target_uv[:, 0:2], gripper_uv[:, 0:2])
        right_entry = self._same_camera_cell(target_uv[:, 2:4], gripper_uv[:, 2:4])
        return camera_region_error, left_entry & right_entry & self.target_stereo_visible

    def _compute_target_approach_terms(self) -> tuple[torch.Tensor, torch.Tensor]:
        target_xy = self.target_pos[:, :2]
        gripper_xy = self.gripper_center_pos[:, :2]
        base_to_target = target_xy
        base_to_target = base_to_target / torch.clamp(
            torch.linalg.norm(base_to_target, dim=-1, keepdim=True), min=1.0e-6
        )

        gripper_past_target = torch.sum((gripper_xy - target_xy) * base_to_target, dim=-1)
        overshoot = torch.clamp(gripper_past_target, min=0.0)

        base_side_gap = torch.clamp(-gripper_past_target, min=0.0)
        above_gap = torch.clamp(self.gripper_center_pos[:, 2] - self.target_pos[:, 2], min=0.0)
        preferred_gap = torch.maximum(base_side_gap, above_gap)
        preferred_error = torch.clamp(self.cfg.preferred_approach_margin - preferred_gap, min=0.0)
        return overshoot, preferred_error

    def _same_camera_cell(self, target_uv: torch.Tensor, gripper_uv: torch.Tensor) -> torch.Tensor:
        target_norm = ((target_uv + 1.0) * 0.5).clamp(0.0, 0.999999)
        gripper_norm = ((gripper_uv + 1.0) * 0.5).clamp(-1.0, 2.0)

        cols = self.region_cols
        rows = self.region_rows
        target_col = torch.clamp((target_norm[:, 0] * cols).long(), max=cols - 1)
        target_row = torch.clamp((target_norm[:, 1] * rows).long(), max=rows - 1)
        cell_u = 1.0 / float(cols)
        cell_v = 1.0 / float(rows)
        margin_u = self.cfg.region_success_margin_fraction * cell_u
        margin_v = self.cfg.region_success_margin_fraction * cell_v
        u_min = target_col.float() * cell_u - margin_u
        u_max = (target_col.float() + 1.0) * cell_u + margin_u
        v_min = target_row.float() * cell_v - margin_v
        v_max = (target_row.float() + 1.0) * cell_v + margin_v
        return (
            (gripper_norm[:, 0] >= u_min)
            & (gripper_norm[:, 0] <= u_max)
            & (gripper_norm[:, 1] >= v_min)
            & (gripper_norm[:, 1] <= v_max)
        )

    def _face_uv(self, points: torch.Tensor, face_ids: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        span = torch.clamp(self.workspace_max - self.workspace_min, min=1e-6)
        norm = ((points - self.workspace_min) / span).clamp(-1.0, 2.0)
        u = torch.zeros((points.shape[0],), device=self.device)
        v = torch.zeros((points.shape[0],), device=self.device)

        x_face = (face_ids == 0) | (face_ids == 1)
        y_face = (face_ids == 2) | (face_ids == 3)
        z_face = (face_ids == 4) | (face_ids == 5)
        u[x_face] = norm[x_face, 1]
        v[x_face] = norm[x_face, 2]
        u[y_face] = norm[y_face, 0]
        v[y_face] = norm[y_face, 2]
        u[z_face] = norm[z_face, 0]
        v[z_face] = norm[z_face, 1]
        return u, v

    def _project_to_stereo(self, points: torch.Tensor) -> torch.Tensor:
        left = self._project_to_camera(points, torch.tensor(self.cfg.left_camera_pos, device=self.device))
        right = self._project_to_camera(points, torch.tensor(self.cfg.right_camera_pos, device=self.device))
        return torch.cat([left, right], dim=-1)

    def _project_to_gripper_camera(self, points: torch.Tensor) -> torch.Tensor:
        camera_offset_b = torch.tensor(self.cfg.gripper_camera_offset_b, device=self.device).repeat(self.num_envs, 1)
        forward_axis_b = torch.tensor(self.cfg.gripper_forward_axis_b, device=self.device).repeat(self.num_envs, 1)
        ee_quat_w = self.robot.data.body_quat_w[:, self.ee_body_id, :]
        ee_pos_w = self.robot.data.body_pos_w[:, self.ee_body_id, :]
        ee_pos = ee_pos_w - self.scene.env_origins
        camera_pos = ee_pos + math_utils.quat_apply(ee_quat_w, camera_offset_b)
        camera_forward = math_utils.quat_apply(ee_quat_w, forward_axis_b)
        forward, right, up = self._dynamic_camera_basis(camera_forward)

        rel = points - camera_pos
        depth = torch.sum(rel * forward, dim=-1)
        x = torch.sum(rel * right, dim=-1)
        y = torch.sum(rel * up, dim=-1)
        focal = 1.0 / torch.tan(torch.deg2rad(torch.tensor(self.cfg.gripper_camera_fov_deg * 0.5, device=self.device)))
        u = focal * x / torch.clamp(depth, min=1e-4)
        v = focal * y / torch.clamp(depth, min=1e-4)
        visible = (
            (depth > self.cfg.gripper_camera_min_depth)
            & (depth < self.cfg.gripper_camera_max_depth)
            & (torch.abs(u) <= 1.0)
            & (torch.abs(v) <= 1.0)
        )
        depth_norm = (
            (depth - self.cfg.gripper_camera_min_depth)
            / max(self.cfg.gripper_camera_max_depth - self.cfg.gripper_camera_min_depth, 1.0e-6)
        )
        depth_feature = (depth_norm * 2.0 - 1.0).clamp(-2.0, 2.0)
        return torch.stack([u.clamp(-2.0, 2.0), v.clamp(-2.0, 2.0), visible.float(), depth_feature], dim=-1)

    def _project_to_camera(self, points: torch.Tensor, camera_pos: torch.Tensor) -> torch.Tensor:
        forward, right, up = self._camera_basis(camera_pos)

        rel = points - camera_pos
        depth = torch.sum(rel * forward, dim=-1)
        x = torch.sum(rel * right, dim=-1)
        y = torch.sum(rel * up, dim=-1)
        focal = 1.0 / torch.tan(torch.deg2rad(torch.tensor(self.cfg.camera_fov_deg * 0.5, device=self.device)))
        u = focal * x / torch.clamp(depth, min=1e-4)
        v = focal * y / torch.clamp(depth, min=1e-4)
        visible = (depth > 0.0) & (torch.abs(u) <= 1.0) & (torch.abs(v) <= 1.0)
        return torch.stack([u.clamp(-2.0, 2.0), v.clamp(-2.0, 2.0), visible.float()], dim=-1)

    def _success(self) -> torch.Tensor:
        stereo_visible = self.target_stereo_visible & self.gripper_stereo_visible
        if self.cfg.curriculum_stage == "workspace_entry":
            return (self.workspace_entry_error < self.cfg.workspace_entry_success_radius) & self.gripper_stereo_visible
        if self.cfg.curriculum_stage == "plane_localization":
            center_reached = self.distance < self.cfg.center_success_radius
            return self.in_target_region & center_reached & stereo_visible
        return (self.distance < self.cfg.success_radius) & stereo_visible

    def _uses_region_mastery(self) -> bool:
        return (
            bool(self.cfg.master_regions_sequentially)
            and self.cfg.curriculum_stage == "plane_localization"
        )

    def _update_region_mastery(self, success: torch.Tensor):
        if not self._uses_region_mastery() or not torch.any(success):
            return

        success_region_ids = self.region_ids[success].detach()
        success_rewards = self.episode_rewards[success].detach()
        for region_id_tensor in torch.unique(success_region_ids):
            region_id = int(region_id_tensor.item())
            region_mask = success_region_ids == region_id
            self.region_success_counts[region_id] += int(region_mask.sum().item())
            best_reward = torch.max(success_rewards[region_mask])
            if best_reward > self.region_best_episode_reward[region_id]:
                self.region_best_episode_reward[region_id] = best_reward

        mastery_target = max(int(self.cfg.region_mastery_successes), 1)
        while (
            self.active_region_id < self.total_regions
            and int(self.region_success_counts[self.active_region_id].item()) >= mastery_target
        ):
            self.region_mastered[self.active_region_id] = True
            self.active_region_id += 1

        if self.active_region_id >= self.total_regions:
            self.active_region_id = self.total_regions - 1

        self._write_region_mastery_snapshot()

    def _write_region_mastery_snapshot(self):
        log_dir = getattr(self.cfg, "log_dir", None)
        if not log_dir:
            return

        out_path = Path(log_dir) / "region_mastery.csv"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["region_number,success_count,best_episode_reward,mastered,active\n"]
        for region_id in range(self.total_regions):
            best_reward = self.region_best_episode_reward[region_id]
            best_value = "" if not torch.isfinite(best_reward) else f"{float(best_reward.item()):.6f}"
            lines.append(
                ",".join(
                    [
                        str(region_id + 1),
                        str(int(self.region_success_counts[region_id].item())),
                        best_value,
                        "1" if bool(self.region_mastered[region_id].item()) else "0",
                        "1" if region_id == self.active_region_id else "0",
                    ]
                )
                + "\n"
            )
        out_path.write_text("".join(lines), encoding="utf-8")
        self.region_mastery_snapshot_writes += 1

    def _update_markers(self, success: torch.Tensor | None = None):
        if not hasattr(self, "target_markers"):
            return
        target_pos_w = self.target_pos + self.scene.env_origins
        self.target_markers.visualize(target_pos_w)
        if success is None:
            success_pos_w = target_pos_w
        else:
            success_pos_w = target_pos_w.clone()
            success_pos_w[~success] = torch.tensor((0.0, 0.0, -10.0), device=self.device)
        self.success_markers.visualize(success_pos_w)
