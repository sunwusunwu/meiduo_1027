from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData


class User(AbstractUser):
    """自定义用户类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_email_verify_url(self):
        """生成激活邮箱url"""
        # 创建加密的序列化器
        serializer = TJWSSerializer(settings.SECRET_KEY, 3600 * 24)
        # 调用dumps方法加密
        data = {'user_id': self.id, 'email': self.email}
        token = serializer.dumps(data).decode()
        # 拼接url
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token
        return verify_url

    @staticmethod
    def check_verify_email_token(token):
        """解密token并查询对应的user"""
        # 创建加密序列化器
        serializer = TJWSSerializer(settings.SECRET_KEY, 3600 * 24)
        # loads解密和查询user
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            user_id = data.get('user_id')
            email = data.get('email')
            try:
                user = User.objects.get(id=user_id, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user