from django.db import models


class Area(models.Model):
    """省市区行政区，外键自关联"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='上级行政区')
    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政划区'
        verbose_name_plural = '行政划区'

    def __str__(self):
        return self.name
