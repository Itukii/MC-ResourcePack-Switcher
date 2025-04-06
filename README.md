MinecraftResourcePack BE/Java Switcher
这是一个旨在帮助Minecraft玩家和开发者在 Minecraft Bedrock Edition 和 Java Edition 之间切换资源包的小工具。该工具目前提供了一些基本功能，允许用户通过以下方式来适配资源包：

当前功能：

Hash-based 文件对比：对比Bedrock和Java版本中相同贴图文件的哈希值，帮助用户识别和匹配对应的资源文件。

自动改名：对资源包中的纹理文件进行自动重命名，以确保符合不同版本的命名规则。

自动生成 .mcmeta 文件：为Java版资源包中的动画贴图生成对应的 .mcmeta 文件，从而确保动画效果的正常播放。

已知问题/限制：

UI不完全适配：目前提供的UI界面功能未完全适配，可能无法正常工作。

资源包不自动生成：生成的文件需要手动将 textures 文件放入Minecraft资源包中，工具并未自动创建完整的资源包结构。

功能扩展：目前工具主要支持对文件进行对比和名称修改，未来计划实现更多功能，如自动转换完整资源包格式等。

未来目标：

自动生成Minecraft资源包结构，用户可以一键生成完整的资源包文件。

完善UI界面，提升用户体验。

扩展更多对不同类型资源的支持（如声音、模型等）。

Installation
下载并解压该项目。

运行脚本后，选择Bedrock版和Java版资源包文件夹。

自动化对比和修改贴图文件，并根据需要手动构建资源包。

