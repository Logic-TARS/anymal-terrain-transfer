# Task 2 Implementation Notes

## 任务目标

任务 2 包含两个主要部分：

1. 将 Isaac-navigation 任务的地形改为复杂地形。
2. 将 ANYmal-C 导航任务迁移到 MotrixLab，并完成训练与评估分析。

## Isaac Lab 侧修改

原任务使用平坦地形配置。复杂地形下，机器人如果仅依赖本体状态和速度命令，容易因为缺少地形高度信息而失稳。因此任务迁移需要同步修改底层环境配置和预训练策略。

关键改动：

- 将 `AnymalCFlatEnvCfg` 替换为 `AnymalCRoughEnvCfg`。
- 使用 rough-terrain 配置自带的 HeightScan 观测。
- 将预训练策略路径切换到 `ANYmal-C/HeightScan/policy.pt`。
- 保持低层动作接口为 `LOW_LEVEL_ENV_CFG.actions.joint_pos`。
- 保持低层观测接口为 `LOW_LEVEL_ENV_CFG.observations.policy`。

示例代码见 [../examples/isaaclab_navigation_env_cfg_patch.py](../examples/isaaclab_navigation_env_cfg_patch.py)。

## MotrixLab 侧修改

MotrixLab 中保留平坦地形任务，同时新增粗糙地形版本：

- `anymal_c_navigation_flat`
- `anymal_c_navigation_rough`

粗糙地形版本继承原 ANYmal-C 导航任务配置，仅替换场景文件：

```python
@registry.envcfg("anymal_c_navigation_rough")
@dataclass
class AnymalCEnvRoughCfg(AnymalCEnvCfg):
    """崎岖地形版本，指向粗糙地形场景文件。"""

    model_file: str = rough_model_file
```

`scene_rough.xml` 使用 height-field 地形：

```xml
<hfield name="hfield" file="../locomotion/go1/xmls/assets/heightmap.png" size="20 20 2.5 0.1"/>
<geom name="ground" pos="0 0 -1" type="hfield" hfield="hfield" material="groundplane"/>
```

## 动作与观测空间

ANYmal-C 导航任务使用 12 维动作空间，对应四足机器人的 12 个关节位置控制命令：

```text
Box(-1.0, 1.0, shape=(12,), dtype=float32)
```

观测空间为 54 维，包含本体状态、历史动作、速度命令和导航目标状态：

```text
Box(-inf, inf, shape=(54,), dtype=float32)
```

观测内容包括：

- base linear velocity
- base angular velocity
- projected gravity
- joint positions
- joint velocities
- previous actions
- velocity commands
- target position error
- target heading error
- arrival and stopping flags

## 训练与评估

训练命令：

```bash
uv run scripts/train.py --env anymal_c_navigation_rough --num-envs 4096
```

评估命令：

```bash
uv run ./scripts/play.py --env anymal_c_navigation_rough --num-envs 64
```

本仓库提供封装脚本：

- [../scripts/train_anymal_c_navigation_rough.bash](../scripts/train_anymal_c_navigation_rough.bash)
- [../scripts/eval_anymal_c_navigation_rough.bash](../scripts/eval_anymal_c_navigation_rough.bash)
