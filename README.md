# prime-account-dist
官匹死号账号自动分发工具
# 技术栈
 - vue3 js
 - vue-router
 - antdv
 - python
 - flask
 - sqlite
# 演示(自用)站
 - [hvhgod.onl](https://hvhgod.onl)
# 部署
 ## 前端
  - 一台装了Node 22.x的Linux/Win服务器\(推荐版本\)
  - 解压此项目至网站根目录
  - ### 安装依赖
  - ```npm i```
  - ### 构建
  - ```npm run build```
  - ### 运行
  - ```npm run preview```
  - ### 开发
  - ```npm run dev```
  - ## 注：修改.env文件的接口为你的后端接口,结尾不带/,保留http\(s\):\/\/,替换完成后重新打包
## 后端
  - 解压此项目的backend文件夹
  - cd到backend文件夹
  - ### 安装依赖
  - ```pip install -r requirements.txt```
  - ### 运行
  - ```python app.py```
  - ## 注：可修改debug模式为False
