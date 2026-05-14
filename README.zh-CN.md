<div align="center">

# ANYmal-C 复杂地形导航迁移

### 四足机器人强化学习 · 仿真任务迁移 · PPO 训练稳定性分析

[English](README.md) · [实现文档](docs/task2-implementation.md) · [训练分析](docs/training-analysis.md) · [简历描述](docs/resume-bullets.md)

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Isaac Lab](https://img.shields.io/badge/Isaac%20Lab-Robotics%20Simulation-76B900)
![MotrixLab](https://img.shields.io/badge/MotrixLab-RL%20Training-F97316)
![PPO](https://img.shields.io/badge/Algorithm-PPO-7C3AED)
![Task](https://img.shields.io/badge/Task-Rough%20Terrain%20Navigation-0F766E)

<br />

![ANYmal-C rough terrain preview](media/anymal_rough_terrain_preview.gif)

</div>

## 问题

四足机器人在平地上可以稳定行走，但面对**复杂地形（碎石、斜坡、起伏地面）**，仅靠本体状态和速度命令远远不够。机器人需要感知脚下地形的高度变化，才能调整步态保持稳定。

本项目的目标：将 ANYmal-C 四足机器人的导航任务从**平坦地形迁移到复杂地形**，使其具备地形感知能力，并分析 PPO 训练中的稳定性问题。

> 核心挑战不是从零训练一个策略，而是在现有仿真框架（Isaac Lab / MotrixLab）下完成**任务迁移、策略适配和训练分析**——更贴近真实工程场景。

## 效果

| 近景机器人 | 复杂地形全景 |
| --- | --- |
| ![robot closeup](media/robot_closeup.png) | ![rough terrain overview](media/rough_terrain_overview.png) |

| 导航目标标记 | 多环境评估 |
| --- | --- |
| ![navigation targets](media/navigation_targets.png) | ![multi env evaluation](media/multi_env_evaluation.png) |

完整演示视频：[media/anymal_c_rough_terrain_demo.mp4](media/anymal_c_rough_terrain_demo.mp4)

## 工作内容

### 环境适配

- 将 Isaac Lab 低层环境配置从 `AnymalCFlatEnvCfg`（平坦地形）替换为 `AnymalCRoughEnvCfg`（复杂地形）
- 在 MotrixLab 中新增 `anymal_c_navigation_rough` 任务，使用 height-field 生成起伏地形
- 保持导航任务接口（动作/观测空间）一致，实现配置级迁移

### 策略迁移

- 接入 HeightScan 高度扫描观测，使机器人能感知脚下地形起伏
- 加载预训练 `ANYmal-C/HeightScan/policy.pt` 低层 locomotion 策略
- 保持 12 维动作空间（关节位置控制）和 54 维观测空间接口

### 训练评估

- 组织并验证 MotrixLab 训练和评估脚本（4096 并行环境训练，64 环境评估）
- 训练过程可复现，训练命令见下方

### PPO 稳定性分析

通过分析训练日志，发现：

| 指标 | 观察结果 |
|------|---------|
| 学习率趋势 | 从 `2e-4` 震荡衰减至 `2e-5`，呈现自适应 KL 调整特征 |
| 2k–6k 步区间 | 学习率仍高于 `1e-4` 且波动明显，episode length 剧烈抖动 |
| 10k 步以后 | 学习率降至 `5e-5` 以下，策略更新更细，性能趋于稳定 |

**结论**：策略不是学不会，而是初步成型后被过大的自适应学习率反复扰动。

**优化建议**：线性学习率衰减替代自适应调整、初始学习率从 `2e-4` 降至 `1e-4` 或 `5e-5`。

详细分析见 [docs/training-analysis.md](docs/training-analysis.md)。

## 核心流程

```mermaid
flowchart LR
    A["Flat Terrain Navigation"] --> B["Rough Terrain Config"]
    B --> C["HeightScan Observation"]
    C --> D["Pretrained Low-level Policy"]
    D --> E["MotrixLab Training / Evaluation"]
    E --> F["PPO Stability Analysis"]
```

## 技术栈

| 模块 | 内容 |
| --- | --- |
| 机器人平台 | ANYmal-C 四足机器人 |
| 仿真框架 | Isaac Lab, MotrixLab, MotrixSim |
| 强化学习算法 | PPO（SKRL 实现） |
| 策略适配 | HeightScan 低层 locomotion 策略 |
| 训练工具 | SKRL, TensorBoard, Python |
| 任务类型 | Rough Terrain Navigation, Target Tracking, Yaw Alignment |

## Isaac Lab 关键改动

将平坦地形的低层配置替换为复杂地形配置，并加载 HeightScan 策略：

```python
from isaaclab_tasks.manager_based.locomotion.velocity.config.anymal_c.rough_env_cfg import (
    AnymalCRoughEnvCfg,
)

LOW_LEVEL_ENV_CFG = AnymalCRoughEnvCfg()

pre_trained_policy_action = mdp.PreTrainedPolicyActionCfg(
    asset_name="robot",
    policy_path=f"{ISAACLAB_NUCLEUS_DIR}/Policies/ANYmal-C/HeightScan/policy.pt",
    low_level_decimation=4,
    low_level_actions=LOW_LEVEL_ENV_CFG.actions.joint_pos,
    low_level_observations=LOW_LEVEL_ENV_CFG.observations.policy,
)
```

完整示例见 [examples/isaaclab_navigation_env_cfg_patch.py](examples/isaaclab_navigation_env_cfg_patch.py)。

## 训练与评估

```bash
# 训练（4096 并行环境）
bash scripts/train_anymal_c_navigation_rough.bash

# 评估（64 环境）
bash scripts/eval_anymal_c_navigation_rough.bash
```

原始 MotrixLab 命令：

```bash
uv run scripts/train.py --env anymal_c_navigation_rough --num-envs 4096
uv run ./scripts/play.py --env anymal_c_navigation_rough --num-envs 64
```

## 仓库结构

```text
.
├── README.md / README.zh-CN.md   # 中英文项目说明
├── docs/
│   ├── project-positioning.md     # 项目定位
│   ├── task2-implementation.md    # 实现细节
│   ├── training-analysis.md       # PPO 训练分析
│   └── resume-bullets.md          # 简历描述
├── examples/
│   └── isaaclab_navigation_env_cfg_patch.py  # 配置迁移示例
├── scripts/
│   ├── train_anymal_c_navigation_rough.bash
│   └── eval_anymal_c_navigation_rough.bash
└── media/                       # 演示截图和视频
```

## 简历摘要

> 基于 Isaac Lab 与 MotrixLab 完成 ANYmal-C 四足机器人复杂地形导航迁移，将平坦地形导航任务适配至 Rough Terrain 场景，接入 HeightScan 高度感知策略，并分析 PPO 训练中学习率震荡导致的策略不稳定问题，提出线性衰减和降低初始学习率等优化方案。

中英文完整简历描述见 [docs/resume-bullets.md](docs/resume-bullets.md)。

## 说明

本仓库是独立整理的作品集项目，重点展示机器人任务迁移、仿真框架适配、强化学习训练分析和工程文档化能力。上游仿真框架、机器人资产和相关工具归其原维护者所有。
