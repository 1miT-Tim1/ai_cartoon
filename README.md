# ai_cartoon

# 🎨 AI 卡通肖像大师

> 上传一张人像照片，AI 帮你生成专属卡通头像

## 📖 项目简介

这是一个基于 Flask 和 ModelScope DCT-Net 模型的 Web 应用。用户上传照片后，系统自动识别面部特征，生成高质量卡通化头像。

**核心特性：**
- 🔐 用户注册/登录系统
- 🖼️ 一键上传，秒级生成卡通头像，可自行选择风格
- 🎯 基于ModelScope里深度学习模型
- 📱 响应式设计，支持 PC 和移动端
- 💾 历史作品自动保存

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| **Flask** | Web 框架 |
| **ModelScope** | AI 模型调用 |
| **DCT-Net** | 人脸卡通化 |
| **OpenCV** | 图像预处理 |
| **Flask-Login** | 用户认证 |
| **Flask-SQLAlchemy** | 数据库 ORM |
| **SQLite** | 数据库（开发环境） |
| **Bootstrap** | 前端样式 |

## 🚀 快速开始

### 环境要求

- Python 3.11（**必须**，3.12+ 不兼容 TensorFlow）
- pip 包管理器

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/AI_cartoon.git
cd AI_cartoon

# 2. 创建虚拟环境（Python 3.11）
py -3.11 -m venv .venv

# 3. 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 初始化数据库
flask db init
flask db migrate -m "init database"
flask db upgrade

# 6. 运行项目
python app.py
```

访问 http://127.0.0.1:5000 即可使用。

首次运行注意事项

· 首次启动会自动下载 DCT-Net 模型（约 500MB），请保持网络畅通
· 下载可能需要 3-5 分钟，请耐心等待
