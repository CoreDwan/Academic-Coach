# Packaging and Distribution

Use this note when maintaining the public Academic Coach repository or exporting the skill for reuse.

## Distribution patterns seen in the market

Across current agent ecosystems, skill distribution usually falls into three buckets:

1. Native marketplace / registry
   - Examples: Claude Marketplace, Hermes skills hub/taps
   - Best when the platform has a first-class install surface

2. CLI / package-manager installer
   - Examples: `npx ...`, `npm install -g ...`, dedicated installer CLIs
   - Best when a project needs to generate platform-specific files for many agents

3. Source repo / manual clone / copy
   - Examples: `git clone`, copying a skill folder into an agent-specific directory, vendoring prompt files into project instructions
   - Best when the skill is markdown-first, multi-file, or still evolving quickly

## Recommended Academic Coach packaging

Academic Coach currently fits a hybrid model:
- Hermes: repository tap install
- Other agents: manual clone/copy/adapt

Reason: the canonical artifact is a multi-file protocol with linked references, templates, and persistent-state assumptions. It is not just a single prompt file.

## Hermes repository tap layout

If the repo is meant to be installable via Hermes custom skill taps, mirror the installable asset tree under:

- `skills/note-taking/academic-coach/`

That subtree should contain:
- `SKILL.md`
- `references/`
- `templates/`

Recommended install flow for users:

```bash
hermes skills tap add CoreDwan/Academic-Coach
hermes skills install CoreDwan/Academic-Coach/academic-coach
```

## Manual install fallback

For users who want to inspect files first, manual clone/copy remains valid:

```bash
git clone https://github.com/CoreDwan/Academic-Coach.git
mkdir -p ~/.hermes/skills/note-taking
cp -R Academic-Coach/skills/note-taking/academic-coach ~/.hermes/skills/note-taking/
```

## Public README structure preference

For public-facing repos, prefer:
- `README.md` as a compact preview/entry page
- `README.en.md`, `README.zh-CN.md`, or other language-specific files for full docs
- top-of-page links in `README.md` to those language docs, plus installation/license links

Avoid using one mixed bilingual README as the primary long-form document when the repo is intended for public reuse. Separate language documents are easier to scan, link, and maintain.

## When not to promise one-click cross-agent install

Do not oversell `npx`-style installation unless the project really ships and maintains:
- agent-specific file generation
- stable multi-platform install logic
- upgrade/uninstall behavior
- compatibility guarantees across agents

For protocol-heavy skills, a clear manual path is better than a fake universal installer.
