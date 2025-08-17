from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe


def home(requests):
    context = {
        'total': '2',
    }
    return render(requests, 'index.html', context)


stripe.api_key = settings.STRIPE_SECRET_KEY
@csrf_exempt
def checkout(request):
    """
    Is possible to test the checkout with test cards numbers:
    https://docs.stripe.com/testing#international-cards
    """
    if request.method == 'POST':
        name = 'Video'
        try:
            total = int(request.POST.get('total')) * 100 # EUR to cents
            country = request.POST.get('country')
            complex_name = request.POST.get('complex_name')
            date = request.POST.get('date')
            time = request.POST.get('time')
            name += f' {country} > {complex_name} > {date} > {time}'
        except (ValueError, TypeError):
            total = 100  # Security fallback, 1 EUR

        home_url = request.build_absolute_uri(reverse('home'))

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': name,
                    },
                    'unit_amount': total,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=home_url + '?status=success',
            cancel_url=home_url + '?status=cancel',
        )
        return redirect(session.url, code=303)
    return redirect('home')


def video(requests):
    context = {
        "video_url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    }
    return render(requests, 'video.html', context)
