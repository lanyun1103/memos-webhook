import sqlite3

# 连接到数据库
conn = sqlite3.connect('/root/data/docker_data/memos/.memos/memos_prod.db')

# 创建一个游标对象
cursor = conn.cursor()

# 指定表名并查询表结构
table_name = 'main'
cursor.execute(f"PRAGMA table_info({table_name})")

# 获取查询结果
table_info = cursor.fetchall()

# 打印表结构
for column_info in table_info:
    print(column_info)

# 关闭数据库连接
conn.close()

