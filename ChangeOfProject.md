## 修改记录

### 1. 用户的源文件：`install.inf`
* **修改内容**：将 `AddReg = Scheme.Reg,Wreg` 修改为了 `AddReg = Scheme.Reg`。
* **修改原因**：绕过 capeify 解析脚本中将逗号（`,`）错误剔除导致合并成 `Scheme.RegWreg` 的 Bug。以此解决了运行报错 `TypeError: 'NoneType' object is not iterable` 的问题，让代码正确读取包含鼠标映射的长串区块。

### 2. 核心控制脚本：`Capeify/main.py`
* **修改内容①：添加鼠标坐标及尺寸的缩放运算**
  * **功能**：在处理 `.cur` 和 `.ani` 循环中，对 `w`、`h`、`hs_x`、`hs_y` 均除以了 `scale_factor` 进行等比缩小。
  * **原因**：Windows 指针转到 macOS/Mousecape 下会由于 DPI / 逻辑像素处理差异而显得巨大（通常为2倍以上大小），因此需要在组装 XML 前对长宽和点击热点坐标做出修正。
* **修改内容②：增加一次性全局交互选择**
  * **功能**：在 `convert` 函数执行之初，通过 `input()` 获取用户的“分辨率策略”和“最终缩放因子（1/2/5/10）”选项。
  * **原因**：避免针对每个鼠标文件重复询问，让同一目录下的所有鼠标基于同一种配置进行统一缩放及分辨率抽取。
* **修改内容③：元数据（作者及主题名）自定义**
  * **功能**：替换了末尾直接使用 `args.path`（提取文件夹名称）作为 `Author` 和 `CapeName` 的硬编码行为，改为了让用户自定义输入（或增加对应的 argparse 参数）。
  * **原因**：修复了生成的 `.cape` 内作者变为毫无意义的哈希文件夹名的问题。

### 3. 光标抽取脚本：`Capeify/scripts/cur/convert2png.py`
* **修改内容**：添加了让用户选择分辨率的函数（如 `get_resolution_choice`），并重写了 `convert_cur2png` 加入 `resolution_index` 参数（或者匹配特定大小的 lambda 函数）。
* **原因**：原作者代码中写死了 `max(cur.sequence, key=lambda im: im.width * im.height)` 来获取文件里图层最大的一张。改动后即可由用户手动决定是提取原图结构底层的最大值、最小值或是指定清晰度的图层。
