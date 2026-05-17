"""
相关配置
1.数据库配置：为了在项目中用来存储新闻数据以及用户数据的
2.redis配置：缓存访问频率高的内容，存储session信息，图片验证码，短信验证码
3.session配置:将来用来保存用户的登录信息
4.csrf配置:保护app，防止csrf攻击
"""
from info import create_app

# 调用方法获取app
app = create_app('development')



if __name__ == '__main__':
    app.run()