# API文档模板

## 基本信息
- 名称：{接口名称}
- 描述：{简要描述}
- 版本：{版本号}
- 作者：{作者}

## 接口定义

### 请求信息
- Method: {GET|POST|PUT|DELETE}
- URL: {接口地址}
- Content-Type: {数据类型}

### 请求参数
| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| param1 | string | 是 | - | 参数1描述 |
| param2 | number | 否 | 0 | 参数2描述 |

### 响应结果
```json
{
    "code": 0,
    "message": "success",
    "data": {
        "key": "value"
    }
}
```

### 响应参数
| 参数名 | 类型 | 描述 |
|--------|------|------|
| code | number | 响应码 |
| message | string | 响应消息 |
| data | object | 响应数据 |

## 错误码
| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 400 | 参数错误 | 检查参数 |
| 401 | 未授权 | 重新登录 |

## 示例代码
```javascript
// 请求示例
const response = await fetch('/api/endpoint', {
  method: 'POST',
  body: JSON.stringify({ param1: 'value1' })
});
```

## 变更历史
| 版本 | 变更日期 | 变更内容 | 作者 |
|------|----------|----------|------|
| 1.0.0 | 2025-06-28 | 初始版本 | @jackycchen |

最后更新：2025-06-28 23:34:11 UTC
当前用户：@jackycchen
```