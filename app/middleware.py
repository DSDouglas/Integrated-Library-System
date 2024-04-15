from datetime import datetime
from .models import Book


class RemoveOverdueHoldsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Remove overdue holds on first load
        if not request.session.get("overdue_holds_removed"):
            Book.objects.filter(on_hold=True, hold_end__lt=datetime.now()).update(
                on_hold=False, hold_end=None
            )
            request.session["overdue_holds_removed"] = True

        response = self.get_response(request)
        return response
