---
name: vocab-quiz-builder
description: 从词库生成单文件 HTML 单词测试应用。当用户需要制作英语单词测试、词汇测验、背单词练习网页时使用。支持五种题型（英译中选择/中译英选择/英译中输入/中译英输入/填空补全）、自定义题数、30秒倒计时、美式发音、多用户成绩、排行榜、错题回顾、词汇表（含单词详情弹窗：多词性释义、单词变形、固定搭配、讲义搭配）。集成 DeepSeek 12655 词库。输出为可直接在浏览器打开的单个 HTML 文件。
---

# Vocab Quiz Builder

从词库数据生成功能完整的单文件单词测试 HTML 应用。

## 快速生成（推荐）

使用脚本自动完成数据匹配和注入：

```bash
python3 scripts/generate.py <词库.json> <输出.html> [--title "自定义标题"]
```

脚本会自动：
1. 从 `assets/global-words.json`（12655词）匹配多词性释义和固定搭配
2. 从 `assets/inflections-cache.json` 匹配单词变形数据
3. 注入模板、JS 语法验证、输出 HTML

## 手动生成流程

1. **获取词库**：从用户提供的讲义、图片、PDF、文本中提取单词和短语
2. **组织数据**：按 [references/wordlist-schema.md](references/wordlist-schema.md) 的 JSON 格式组织
3. **匹配丰富数据**：从 `assets/global-words.json` 查找本次词库单词的释义和搭配；从 `assets/inflections-cache.json` 查找变形
4. **注入模板**：读取 `assets/quiz-template.html`，替换两个占位符
5. **语法验证**：提取 `<script>` 内容用 `node --check` 验证
6. **交付**：保存为单个 .html 文件

## 数据注入方式

将模板中的 `/*WORD_DATA_PLACEHOLDER*/` 替换为：

```js
const WORD_DATA = { "themes": [...] };
```

将 `/*DEEPSEEK_DATA_PLACEHOLDER*/` 替换为（仅包含本次测试用到的单词）：

```js
const DEEPSEEK_DATA = {
  "protect": {
    "translations": [{"type":"v","translation":"保护"}],
    "phrases": [{"phrase":"protect from","translation":"保护免受"}],
    "inflections": [{"type":"名词","word":"protection","cn":"保护"}]
  }
};
```

若无需丰富数据，替换为 `const DEEPSEEK_DATA = {};`。

## 功能清单

### 导航结构
- **首页**：三个大按钮 —— 📝 单词默写、📖 词汇表、🏆 排行榜
- **单词默写**：选择课本 → 选择单元 → 输入题数 → 开始测试
- **词汇表**：选择课本 → 选择单元 → 浏览单词（点击弹出详情）
- 词库数据结构：themes（课本）→ lessons（单元）→ words/phrases

### 测试核心
- 5 种题型随机混合：英译中选择、中译英选择、英译中输入、中译英输入、填空补全
- 短语不参与填空题（因含空格）
- 自定义题数：点击课时后弹出**网页内题数选择弹窗**（5/10/20/全部快捷按钮 + 自定义数字输入），默认 10 题，词库不足则全抽
- 每题 30 秒倒计时，最后 5 秒数字变红脉冲
- 答对 +1 分 + 连击 +1，答错/超时连击清零
- 测试结束展示错题回顾（题目、你的答案、正确答案）

### 词汇表（原"单词朗读"）
- 按课时分组列出所有单词和短语
- 点击单词弹出详情弹窗，点击短语直接发音
- 详情弹窗包含四个板块：
  - 📖 **释义**：多词性释义（来自 DeepSeek 词库）
  - 🔄 **单词变形**：名词/动词/形容词/副词变形链（来自变形缓存）
  - 🔗 **固定搭配**：最多 8 条（来自 DeepSeek 词库）
  - 💡 **讲义搭配**：用户词库 `col` 字段中的搭配

### 发音
- 美式发音 lang='en-US'，rate 0.78，pitch 0.95
- 每道题自动朗读，可点击单词或🔊按钮重听
- 词汇表点击单词/短语单独发音

### 用户系统
- 多用户支持（添加/切换/删除），成绩独立
- 排行榜（总分/正确率/最高连击排序）
- 所有数据存储在 localStorage，无需联网
- 清除数据按钮重置全部

### 界面
- 清新海洋风：天蓝→靛蓝→紫渐变背景 + 白色毛玻璃卡片
- 响应式设计，适配手机和电脑
- 按钮悬停上浮+发光，弹窗弹性缩放动画
- 输入框同时设置 autocomplete/correct/capitalize="off"、spellcheck="false"（仅基础措施，**不足以阻止第三方输入法联想**，真正方案见下）

### 手机端兼容（硬要求，模板已内置，禁止回退）
目标场景是学生在手机浏览器（含微信/QQ 内置浏览器）中作答，必须遵守：

1. **禁止使用 `prompt()`、`alert()`、`confirm()`**：手机浏览器（尤其微信/QQ 内置浏览器）会直接屏蔽 `prompt()`，表现为点击卡片只有按压动画但不跳转。
   - 题数输入 → 网页内自定义模态框（模板中的 `#countModal`：5/10/20/全部 + 自定义数字框，数字框用 `type="number" inputmode="numeric"`）
   - 错误/提示 → 网页内 `showToast()` 浮动提示条
2. **英文作答必须使用网页内置键盘，禁止调用系统键盘**：搜狗、百度、讯飞等第三方输入法的联想弹窗无法用 HTML 属性关闭。
   - **中译英输入题（input2en）、填空补全题（fillblank）**：输入框设 `readonly` + `inputmode="none"`，不聚焦、不弹系统键盘；底部滑出内置 QWERTY 键盘（模板 `.vk-wrap`：26 字母 + 空格 + 退格 + 确认）
   - **英译中输入题（en2input）**：保留系统中文输入法（考中文，不存在英文联想问题）
   - 选择题、结果页、切换任何页面时调用 `hideVK()` 收起键盘
   - 键盘需适配 `env(safe-area-inset-bottom)`（刘海屏），电脑端居中限宽 640px
3. 内置键盘需含空格键（中译英可能考短语），确认键等价于提交按钮

## DeepSeek 词库集成

`assets/global-words.json` 来自 [vocabulary-book-by-deepseek](https://github.com/vxiaozhi/vocabulary-book-by-deepseek)，包含 12655 个单词的多词性释义和固定搭配。

`assets/inflections-cache.json` 是从该项目 `result/all/{首字母}/{word}.json` 的 DeepSeek AI 分析中提取的单词变形数据，目前覆盖 Environment 主题 21 词。生成新主题时，可通过 GitHub API 获取对应单词的分析文件，提取"单词变形"章节后追加到缓存中。

## 关键规则

- 输出为**单个 HTML 文件**，所有 CSS/JS 内联，无需联网（发音需浏览器 Web Speech API）
- 中文释义用分号 `；` 分隔多个意思，答题时任一即可匹配
- 英译中支持近义词/包含关系容错；中译英/填空精确匹配（忽略大小写和空格）
- 干扰项自动从词库随机选取，无需手动配置
- **手机端硬约束**：禁用 `prompt/alert/confirm`（用网页内 modal/toast）；英文输入题必须用内置键盘（readonly 输入框 + `.vk-wrap`），只有英译中输入题可用系统中文键盘
- 生成后必须用 `node --check` 验证 JS 语法；验证脚本中不得出现任何 `prompt(`/`alert(` 调用

## 注意事项

- 若用户提供 PDF/DOCX/图片讲义，先提取单词和释义再按 schema 组织
- 生成后建议在浏览器中打开验证首页、词汇表弹窗和一次测试流程
- 变形缓存仅覆盖已处理的单词，新主题需补充数据后变形板块才会显示
