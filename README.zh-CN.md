# Academic Coach

Academic Coach 是一个可复用的学科助教协议，用于长期课程学习、考试准备，以及跨会话持续维护学习状态。

这个仓库从设计上就是多语言的：
- 协议本身可以用中文、英文、中英双语或用户指定的其他语言教学
- 在 `academic-coach init` 阶段，agent 必须明确确认后续的 teaching/output language
- 如果更利于理解，术语可以保留双语

当前状态：
- 以 protocol 为核心
- 是 pure skill workflow，不是 Hermes 原生 slash command
- 已支持通过这个 GitHub 仓库做 Hermes custom tap 安装
- 默认支持 Obsidian 工作区，也支持用户选择 external markdown workspace
- init 时必须明确 `workspace_mode`（`obsidian` / `external-markdown`）
- 支持教材、PPT/PPTX、PDF、笔记、图片、实验报告、作业、历年卷等混合资料

核心思路：
Academic Coach 把一门课当成“持续维护的学习系统”，而不是一次性问答。

Hermes 快速安装：
```bash
hermes skills tap add CoreDwan/Academic-Coach
hermes skills install CoreDwan/Academic-Coach/academic-coach
```

手动 clone/copy 和其他 agent 的适配方式见 `docs/INSTALLATION.md`。

仓库结构：
- `SKILL.md` — 主协议定义
- `templates/` — 可复用 markdown/json 模板
- `references/` — 初始化问卷、cron prompt patterns 等操作参考
- `docs/` — 属于公开协议的一部分的操作/说明文档

受管理的 study-system 文件：
必需：
- `COURSE_OVERVIEW.md`
- `PROGRESS.md`
- `KNOWLEDGE_TREE.md`
- `WEAK_POINTS.md`
- `MISTAKES.md`
- `EXAM_FOCUS.md`
- `REVIEW_SCHEDULE.md`
- `SYLLABUS_ASSETS.md`
- `KNOWLEDGE_REGISTRY.json`

推荐但可选：
- `STATUS.md`
- `TEACHING_LOG.md`
- `EXAM_SIMULATIONS.md`
- `COURSE_CONFIG.json`

命令协议：
- `academic-coach help`
- `academic-coach init`
- `academic-coach status`
- `academic-coach continue`
- `academic-coach review`
- `academic-coach weak`
- `academic-coach plan`
- `academic-coach exam`
- `academic-coach sync`
- `academic-coach mistakes`
- `academic-coach schedule`
- `academic-coach audit`

重要 bootstrap 规则：
如果用户在一个还没有现成 study-system 的工作区里，直接使用非 `init` 命令，或者直接自然语言触发 academic-coach，请不要伪造状态，而应进入 implicit bootstrap gate。

Lightweight bootstrap：
如果用户在全新工作区里需要“立刻开始”，但现有证据还不足以支撑完整初始化，可以使用 lightweight bootstrap。
它应该：
- 先确认最小必要上下文
- 不凭空生成完整知识树或考试重点排名
- 按需只创建最小持久化文件
- 允许先执行一次即时 teaching/review/exam 任务
- 明确把当前工作区标记为 partially initialized

设计约束：
- 每轮只讲一个知识点
- 必须等用户回答后才能继续
- 如果 teaching/output language 未知，必须在 init 时确认
- 受管理文件名使用大写英文
- cron 相关改动必须先确认
- 不伪造掌握度、不伪造覆盖范围、不虚构证据

另见：
- `docs/INSTALLATION.md`
- `docs/OPERATOR_GUIDE.md`
- `docs/INIT_CHECKLIST.md`
- `docs/INIT_RESPONSE_SKELETON.md`
- `docs/COMMAND_ROUTING_MATRIX.md`
- `docs/MINIMAL_WORKFLOW.md`
- `docs/AUDIT_SPEC.md`
