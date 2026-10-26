# Vocab Quiz Builder ｜ 单词测试生成器

一个面向英语教师的单词测试网页生成工具：准备好词库 JSON，运行一条命令，即可生成**单文件 HTML** 的单词测试应用——学生用手机浏览器打开就能做，无需安装任何 App、无需联网（发音除外）。

最初为译林版高中英语教材（必修一至选修四）开发，适用于任意英语教材的词汇测验场景。

## 功能特性

- **五种题型随机混合**：英译中选择、中译英选择、英译中输入、中译英输入、填空补全（短语不参与填空）
- **自定义题数**：每次可选 5 / 10 / 20 / 全部，或输入任意题数
- **30 秒倒计时**：最后 5 秒变红，超时自动判错
- **美式发音**：Web Speech API，`en-US`，语速 0.78，每题自动朗读，可点单词重听
- **词汇表**：按单元浏览，点击单词查看详情——多词性释义、单词变形（名词/动词/形容词/副词/过去式/过去分词/复数）、固定搭配、讲义搭配
- **多用户与排行榜**：成绩存于浏览器 localStorage，支持多用户、总分/正确率/最高连击排行、错题回顾
- **手机端深度适配（重点）**：
  - 英文输入题使用**网页内置 QWERTY 键盘**，彻底规避搜狗、百度、讯飞等第三方输入法的单词联想（杜绝作弊干扰）
  - 全部交互使用网页内弹窗与提示条，不使用手机浏览器会屏蔽的 `prompt()/alert()/confirm()`
  - 适配刘海屏安全区，选择题点按区域大，电脑端同样可用
- **单文件交付**：所有 CSS/JS/数据内联在一个 HTML 文件中，可通过微信/QQ/AirDrop 直接发给学生

## 快速开始

需要 Python 3（生成脚本）和 Node.js（仅用于生成时的语法检查）：

```bash
# 1. 准备词库 wordlist.json（格式见下文）
# 2. 生成测试网页
python3 scripts/generate.py wordlist.json 单词测试.html --title "高一英语 Unit 1"

# 3. 双击生成的 HTML 文件即可在浏览器打开
```

脚本会自动从内置词库（`assets/global-words.json`，12655 词）匹配多词性释义、固定搭配与单词变形并嵌入页面。

## 词库格式

```json
{
  "themes": [
    {
      "name": "必修一",
      "bgSeed": "classroom",
      "lessons": [
        {
          "name": "Unit 1",
          "words": [
            {"en": "protect", "cn": "保护；保存", "ph": "/prəˈtekt/"},
            {"en": "improve", "cn": "改进；改善", "ph": "/ɪmˈpruːv/"}
          ],
          "phrases": [
            {"en": "take place", "cn": "发生"}
          ]
        }
      ]
    }
  ]
}
```

完整字段说明见 [`references/wordlist-schema.md`](references/wordlist-schema.md)。

- `themes` 对应课本/主题，`lessons` 对应单元
- 中文释义用分号 `；` 分隔多个意思，答题时任一即可匹配
- 短语无音标字段（`ph`），不参与填空题

## 项目结构

```
vocab-quiz-builder/
├── SKILL.md                        # AI Agent 技能说明（给 AI 助手使用）
├── scripts/
│   └── generate.py                 # 词库 → HTML 生成脚本
├── assets/
│   ├── quiz-template.html          # 应用模板（含全部交互逻辑与内置键盘）
│   ├── global-words.json           # 12655 词释义/搭配数据（第三方，Apache-2.0）
│   └── inflections-cache.json      # 单词变形缓存（由第三方词库数据提取）
└── references/
    └── wordlist-schema.md          # 词库 JSON 格式规范
```

## 数据来源与许可

- **本项目自有代码**（模板、脚本、SKILL.md、格式文档）：以 [MIT License](LICENSE) 发布
- **`assets/global-words.json` 与 `assets/inflections-cache.json`**：衍生自 [vxiaozhi/vocabulary-book-by-deepseek](https://github.com/vxiaozhi/vocabulary-book-by-deepseek)，该项目以 Apache License 2.0 发布，数据的版权与许可声明详见 [NOTICE.md](NOTICE.md)

## 面向 AI 助手

本仓库本身即一个可复用的 AI Skill：将其放入 AI 助手的 skills 目录后，助手即可在你提供词库（文本、图片、PDF）时自动提取单词、匹配数据并生成测试网页。完整工作流见 [`SKILL.md`](SKILL.md)。
