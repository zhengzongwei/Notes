# alembic 操作

1. 查看当前数据库迁移版本

   ```bash
   alembic current
   ```

2. 升级数据库

   ```bash
   alembic upgrade head
   ```

3. 查看未应用的迁移

   ```bash
   alembic history
   ```

4. 列出未应用的迁移

   ```bash
   alembic heads
   ```

5. 同步数据库版本

   ```bash
   alembic stamp head
   ```

6. 重新生成迁移文件

   ```bash
   alembic revision --autogenerate -m "message"
   ```

   