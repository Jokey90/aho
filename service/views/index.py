from main.backends import render_mobile as render


def index(request):
    context = {}
    return render(request, 'service/index.html', context)
