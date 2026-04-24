from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    pass


class InfoGame(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2)
    genre = models.CharField(_("Жанр"), max_length=100)

    class Meta:
        verbose_name = _("Игра")
        verbose_name_plural = _("Игры")


class PurchasedGame(models.Model):
    info = models.ForeignKey(InfoGame, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bought_game')
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    hours_played = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"You played in this game {self.hours_played}"


class ShoppingCartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items', verbose_name="Пользователь")
    game = models.ForeignKey(InfoGame,on_delete=models.CASCADE,verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество товара")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ['user', 'game']

    def __str__(self):
        return f"{self.user.name} — {self.game.name} ({self.quantity} шт.)"


class GameCatalog(models.Model):
    name = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    image = models.ImageField('Изображение', upload_to='images/',
                              blank=True, null=True, default='images/default.jpg')
