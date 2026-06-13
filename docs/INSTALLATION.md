# Installation and Distribution

Academic Coach is distributed in a few different ways because AI agents do not share one universal skill/plugin format.

## Why some skills use `npx` and others use `git clone`

In practice, the market has converged on two broad installation styles:

1. Native or semi-native installer flow
   - Examples: Claude Marketplace, agent-specific plugin registries, `npx ...`, `npm install -g ...`, dedicated CLIs
   - Best when the project ships templates, manifests, and agent-specific install logic
   - Good for one-command installs across many agents

2. Source-repo / clone / manual import flow
   - Examples: `git clone ...`, copy a prompt/skill directory, vendor files into an existing agent workspace
   - Best when the project is markdown-first, tool-agnostic, or needs human inspection and adaptation
   - Good for protocol-heavy skills that include multiple linked files

Academic Coach currently uses a hybrid approach:
- native repository-tap install for Hermes
- manual clone/copy install for other agents and custom workflows

It intentionally does not ship an `npx` installer yet, because its canonical artifact is a multi-file skill with references and templates, not a single prompt file.

## Supported Distribution Modes

### 1. Hermes Agent — custom repository tap (recommended)

This GitHub repository itself is the tap source. It includes a Hermes tap-compatible layout under:

- `skills/note-taking/academic-coach/`

Install from the repo as a custom skill source:

```bash
hermes skills tap add CoreDwan/Academic-Coach
hermes skills search academic-coach --source CoreDwan/Academic-Coach
hermes skills install CoreDwan/Academic-Coach/academic-coach
```

Then verify:

```bash
hermes skills list | grep academic-coach
```

### 2. Hermes Agent — manual clone/copy

If you prefer manual installation or want to inspect the files before installing:

```bash
git clone https://github.com/CoreDwan/Academic-Coach.git
mkdir -p ~/.hermes/skills/note-taking
cp -R Academic-Coach/skills/note-taking/academic-coach ~/.hermes/skills/note-taking/
```

Then start a fresh Hermes session and load/use the skill.

### 3. Hermes Agent — direct source inspection

If you want to review the raw protocol before installing:

- `SKILL.md`
- `references/`
- `templates/`
- `docs/`

The root of this repo is the human-facing source tree.
The mirrored `skills/note-taking/academic-coach/` subtree is the installable Hermes package layout.

### 4. Other agents — clone and adapt manually

For agents like Claude Code, Codex CLI, Cursor, Continue, or custom in-house agents, there is no universal skill standard yet.

Recommended workflow:

```bash
git clone https://github.com/CoreDwan/Academic-Coach.git
cd Academic-Coach
```

Then adapt the following files into the target agent's skill/custom-instructions system:
- `SKILL.md` — primary protocol
- `references/` — init questionnaire, command help, review schemas
- `templates/` — managed study-system file templates
- `docs/` — operator guidance and bootstrap rules

When another agent only supports one markdown instruction file, start with `SKILL.md` and keep the rest of the repo nearby as reference material.

## Agent Compatibility Notes

### Hermes
- best-supported runtime today
- supports linked skill files, persistent memory, cron jobs, and long-lived course workflows
- pseudo-command patterns like `academic-coach init` fit Hermes well

### Claude Code / Cursor / Codex / Continue / similar agents
- can reuse the protocol conceptually
- installation is usually manual because each agent has a different folder structure and trigger model
- some agents prefer slash commands, some prefer auto-activation, some prefer project-level custom instructions

### Why this repo does not promise one-click install everywhere

Unlike a purely presentational skill, Academic Coach depends on:
- linked templates
- linked references
- a consistent persistent-state model
- filesystem write behavior
- optional scheduling behavior

That means the skill is portable, but not yet uniformly packageable across every agent with one command.

## Recommended Open-Source Consumption Paths

If you are evaluating or adopting this project:

1. Read `README.en.md` or `README.zh-CN.md`
2. Read `docs/OPERATOR_GUIDE.md`
3. If you use Hermes, install via repository tap
4. If you use another agent, clone the repo and adapt `SKILL.md` + linked assets manually

## Future Packaging Directions

Possible future additions:
- agent-specific install wrappers
- a dedicated cross-agent installer CLI
- marketplace manifests for more platforms
- prebuilt distribution bundles for non-Hermes agents
