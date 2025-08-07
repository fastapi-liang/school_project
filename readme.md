# 学生管理接口文档

---

## 1. 根据班级获取学生信息

### 请求

`GET api/students_by_class/`

### 请求参数

| 参数名 | 类型   | 必填 | 说明     | 位置  |
|--------|--------|------|----------|-------|
| name   | string | 是   | 班级名称 | query |

### 响应示例

```json
[
  {
    "id": 1,
    "name": "刘德华",
    "gender": "M",
    "student_id": "111",
    "class_name": 1
  },
  {
    "id": 2,
    "name": "郭德纲",
    "gender": "M",
    "student_id": "122",
    "class_name": 1
  }
]
```
## 2. 根据学生姓名获取学生信息

### 请求

`GET /student_by_name/`

### 请求参数

| 参数名 | 类型   | 必填 | 说明     | 位置  |
|--------|--------|------|----------|-------|
| name   | string | 是   | 学生姓名 | query |

### 响应示例

```json
{
  "id": 1,
  "name": "刘德华",
  "gender": "M",
  "student_id": "111",
  "class_name": "清华班"
}
```


## 3. 创建学生

### 请求

`POST /students/`

### 请求体示例

```json
{
  "name": "张三",
  "gender": "M",
  "student_id": "200",
  "class_name": 1
}
```

## 4. 更新学生信息（全部更新）

### 请求

`PUT api/students/{pk}/`

### 路径参数

| 参数名 | 类型 | 说明   |
|--------|------|--------|
| pk     | int  | 学生ID |

### 请求体示例

```json
{
  "name": "张三",
  "gender": "M",
  "student_id": "200",
  "class_name": 1
}
`````

## 5. 更新学生信息（部分更新）

### 请求

`PATCH api/students/{pk}/```

### 路径参数

| 参数名 | 类型 | 说明   |
|--------|------|--------|
| pk     | int  | 学生ID |

### 请求体示例

```json
{
  "name": "张三丰"
}