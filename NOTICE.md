# Third-Party Notices ｜ 第三方数据声明

本项目包含以下第三方数据。除本声明覆盖的数据文件外，其余代码与文档以 MIT License 发布（见 [LICENSE](LICENSE)）。

## assets/global-words.json 与 assets/inflections-cache.json

- **来源项目**：[vxiaozhi/vocabulary-book-by-deepseek](https://github.com/vxiaozhi/vocabulary-book-by-deepseek)
- **作者**：vxiaozhi（GitHub: https://github.com/vxiaozhi）
- **许可证**：Apache License 2.0（http://www.apache.org/licenses/LICENSE-2.0）

**改动说明**：

1. `global-words.json` 由原项目的单词分析结果（`result/` 目录下的 JSON 文件）汇总、转换格式而来，仅保留每个单词的词性释义（translations）与固定搭配（phrases）字段，删除了词根、例句、助记图像等字段，供本项目的单词详情弹窗与干扰项匹配使用。
2. `inflections-cache.json` 由原项目单词分析结果中的"单词变形"章节提取而来；对于原项目未覆盖的单词，由本项目的规则生成器按英语常规词形变化规则补充生成。

依据 Apache License 2.0 第 4 条，对上述数据的再分发保留原项目的来源与许可声明。原许可证全文可从以下地址获取：

http://www.apache.org/licenses/LICENSE-2.0

## Apache License 2.0 摘要

Apache License 2.0 允许商业使用、修改、分发和再授权，但要求：

- 保留版权声明、许可证副本及本声明；
- 对修改过的文件予以标注；
- 不使用原作者的名义为衍生作品背书。

本声明不构成法律意见，完整权利与义务以 Apache License 2.0 原文为准。
