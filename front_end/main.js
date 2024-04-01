const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const cors = require('cors');

const { app, BrowserWindow } = require('electron');

const appExpress = express();
const PORT = process.env.PORT || 3000;
const dbPath = 'D:\\data\\users.sqlite';
const publicPath = path.join(__dirname, 'public');

appExpress.use(bodyParser.json());
appExpress.use(cors()); // 使用 CORS 中间件

// 创建数据库连接
const db = new sqlite3.Database(dbPath);

// 创建用户表
db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)");
});

// 模拟用户数据
const users = [
    { id: 1, username: 'user1', password: 'password1' },
    { id: 2, username: 'user2', password: 'password2' },
    // 添加更多用户...
];

// 将模拟用户数据插入数据库
db.serialize(() => {
    const stmt = db.prepare("INSERT INTO users (username, password) VALUES (?, ?)");
    users.forEach(user => {
        stmt.run(user.username, user.password);
    });
    stmt.finalize();
});

// 用户登录路由
appExpress.post('/login', (req, res) => {
    const { username, password } = req.body;
    db.get("SELECT * FROM users WHERE username = ? AND password = ?", [username, password], (err, user) => {
        if (err || !user) {
            res.json({ success: false, message: 'Invalid username or password' });
        } else {
            res.json({ success: true });
        }
    });
});

// 静态文件中间件，用于提供静态文件
appExpress.use(express.static(publicPath));

// 启动 Express 服务器
appExpress.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

// 创建 Electron 窗口
function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: false, // 在渲染器进程中禁用Node.js集成
            contextIsolation: true, // 启用上下文隔离
            preload: path.join(__dirname, 'preload.js') // preload脚本的路径
        }
    });

    win.loadFile('public/login.html'); // 加载login.html文件
}


// 在 Electron 就绪时创建窗口
app.whenReady().then(createWindow);
