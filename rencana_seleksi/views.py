from django.views import generic
from django.urls import reverse_lazy
from .models import (rencana_seleksinya)
from django.shortcuts import render
from django.db import connection

import requests
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
import json

# Create your views here.
def api_get_judulby_tahun(request, tahun):
    if request.user.is_authenticated:
        if request.method == 'GET':
            my_list = []

            query = "SELECT id, judul FROM rencana_seleksi_rencana_seleksinya WHERE tahun::text LIKE %s"
            params = [f"%{tahun}%"]

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()

                for row in results:
                    obj = {
                        "id": row[0],
                        "judul": row[1],
                    }
                    my_list.append(obj)

            return JsonResponse(my_list, safe=False)
            # return HttpResponse(queryset)
