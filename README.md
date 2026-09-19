# 社区商店微信群运营小程序

## 项目结构
```
community-store-miniprogram/
├── miniprogram/          # 微信小程序前端
│   ├── pages/            # 页面（login, index, product, push, mark, marks, admin）
│   ├── utils/            # 工具函数
│   ├── app.js / app.json / app.wxss
│   └── project.config.json
├── cloud/                # Python 后端（微信云托管）
│   ├── src/
│   │   ├── main.py       # FastAPI 入口
│   │   ├── models/       # 数据模型
│   │   ├── routes/       # API 路由
│   │   └── services/     # 业务逻辑
│   ├── requirements.txt
│   └── Dockerfile
└── README.md
```

## 部署
1. 配置微信云托管环境
2. 构建镜像：`docker build -t community-store -f cloud/Dockerfile .`
3. 推送至微信云托管
