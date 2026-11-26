---
title: 文献综述Skill选型、安装与真实测试报告
lang: zh-CN
mainfont: Noto Serif CJK SC
sansfont: Noto Sans CJK SC
monofont: Noto Sans Mono CJK SC
header-includes:
  - '\XeTeXlinebreaklocale "zh"'
  - '\XeTeXlinebreakskip=0pt plus 1pt'
---

# 结果与验证边界

已选择并安装 **K-Dense literature-review v1.11的建筑学适配版**，保留其七阶段工作流与三个实用脚本，增加标准库检索/导出适配及建筑LCA证据要求。未安装完整科研技能库或DeerFlow应用。来源、固定提交、许可证、依赖锁、文件哈希与小型真实试验均保存在现有spexialsun仓库的独立分支中。

本次试验取得60条Crossref记录，补充1条中文期刊记录，选取15篇覆盖性样本；15个DOI均注册成功，14篇由Crossref和OpenAlex交叉核验，中文1篇由期刊官网及PDF核验。完成2篇全文、12篇摘要或摘要片段阅读；另1篇仅题录，不用于结论综合。已输出文献矩阵、综述框架、BibTeX、RIS、CSL JSON及GB/T 7714—2015渲染题录。

**尚未完成宿主选择器与自动触发验证。** 当前云端executor技能服务返回空列表；另启Codex app-server的skills/list探测因只读状态目录失败，临时sqlite/log目录配置亦未使其启动。项目标准目录安装、显式读取SKILL和实际脚本工作流已验证；不把它们等同于桌面选择器发现、自然语言自动选择或新云端任务验证。用户可按使用指南用绝对路径显式调用。没有改动平台只读设置或用户账号。

# 候选检索与比较

2026年11月26日检索GitHub、官方openai/skills目录及可信开发者的原始仓库。GitHub连接器确认仓库身份；其返回的元数据不含Stars等完整字段，因此额外保存公开GitHub REST元数据、目录提交历史和近期Issues/PR摘要。原始对比数据见本目录三个仓库JSON。

| 候选及原始入口 | 仓库Stars / Forks | 仓库最近推送 / 技能最近提交 | 协议与维护者 | 适用性与限制 |
|---|---:|---|---|---|
| [K-Dense literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/literature-review) | 58,520 / 5,124 | 2026-11-23 / 2026-10-01 | MIT；K-Dense组织 | 七阶段检索、筛选、抽取、综合和核验；明确区分注册与论据支持，适合现有citation-management；需补建筑数据库与中文适配 |
| [DeerFlow systematic-literature-review](https://github.com/bytedance/deer-flow/tree/main/skills/public/systematic-literature-review) | 85,839 / 12,116 | 2026-11-26 / 2026-11-08 | MIT；ByteDance组织 | 轻量arXiv检索与跨论文综合；有APA/IEEE/BibTeX模板；该技能明确仅arXiv，材料期刊覆盖弱，默认路径及present_files等需适配Codex |
| [LitReviewSkill write-literature-review](https://github.com/Zsun79/LitReviewSkill/tree/main/skills/write-literature-review) | 31 / 5 | 2026-06-08 / 2026-06-08 | 仓库未声明可确认许可证；独立开发者 | OpenAlex种子检索、前后向引文扩展、筛选、排序、全文发现、知识图谱；流程细致，但授权不明、社区较小、维护间隔较长，未安装 |

以上计数为仓库级实时快照，既不是单个技能的评分，也不是科研结果准确率或活跃用户数。K-Dense近期有引用验证修复等PR（例如[#383](https://github.com/K-Dense-AI/scientific-agent-skills/pull/383)），DeerFlow近期有技能包校验及代理数据处理修复（例如[#8685](https://github.com/bytedance/deer-flow/pull/8685)）；这些证明维护活动，不能证明综述质量。LitReviewSkill可见一条已关闭引用格式PR；未取得可靠安装量、独立使用调查或正式准确率评测，均不编造。

官方 [openai/skills](https://github.com/openai/skills) 检索到了notion-research-documentation，主要面向Notion资料综合，不等于本任务所需的跨学术数据库文献综述；在本次官方目录快照中未发现同等用途的专门literature-review，未因为“官方”标签而替代科研适用性判断。

## 按需求综合评价

| 维度 | K-Dense | DeerFlow该技能 | LitReviewSkill |
|---|---|---|---|
| 完整方法 | 范围、筛选、质量与主题综合较完整 | 五阶段清楚，来源窄 | 迭代检索与引文追踪突出 |
| 检索执行 | 核心脚本主要后处理；需数据库客户端 | 自带arXiv客户端 | 自带OpenAlex等适配 |
| 核验/防幻觉 | DOI注册、Crossref元数据、明确论据支持仍需审阅 | 要求以摘要/全文为依据，但非完整DOI审计 | 强调仅用最终纳入集；未验证独立真实性审计 |
| 建筑学覆盖 | 可扩展Crossref/OpenAlex，方法可适配 | arXiv难代表建筑材料期刊 | OpenAlex有跨学科优势，中文仍需补充 |
| 成本依赖 | 核心requests；付费Parallel/OpenRouter均可选 | 单脚本低依赖；完整DeerFlow不必安装 | 网络、可选CORE服务、图形渲染；账号与配额需另核 |
| Codex兼容 | SKILL规范易适配、原始元数据含其他宿主字段 | 默认路径/工具名需改；不移植整个应用 | 标准SKILL结构，输出路径与流程需适配 |
| 安全/维护 | 固定SHA、MIT、最小安装后较易审查 | arXiv脚本含HTTP端点，安装前应改HTTPS并测试 | 授权不明为安装障碍；较少维护证据 |

最终选择K-Dense，理由是流程较完整、协议清楚、可与已下载的引用技能协同，且避免重复安装完整应用。选择的是成熟社区仓库中的工作流基础，**本地建筑适配器是新写的小型组件，尚无独立社区认可度**，不能把上游热度转移成它的质量背书。

# 安装、审查与配置

## 固定版本和位置

- 仓库：`/workspace/repos/spexialsun`。
- 分支：`codex/literature-review-20261126`。
- 核心：`.agents/skills/literature-review/SKILL.md`。
- 上游固定SHA：`c21d13b3cc2894680229ba9959a53281acb9200e`；技能声明v1.11，本地标记architecture-adaptation-1。
- MIT原始版权保留在技能目录LICENSE.md；上游原SKILL另存本报告目录，便于比较升级。
- Python3.12.14；requests2.34.2及certifi、charset-normalizer、idna、urllib3固定版本和哈希见requirements-literature.lock；隔离安装到仓库.venv。
- Pandoc、XeLaTeX为环境已有工具，检查可用；未新增系统级软件或全局Python包。
- GB/T 7714—2015顺序编码CSL来自citation-style-language/styles，固定SHA与CC-BY-SA-3.0许可链接见styles/source.json和CSL的rights字段。

## 审查范围与实际操作

1. 阅读项目README、context、AGENTS及技能管理规则，确认原工作区干净，创建独立分支，先运行原bootstrap。
2. 最新核对 [Codex官方Build skills](https://learn.chatgpt.com/docs/build-skills)：必需name/description、项目.agents/skills路径、按需加载与宿主发现分开处理。
3. 将候选下载到仓库外/tmp审查，固定完整提交，检查说明、脚本、许可证与网络目的地；未执行远端安装钩子或curl管道脚本。
4. K-Dense的去重脚本仅读写显式本地文件；DOI核验访问doi.org及api.crossref.org；PDF脚本以参数数组调用Pandoc，没有shell=True。未发现保留脚本中的动态eval、混淆执行、关闭TLS、删除系统数据或任意凭据收集。
5. 上游可选AI绘图代码会查找父目录.env并调用OpenRouter，超出本次最小流程；已从安装目录移除两份绘图脚本，重写本地SKILL以免引用不存在功能。未运行其付费接口。
6. 新增retrieve.py仅访问固定学术元数据服务，支持原始响应、时间、URL、哈希、导出量、限额和失败记录；OpenAlex可选密钥仅进入本服务Authorization头。新增export_review.py只导出审阅后的记录，不自动编造研究发现。
7. 增加建筑学质量字段、全文/摘要分层、61条筛选台账；将“原研究局限”与“审阅者判断”分列。未将已有六个下载技能全部再次安装或改写。
8. uv默认缓存只读，改用/tmp下的任务缓存；依赖仍装入项目虚拟环境。来源、许可证和每个技能文件哈希通过既有skills.py登记。

这是有范围的人工源码审查加针对性测试，不是恶意软件免疫保证或第三方安全认证。后续更新要重新审查，不能直接刷新哈希当作安全通过。

# 真实试验结果

主题为“竹木等可再生建筑材料在建筑低碳设计中的应用研究”。协议、检索日志和矩阵独立保存在projects/renewable-materials-review；详细中文研究结果见该目录review.md。

| 环节 | 已观察结果 |
|---|---|
| 关键词与查询 | 中英文关键词及概念布尔式；3个Crossref实际查询，3个OpenAlex查询；补充中文官网检索 |
| 数据库检索 | Crossref60条；OpenAlex关键词429；S2关键词429，原样记录 |
| 去重与筛选 | 60条去重后仍60；加中文1条共61；15条试验样本、13条题名范围排除、33条待筛 |
| 文献身份 | 15个DOI注册正常；英文14条Crossref与OpenAlex核对；中文1条出版社/PDF核对 |
| 日期冲突 | 2条网络首发与卷期年份差异，未静默改写或按DOI年份猜测 |
| 深度提取 | R13/R15两篇全文；12篇摘要/片段；R02仅题录，不贡献结论 |
| 分析输出 | 完整多字段CSV/JSON、摘要矩阵、主题综合、5个待检验研究方向、7节综述框架 |
| 导出 | 15篇BibTeX、RIS、CSL JSON、GB/T7714—2015真实citeproc渲染 |
| 计量/质量边界 | 没有双人最终筛选、正式偏倚工具评分、元分析或穷尽检索 |

最有价值的试验发现不是一个统一减碳百分比，而是三种边界必须分开：材料性能与碳表现、单位材料与整栋建筑、生物碳/回收信用与永久净减排。中文原文还暴露出钢参照来自外部文献换算的条件；若只读摘要，容易把建筑热工与情景差异误当材料的独立因果效应。

# 能力与限制

已实现问题驱动的中英文词扩展、分库查询记录、Crossref检索、OpenAlex身份核验、DOI注册、去重、纳排/待筛台账、阅读深度、建筑学分析矩阵、跨论文综合和多格式引用导出。关键词扩展、相关性与综述判断由Codex按技能完成，脚本不声称具备独立智能科研能力。

仍需人工及合法全文支持：数据库范围和配额、中文期刊覆盖、全部全文取得、作者结论定位、偏倚评价、撤稿/更正补检和正式投稿样式核查。没有宣称Web of Science、Scopus、CNKI、Google Scholar已接通。OpenAlex和S2关键词检索的限流意味着本次多源“发现”覆盖不足，即使逐条核验成功也不能抵消此限制。

本次未进行自动触发正反例的模型实测；描述明确将单篇审阅和普通网页问答排除，但这只是触发设计，不是已通过宿主分类测试。新任务持久性需要从GitHub检出后在该宿主再测。未连接用户Windows Zotero、未安装CiteSpace/VOSviewer，也未建立自动长期记忆服务。

# 调用、长期维护及成本

零基础步骤、提示词、账号配置、更新、卸载、回滚与扩展接口见docs/literature-review-guide.md。建议固定流程为“协议→检索→筛选→阅读→矩阵→综合→引用核验→持久化”，每轮使用新run目录，优先补充会影响设计决定的缺失证据。

当前真实试验没有使用额外付费API。若要提高OpenAlex稳定性，可在官方设置取得Key后存入云端秘密管理；S2、WoS/Scopus和CNKI的授权及操作步骤在指南单列。不要把密钥粘贴进聊天或公共仓库。

按照上游署名要求，软件说明引用已核验的开发者论文：Timothy Kassis, Vinayak Agarwal, Yuhuan He, Darshil Patel, Aubrey M. Brueckner. *Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*. 2026. [arXiv:2609.00065](https://arxiv.org/abs/2609.00065)。作者/题名由实时arXiv记录核对，证据在software-paper-verification.json；此软件文献单列，不计入15篇建筑材料样本。

Git提交与联网/离线验证的最终状态见本目录validation.json及项目context.md；报告不以成功下载或脚本退出码替代真实性和论据审阅。
