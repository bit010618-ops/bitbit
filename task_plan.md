# DSP Complete Handout Regression Plan

## Goal
对完整《华理814DSP讲义》做全量回归校对：以原 DSP 课件为唯一图形基准，逐图核对并重画所有坐标图、系统框图、FFT 蝶形流图、IIR/FIR 结构图等，使节点、连线、箭头、标签、比例和重点标色与原图一致；修复空白页、重叠、截断和对齐问题；最终输出一份适合直接彩印的完整 A4 讲义，正文与页面装饰以黑白为主，原课件中必要的彩色公式、图形、曲线和重点标色原样保留，并新增简洁封面。

## Phases
- [completed] 建立校对清单，定位 PDF、原课件、批次脚本与页码映射。
- [completed] 修复早期批次的坐标轴、空白页、系统框图与第 4 章 FFT 蝶形图。
- [completed] 修复第 5-6 章 IIR/FIR 图形、重点色和重叠。
- [in_progress] 建立全书“原课件页 - 讲义页 - 图形类型 - 差异 - 复验结果”逐图对照矩阵。
- [pending] 按章节逐图重绘与复验：第 1-3 章坐标图和系统框图。
- [pending] 按章节逐图重绘与复验：第 4 章 FFT 分解图、蝶形图和完整流图。
- [pending] 按章节逐图重绘与复验：第 5-7 章 IIR/FIR 结构图、频响图和多采样率框图。
- [pending] 全书逐页视觉回归，修复余下截断、重叠、错误分页和遗漏红色重点。
- [pending] 统一全书彩印友好版式：取消蓝色页眉条和非必要蓝色装饰框，改为白底、黑灰页眉细线、黑白表格；保留原课件必要颜色并新增封面。
- [pending] 合并最终 PDF，验证封面、目录、页眉页脚、页码、内容完整性、图形一致性和直接彩印效果。

## Decisions
- 原 DSP 课件是唯一内容与图形参考；讲义只做 A4 排版，不自行改造图形拓扑。
- 公式、红字重点、箭头方向、块图连接和图形比例应保留原意。
- 所有输出必须渲染成图片后进行视觉复核。
- 图形验收不只看“无重叠”，还必须逐项核对拓扑、线序、箭头方向、节点位置、标签归属和相对比例；未经原图对照复验的图不得标记完成。
- 不再单独生成黑白版。最终版按参考文件《【A4】小马哥960题目册做题本》的克制版式处理：白底、黑色正文、页眉小字加细线、页脚居中页码；原 DSP 课件中本来存在的蓝色标题、红色重点和彩色图形保留原色。
- 合并后的目录是第 1 页；用户反馈中的旧页码应按批次边界换算，不直接按旧页号套用。

## Errors Encountered
| Error | Cause | Resolution |
|---|---|---|
| `python` command not found | 系统未配置 Python PATH | 固定使用 Codex 内置 Python 运行时完整路径 |
| `pdftoppm` command not found | 系统未配置 Poppler PATH | 使用内置 Python 图像渲染库进行 PDF 页面回归检查 |
| `fitz` module not found | 内置 Python 未安装 PyMuPDF | 查找内置 Poppler；若无则使用现有渲染工具链 |
| 内置 `pdftoppm.cmd` 首次调用失败 | 命令封装或路径参数待确认 | 先单独验证封装脚本与可执行文件路径，再执行批量渲染 |
| 2026-07-14 再次调用 `pdftoppm.cmd` 未产出页面 | PATH 包装器仍指向无效路径 | 固定使用 `dependencies/native/poppler/Library/bin/pdftoppm.exe` |
| 并行读取技能说明触发 `CreateProcessWithLogonW failed: 1056` | Windows 沙箱并发创建登录进程冲突 | 改为单进程顺序读取，避免重复触发 |
| `git diff --stat` 失败 | 当前工作目录不是有效 Git 仓库 | 使用计划文件、脚本时间戳、批次 PDF 和渲染图记录变更 |
| `rg work\\make_dsp_*.py` 在 Windows 报路径语法错误 | `rg` 不接受该位置的 PowerShell 通配路径 | 改用 `rg -g 'make_dsp_*.py' ... work` |
| 图形清单测试首次导入失败 | 从项目根运行时 `work` 不在裸模块搜索路径 | 使用 `work.build_figure_audit_inventory` 包路径导入 |
| AST 扫描第六批脚本出现 `U+FEFF` 语法错误 | 文件开头含 UTF-8 BOM | 使用 `utf-8-sig` 解码后解析 |
