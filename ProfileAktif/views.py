from django.shortcuts import render

def show_main(request):
    context = {
        'player_name': 'Marselino Ferdinan',
        'position': 'Gelandang Serang',
        'club': 'KMSK Deinze (Belgia)',
        'age': 20,
        'market_value': '€2.00 juta',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/2/24/Marselino_Ferdinan_2023.jpg'
    }

    return render(request, "main.html", context)
