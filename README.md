# 特朗普语料、处理阶段与文本结构化代码

本项目保存抓取基线、清洗和整理副本、语言学标注及历史代码。**这些版本不能直接相加为独立演讲数量。** 请选择需要的处理阶段，再下载相应材料。

GitHub：[Trump_compaign_speech_annotation](https://github.com/Mystery-W/Trump_compaign_speech_annotation)。本地 `D:\Trump_Text_Structuring` 只保留代码、编译缓存、说明和迁移清单。

## 1. 应该下载哪一份？

全部归档见 [2026-10-31 Release](https://github.com/Mystery-W/Trump_compaign_speech_annotation/releases/tag/corpus-archive-2026-10-31)。

| 使用目的 | 下载文件 | 包内入口 |
| --- | --- | --- |
| 从抓取文本重新筛选、清洗 | [trump-factbase-original.zip](https://github.com/Mystery-W/Trump_compaign_speech_annotation/releases/download/corpus-archive-2026-10-31/trump-factbase-original.zip) | `All/`；补充材料见 `Complement/`、`补充：一些演讲/` |
| 使用已经清洗的 CSV 或纯文本 | 同上 | `Trump Speech Study/cleaned_csv/` 或 `Trump Speech Study/txt/` |
| 使用已有语言学标注 | [trump-annotated-xml.zip](https://github.com/Mystery-W/Trump_compaign_speech_annotation/releases/download/corpus-archive-2026-10-31/trump-annotated-xml.zip) | 六个竞选阶段目录，共 599 份 XML；仓库根目录也保存同一批文件 |
| 查阅早期 2024 年集会语料和 MAT 分析 | [trump-rally-original-and-derived.zip](https://github.com/Mystery-W/Trump_compaign_speech_annotation/releases/download/corpus-archive-2026-10-31/trump-rally-original-and-derived.zip) | 按第 4 节区分原始输入、清洗文本和分析产物 |
| 查看处理逻辑或继续开发 | 无需下载语料 ZIP | GitHub 的 `code/`；本地同名子目录直接位于整理目录下 |

**`original.zip` 表示“旧备份包的原样归档”，不表示包内全部是原始语料。** 两个历史研究包同时包含输入、处理结果和辅助材料；此次保留原有组织，没有重新拆包。

## 2. “原始”和“已处理”的定义

| 类别 | 本项目中的含义 |
| --- | --- |
| 抓取基线／相对原始语料 | 从来源网站提取成 CSV/TXT 的文本，是后续处理的输入；不是原始网页、音视频，也不保证从未经过网站编辑或爬虫格式整理。 |
| 整理或筛选副本 | 按年份、类型、日期或研究条件组织的副本。正文可能未变，但范围或目录结构已经改变。 |
| 清洗／格式转换结果 | 发言人筛选、删除方括号内容、字符或空白处理、合并 TEXT 列、导出 TXT 等步骤的输出。 |
| 结构化／自动标注结果 | 段落—句子—词级 XML，以及词性、依存关系、情感或定量语言学指标；各版本的字段不同。 |
| 分析产物／辅助材料 | 统计表、图、测试文件、索引、映射表和失败日志，不应按独立演讲计数。 |

下文数量来自归档逐文件清单，表示文件数，**不是去重后的独立演讲数**。相同内容的判断依据 SHA-256；处理步骤依据留存代码。尚未确认的历史步骤单独注明。

## 3. Factba.se 历史包

`trump-factbase-original.zip` 共 16,921 个文件条目。

| 包内路径 | 数量 | 类别与说明 |
| --- | ---: | --- |
| `All/` | 4,169 CSV | 抓取基线，包含多种活动类型，不全是竞选演讲，也不能默认每一行都是特朗普发言。爬虫提取 `ADDRESS`、`DATE`、`TITLE`、`LINK`、`SPEAKER`、`DURATION`、`TEXT` 等字段，实际列以文件为准。 |
| `Complement/` | 380 CSV + 1 TXT | 另一次补充抓取及辅助文本。留存爬虫允许在未取得正文时写入空 `TEXT` 行，使用前须检查完整性；不能默认全部有效或已经并入 `All/`。 |
| `补充：一些演讲/` | 15 文件 | 补充材料、拆分代码和 `Separated/` 下的 12 个文件，属于混合目录。 |
| `sort_by_year/` | 4,169 CSV | 按年份整理的副本；所有文件哈希均能在 `All/` 中找到相同内容。 |
| `sort_by_category/` | 4,169 CSV | 按类型整理的副本；所有文件哈希均能在 `All/` 中找到相同内容。不要与上述两组累加统计规模。 |
| `Trump Speech Study/csv_raw/` | 625 CSV | 三个研究时段的筛选输入。留存代码按标题含 `Speech` 和日期范围从 `All/` 复制；实际 617 份与 `All/` 内容相同，其余 8 份的来源或修改过程尚未确认。 |
| `Trump Speech Study/cleaned_csv/` | 625 CSV | 已清洗语料。代码含多个版本：只保留 `Donald Trump` 发言、删除方括号内容；另有字符白名单和空白规范化版本。缺少逐文件执行记录，不能保证全部采用同一版本。 |
| `Trump Speech Study/txt/` | 625 TXT | 从清洗 CSV 的 `TEXT` 列合并并规范化空白得到的纯文本，其他元数据列不随正文保留。 |
| `Trump Speech Study/txt_short/` | 625 TXT + 1 CSV | 根据留存代码，仅缩短文件名并复制正文，**不是截短演讲文本**。`filename_mapping.csv` 保存长短文件名映射。 |
| `Trump Speech Study/txt_short_final/` | 546 TXT | 历史后续版本，筛选、删除或修改规则尚未完整确认；不能仅凭 `final` 将其视为统一推荐版本。 |
| `Trump Speech Study/txt_short_sampled/` | 900 TXT、19 CSV、31 PNG | 历史派生文本与统计产物。目录名指向抽样用途，但抽样单位、随机种子、重复抽取情况和版本对应关系尚未确认；900 个 TXT 不代表 900 场独立演讲。 |
| `index and err/`、`R_Statistics/`、笔记本等 | 其余条目 | 索引、错误记录、统计代码和研究辅助文件，不要整体当作正文导入。 |

留存代码表达的处理顺序如下；这不等于所有文件都已逐一复现：

```text
All/（抓取基线）
  ├─ sort_by_year/、sort_by_category/（整理副本）
  └─ 标题和日期筛选 → csv_raw/
       └─ 发言人筛选、文本清洗 → cleaned_csv/
            └─ 合并 TEXT 列 → txt/
                 └─ 仅缩短文件名 → txt_short/

txt_short_final/、txt_short_sampled/：保留历史产物，后续处理链尚不完整。
```

依据：[Codes.ipynb](https://github.com/Mystery-W/Trump_compaign_speech_annotation/blob/main/code/factbase_legacy/Trump%20Speech%20Study/Codes.ipynb) 和 [Crawler.ipynb](https://github.com/Mystery-W/Trump_compaign_speech_annotation/blob/main/code/factbase_legacy/Crawler.ipynb)。

## 4. 早期 Rally 包

`trump-rally-original-and-derived.zip` 共 886 个文件条目。

| 包内路径 | 数量 | 类别与说明 |
| --- | ---: | --- |
| `General Election rallies (June 2024–November 2024)/` | 75 文件 | 早期集会文本的清洗输入，是此处理链中相对原始的一组；不据此推断与 Factba.se 包不存在重叠。 |
| `cleaned/` | 75 文件 | `clean.py` 指向的输出目录：删除方括号及其内部内容。 |
| `cleaned_trump_speech/` | 75 文件 | 历史清洗版本，与 `cleaned/` 的具体处理差异尚未完整确认。 |
| `cleaned_trump_speech_copy/` | 236 文件 | 混合目录：根部有 75 份文本，另有 MAT/ST 文件及统计结果，不能整体当作独立语料集。 |
| `xml/` | 75 XML | 较早的结构化结果。留存 `annotation.py` 使用 Stanza 分句分词，保存地点／日期元数据和段落—句子—词层级；不等于下节 599 份 XML 的完整语言学标注。 |
| `xml_annotated/` | 1 日志 | **只有 `failed_files.log`，没有标注 XML。** |
| `MAT file/` | 321 文件 | MAT/ST 处理版本、统计结果及相关副本，属于派生分析材料。 |
| `Test/` | 26 文件 | 测试输入和 MAT/ST 输出，不能默认纳入正式样本。 |
| `new.xlsx`、`Trump General Election Rallies.xlsx` | 2 文件 | 历史工作表，具体列和用途需查看确认，不按演讲篇数计数。 |

依据：[clean.py](https://github.com/Mystery-W/Trump_compaign_speech_annotation/blob/main/code/rally_legacy/clean.py) 和 [annotation.py](https://github.com/Mystery-W/Trump_compaign_speech_annotation/blob/main/code/rally_legacy/annotation.py)。

## 5. 599 份 XML：已处理的语言学标注

`trump-annotated-xml.zip` 和仓库根目录六个演讲目录保存同一批文件。ZIP 是下载副本，不是另一批语料。

| 目录 | 文件数 |
| --- | ---: |
| `General_Election_Season_2016 (2016-06-10 to 2016-11-07)` | 160 |
| `General_Election_Season_2020 (2020-06-20 to 2020-11-02)` | 73 |
| `General_Election_Season_2024 (2024-06-06 to 2024-11-04)` | 90 |
| `Primary_Season_2016 (2015-06-16 to 2016-06-03)` | 144 |
| `Primary_Season_2020 (2019-06-18 to 2020-03-02)` | 53 |
| `Primary_Season_2024 (2023-01-28 to 2024-05-23)` | 79 |
| **合计** | **599** |

已查看的 XML 包含 `Speech/Metadata`、段落、句子与词级结构，以及词形还原、词性、依存关系、实体标签、树深度、依存距离、情感分数和 QUITA 指标。这些是已有自动处理结果，**不是人工金标准标注**。本次没有验证所有文件的字段完整性、模型准确率或公式正确性。

这 599 份 XML、Factba.se 研究子集的 625 份 CSV 和早期 Rally 的 75 份文本尚未建立逐篇对应表。不能把数量差异直接解释为某一步过滤，也不能直接合并为独立样本。

## 6. 代码位置及可维护性

GitHub 代码位于 `code/`；本地 `D:\Trump_Text_Structuring` 下直接使用下表子目录名，没有外层 `code/`。

| 子目录 | 内容与边界 |
| --- | --- |
| `quita_nltk/` | `quita.py` 源码，含 `QuitaText` 和 `getQuitaFeature`；使用 NLTK、NumPy、pandas。 |
| `chinese_adaptation/` | 从特朗普组件改编的中文源码，使用中文 spaCy 模型与 SnowNLP；可参考结构，不能直接当作英文原版。 |
| `recovery_cache/` | 英文原版及中文改编版的 Python 3.10/3.12 编译缓存，含 `quita_spacy`、`quita_analyzer`；不是已恢复的 `.py` 源码。 |
| `factbase_legacy/` | 抓取、筛选、清洗、文本导出笔记本及辅助 Python/R 代码。整理副本清空了笔记本输出，原始笔记本在历史 ZIP 中。 |
| `rally_legacy/` | 较早的清洗、Stanza 分句分词和 XML 结构化脚本及爬虫笔记本。 |
| `migration/`（位于仓库／本地根目录） | 归档清单、SHA-256 和下载回验记录；操作脚本与本地清理记录仅存本地。 |

这些是历史代码，尚未整理成可分发的统一程序。部分脚本在顶层执行并包含旧绝对路径；运行前应检查路径和环境。此次没有执行爬虫／模型、重新计算指标或修改 Conda 环境。

已知问题：NLTK 版 `getQuitaFeature()` 两次写入 `R` 键，分别用于 H-point 和 CLI，后者会覆盖前者；代码尚未修复。XML 出现独立 `HPoint`、`CLI` 字段，也不说明现有 NLTK 源码能原样复现所有 XML。英文 spaCy 版源码恢复和指标验证仍待进行。

## 7. 完整性、来源与研究使用边界

- 2026-10-31 归档保留了历史文件内容，没有重新清洗或合并研究版本。三个 ZIP 已从 GitHub 下载回验，SHA-256 与上传前一致。这证明传输完整，不证明语料或标注正确。
- [归档校验值](https://github.com/Mystery-W/Trump_compaign_speech_annotation/blob/main/migration/archive_checksums.json)记录各 ZIP 大小、SHA-256 和条目数；[逐文件清单](https://github.com/Mystery-W/Trump_compaign_speech_annotation/blob/main/migration/corpus_inventory.json)记录包内路径、大小与哈希。三包共 18,406 个条目，包含重复内容、代码和辅助文件，不代表独立演讲规模。
- 历史 ZIP 部分中文名称采用 GBK。清单 `path` 提供恢复后的可读名称，`stored_path` 保留 ZIP 解码得到的存储名称；解压时注意编码。
- 来源包括 Factba.se/Roll Call。此次归档不新增覆盖第三方语料或软件的开源许可证。
- 分析前请确定时段、活动类型、发言人和处理阶段，并检查空文本、重复项、编码及样本对应关系。`All/` 不保证每行都是特朗普发言，`cleaned`／`final` 等名称也不等于质量验收。
- 本地仅保留代码与记录。需要语料时从 Release 下载到单独数据目录；无关中文研究数据、第三方手册和文稿不在此次整理范围。
