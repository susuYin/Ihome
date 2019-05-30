from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from ihome import db
#####目的：开启flask框架
from ihome import creat_app

app=creat_app("pro")
#实例终端命令执行对象
manager=Manager(app)
#迁移初始化，第一个参数是flask实例， 第二个参数是数据库实例
Migrate(app,db)
#为manager添加迁移命令
manager.add_command("db",MigrateCommand)
if __name__ == '__main__':
    manager.run()