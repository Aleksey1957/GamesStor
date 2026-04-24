from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages

from .forms import CustomUserCreationForm
from .models import InfoGame, ShoppingCartItem, CustomUser, PurchasedGame


@login_required
def home(request):
    cart_count = ShoppingCartItem.objects.filter(user=request.user).count()
    games_count = InfoGame.objects.count()

    return render(request, "home.html", {
        "cart_count": cart_count,
        "games_count": games_count,
    })


def main(request):
    games = InfoGame.objects.all()

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = ShoppingCartItem.objects.filter(user=request.user).count()

    return render(request, "main.html", {
        "games": games,
        "cart_count": cart_count,
    })


def items_list(request):
    games = InfoGame.objects.all()
    return render(request, "products_list.html", {'games': games})


def product_card(request, game_id):
    game = get_object_or_404(InfoGame, id=game_id)

    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = PurchasedGame.objects.filter(user=request.user, info=game).exists()

    similar_games = InfoGame.objects.filter(genre=game.genre).exclude(id=game.id)[:4]

    return render(request, "product.html", {
        'game': game,
        'is_purchased': is_purchased,
        'similar_games': similar_games,
    })


@login_required
def shopping_cart(request):
    cart_items = ShoppingCartItem.objects.filter(user=request.user)

    for item in cart_items:
        item.total = item.game.price * item.quantity

    total_price = sum(item.total for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "total_quantity": total_quantity,
    })


@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(InfoGame, id=game_id)

    cart_item, created = ShoppingCartItem.objects.get_or_create(
        user=request.user,
        game=game
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество "{game.name}" увеличено в корзине')
    else:
        messages.success(request, f'Игра "{game.name}" добавлена в корзину')

    return redirect("items_list")


@login_required
def remove_from_cart(request, game_id):
    cart_item = get_object_or_404(ShoppingCartItem, user=request.user, game_id=game_id)
    game_name = cart_item.game.name
    cart_item.delete()
    messages.success(request, f'Игра "{game_name}" удалена из корзины')
    return redirect("shopping_cart")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "sign_up.html", {"form": form})


@login_required
def profile(request):
    purchased_games_count = PurchasedGame.objects.filter(user=request.user).count()

    total_hours = PurchasedGame.objects.filter(user=request.user).aggregate(
        total=Sum('hours_played')
    )
    total_hours_played = total_hours['total'] if total_hours['total'] else 0

    cart_items_count = ShoppingCartItem.objects.filter(user=request.user).count()

    recent_purchases = PurchasedGame.objects.filter(
        user=request.user
    ).select_related('info').order_by('-id')[:4]

    return render(request, "profile.html", {
        'purchased_games_count': purchased_games_count,
        'total_hours_played': total_hours_played,
        'cart_items_count': cart_items_count,
        'recent_purchases': recent_purchases,
    })


def logout_account(request):
    return render(request, "logout_now.html")