### 1. 为了简化操作，你在 Mac 系统中做的设置

为了不用每次都输入 Docker 命令，我们对 Mac 的终端环境做了以下优化：

*   **创建了快捷别名 (Alias)**：
    在 `~/.zshrc` 文件中添加了这一行：
    `alias capeify-docker='docker run -it --rm -v "$(pwd):/app" capeify-pro'`
    *   **作用**：现在你只需在任何包含指针的文件夹下输入 `capeify-docker`，就相当于启动了那个复杂的 Docker 容器，并自动把当前 Mac 文件夹映射到了容器的 `/app` 目录。
*   **绕过了本地安装**：
    你放弃了在 macOS 13 上通过 Homebrew 安装那 2GB+ 且容易报错的依赖（ImageMagick 等），转而将所有逻辑封装在约 200MB 的 Docker 镜像中，节省了大量的系统空间和排错时间。

---

### 2. 以后调试和维护 Docker 镜像的常用命令

如果你以后想修改 `capeify` 的源码或者查看内部环境，请查阅下表：

| 动作 | 命令 | 说明 |
| :--- | :--- | :--- |
| **进入命令行** | `docker run -it --rm -v "$(pwd):/app" --entrypoint /bin/bash capeify-pro` | 覆盖默认入口，进入容器内部的 Bash。挂载当前目录到/app |
| **复制文件进容器** | `docker cp ./main.py <容器ID>:/usr/local/lib/python3.11/site-packages/Capeify/main.py` | 在容器运行状态下，把 Mac 上改好的代码推进去。 |
| **封装/保存镜像** | `docker commit --change='ENTRYPOINT ["capeify"]' <容器ID> capeify-pro` | 将调试好的容器保存为新镜像，并恢复自动运行功能。 |
| **清理空间** | `docker system prune` | 删除所有停止的容器和缓存。 |
| **导出镜像备份** | `docker save -o ~/Desktop/capeify-backup.tar capeify-pro` | 把调好的镜像存成文件，防止重装 Docker 丢失。 |

---

### 3. 从工作目录开始的完整转换步骤

当你下载了一个新的 Windows 指针包，想把它转为 Mac 的 `.cape` 时，请按此流程操作：

#### 第一步：准备工作目录
1.  进入存放 `.ani` 或 `.cur` 文件的文件夹。
2.  **关键：处理 `install.inf`**。不要直接用原版的，要按照我们调试出的“兼容版”格式修改（见下方注意事项）。
3.  确保 `install.inf` 的编码是 **UTF-8**（在 VS Code 右下角检查）。

#### 第二步：调用 Docker 执行转换
打开终端，`cd` 到该文件夹，输入：
```bash
capeify-docker-convert
```
或：
```bash
capeify-docker convert --path /app --inf-file install.inf --out my_mouse.cape
```
*(如果没设别名，就用完整的 `docker run -it --rm -v "$(pwd):/app" capeify-pro ...`)*

#### 第三步：注意事项（避坑指南）
*   **修改`install.inf`文件**：
    确保`AddReg    = Scheme.Reg`：
    ```text
    [DefaultInstall]
    CopyFiles = Scheme.Cur,Scheme.Txt
    AddReg    = Scheme.Reg
    ```
*   **Unicode 错误**：如果看到 `UnicodeDecodeError`，说明你的 `install.inf` 还是 GBK 编码，请务必转成 UTF-8。
*   **权限问题**：如果在 Docker 运行时提示权限拒绝，请检查 Docker Desktop 是否获得了访问该文件夹的权限。

#### 第四步：后续
转换完成后，你会得到一个 `result.cape`。
1.  双击它，它会导入到 **Mousecape** 软件中。
2.  在 Mousecape 里点击该主题，然后点 **Apply** 即可生效。

