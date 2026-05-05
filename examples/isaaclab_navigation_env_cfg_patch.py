"""Isaac Lab navigation rough-terrain policy adaptation example.

This snippet documents the key Task 2 change: replacing the flat ANYmal-C
low-level locomotion environment with the rough-terrain HeightScan policy.
It is meant as a readable patch reference, not a standalone executable file.
"""

from isaaclab.utils.assets import ISAACLAB_NUCLEUS_DIR
from isaaclab_tasks.manager_based.locomotion.velocity.config.anymal_c.rough_env_cfg import (
    AnymalCRoughEnvCfg,
)

# The original navigation task used the flat-terrain low-level config.
# Rough terrain requires terrain-aware observations from the HeightScan policy.
LOW_LEVEL_ENV_CFG = AnymalCRoughEnvCfg()

pre_trained_policy_action = mdp.PreTrainedPolicyActionCfg(  # noqa: F821
    asset_name="robot",
    policy_path=f"{ISAACLAB_NUCLEUS_DIR}/Policies/ANYmal-C/HeightScan/policy.pt",
    low_level_decimation=4,
    low_level_actions=LOW_LEVEL_ENV_CFG.actions.joint_pos,
    low_level_observations=LOW_LEVEL_ENV_CFG.observations.policy,
)
