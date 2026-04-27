# 🖼️ Image Tools Pro

**免费图片处理API** - 压缩、格式转换、调整大小

## ✨ 功能

| 功能 | 说明 | API路径 |
|------|------|---------|
| 图片压缩 | 可调节质量，减小体积 | POST /compress |
| 格式转换 | PNG/JPEG/WEBP/BMP/GIF互转 | POST /convert |
| 调整大小 | 自定义尺寸，支持保持比例 | POST /resize |

## 🚀 部署

### Docker
\`\`\`bash
docker build -t image-tools .
docker run -d -p 5050:5050 image-tools
\`\`\`

### 测试
\`\`\`bash
curl -X POST http://localhost:5050/compress \
  -F "file=@test.png" \
  -F "quality=75" \
  --output compressed.jpg
\`\`\`

## 💰 端点说明

### POST /compress
压缩图片
- file: 图片文件 (必填)
- quality: 质量 1-100 (默认75)

### POST /convert
转换格式
- file: 图片文件 (必填)
- format: PNG/JPEG/WEBP/BMP/GIF (默认WEBP)

### POST /resize
调整大小
- file: 图片文件 (必填)
- width: 宽度像素 (可选)
- height: 高度像素 (可选)

## 📜 License

MIT
