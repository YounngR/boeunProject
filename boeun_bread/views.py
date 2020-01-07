from django.shortcuts import render


def main(request):
    return render(request,'boeun_bread/main.html')
