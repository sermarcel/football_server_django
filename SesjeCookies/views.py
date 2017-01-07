from django.shortcuts import render
from django.http import HttpResponse, response
from django.views.decorators.csrf import csrf_exempt
from mysql.connector import connect
from django.http import HttpResponseRedirect
from django.views import View

COUNTER='counter'

class SetSession(View):
    def get(self,request):
        request.session['counter'] = 0
        return HttpResponse("counter wyzerowany")
    
class ShowSession(View):
    def get (self,request):
        if COUNTER in request.session: # sprawdzamy czy counter istnieje
            counter=request.session.get(COUNTER) # odbieram counter
            print(counter)
            counter=int(counter)
            counter+=1 # dodajemy +1
            request.session[COUNTER] = counter
            return HttpResponse ("Counter = {}".format(counter))
            
        else:
            return HttpResponse("Counter nie istnieje")

class DeleteSession(View):
    def get (self,request):
        if COUNTER in request.session: # sprawdzamy czy counter istnieje
            del(request.session[COUNTER])
            return HttpResponse("Counter usunięty")
        else:
            return HttpResponse ("Counter nie istnieje")
      

        
class Login(View):
    
    def get(self,request):
        
        if 'loggedUser' in request.session:
            loggedUser= request.session.get("loggedUser") 
            ctx = {'name': loggedUser}
            return render(request, "hello.html", ctx)
        else:
            return render(request, "login_form.html")
    
    def post(self,request):
        
        action= request.POST.get("login")
        if action =="logout":
            if 'loggedUser' in request.session['loggedUser']:
                del (request.session["loggedUser"])
            return render(request,"login_form.html")
        
        elif action=="login":
        
            user_name = request.POST.get("name")
            request.session["loggedUser"]=user_name
            
            ctx={'name':user_name}
            
            return render(request, "hello.html", ctx)
VALUE='value'
KEY='key'
class AddSession(View):
    
    
    def get(self,request):
        
    
        return render(request, 'add.html')
    
    def post(self,request):
        
        if request.POST.get("adding"):
        
            value=request.POST.get('value')
            key=request.POST.get("key")
            print (key)
            
            sql='insert into Keys1 values ({},{})'.format(key,value)
            print(sql)
            
            username= "root"
            passwd= "coderslab"
            hostname= "localhost"
            db_name= "projekt_1"
           
            try:
               
                cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
                cursor = cnx.cursor()
                cursor.execute(sql)
                cnx.commit()
            except:
                raise
            
            return HttpResponse ("poprawne dodanie")
        
        if request.POST.get("results"):
        
        
            sql = '''select * from Keys1;'''
            username= "root"
            passwd= "coderslab"
            hostname= "localhost"
            db_name= "projekt_1"

   

        try:
            cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
            cursor = cnx.cursor()
            cursor.execute(sql)
            keys_from_cursor=cursor.fetchall()
        
        except:
            raise
        
        cursor.close()
        cnx.close()
        ctx={'klucze':keys_from_cursor}
       
        return render(request,"odczyt_kluczy.html",ctx)
    
        
        
class SetCookies(View):
    
    def get(self, request):
        
        response =HttpResponse("Setting cookie")
        response.set_cookie("User", "Marcin")
        return response
        
        
        
class ShowCookie(View):
        
    def get(self,request):
        if "User" in request.COOKIES:
            user_name = request.COOKIES.get("User")
            return HttpResponse("User: {}".format(user_name))
        else: 
            return HttpResponse ("cookie nie istnieje")
    
class DelCookie(View):
        
        def get(self,request):
            response= HttpResponse()
            response.write("Deleting cookie")
            if "User" in request.COOKIES:
                response.delete_cookie("User")
            return response
            
class SetCookie2(View):
    
    def get(self, request):
        userName = "Marcinek"
        ctx={"name": userName}
        response = render(request, "przyklad_cookies.html", ctx)
        response.set_cookie("User", userName)
        return response
    
class AddCookie (View):      
    
    def get (self,request):
        
        return render(request, "add_to_cookie.html")
        
        # return render(request,'add_to_cookie.html')
    
    def post (self,request):
        
        if request.POST.get('adding'):
            value1=request.POST.get("value")
            key1=request.POST.get("key")
            response=HttpResponse("Dodano cookie")
            response.set_cookie(key1, value1)
            return response
        
class ShowAllCookies(View):
    
    def get (self, request):
        
        keys=[]
        values=[]
        for k in request.COOKIES:
            keys.append(k)     
            v=request.COOKIES.get(k)
            values.append(v)
        print (keys)
        ctx={"klucz": keys, "wartosc":values}
        
        return render(request,"show_all_cookies.html",ctx)
        
        
    
    
    