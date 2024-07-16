from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import TelegramUsers
from .models import UserCard
from .models import Shop
from .models import Categories

from server.const import BOT_NAME
from server.const import HOST_DNS

class TestView(View):
    def get(self, request):
        result = []
        return JsonResponse({'result': result})
    
    # function filterCategory() {
    #     let input = document.getElementById('searchInput').value.toLowerCase();
    #     let table = document.getElementById('table');
    #     let rows = table.getElementsByTagName('tr');

    #     for (let i = 1; i < rows.length; i++) {
    #         let row = rows[i];
    #         let cells = row.getElementsByTagName('td');
    #         let rowContainsInput = false;

    #         for (let j = 0; j < cells.length; j++) {
    #             let cell = cells[j];
    #             if (cell) {
    #                 let txtValue = cell.textContent || cell.innerText;
    #                 if (txtValue.toLowerCase().indexOf(input) > -1) {
    #                     rowContainsInput = true;
    #                     break;
    #                 }
    #             }
    #         }

    #         if (rowContainsInput) {
    #             row.style.display = "";
    #         } else {
    #             row.style.display = "none";
    #         }
    #     }
    # }