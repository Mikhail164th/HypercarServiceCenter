from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

current = None

line_of_cars = {
    "change_oil": [],
    "inflate_tires": [],
    "diagnostic": [],
}

total = 0


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/welcome.html')


def menu_view(request):
    return render(request, 'tickets/menu.html')


def line_view(request, service_name):
    global total
    total +=1
    waiting_time = len(line_of_cars["change_oil"]) * 2
    if service_name != "change_oil":
        waiting_time += len(line_of_cars["inflate_tires"]) * 5
    if service_name != "inflate_tires":
         waiting_time += len(line_of_cars["diagnostic"]) * 30
    line_of_cars[service_name].append(total)
    context = {"ticket_number": total, "minutes_to_wait": waiting_time}
    return render(request, "tickets/the_ticket.html", context)


def processing_view(request):
    if request.method == 'POST':
        global current
        show_number = True
        if len(line_of_cars["change_oil"]) != 0:
            current = line_of_cars["change_oil"].pop(0)
        elif len(line_of_cars["inflate_tires"]) != 0:
            current = line_of_cars["inflate_tires"].pop(0)
        elif len(line_of_cars["diagnostic"]) != 0:
            current = line_of_cars["diagnostic"].pop(0)

        return HttpResponseRedirect(reverse('tickets:next'))
    else:
        context = {
        "change_oil": len(line_of_cars["change_oil"]),
        "inflate_tires": len(line_of_cars["inflate_tires"]),
        "diagnostic": len(line_of_cars["diagnostic"]),
    }
        return render(request, "tickets/processing.html", context)


def next_view(request):
    context = {}
    if current is None:
        context["text"] = "Waiting for the next client"
    else:
        context["text"] = f'Ticket #{current}'

    return render(request, 'tickets/next.html', context)
