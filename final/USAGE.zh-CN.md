# 维维美：使用说明

[English](USAGE.md) | **简体中文**

![九组动作预览](previews/states-overview.png)

## 预览

在浏览器中打开本说明旁边的 `index.html`，可以切换九组动作、十六个方向、深浅背景和小尺寸，无需联网。

网页中的持续播放和鼠标方向控制用于演示素材。Codex 原生客户端的播放和交互由客户端另外控制。

## 在 Windows 中安装

1. 把 `weiweimei` 文件夹复制到 `%USERPROFILE%\.codex\pets\`。如果设置了 `CODEX_HOME`，则复制到 `<CODEX_HOME>\pets\`。
2. 确认复制后的文件夹中直接包含 `weiweimei\pet.json` 和 `weiweimei\spritesheet.webp`。
3. 打开 **设置 → Pets / Mini / Mini 与虚拟宠物**，刷新列表，选择“维维美”，再打开宠物显示或唤醒 Mini。实际按钮名称可能随客户端版本变化。

需要用脚本复制并检查哈希时，在本说明所在文件夹打开 PowerShell，运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Install-Pet.ps1
```

脚本使用 `CODEX_HOME`；也可通过 `-PetCodexHome 'C:\your-codex-home'` 指定目录。遇到已有同名宠物目录会停止，不会更改当前选择或应用设置。

## 动作

| 素材 | 原生图集行 |
| --- | --- |
| 安静眨眼 | `idle` |
| 向右／向左迈步 | `running-right` / `running-left` |
| 挥手问候 | `waving` |
| 小跳 | `jumping` |
| 短暂炸毛 | `failed` |
| 耐心等待 | `waiting` |
| 思考工作 | `running` |
| 完成开心 | `review` |

![十六方向素材](previews/look-directions.png)

v2 图集中已包含十六个方向，零度朝上，顺时针每 22.5 度一帧。

## 当前限制

项目所有者已确认 Windows 原生客户端中选择、显示成功，外观正常，并观察到短暂的思考动作。

已检查的客户端中，工作动画默认播放三轮，约 2.46 秒后回到常态。素材配置无法开启持续工作循环；判断任务是否仍在运行，应查看客户端中的任务状态。

原生窗口没有持续跟随手动鼠标位置。完成、等待回应、失败、拖动和重开后仍可选尚未逐项实测。其他客户端版本和操作系统未验证。

## 检查安装包

图集为 1536 × 2288 像素，包含 73 个有效格与 15 个透明空格。`validation.json` 保存素材检查，`QA.md` 说明验证范围。

本地生成的安装 ZIP 包含 `SHA256SUMS.txt`，打包脚本还会在 ZIP 旁生成 `ZIP-SHA256.txt`。安装只需要 `weiweimei/` 中的两个文件；Python 仅用于开发和打包。

## 换回原来的宠物

在 Codex 设置中选择之前的宠物，或关闭宠物显示。切换后，若不再需要维维美，只删除新增的 `weiweimei` 文件夹即可。

## 来源

主体依据项目所有者提供的维维美参考素材，缺少动作和方向通过 ImageGen 补绘。提示词保存在 `sources/`。制作组织参考了 [zili-codex-pet](https://github.com/2846182283/zili-codex-pet)，未使用其角色图集。
