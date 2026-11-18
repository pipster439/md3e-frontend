# M3 Expressive 官方规范对照审查

审查日期：2026-09-15。对象：当前 `md3e-frontend` 技能包。

> [!NOTE]
> **2026-11-18 修复跟进（第一轮 + 第二轮 + 桌面端与全仓对齐）**：
> - **第一轮**：本文档最初列出的 12 项问题（2 项 P1 + 10 项 P2）以及后续排查出的图标防幻觉/FOUT 保护、WAAPI/形态变形动画、Tailwind 动效映射与响应式示例缺陷已在当前版本全部落地修复，并新增 `references/icons.md`、回归测试 `scripts/test_md3e.py` 与静态检查器规则 `MD3E017`–`MD3E021`（完整规则集现涵盖 `MD3E001`–`MD3E022`）。
> - **第二轮（配色方案 + 异形容器 + 模糊 + 动效 + 桌面优化对齐）**：修复了 `[data-color-variant="vibrant"]` 在暗色下完全无变化、深色模式下 `surface` (`#1C1B1F` N10) 与 `surface-container-low` (`#1D1B20` N10) 阶梯坍塌的问题，改为 `N98 #FEF7FF` / `N6 #141218`；新增纯标准库 CAM16/HCT + MCU `SPEC_2025` 生成器 `scripts/color_to_css.py`、多主题预设 `assets/tokens/md3e-palettes.css`（6 个种子色 × 5 种变体 × 3 档对比度 + `@media (forced-colors: active)`）；移植 AOSP `MaterialShapes.kt` 全部 35 种官方异形容器及 7 边形 `LoadingIndicator` 变形序列至 `scripts/shapes_to_css.py` / `assets/tokens/md3e-shapes.css`；完善动效生成器 `scripts/spring_to_css.py` 与 `assets/tokens/md3e-motion.css`，新增动效 `-bezier` 官方曲线对照驱动与可打断速度继承物理弹簧 `assets/tokens/md3e-spring.js`；明确区分官网无 `md.sys.blur.*` 令牌与 Android 16 系统窗口模糊，新增受保护的 `.md3e-frosted-surface` 与检查器规则 `MD3E022`，并补全桌面多窗格布局、Navigation Rail 折叠/展开及视觉密度（`data-density`）规范。
> - **当前工具与资产清单**：
>   - **5 个脚本（`scripts/`）**：`color_to_css.py`（支持 `--seed` 与 `--image` 传图取色）、`shapes_to_css.py`、`spring_to_css.py`、`audit_md3e.py`（支持 `--mode=strict` 与 `--mode=desktop-bento`，规则涵盖 `MD3E001`–`MD3E023` 与 `MD3E101`–`MD3E104`）、`test_md3e.py`。
>   - **9 个令牌与运行时文件（`assets/tokens/`）**：`md3e-tokens.css`、`md3e-palettes.css`、`md3e-blur.css`（带 `@media (prefers-reduced-transparency: reduce)` 自动纯色回退）、`md3e-shapes.css`、`md3e-motion.css`、`md3e-material-web.css`、`md3e-spring.js`、`md3e-morph.js`（AndroidX `RoundedPolygon` + `Morph` 三阶贝塞尔实时形变插值器）、`md3e-dynamic-color.js`（浏览器端上传图片取色 `QuantizerCelebi` + `Score` + `SPEC_2025` 实时换肤）。
>   - **Tailwind 与 Starter 资产**：`assets/tailwind/md3e-theme.css`、`assets/tailwind/tailwind.config.js`、`assets/starter/index.html`、`assets/starter/desktop-bento.html`（独立桌面端高密度 Bento 仪表盘演示页）。
> - **第三轮（Web 原生完备度 + 桌面端高密度 Bento 系统升级）**：在 `SKILL.md` 建立上下文预算防溢出机制与 `references/desktop-bento.md` 可选覆写层解耦；新增 `md3e-blur.css`、`md3e-morph.js`，并在 `expressive-recipes.md` / `typography.md` / `starter` 示例中补齐实时贝塞尔形变、100% 自动拉直双实现波浪进度条（SVG + Canvas）、悬浮/停靠双向工具栏、按钮组邻居宽度挤压、可变字体 `GRAD`/`ROND`/`wght` 弹簧过渡及 View Transitions 容器展开配方。

## 结论（初版审查快照）

**当前版本不宜作为“严格符合官方规范”的自动验收依据。** 本次确认 12 项可行动问题：2 项 P1、10 项 P2。主要风险集中在无障碍颜色、规范断言、可复制的组件示例以及检查器漏报。

P1 表示应优先修复、可能直接影响可读性或错误放行；P2 表示应在下一轮维护中修正。

## 依据与方法

- 以用户指定的 [abhixv/m3-expressive-design-skill](https://github.com/abhixv/m3-expressive-design-skill) 作为结构化参考。它是第三方整理，不是 Google 官方发布的技能。
- 实际加载并展开 m3.material.io 的动效与排版页面，读取按钮指南；争议以官网当前展示为准。
- 检查技能入口、系统参考、组件参考与 recipes、三份设计变量样式、Tailwind 映射、starter、两份 Python 脚本。重点核验可传播到下游项目的规则与实现。没有对全部组件图示的每个尺寸逐一认证，也没有完成所有组件的全状态、全断点测试。
- 在浏览器运行 starter，读取真实 DOM、计算样式和媒体条件；使用独立小样本检验检查器。浏览器临时媒体模拟已撤销。

## P1：优先修复

### 1. 暗色高对比度把容器与内容变成同色

位置：[md3e-tokens.css:478](C:/Users/ROG/.gemini/config/skills/md3e-frontend/assets/tokens/md3e-tokens.css:478)。

`prefers-contrast: more` 内的 `:root` 将 `primary-container` 改为 P90；后面的暗色分支没有恢复这个角色，也没有同步改其 `on-` 角色。因此显式暗色与高对比度同时启用时，实际计算结果为：

| 条件 | primary-container | on-primary-container | 对比度 |
|---|---|---|---|
| data-theme=dark，prefers-contrast=more | #EADDFF | #EADDFF | 1:1 |

这使消费该配对的图标、文字不可辨认，恰好影响主动请求更高对比度的用户。建议按浅色、暗色分别定义完整且成对的高对比度角色，并检验所有 container/on-container 组合。对比度依据：[WCAG 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)。

### 2. 大文本门槛将 pt 错写为 px

位置：[accessibility.md:11](C:/Users/ROG/.gemini/config/skills/md3e-frontend/references/accessibility.md:11)。

当前把 `18px+` 或 `14px bold` 视为大文本，允许仅 3:1 对比度。WCAG 的门槛是 18pt 常规或 14pt 粗体，对应约 24 CSS px 或 18.67 CSS px。当前规则会把不少普通正文和按钮标签错误放行。

建议修正单位，并保留普通文本 4.5:1 门槛；不要将组件容器/图标的对比度要求与标签文字要求混为一谈。依据：[W3C 对大文本及单位换算的说明](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)。

## P2：规范与实现偏差

### 3. 跟随系统暗色仅改变浏览器外观，未切换角色

位置：[md3e-tokens.css:414](C:/Users/ROG/.gemini/config/skills/md3e-frontend/assets/tokens/md3e-tokens.css:414)。

系统暗色分支只有 `color-scheme: dark`，真正的颜色变量仅在 `[data-theme="dark"]` 生效。这与技能入口“可留给 prefers-color-scheme”及颜色参考中的承诺不一致。

浏览器复现：移除显式主题、模拟系统暗色后，`color-scheme=dark`，但 `surface=#FFFBFE`，body 背景仍为 `rgb(255, 251, 254)`。建议把暗色角色同时应用于系统暗色默认路径，并保留显式浅色覆盖的优先级。

### 4. 一律禁止 duration/easing 会拒绝官方 Web 实现

位置：[motion.md:80](C:/Users/ROG/.gemini/config/skills/md3e-frontend/references/motion.md:80)、[audit_md3e.py:244](C:/Users/ROG/.gemini/config/skills/md3e-frontend/scripts/audit_md3e.py:244)。

官网明确允许在无中断、无手势的 Web 动画中使用模拟弹簧的曲线，并提供曲线和时长表。当前检查器把官方 expressive fast spatial 的 `350ms cubic-bezier(0.42, 1.67, 0.21, 0.90)` 判为 MD3E004 error。

建议区分官方曲线、项目生成的采样曲线、任意手写曲线，以及手势驱动场景。当前生成器的采样 linear() 可以保留为实现选择；其自行推导的收敛时长不应被称为官网 Web 转换表。依据：[官方 Motion Specs](https://m3.material.io/styles/motion/overview/specs)。

### 5. 把官方建议与可定制项写成绝对禁令

位置：[SKILL.md:37](C:/Users/ROG/.gemini/config/skills/md3e-frontend/SKILL.md:37)、[components.md:64](C:/Users/ROG/.gemini/config/skills/md3e-frontend/references/components.md:64)。

两例已经官网核实：

- “每个 view 必须恰好一个 filled button”：官方说应节制使用，理想情况下每页一个此类动作。它不是必须存在一个，也不是所有页面结构的绝对数量限制。[官方按钮指南](https://m3.material.io/components/buttons/guidelines)
- “字体大小只能使用 11 个值”：官方提供默认标尺，也明确允许按产品需求定制标尺、增删样式或调整大小。可规定项目默认使用原始标尺，但应标注这是项目约束。[官方排版规范](https://m3.material.io/styles/typography/type-scale-tokens)

建议在技能中明确标注“官方默认值 / 官方建议 / 本项目约束 / 自定义实现”，防止代理把合理定制作为违规改掉。

### 6. Split button 与 connected group 示例缺少官方间距和形状行为

位置：[expressive-recipes.md:136](C:/Users/ROG/.gemini/config/skills/md3e-frontend/references/components/expressive-recipes.md:136)、[expressive-recipes.md:230](C:/Users/ROG/.gemini/config/skills/md3e-frontend/references/components/expressive-recipes.md:230)。

两个示例都主要使用外层连续容器、裁剪和 1px 分隔线。Split button 没有两个按钮之间的 2dp 空隙及内部圆角变化；connected group 没有 2dp 间距，也没有选中/按压时的形状变化。starter 重复了同一做法。

项目自身的 `components/action.md` 已记录对应要求；与指定参考的按钮组件章节一致。建议按尺寸与状态实现间距和内部圆角，将当前实现明确标为简化示意，直至补齐。依据：[结构化按钮参考](https://github.com/abhixv/m3-expressive-design-skill/blob/main/skills/m3-expressive/references/components/buttons.md)，其对应官方页面为 [Split button Specs](https://m3.material.io/components/split-button/specs) 与 [Button groups Specs](https://m3.material.io/components/button-groups/specs)。

### 7. 五档按钮尺寸在示例和桥接层中没有完整落实

位置：[starter/index.html:134](C:/Users/ROG/.gemini/config/skills/md3e-frontend/assets/starter/index.html:134)、[md3e-material-web.css:258](C:/Users/ROG/.gemini/config/skills/md3e-frontend/assets/tokens/md3e-material-web.css:258)。

浏览器实测：starter 的 XS、S 都是 48px 高。原因是直接在有背景的按钮上设置 `min-height:48px`，覆盖了 32px、40px 的视觉高度。应保持视觉容器高度，再扩展透明命中区。

桥接样式也不完整：L 的 padding、icon、label 只完整更新 filled/outlined；XL 的完整映射主要只有 filled，text 连高度也未更新。使用同一个 `.md3e-size-xl`，不同按钮类型会得到不同尺寸体系。

建议覆盖各颜色样式与 XS/S/M/L/XL 的完整矩阵，并分别测量容器、命中区、标签和图标。尺寸依据：[指定结构化按钮参考](https://github.com/abhixv/m3-expressive-design-skill/blob/main/skills/m3-expressive/references/components/buttons.md)，也见本项目 `references/components/action.md` 的测量表。

### 8. 状态层 color-mix 使用无效权重，悬停反馈失效

位置：[expressive-recipes.md:75](C:/Users/ROG/.gemini/config/skills/md3e-frontend/references/components/expressive-recipes.md:75)、同文件 199、263 行。

`color-mix(... currentColor 0.08, ...)` 使用了数值而非百分比；把数值 opacity 变量直接放在这个位置同样无效。浏览器 `CSS.supports` 对该表达式返回 false，声明会被忽略。

建议使用正确百分比，或使用独立 state-layer 元素，通过 `opacity` 消费数值 token。后者也能避免直接替换选中态底色。修复后逐一验证 hover/focus/pressed 的计算样式。

### 9. FAB menu 关闭后仍保留不可见的键盘焦点

位置：[expressive-recipes.md:343](C:/Users/ROG/.gemini/config/skills/md3e-frontend/references/components/expressive-recipes.md:343)、同文件 390 行附近的事件处理。

关闭逻辑只有 opacity、pointer-events 与 aria-hidden。它们不会让内部原生按钮退出 Tab 顺序；于是焦点可进入隐藏菜单。代码也没有 Escape 关闭及焦点恢复，40×40 的 mini 按钮没有扩展命中区。

这是静态代码确认，未把该 recipe 单独装载为完整交互测试。建议使用 hidden/inert 或等价焦点管理，补齐打开、关闭、Escape、焦点返回和实际命中区。与本项目无障碍参考中的键盘可达性要求冲突。

### 10. Starter 的文本框闭合错误使滑块进入未显示的内容

位置：[starter/index.html:485](C:/Users/ROG/.gemini/config/skills/md3e-frontend/assets/starter/index.html:485)。

`<md-outlined-text-field>` 被 `</md-filled-text-field>` 关闭。浏览器实际 DOM 中，后续 slider 成为 outlined text field 的后代；可访问性树中未出现 Volume slider。

建议先修正闭合标签，再验证文本框与滑块分别可见、可聚焦。另应修正同页 473、478 行的可访问名称：可见 Wi-Fi 对应 Airplane mode，Notifications 对应 Option A，语义不一致。

### 11. 自动检查器的零问题结果不能证明合规

位置：[audit_md3e.py:157](C:/Users/ROG/.gemini/config/skills/md3e-frontend/scripts/audit_md3e.py:157)、[audit_md3e.py:380](C:/Users/ROG/.gemini/config/skills/md3e-frontend/scripts/audit_md3e.py:380)。

本次运行 `python scripts/audit_md3e.py assets --json`，扫描 6 文件，结果 error=0、warn=0、info=0。独立样本却确认：

| 输入 | 当前结果 | 问题 |
|---|---|---|
| HTML 内联 background: #ff0000 | 无报告 | 内联 style 未被可靠解析 |
| 仅使用 spring var()，无 reduced-motion 路径的 CSS | 无报告 | has_motion 依赖字面量时间，漏掉推荐写法 |
| height:32px; min-height:48px | MD3E006 warn | 未合并声明判断实际尺寸 |
| 官方 Web spring 转换曲线 | MD3E004 error | 把官方允许的实现判错 |

目录扫描也不会审查 Markdown 内可复制的 CSS/HTML 示例。建议将工具描述为启发式静态检查器，加入 CSS/HTML 解析、跨声明与跨文件判断，以及浏览器补充验证；不要把零告警直接作为规范通过结论。

### 12. Loader 把空间弹簧同时用于颜色，并意外引入延迟

位置：[starter/index.html:272](C:/Users/ROG/.gemini/config/skills/md3e-frontend/assets/starter/index.html:272)、[expressive-recipes.md:427](C:/Users/ROG/.gemini/config/skills/md3e-frontend/references/components/expressive-recipes.md:427)。

同一组 keyframes 同时改变 transform、border-radius 和 background，并统一使用 spatial 曲线。这不符合空间变化与颜色效果分用 spatial/effects 的规则。

此外，`animation: shape-morph 2.4s var(--md-sys-motion-default-spatial) infinite` 中，变量本身包含 `460ms` 和曲线。浏览器将第二个时间解释为延迟：实测 duration=2.4s、delay=0.46s。该写法不是语法失效，但会意外推迟加载反馈，也不是以该弹簧收敛时长播放。

建议分离几何和颜色动画，并将 duration/easing 拆成适合 animation 组合的变量，或直接使用固定颜色。时长、循环节奏属于实现选择，应清楚标注。依据：[官方 Motion Specs](https://m3.material.io/styles/motion/overview/specs) 及[指定动效 token 参考](https://github.com/abhixv/m3-expressive-design-skill/blob/main/skills/m3-expressive/references/tokens.md)。

## 争议处理与可保留部分

- **未把第三方排版表机械覆盖到项目。** 其强调字距表与官网当前展开值存在差异。例如官网强调 title-medium、body-large、label-large 的 tracking 为 0，本项目这些值与官网一致；不能仅因与 Compose 整理表不同判错。官网当前 body-small 强调 tracking 为 0，而项目为 0.1px，后续应在记录字体、平台、版本上下文后单独校准。[官方排版 tokens](https://m3.material.io/styles/typography/type-scale-tokens)
- 十档系统圆角与两套弹簧 damping/stiffness 参数，与指定结构化参考吻合。本次没有理由整体推倒重建。
- `spring_to_css.py` 重新生成的文本与现有 `md3e-motion.css` 一致；生成流程可复现。采样 linear() 是可解释的实现方案，主要问题是规范表述及使用方式。
- Tailwind 映射本轮未做 v3/v4 构建验证；各框架集成例子也未逐一运行，因此没有给出“全部兼容”的结论。
- 官网对自定义排版和 Web 动效存在明确支持；审查不应把偏好、默认值和硬性要求混为一谈。

## 建议修复顺序

1. 修复高对比度配色和文本对比度单位。
2. 修复系统主题、starter 标签、状态层语法及 FAB 菜单焦点。
3. 对齐按钮几何、尺寸矩阵与 loader 动效。
4. 修订规范措辞，并用已确认的正反例校准检查器。

完成修复后，应至少回归浅色/暗色、系统跟随、高对比度、reduced-motion、键盘与触控、五档按钮尺寸；对 starter 再进行窄屏及 200% 文本缩放检查。
