# tasky-vue
## 环境配置
|Windows开发环境|Ubuntu 20.04 Linux wang-340XAA-350XAA-550XAA 6.14.0-37-generic #37~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 20 10:25:38 UTC 2 x86_64 x86_64 x86_64 GNU/Linux|
|---|---|
|Visual Studio Code 1.108.2 | Visual Studio Code  1.108.1 |
|git version 2.50.1.windows.1| git version 2.43.0 |
|Node.js v16.14.2| v20.18.0 |
|npm 8.7.0| npm 11.7.0 |
|Python 3.13.5 Conda环境| Python 3.13.11 conda 25.11.1 |

---
**对于某些符合以下两个条件的人**
①使用VSCode IDE编译项目
②计划使用Conda虚拟环境而不是系统环境变量中的Python
③使用Windows平台开发的
④使用powershell终端编译的
**你需要在终端执行 conda init powershell 命令**

---

## 项目安装
```
npm install
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
git config user.name [你的名字]
git config user.email [你的邮箱]
```

### 开发时编译并热重载
```
npm run electron:serve
```

### 编译并压缩用于生产环境
```
npm run electron:build
```

### 检查并修复文件
```
npm run lint
```
### 自定义配置
See [Configuration Reference](https://cli.vuejs.org/config/).
