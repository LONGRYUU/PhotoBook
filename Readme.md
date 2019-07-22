这是一个用Vue+Element-UI作前端，Flask+Tornado作为后端实现的web相册demo

它有基本相册的保存、查看、删除图片的功能

然后结合Image Caption技术，实现了一些图片检索、图片分类和图片信息统计的功能

在实现过程中，不但学习了许多前端的知识（虽然还是很菜

也学习了很多图像处理、自然语言处理等人工智能方面的知识（虽然还是入门

还学习了一下很多工具和框架的使用，譬如nginx、flask等

做得不是很精致，但还是决定push上来留作纪念

或许未来这个框架可以单纯地作为一个算法模型的测试框架来使用

由于项目的运行环境较为复杂，需要安装的软件和框架较多，且需要准备数据。所以此处只能给出源码，而不能直接给出可执行文件。

### PhotoBook

前端部分工程文件比较复杂，包含许多框架自动生成的文件，仅说明其中的主要部分

- src目录：前端源码
- dist目录：编译后的文件（可以部署到服务端）
- package.json：项目依赖文件
- config：配置文件

### Server

后端部分文件，主要包括

- api：实现各个功能的接口
- app：路由配置模块
- build_dict：数据预处理时针对描述语句的处理模块
- classification：分类模块
- global_vars：全局变量
- infer：描述生成模块
- model：图像描述模型
- models：InferSent模型
- resizer：图片放缩模块
- server：调用tornado模块，用于包裹flask应用
- similarityMethods：语义相似度计算模块

