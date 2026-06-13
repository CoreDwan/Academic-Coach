# Academic Coach

Academic Coach 是一个可复用的学科助教协议，用于长期课程学习、考试准备，以及跨会话持续维护学习状态。

当前结论：它现在已经可以用了，但它是 skill protocol，不是 Hermes 原生 slash command。

## 它是什么

Academic Coach 的核心思路，是把一门课当成“持续维护的学习系统”，而不是一次性问答。

它现在支持：
- 通过这个 GitHub 仓库作为 Hermes custom tap 安装
- 教材、PPT/PPTX、PDF、笔记、图片、实验报告、作业、历年卷等混合资料
- 多轮学习进度维护
- 每轮只处理一个知识点
- 错题记录、间隔复习、考试模式
- Obsidian 或 external-markdown 工作区
- `chat` / `doc` / `hybrid` 三种交互模式

## Hermes 快速安装

```bash
hermes skills tap add CoreDwan/Academic-Coach
hermes skills install CoreDwan/Academic-Coach/academic-coach
hermes skills list
```

如果不是 Hermes，或者你想手动适配其他 agent，就直接 clone 仓库并从 `SKILL.md` 开始。

## 简要使用说明

### 1. 调用 skill
先启动 Hermes，再加载或触发 `academic-coach`。

常用入口：
- 先进入 Hermes，然后输入 `/skill academic-coach`
- 或者启动时直接预加载：`hermes -s academic-coach`

你可以用自然语言，也可以用伪命令形式：
- `academic-coach help`
- `academic-coach init`
- `academic-coach continue`
- `/academic-coach review`
- `use academic-coach to help me study digital electronics`

### 2. 初始化课程
当你想为某门课建立长期维护的学习系统时，用：
- `academic-coach init`

init 阶段会先确认这些信息，再创建文件：
- 课程名称
- 教学/输出语言
- 工作区模式（`obsidian` / `external-markdown`）
- 交互模式（`chat` / `doc` / `hybrid`）
- 目标文件夹
- 当前已有资料
- 考试时间与当前目标

### 3. 日常使用
初始化后，主要用这些命令：
- `academic-coach status`：看当前进度和下一步建议
- `academic-coach continue`：讲一个知识点
- `academic-coach review`：做一轮间隔复习
- `academic-coach weak`：专攻薄弱点
- `academic-coach exam`：进入模拟考试模式
- `academic-coach audit`：检查学习系统是否漂移或不一致

### 4. 还没 init 也能开始
如果你一上来就说 `continue` / `review`，而当前还没有现成的 study-system，Academic Coach 不应该伪造状态。

它应该进入 bootstrap：
- 先追问最小必要信息
- 判断是 full init 还是 lightweight bootstrap
- 必要时只创建部分文件
- 先支持你开始一次真实学习任务

## 使用注意

- 这是 custom tap，不是 Hermes 官方内置 skill。
- 可以用中文、英文、中英双语或你指定的语言教学。
- 受管理学习文件使用大写英文文件名。
- 支持 cron 提醒，但创建/修改 schedule 之前仍应确认。
- 它更适合“长期课程助教”，不是随手问一句就结束的临时问答。

## 进一步阅读

如果你要看协议内部设计，优先读：
- `SKILL.md`
- `docs/COMMAND_AND_TARGET_MODEL.md`
- `docs/INIT_SCAFFOLDING_SPEC.md`
- `docs/DOC_INTERACTION_PROTOCOL.md`
- `docs/INSTALLATION.md`
