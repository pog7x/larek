from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.template import Context, Template


async def pepe(request):
    html = """
        {% load static %}
        <body align="center" style="background-color:magenta;">
            <img src="{% static 'pepe/pepe.svg' %}" style="width:100%;height:100%"/>
        </body>
    """
    return StreamingHttpResponse(Template(html).render(Context()))


async def pepe1(request):
    return render(request, "pepe/pepe.html", {})
