from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    else:
        order.created_at = "2020-11-10 14:40"
    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user).select_related("user")

    return Order.objects.select_related("user")
