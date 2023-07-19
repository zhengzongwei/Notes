# terminaltables

## 简介

从字符串列表中轻松绘制终端/控制台应用程序中的表。支持多行。

## 安装

```bash
pip install terminaltables
```

## 用法

```python
from terminaltables import AsciiTable

table_data = [
    ['Heading1', 'Heading2'],
    ['row1 column1', 'row1 column2'],
    ['row2 column1', 'row2 column2'],
    ['row3 column1', 'row3 column2']
]
table = AsciiTable(table_data)
print
table.table
```

```bash
+--------------+--------------+
| Heading1     | Heading2     |
+--------------+--------------+
| row1 column1 | row1 column2 |
| row2 column1 | row2 column2 |
| row3 column1 | row3 column2 |
+--------------+--------------+
```



## 参考链接

1. [terminaltables · PyPI](https://pypi.org/project/terminaltables/)

   

  

