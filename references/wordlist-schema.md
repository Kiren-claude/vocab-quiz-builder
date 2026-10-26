# 词库 JSON 格式规范

生成测试应用时，需将词库数据按以下 JSON 格式组织，并注入模板的 `/*WORD_DATA_PLACEHOLDER*/` 位置。

## 顶层结构

```json
{
  "themes": [
    {
      "name": "课本名称（如 必修一、必修二）",
      "bgSeed": "背景关键词（如 back-to-school / nature-forest）",
      "lessons": [
        {
          "name": "单元名称（如 Unit 1 Back to school）",
          "words": [...],
          "phrases": [...]
        }
      ]
    }
  ]
}
```

> 数据结构中 `themes` 对应课本，`lessons` 对应单元。首页三按钮导航：单词默写/词汇表 → 选课本 → 选单元。

## 单词条目（words）

```json
{
  "en": "英文单词",
  "cn": "中文释义（多个用分号分隔，如 \"保护；保存\"）",
  "ph": "/音标/（如 /prəˈtekt/）",
  "col": "讲义搭配（可选，如 \"protect the ecosystem 保护生态系统\"）"
}
```

字段说明：
- `en`：英文单词（必填）
- `cn`：中文释义，多个意思用分号 `；` 分隔（必填）
- `ph`：国际音标（可选，短语可无）
- `col`：讲义中的核心搭配，点击单词详情弹窗时在「💡 讲义搭配」板块显示（可选）

## 短语条目（phrases）

```json
{
  "en": "英文短语",
  "cn": "中文释义"
}
```

短语规则：
- 无音标字段
- 不参与"填空补全"题型（因含空格）
- 英译中匹配同样支持近义词/分号分隔容错
- 在词汇表页面点击短语仅发音，不弹出详情

## 示例

```json
{
  "themes": [
    {
      "name": "Environment & Nature",
      "bgSeed": "nature-forest",
      "lessons": [
        {
          "name": "Part 1 Word Bank",
          "words": [
            {"en": "protect", "cn": "保护；保存", "ph": "/prəˈtekt/", "col": "protect the ecosystem 保护生态系统"},
            {"en": "environment", "cn": "环境", "ph": "/ɪnˈvaɪrənmənt/"}
          ],
          "phrases": [
            {"en": "water resource", "cn": "水资源"},
            {"en": "natural wetland", "cn": "天然湿地"}
          ]
        }
      ]
    }
  ]
}
```

## 规则

- themes 数组通常只放一个元素，name 作为页面大标题
- 每个 theme 下有多个 lesson，首页直接列出所有课时
- 每个 lesson 有 words（单词）和 phrases（短语）两个数组
- 中文释义支持分号分隔多个意思，答题时任一即可匹配
- bgSeed 用于生成与主题相关的背景图（可选，不填则用默认图）
- 测试题数由用户在点击课时后弹窗输入（默认 10），不再固定 25 题
