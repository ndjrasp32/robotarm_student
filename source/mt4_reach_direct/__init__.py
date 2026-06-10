import gymnasium as gym

from .mt4_reach_env import MT4ReachEnv, MT4ReachEnvCfg
from .mt4_mars_twin_env import (
    MT4MarsTwinEnv,
    MT4MarsTwinPickEnvCfg,
    MT4MarsTwinPlaceEnvCfg,
    MT4MarsTwinPullEnvCfg,
    MT4MarsTwinPushEnvCfg,
    MT4MarsTwinStackEnvCfg,
)
from .mt4_coordinate_curriculum_env import (
    MT4CoordinateCurriculumEnv,
    MT4CoordinatePlaneEnvCfg,
    MT4CoordinateSphereEnvCfg,
    MT4CoordinateVolumeEnvCfg,
    MT4CoordinateWorkspaceEntryEnvCfg,
)
from . import agents

gym.register(
    id="Isaac-MT4-Simplified-Reach-Direct-v0",
    entry_point=f"{__name__}.mt4_reach_env:MT4ReachEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": MT4ReachEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:MT4ReachPPORunnerCfg",
    },
)

_MARS_TWIN_TASKS = {
    "Isaac-MT4-Mars-Twin-Pick-Direct-v0": MT4MarsTwinPickEnvCfg,
    "Isaac-MT4-Mars-Twin-Place-Direct-v0": MT4MarsTwinPlaceEnvCfg,
    "Isaac-MT4-Mars-Twin-Stack-Direct-v0": MT4MarsTwinStackEnvCfg,
    "Isaac-MT4-Mars-Twin-Push-Direct-v0": MT4MarsTwinPushEnvCfg,
    "Isaac-MT4-Mars-Twin-Pull-Direct-v0": MT4MarsTwinPullEnvCfg,
}

for task_id, cfg_cls in _MARS_TWIN_TASKS.items():
    gym.register(
        id=task_id,
        entry_point=f"{__name__}.mt4_mars_twin_env:MT4MarsTwinEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": cfg_cls,
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:MT4ReachPPORunnerCfg",
        },
    )

_COORDINATE_CURRICULUM_TASKS = {
    "Isaac-MT4-Coordinate-Workspace-Entry-Direct-v0": MT4CoordinateWorkspaceEntryEnvCfg,
    "Isaac-MT4-Coordinate-Plane-Direct-v0": MT4CoordinatePlaneEnvCfg,
    "Isaac-MT4-Coordinate-Volume-Direct-v0": MT4CoordinateVolumeEnvCfg,
    "Isaac-MT4-Coordinate-Sphere-Direct-v0": MT4CoordinateSphereEnvCfg,
}

for task_id, cfg_cls in _COORDINATE_CURRICULUM_TASKS.items():
    gym.register(
        id=task_id,
        entry_point=f"{__name__}.mt4_coordinate_curriculum_env:MT4CoordinateCurriculumEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": cfg_cls,
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:MT4CoordinatePPORunnerCfg",
        },
    )
