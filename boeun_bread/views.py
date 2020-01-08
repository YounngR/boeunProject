from django.shortcuts import render


def main(request):
    return render(request,'boeun_bread/main.html')

def manage(request):
    return render(request,'manage/manage_main.html')
