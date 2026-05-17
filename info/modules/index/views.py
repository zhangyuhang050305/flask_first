import logging
from flask import current_app

from info import redis_store
from info.modules.index import index_blue

@index_blue.route('/', methods=['GET', 'POST'])
def index():
    # 测试redis存取数据
    # redis_store.set('name','laowang')
    # print(redis_store.get('name'))

    # 测试session存取
    #session['name'] = 'zhangsan'
    #print(session.get('name'))

    # 使用日志记录方法loggin进行输出可控
    logging.debug('输入调试信息')
    logging.info('输入详细信息')
    logging.warning('输入警告信息')
    logging.error('输入错误信息')

    # 使用current_app进行输出可控
    current_app.logger.debug('输入调试信息')
    current_app.logger.info('输入详细信息')
    current_app.logger.warning('输入警告信息')
    current_app.logger.error('输入错误信息')

    return 'hello world'