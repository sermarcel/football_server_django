
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from random import randint
from mysql.connector import connect
# Create your views here.

def say_hello(request):
    answer = """
    
    <html>
        <body>
            <p> Hello world ! </p>
        </body>
    </html>
    """ 
    return HttpResponse(answer)

def random_result(request):  # należt wpisać po random '?name='
    if request.method=="GET":
        name = request.GET['name']
        
        
    result = randint(0,100)
    answer = """
    
    <html>
        <body>
            <p> Cześć {} </p>
            <p> Random number is {} </p>
        </body>
    </html>
    """ .format(name,result)
    return HttpResponse(answer)


def random_result2 (request, max_number):
    result = randint(0,int(max_number))
    
    answer = """
    
    <html>
        <body>
            <p> Użytkownik podał wartość %s </p>
            <p> Wylosowano liczbę %s </p>
        </body>
    </html>
    """ % (int(max_number), result)
    return HttpResponse(answer)
    
def random_result3 (request, min_number, max_number):
    
    result = randint(int(min_number),int(max_number))
    
    answer = """
    
    <html>
        <body>
            <p> Użytkownik podał wartość %s i %s </p>
            <p> Wylosowano liczbę %s </p>
        </body>
    </html>
    """ % (int(min_number),int(max_number), result)
    return HttpResponse(answer)

def y_name(request, name1):     
    answer = """
    
    <html>
        <body>
            <p> Witaj %s </p>
        </body>
    </html>
    """ % str(name1)
    return HttpResponse(answer)
    



def print_2 (request):  # wykorzystanie GET napierw '?' i '&'

    if request.method == 'GET':
        numbers=[]

        if request.GET.get('start') and request.GET.get('end'):
            start = request.GET.get('start')
            end = request.GET.get('end')

        else:
            return HttpResponse('Brakuje parametru')
        try:

            for num in range (int(start)+1,int(end)):        
                numbers.append(num)

        except ValueError:
            return HttpResponse('Parametr musi być liczba')

        if start > end:
            return HttpResponse ('Start wieksze od end')
    else:
        return HttpResponse('Metoda not GET' )    
    
    html = """
    
    <html>
        <body>
            <p> Twoje liczby to {} i {}, a liczby pomiędzy to {}  </p>
        </body>
    </html>
    """.format(start, end, numbers)
    '''
    response=HttpResponse()
    response.write('<ul>')
    for num in range (start,end):
        response.write("<li>%s</li>" % num)
    response.write("</ul>")
    '''
    return HttpResponse(html)


    

def multiply (request):

    if request.method == 'GET':
        w = request.GET.get('w')
        h = request.GET.get ('h')

    if w and h:
        response = HttpResponse()
        response.write('<table>')
        w = int(w)
        h = int(h)
    
    response= HttpResponse()
    response.write('<html><body><table>')
    
    for num in range (1, h + 1):
        response.write ('<tr>')

        for num2 in range (1, w + 1):
            response.write ('<td>{}</td>'.format( num2 * num))
        response.write('</tr>')
    response.write('</table>')
    


    return response




def print_ (request):

    if request.method == 'GET':
        numbers=[]

        if request.GET.get('start') and request.GET.get('end'):
            start = request.GET.get('start')
            end = request.GET.get('end')

        #if start > end:
         #   return HttpResponse ('Start wieksze od end')

        else:
            return HttpResponse('Brakuje parametru')
        try:

            response = HttpResponse()
            response.write ('<ul>')
            for num in range(int(start)+1,int(end)):
                response.write("<li>%s</li>" % num)
            response.write('</ul>')
            #for num in range (int(start)+1,int(end)):        
             #   numbers.append(num)

        except ValueError:
            return HttpResponse('Parametrem musi być liczba')

    else:
        return HttpResponse('Metoda not GET' )    
    
    '''html = """
    
    <html>
        <body>
            <p> Twoje liczby to {} i {}, a liczby pomiędzy to {}  </p>
        </body>
    </html>
    """.format(start, end, numbers)'''
    '''
    response=HttpResponse()
    response.write('<ul>')
    for num in range (start,end):
        response.write("<li>%s</li>" % num)
    response.write("</ul>")
    '''
    return response
     
    
    




