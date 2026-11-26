# 文献综述技能使用与维护

## 零基础开始

在Codex中选择仓库 spexialsun，工作目录为 `/workspace/repos/spexialsun`。新云端工作区先检出本次成果分支，运行 `bash scripts/bootstrap.sh`。项目技能位于 `.agents/skills/literature-review/SKILL.md`，会随Git保存；它不依赖Windows上的个人技能目录。

当前聊天已经读取技能并执行了真实工作流。当前云端Skill服务列表为空，另启本机app-server进行宿主发现探测被只读状态目录阻断，不能声称桌面技能选择器或自动选择已验证。即使选择器未显示，也可明确要求：

> 请读取 `/workspace/repos/spexialsun/.agents/skills/literature-review/SKILL.md`，按其中流程为我的课题开展综述。先给出研究问题和纳排标准，保存检索与证据记录，再开始综合。

在能够扫描项目技能的Codex宿主中，刷新/新开本仓库会话后可用 `$literature-review`。若未显示，先确认工作目录和分支，不要把“文件已保存”当成“宿主已发现”。本次没有改变平台只读配置。

## 推荐工作流程

研究问题与范围 → 中英文同义词和分库检索式 → 检索原始记录 → 去重和人工筛选 → 全文取得与阅读状态 → 分项证据与适用性评估 → 跨文献主题综合 → 引用核验 → 文稿/矩阵/题录保存 → 下一轮补检。

建议先做20—50条探索检索确定术语，正式综述另设协议、分页检索、独立复核和停止条件。不要直接将本次15篇样本扩写成正式系统综述。

## 可直接使用的提示词

**新项目：**

> 用 literature-review 研究“[主题]”。范围为[年份]、[中英文]、[研究类型]。先明确问题、功能比较基准、关键词、分库检索式和纳排标准；把原始记录、失败与限流、筛选理由和阅读深度保存到 projects/[项目名]/。严禁虚构文献，关键结论关联来源定位，区分原文结论与推断。未经全文核对不得生成全文细节。

**带PDF：**

> 读取我的PDF目录[私有路径]。先建立DOI和文件SHA256索引；按方法、数据、结果、作者局限及我的课题启示整理矩阵，每项给页码/图表。把未找到的项目写未核实，不向公共仓库提交全文。

**形成综述：**

> 基于已完成的证据矩阵，按研究问题综合方法、共识和争议。解释差异是否来自边界、功能单位、地区或质量。研究空白区分原文明确指出与当前样本推断；正文每个关键判断链接证据ID，导出BibTeX、RIS和GB/T 7714—2015题录。

**继续项目：**

> 读取 projects/[项目名]/context.md 和上次检索、筛选台账。只补检[日期/子问题]；保留旧记录，新增本次run目录，说明新增证据是否改变既有判断。

## 依赖和复现实例

基础为Python 3.10+。数据库适配、去重、矩阵及导出使用标准库；DOI核验使用隔离 `.venv` 内的 requests，直接和传递依赖锁在 requirements-literature.lock。当前Python为3.12.14。

```bash
cd /workspace/repos/spexialsun
UV_CACHE_DIR=/tmp/litreview-uv-cache uv venv .venv
UV_CACHE_DIR=/tmp/litreview-uv-cache uv pip sync --python .venv/bin/python requirements-literature.lock
bash scripts/bootstrap.sh
python3 scripts/test_literature_review.py
```

重跑检索使用SKILL.md里的命令，输出必须使用新的目录，如run-02。原始数据已保存，可以不联网重做导出：

```bash
python3 .agents/skills/literature-review/scripts/export_review.py \
  --records projects/renewable-materials-review/analysis/records.json \
  --annotations projects/renewable-materials-review/analysis/annotations.json \
  --output projects/renewable-materials-review/outputs-recheck
```

本机已有Pandoc与XeLaTeX，可选生成PDF。GB/T样式保存在styles/，由Pandoc citeproc真实渲染；不是手写列表冒充符合规范。正式投稿仍需按学校或期刊细则复核标点、作者转写与文献类型。

## 账号、成本和数据库边界

- **本次无需API Key，没有调用额外付费LLM。** 仍消耗Codex本身额度和计算资源。Crossref公开查询成功；匿名OpenAlex关键词检索429，而单DOI查询成功；Semantic Scholar检索429。
- **OpenAlex可选：** 在[官方账号设置](https://openalex.org/settings/api)创建账号并取得API Key；在云端Personal vault/HTTP secrets中设置 `OPENALEX_API_KEY`。不要发到聊天、写入Git或日志。当前适配器仅向api.openalex.org发送Authorization头，配置后在新run实测预算和限流，不能保证永久免费无限调用。
- **Semantic Scholar可选：** 按[官方API说明](https://www.semanticscholar.org/product/api)申请密钥；本次未安装持久S2客户端，后续审查后接入，密钥仅发给S2。
- **Google Scholar：** 无官方公开批量检索API；可人工补检和引文追踪。本次没有安装抓取库或绕过验证码。
- **arXiv：** 可作为预印本补充，不覆盖主要建筑材料期刊；预印本须与正式发表版本关联。
- **Web of Science / Scopus：** 需机构订阅及相应API/导出授权；网页访问权限不等于API权限。先由学校确认可用产品和批量导出条件，再提供合法RIS/BibTeX/CSV导出或配置授权；本次未接入。
- **CNKI：** 本次通过期刊自己的公开页面取得中文文献，不代表检索了CNKI。学校访问权限、下载和批量使用条款须分别确认；可先人工导出题录再导入，不保存学校账号或绕过访问控制。
- **OpenRouter / Parallel：** 未安装、未配置；可选付费绘图代码已从核心安装中移除，科研流程无需这些服务。

## 后续扩展接口

| 工作 | 保留接口 | 本次状态 |
|---|---|---|
| Zotero | DOI、BibTeX、RIS、独立Zotero item key字段 | 文件导出已验证；未连接Windows本机Zotero |
| 私有PDF | 文件SHA256、来源URL、页码和阅读状态 | 2篇公开PDF已读，未发布原文 |
| 中英文 | UTF-8 CSV/JSON、CSL literal作者、保留原文题名 | 中文论文及引用导出已测 |
| CiteSpace/VOSviewer | 题录稳定ID、后续补机构/关键词/被引参考文献 | 未安装；简化RIS不保证满足完整计量分析 |
| Python数据处理 | 结构化JSON、带BOM的UTF-8 CSV | 已导出、离线验证 |
| 长期项目接续 | context.md、追加式run目录、Git | 已实现文件持久化，不是自动记忆服务 |

## 更新、卸载和回滚

来源固定为K-Dense commit `c21d13b3cc2894680229ba9959a53281acb9200e`，本地适配标记architecture-adaptation-1。不要直接覆盖升级。新建分支、下载新SHA到临时目录，审查源码/许可证/依赖和差异，保留本地适配后运行登记、离线验证和一轮小型联网测试。上游原始SKILL与来源审计位于 docs/reports/literature-review-install/。

登记命令见 docs/skills.md；skills-lock.json是项目自己的哈希登记器，不是官方宿主安装清单。依赖更改重新生成带哈希锁文件。

卸载在分支中删除 `.agents/skills/literature-review` 并人工移除skills-lock对应项，更新AGENTS和说明，再提交。项目研究成果独立保留。回滚使用 `git revert <安装提交>` 或恢复技能和锁文件的一致版本，不强推、不覆盖他人成果。依赖环境可单独删除重建；不需要全局卸载Python包。
