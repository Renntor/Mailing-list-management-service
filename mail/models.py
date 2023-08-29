from django.db import models

# Create your models here.

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='почта')
    full_name = models.CharField(max_length=100, verbose_name='фио')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    def __str__(self):
        return f'{self.email}, {self.full_name}, {self.comment}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class SettingMail(models.Model):
    choice_status = [
        ('create', 'Создана'),
        ('start', 'Запущена'),
        ('finish', 'Закончена'),
    ]

    choice_period = [
        (1, 'Раз в день'),
        (7, 'Раз в неделю'),
        (31, 'Раз в месяц'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')

    mailing_time = models.TimeField(verbose_name='время рассылки')
    period = models.PositiveIntegerField(choices=choice_period, verbose_name='периодичность', )
    status = models.CharField(choices=choice_status, default='create', verbose_name='статус')

    def __str__(self):
        return f'{self.mailing_time}, {self.period}, {self.status}'

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'


class Mailing(models.Model):
    setting = models.ForeignKey(SettingMail, on_delete=models.CASCADE, verbose_name='настройки')

    subject = models.TextField(default='no subject', verbose_name='тема')
    text = models.TextField(verbose_name='текст')

    def __str__(self):
        return f'{self.subject}, {self.text}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Log(models.Model):
    mail = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='сообщение')
    setting = models.ForeignKey(SettingMail, on_delete=models.CASCADE, verbose_name='настройки')

    date_last_try = models.DateTimeField(verbose_name='время последний попытки')
    status_try = models.CharField(max_length=50, verbose_name='статус')
    answer = models.TextField(**NULLABLE, verbose_name='ответ')

    def __str__(self):
        return f'{self.date_last_try}, {self.status_try}, {self.answer}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
