from django.db import models


class GoodsCategory(models.Model):
    cag_name = models.CharField(max_length=30)
    cag_css = models.CharField(max_length=20)
    cag_img = models.ImageField(upload_to='cag')

    class Meta:
        ordering = ('cag_name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.cag_name


class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=100)
    goods_price = models.IntegerField(default=0)
    goods_desc = models.CharField(max_length=2000)
    goods_img = models.ImageField(upload_to='goods',
                                  blank=True)
    goods_stock = models.IntegerField(default=1)
    goods_cag = models.ForeignKey(
        GoodsCategory,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.goods_name