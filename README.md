模型debug：
视频识别导出的视频无计数板
摄像头识别导出的视频无法正常播放


前端未完成：
创建密码写入数据库
重设密码更新数据库
账户设置更新数据库
写入数据后统一返回登陆页面
personal center读取数据库信息并显示
集成模型和前端

使用说明：
请首先将data文件夹放在D盘根目录下，若放在其他位置请自行修改server.js中的数据库路径，注意系统读写权限问题
用户jack密码123，用户二rose密码456，未使用加密算法和登陆验证
front_end的out文件夹为打包好的前端，下载"front_end\out\make\squirrel.windows\x64\front_end-1.0.0 Setup.exe"即可直接使用前端，如需重新打包请删除"front_end\forge.config.js"和out文件夹，剩下的为前端源码。注意，需要修改package.json文件
本前端使用electron框架搭建，可参考electron说明文档https://www.electronjs.org/zh/docs/latest/tutorial/quick-start

模型在final文件夹下，相关使用说明请参阅final文件夹下的相关文档
模型源码为mediapipe-Fitness-counter-master，我们修改后的模型（fianl）添加了GUI
本项目未使用云端服务器，具体是将模型部署在本地还是服务器请自行决定
数据库使用sqlite和js读取本地数据库，如需云端数据库请自行搭建

注意！！！
由于github上传文件大小限制，front_end下的out文件夹和node_moudles文件夹我无法上传（也就是打包后的应用和electron框架），但是完整代码我已经发给下一组的组员了
如果有感兴趣的想要完整代码的可以加我私人QQ：1226733301
