from tortoise import Model, fields


class User(Model):
    vkontakte_id = fields.IntField(pk=True)
    token_vkadmin = fields.CharField(max_length=2048, null=True)
    token_vkme = fields.CharField(max_length=2048, null=True)
    nick_name = fields.CharField(max_length=2048, null=True)
    stats_li = fields.IntField(default=0)
    stats_dr = fields.IntField(default=0)
    stats_uv = fields.IntField(default=0)
    stats_ot = fields.IntField(default=0)
    stats_on = fields.IntField(default=0)
    stats_as = fields.IntField(default=0)
    stats_ar = fields.IntField(default=0)
    condition_li = fields.CharField(default='off', max_length=2048)
    condition_dr = fields.CharField(default='off', max_length=2048)
    condition_uv = fields.CharField(default='off', max_length=2048)
    condition_ot = fields.CharField(default='off', max_length=2048)
    condition_as = fields.CharField(default='off', max_length=2048)
    condition_ar = fields.CharField(default='off', max_length=2048)
    condition_ao = fields.CharField(default='off', max_length=2048)
    condition_on = fields.CharField(default='off', max_length=2048)
    condition_off = fields.CharField(default='off', max_length=2048)
    condition_fm = fields.CharField(default='off', max_length=2048)
    rang = fields.IntField(default=1)
    register_time = fields.IntField(default=1)  # дата блять регистрации
    text_uv = fields.CharField(default='Уведомления включил(а)!', max_length=2048)
    list_ignore = fields.CharField(default='[]', max_length=2048)
    list_trusted = fields.CharField(default='[]', max_length=2048)
    prefix_commands = fields.CharField(default='.к', max_length=2048)
    prefix_scripts = fields.CharField(default='.т', max_length=2048)
    prefix_repeats = fields.CharField(default='..', max_length=2048)
    agent = fields.IntField(default=1)
    referral = fields.IntField(default=0)
    start_time = fields.IntField(default=0)
    stop_time = fields.IntField(default=0)
    dont_clear_message = fields.CharField(default=0, max_length=2048)
    achievements = fields.CharField(default='[]', max_length=2048)
    secret_code = fields.CharField(max_length=2048, null=True)
    data_pay = fields.IntField(default=0)
    pref_luxury = fields.CharField(max_length=2048, default='.л')

    class Meta:
        table = 'users'

    @classmethod
    async def get_or_new(cls, **kwargs) -> "User":
        user, _ = await cls.get_or_create(**kwargs)
        return user


class Template(Model):
    id = fields.IntField(pk=True, generated=True)
    vkontakte_id = fields.IntField()
    name = fields.CharField(max_length=4096)
    message = fields.CharField(max_length=4096, null=True)
    attachment = fields.CharField(max_length=4096, null=True)

    class Meta:
        table = 'template'

    @classmethod
    async def get_or_new_temp(cls, **kwargs) -> "Template":
        user, _ = await cls.get_or_create(**kwargs)
        return user


class Referals(Model):
    id = fields.IntField(pk=True, generated=True)
    user_id = fields.IntField()
    reg_id = fields.IntField()

    class Meta:
        table = 'referals'

    @classmethod
    async def get_or_new_ref(cls, **kwargs) -> "Referals":
        user, _ = await cls.get_or_create(**kwargs)
        return user
