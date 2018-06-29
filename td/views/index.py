from django.shortcuts import render, redirect, HttpResponse


def index(request):
    from datetime import date, timedelta
    from td.models import Car, Proxy, TO, Mileage, Driver, Item

    warnings_upcoming = []
    warnings_expired = []
    today = date.today()

    for driver in Driver.objects.filter(active=True).all():
        if driver.license_date < today:
            warnings_expired.append({
                'importance': 0,
                'style': 'danger',
                'type': 'license_ending',
                'title': 'Срок действия прав закончился',
                'text': driver.short_name() + ' права кончились',
                'date': driver.license_date,
                'driver_id': driver.id
            })
        elif driver.license_date-timedelta(days=30) < today:
            warnings_upcoming.append({
                'importance': 0,
                'style': 'warning',
                'type': 'license_ending',
                'title': 'Срок действия прав заканчивается',
                'text': driver.short_name() + ' права кончаются менее чем через месяц',
                'date': driver.license_date,
                'driver_id': driver.id
            })

    for car in Car.objects.filter(active=True).all():

        # доверенности на управление -----------------------------------------------------------------------------------

        proxies = Proxy.objects.filter(car=car, end_date__gte=today, type=0, active=True).all()
        if len(proxies) == 0:
            warnings_expired.append({
                'importance': 0,
                'style': 'danger',
                'type': 'no_proxy',
                'title': 'Срок действия доверенности закончился',
                'text': 'У '+car.name+' ('+car.number+') нет ни одного водителя с доверенностью на управление',
                'car_id': car.id
            })
        else:
            for proxy in proxies:
                if proxy.end_date-timedelta(days=30) < today:
                    warnings_upcoming.append({
                        'importance': 1,
                        'style': 'danger',
                        'type': 'proxy_ending',
                        'title': 'Срок действия доверенности заканчивается',
                        'text': proxy.driver.short_name() + ': ' + proxy.get_type_display() + ' ' + car.name +
                                ' (' + car.number + ') кончается менее чем через месяц',
                        'date': proxy.end_date,
                        'car_id': car.id,
                        'proxy_id': proxy.id
                    })

        # доверенности на сервис и страховую ---------------------------------------------------------------------------

        proxies2 = Proxy.objects.filter(car=car, end_date__gte=today, active=True).exclude(type=0).all()
        for proxy in proxies2:
            if proxy.end_date < today:
                warnings_expired.append({
                    'importance': 3,
                    'style': 'warning',
                    'type': 'proxy_ending',
                    'title': 'Срок действия доверенности закончился',
                    'text': proxy.driver.short_name() + ': ' + proxy.get_type_display() + ' ' + car.name +
                            ' (' + car.number + ') кончилась',
                    'date': proxy.end_date,
                    'car_id': car.id,
                    'proxy_id': proxy.id
                })
            elif proxy.end_date - timedelta(days=30) < today:
                warnings_upcoming.append({
                    'importance': 3,
                    'style': 'warning',
                    'type': 'proxy_ending',
                    'title': 'Срок действия доверенности заканчивается',
                    'text': proxy.driver.short_name() + ': ' + proxy.get_type_display() + ' ' + car.name +
                            ' (' + car.number + ') кончается менее чем через месяц',
                    'date': proxy.end_date,
                    'car_id': car.id,
                    'proxy_id': proxy.id
                })

        # колеса  ------------------------------------------------------------------------------------------------------

        if car.tires_winter_date is not None:
            if car.tires_winter_date < today:
                warnings_expired.append({
                    'importance': 5,
                    'style': 'warning',
                    'type': 'tires_ending',
                    'title': 'Зимние шины изношены',
                    'text': 'Зимние колеса на ' + car.name + ' (' + car.number + ') вероятно уже не очень',
                    'date': car.tires_winter_date,
                    'car_id': car.id
                })
            elif car.tires_winter_date - timedelta(days=30) < today:
                warnings_upcoming.append({
                    'importance': 5,
                    'style': 'warning',
                    'type': 'card_ending',
                    'title': 'Зимние шины почти изношены',
                    'text': 'Зимние колеса на ' + car.name + ' (' + car.number + ') срок кончается менее чем через месяц',
                    'date': car.tires_winter_date,
                    'car_id': car.id
                })

        if car.tires_summer_date is not None:
            if car.tires_summer_date < today:
                warnings_expired.append({
                    'importance': 5,
                    'style': 'warning',
                    'type': 'tires_ending',
                    'title': 'Летние шины изношены',
                    'text': 'Летние колеса на ' + car.name + ' (' + car.number + ') вероятно уже не очень',
                    'date': car.tires_summer_date,
                    'car_id': car.id
                })
            elif car.tires_summer_date - timedelta(days=30) < today:
                warnings_upcoming.append({
                    'importance': 5,
                    'style': 'warning',
                    'type': 'card_ending',
                    'title': 'Летние шины почти изношены',
                    'text': 'Летние колеса на ' + car.name + ' (' + car.number + ') срок кончается менее чем через месяц',
                    'date': car.tires_summer_date,
                    'car_id': car.id
                })

        # ТО -----------------------------------------------------------------------------------------------------------

        '''to = TO.objects.filter(car=car, fact=False, date__lte=(today+timedelta(days=30))).all()

        if len(to) > 0:
            for t in to:
                if t.date > today:
                    warnings_upcoming.append({
                        'importance': 3,
                        'style': 'warning',
                        'type': 'to_coming',
                        'title': 'Запланированное ТО',
                        'text': 'ТО ' + car.name + ' (' + car.number + ') было запланировано на '
                                + str(t.date.strftime('%d.%m.%Y')),
                        'date': t.date,
                        'car_id': car.id,
                        'to_id': t.id
                    })
                else:
                    warnings_expired.append({
                        'importance': 3,
                        'style': 'danger',
                        'type': 'to_coming',
                        'title': 'Запланированное ТО пропущено',
                        'text': 'ТО ' + car.name + ' (' + car.number + ') было запланировано на '
                                + str(t.date.strftime('%d.%m.%Y')),
                        'date': t.date,
                        'car_id': car.id,
                        'to_id': t.id
                    })

        last_mileage = Mileage.objects.filter(car=car).order_by('-value').first()
        last_to = TO.objects.filter(car=car, fact=True).order_by('-date').first()

        if last_to is not None and last_mileage is not None:
            if last_mileage.value >= last_to.mileage + car.to_mileage:
                diff = last_mileage.value - (last_to.mileage + car.to_mileage)
                warnings_expired.append({
                    'importance': 2,
                    'style': 'danger',
                    'type': 'to_missed',
                    'title': 'Пробег превысил установленный между ТО интервал',
                    'text': car.name + ' (' + car.number + ') проехал ' + str(diff) + 'км сверх допустимого для ТО',
                    'car_id': car.id,
                    'next_to': TO.objects.filter(car=car, fact=False).order_by('date').first()
                })'''

    for item in Item.objects.filter(active=True, end_date__isnull=False):
        if item.end_date < today:
            warnings_expired.append({
                'importance': 2,
                'style': 'danger',
                'type': 'item_ending',
                'title': item.get_type_display() + ' срок кончился',
                'text': item.get_type_display() + ' на ' + item.car.name + ' (' + item.car.number + ') срок кончился',
                'date': item.end_date,
                'car_id': item.car.id,
                'item_id': item.id
            })
        elif item.end_date - timedelta(days=30) < today:
            warnings_upcoming.append({
                'importance': 3,
                'style': 'warning',
                'type': 'item_ending',
                'title': item.get_type_display() + ' срок кончается',
                'text': item.get_type_display() + ' на ' + item.car.name + ' (' + item.car.number + ') срок кончается менее чем через месяц',
                'date': item.end_date,
                'car_id': item.car.id,
                'item_id': item.id
            })

    warnings_expired.sort(key=lambda x: x['importance'])
    warnings_upcoming.sort(key=lambda x: x['importance'])

    context = {
        'warnings_expired': warnings_expired,
        'warnings_upcoming': warnings_upcoming,
    }
    return render(request, 'td/index.html', context)
