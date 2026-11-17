# zhangtianping-agent-skills

中文名：掌天瓶 Agent Skills

这是一个面向 Codex、Claude Code、IDE 扩展及其他 agent 客户端的 Agent Skills 项目，展示可复用的工作流设计、脚本工具和跨客户端组织方式。

项目包含通用技能、客户端专用技能、参考资料和配套脚本。欢迎查看、使用和改进；使用前请阅读各技能目录中的说明与许可证。

## 命名由来

“掌天瓶”来自修仙语境里的长期积累、催生灵药、慢慢滚雪球的意象。

Agent skills 也是类似的东西：每个 skill 都是一枚可复用的灵药、一块玉简，记录某类任务的做法、边界、工具和经验。它们平时安静地放在瓶中，用到时被 Codex 或其他 agent 取出，帮助我少踩一次坑、少重复一次流程。

所以这个仓库叫 `zhangtianping-agent-skills`：

- `zhangtianping`：掌天瓶，表示长期收纳、沉淀、增益。
- `agent-skills`：明确告诉未来的我，这里不是普通笔记，而是给 agent / IDE / 自动化工具调用的 skills。

一句话定位：

> 个人 Agent Skills 灵药库：统一托管 Codex、IDE、Claude / cc-switch 等多端可复用技能。

## 目录结构

```text
skills/
  shared/   # 尽量跨客户端通用的 skills
  codex/    # Codex 专用或强依赖 Codex 能力的 skills
  claude/   # Claude / cc-switch / Claude Code 专用 skills
adapters/   # 软链接、同步、检查脚本
docs/       # 设计说明、迁移记录、客户端差异说明
registry.md # skill 清单和来源记录
```

## 使用原则

1. 每个技能以本仓库中的版本为准，避免多个客户端目录中的副本逐渐分叉。
2. 通用 skill 优先放进 `skills/shared`。只有确实依赖某个客户端能力时，才放进 `skills/codex` 或 `skills/claude`。
3. 每个 skill 都要有清晰的 `SKILL.md`，其中 `name` 和 `description` 要能让 agent 判断什么时候该用它。
4. 涉及密钥、账号、token、cookie 的内容不要写进 skill。需要时只写 1Password / 环境变量 / secret reference 的读取方式。
5. 新增或迁移 skill 后，在 `registry.md` 记录用途、适用客户端、来源和迁移状态。

## Codex 推荐接入方式

Codex 会读取用户级 skills 目录：

```text
~/.agents/skills
```

可以将技能目录软链接到客户端技能目录。先设置仓库根目录，再运行：

```bash
REPO_DIR="/path/to/zhangtianping-agent-skills"
ln -s "$REPO_DIR/skills/shared/example-skill" "$HOME/.agents/skills/example-skill"
```

Codex App、Codex CLI 和 Codex IDE extension 都可以通过这个用户级目录发现同一份 skill。

## cc-switch / Claude 推荐接入方式

cc-switch 可以作为分发或同步层，但这个仓库仍然是唯一真源。

如果某个客户端只能读取固定目录，就从这里软链接或复制过去。不要把 cc-switch 的内部存储当作长期维护位置。

## 项目结构

`skills/shared` 收录跨客户端技能，`skills/codex` 收录 Codex 工作流，`adapters` 用于客户端接入，`docs` 记录项目设计与兼容性说明。

