# Resume Bullets

## 中文简历版本

项目名称：ANYmal-C 四足机器人复杂地形导航迁移

项目描述：

基于 Isaac Lab 与 MotrixLab 完成 ANYmal-C 四足机器人导航任务迁移，将平坦地形导航任务适配至复杂地形场景，接入 HeightScan 高度感知策略，并基于 PPO 训练日志分析学习率震荡导致的策略不稳定问题。

项目亮点：

- 基于 Isaac Lab 将 ANYmal-C 导航任务由 `AnymalCFlatEnvCfg` 迁移至 `AnymalCRoughEnvCfg`，适配复杂地形仿真场景。
- 接入 HeightScan 高度扫描观测，并加载 `ANYmal-C/HeightScan/policy.pt` 预训练 locomotion policy，提升复杂地形通过能力。
- 在 MotrixLab 中配置 `anymal_c_navigation_rough` 任务，整理训练、评估脚本和实验运行结果。
- 分析 PPO 训练中自适应学习率从 `2e-4` 震荡衰减至 `2e-5` 的过程，定位 episode length 波动来源。
- 提出线性学习率衰减、降低初始学习率等优化方案，提高短步数训练下的策略稳定性。

## English Resume Version

Project: ANYmal-C Rough Terrain Navigation Transfer

Description:

Migrated the ANYmal-C quadruped navigation task from flat terrain to rough terrain using Isaac Lab and MotrixLab, adapted a HeightScan-based low-level policy, and analyzed PPO training instability caused by adaptive learning-rate oscillation.

Highlights:

- Migrated ANYmal-C navigation from `AnymalCFlatEnvCfg` to `AnymalCRoughEnvCfg` for rough-terrain simulation.
- Integrated HeightScan observations and a pretrained ANYmal-C locomotion policy for terrain-aware control.
- Configured the `anymal_c_navigation_rough` task in MotrixLab and organized training/evaluation scripts.
- Analyzed PPO learning-rate oscillation from `2e-4` to `2e-5` and connected it to episode-length instability.
- Proposed linear learning-rate decay and lower initial learning rates to improve training stability in short runs.

## 简历单行版

基于 Isaac Lab / MotrixLab 完成 ANYmal-C 四足机器人复杂地形导航迁移，适配 HeightScan 感知策略并分析 PPO 学习率震荡问题，提出训练稳定性优化方案。
