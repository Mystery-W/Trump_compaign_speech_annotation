# 特朗普语料文本结构化处理代码

此目录于 2026-10-31 从现有研究材料中整理，保留代码、恢复线索和迁移记录，不保存批量原始语料或分析结果。没有升级、安装或修改 Conda 环境。

## 文件说明

| 目录 | 内容与边界 |
| --- | --- |
| `quita_nltk/` | 已找到的 `quita.py` 源码，含 `QuitaText` 和 `getQuitaFeature`；使用 NLTK、NumPy、pandas。 |
| `chinese_adaptation/` | 从特朗普组件改编的中文处理源码，用于参考结构；使用中文 spaCy 模型与 SnowNLP，不能直接当成英文原版运行。 |
| `recovery_cache/` | 原英文组件及中文改编版留下的 Python 3.10/3.12 缓存，包括 `quita_spacy`、`quita_analyzer`；并非已经恢复的源码。 |
| `factbase_legacy/` | 从旧 ZIP 提取的爬虫、清洗、分组、文本导出笔记本及辅助 Python/R 代码。笔记本输出已清空，原始版本在远端归档中。 |
| `rally_legacy/` | 较早的清洗、Stanza 分句及 XML 结构化脚本和爬虫笔记本。 |
| `migration/` | 迁移程序、文件清单、归档校验值与下载核验记录。 |

## 语料存放位置

GitHub 仓库：https://github.com/Mystery-W/Trump_compaign_speech_annotation

归档 Release：https://github.com/Mystery-W/Trump_compaign_speech_annotation/releases/tag/corpus-archive-2026-10-31

- `trump-factbase-original.zip`：原桌面 ZIP 的逐字节副本，保留原始 CSV、按年份/类型整理的副本、清洗文本和旧代码等；内部名称存在历史 ZIP 编码差异，清单另提供恢复后的中文名称。
- `trump-rally-original-and-derived.zip`：早期 Trump rally 目录中的原始与清洗语料、标注、索引和分析产物。
- `trump-annotated-xml.zip`：599 份 2016/2020/2024 竞选演讲标注 XML。

原语料出处包括 Factba.se/Roll Call。归档用于保存研究材料，不表示获得了语料内容的版权，也没有新增覆盖第三方内容的开源许可证。

## 使用前注意

这些是保留的历史脚本，不是已经整理成统一入口的发行版。部分脚本在顶层执行并包含旧绝对路径；请先检查和调整输入输出位置，再在适当的既有 Conda 环境中运行。本次未执行爬虫、模型推理或重新计算指标，未验证 QUITA 公式与原软件的一致性。不要直接运行迁移脚本的清理阶段。

QUITA 源码中的 `getQuitaFeature()` 两次使用 `R` 键，分别写入 H-point 与 CLI，后者会覆盖前者；本次为保全原件没有改写。后续若要恢复英文管线，应先恢复或重建 spaCy 版、修复字段命名，并针对实际研究定义验证指标。

为保持本地仅含代码，需要语料时请从 Release 下载至单独的数据目录。原有中文研究数据、第三方手册和研究文稿不在此次清理范围。
