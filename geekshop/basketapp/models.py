from functools import cached_property

from django.db import models
from django.conf import settings
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @staticmethod
    def get_items(pk):
        return Basket.objects.get(pk=pk).quantity

    def save(self, *args, **kwargs):
        if self.pk:
            item = self.get_items(self.pk)
            self.product.quantity -= self.quantity - item
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(Basket, self).save(*args, **kwargs)
        # if self.pk:
        #     self.product.quantity -= self.quantity - self.__class__.get_items(int(self.pk)).quantity
        # else:
        #     self.product.quantity -= self.quantity
        # self.product.save()
        # super(self.__class__, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.save()
        super(Basket, self).delete(*args, **kwargs)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    # @property
    # def total_quantity(self):
    #     _items = Basket.objects.filter(user=self.user)
    #     _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
    #     return _totalquantity
    #
    # @property
    # def total_cost(self):
    #     _items = Basket.objects.filter(user=self.user)
    #     _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
    #     return _totalcost

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    @property
    def total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))
