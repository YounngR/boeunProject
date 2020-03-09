from django import template
import math
register = template.Library()

@register.filter
def number_format(number):
    return format(number,',')

@register.filter
def get_total(pk):
    pass
@register.filter
def get_text(text):
    if len(text) > 74:
        return text[:74]+"..."
    return text   
@register.filter
def get_qna_text(text):
    if len(text) > 66:
        return text[:66]+"..."     
    return text
@register.filter
def split_long_text(text,cnt):
    cnt = int(cnt)
    if len(text) > cnt:
        result = "" 
        start  = 0
        end    = cnt   
        length = math.ceil(len(text)/cnt)
        for i in range(length):
            result += (text[start:end]+"\n")
            start  = end 
            end    = start+cnt
        return result    
    return text    
@register.filter
def get_total(count,total):
    return count*total    
@register.filter
def split_filename(file_name):
    arr = str(file_name).split('/')
    return arr[len(arr)-1]


