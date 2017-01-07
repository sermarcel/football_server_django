from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from random import randint
from mysql.connector import connect
from django.template.context_processors import request
from django.views import View
from _datetime import timedelta
from datetime import datetime

def league_table(request):
   sql = '''select * from Teams order by points desc;'''
   username= "root"
   passwd= "coderslab"
   hostname= "localhost"
   db_name= "projekt_1"
   
   

   try:
       cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
       cursor = cnx.cursor()
       cursor.execute(sql)
       teams_from_cursor=cursor.fetchall()
       
       #answer="<html><body>"
       #for row in cursor:
       #    answer += "<a href='games?id={}'>{}</a><br>".format(row[0],row)
       #answer+= "</body></html>"   #        cnx.commit()
   except:
       raise
   
   finally:
       cursor.close()
       cnx.close()
       ctx={'title':'Lista zespołów','teams':teams_from_cursor}
       
       return render(request, 'tables',ctx)


    

def games_played(request):
    
    my_fav =4

    if request.method == 'GET':
        if request.GET.get('id'):
            try:
                my_fav = request.GET.get('id')
            except ValueError:
                return HttpResponse ('Id druzyny musi być liczba')
        

    sql = '''select t.name, t2.name, g.team_away_goals, g.team_home_goals  from Games g

        join Teams t on g.team_home=t.id
        join Teams t2 on g.team_away=t2.id 
        where g.team_home = {} or g.team_away = {}'''.format(my_fav, my_fav)

    
    username = 'root'
    passwd = 'coderslab'
    hostname = 'localhost'
    db_name = 'projekt_1'


    try:    
        cnx = connect (user = username, password=passwd, host=hostname, database=db_name)
        cursor = cnx.cursor()
        
        print(sql)
      
        cursor.execute(sql)
        anwser = '<html><body>'
        for r in cursor:
            anwser += '<p> %s grał z %s wynik %s : %s </p>' % r
        anwser+= '</body'    
        cursor.close()
        cnx.close() 
        return HttpResponse (anwser)
    except:
        raise


def show_games(request, clubid):



    sql = '''select t.name, t2.name  from Games g

        join Teams t on g.team_home=t.id
        join Teams t2 on g.team_away=t2.id 
        where g.team_home = {} or g.team_away = {}'''.format(clubid, clubid)
   
    username= "root"
    passwd= "coderslab"
    hostname= "localhost"
    db_name= "projekt_1"
       
   

    
    cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
    cursor = cnx.cursor()
    cursor.execute(sql)

    answer="<html><body>"
    for r in cursor:
        answer += '<p> %s moze grać na wyjeździe z %s, który gra w domu </p>' % r
    answer+= "</body></html>"   #        cnx.commit()


    cursor.close()
    cnx.close()
    return HttpResponse(answer)

def list_players(request):
    
    sql='''select p.username,t.id, t.name from Players p join Teams t on p.team=t.id order by p.username;'''
    
    username= "root"
    passwd= "coderslab"
    hostname= "localhost"
    db_name= "projekt_1"
       
    
    cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
    cursor = cnx.cursor()
    cursor.execute(sql)
    
    answer='''
        <table>
            
        '''
    
    for r in cursor:
        answer+='''
                <tr>
                    <td>{}</td>
                    <td><a href='games?id={}'>{}</a></td>
                   </tr>       
                          '''.format(r[0],r[1],r[2])
    
    answer+='''</table>'''

    cursor.close()
    cnx.close()
    return HttpResponse(answer)


def show_player(request,player_id):
    
    sql = '''select p.name,p.surname,p.position, p.number, t.name from Players p join Teams t
on p.team=t.id where p.id={}'''.format(player_id)
    
    username= "root"
    passwd= "coderslab"
    hostname= "localhost"
    db_name= "projekt_1"
       
    
    cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
    cursor = cnx.cursor()
    cursor.execute(sql)
    
    print(sql)
    print(cursor)
    
    for r in cursor:
        answer='''
        <form>

    
            <label><h3>Imię</h3></label>
            <label>{}</label>
            
            <label><h3>Nazwisko</h3></label>
            <label>{}</label>
            
            <label><h3>Pozycja</h3></label>
            <label>{}</label>
            
            <label><h3>Numer</h3></label>
            <label>{}</label>
            
            <label><h3>Klub</h3></label>
            <label>{}</label>
            
        </form>'''.format(r[0],r[1],r[2],r[3],r[4])
    
    cursor.close()
    cnx.close()

    return HttpResponse(answer)

def show_team_statistics(request,id_):        

    username= "root"
    passwd= "coderslab"
    hostname= "localhost"
    db_name= "projekt_1"
       
    
    cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
    cursor = cnx.cursor()
 
            
    sql='''select t.name, t.id,sum(team_home_goals),sum(team_away_goals), count(team_away), count(team_home) from Games g
     
     join Teams t on g.team_home=t.id where t.id={}
     
     group by t.name, t.id'''.format(id_)
     
    cursor.execute(sql)
    
    print(sql)
    
    answer='<html> <body>' 
    
    for r in cursor:
        answer+='''<p>Nazwa:{} <br>Suma bramek home: {} <br>Suma bramek na wyjeździe: {} <br>Liczba gier na wyjeździe: {} <br> Liczba gier home: {}<br></p>''' \
                    .format(r[0],r[2],r[3],r[4],r[5])
    answer+='</body></html>'
    
    #  fetchone() -- funkcja cursora, która zwraca jedna rzecz ktora jest np na pierwszym miejscu listy
    #  zamyk równiez kursor
    return HttpResponse (answer)
    

class ShowPlayer2 (View): # zadanie zrobione metodą GET - powyżej zrobione metodą http
    
    def get(self,request):
    
        if request.method=="GET":
            try:
                id=request.GET.get("id")
                id=int(id)
            except ValueError: 
                return HttpResponse ("Należy podać liczbę")
            
            username= "root"
            passwd= "coderslab"
            hostname= "localhost"
            db_name= "projekt_1"
               
    
            cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
            cursor = cnx.cursor()
            
            sql = '''select p.name,p.surname,p.position, p.number, t.name from Players p join Teams t
            on p.team=t.id where p.id={}'''.format(id)
            
            cursor.execute(sql)
            # contact_for_cursor=cursor.fetchone()
            
            
            
            data_from_cursor=cursor.fetchone()
            '''for r in cursor:            
                imie=r[0]
                nazwisko=r[1]
                pozycja=r[2]
                numer=r[3]
                klub=r[4]'''
            print(data_from_cursor)
            if data_from_cursor ==None:
                raise Http404('Nie znaleziono zawodnika')
            else:
                cursor.close()
                cnx.close()
                
            
                ctx={'dane':data_from_cursor}
                
                return render(request, 'players.html', ctx)
                
        else:
            
            return HttpResponse ("Nie użyto metody GET")
        
class ShowTeam(View):
    
    def get(self, request):
    
        if request.method=="GET":
            try:
                id=request.GET.get("id")
                id=int(id)
            
            except ValueError: 
                return HttpResponse ("Należy podać liczbę")
            
            username= "root"
            passwd= "coderslab"
            hostname= "localhost"
            db_name= "projekt_1"
               
    
            cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
            cursor = cnx.cursor()
            
            sql = '''select name, points from Teams where id={}'''.format(id)
            
            
            
            sql1 = '''select t.name as home_name, t2.name as away_name, g.team_away_goals, g.team_home_goals from Games g  
            join Teams t on t.id=g.team_home
            join Teams t2 on g.team_away=t2.id 
            where team_away = {} or team_home = {}'''.format(id, id)
            
           

            sql2 ='''select p.* from Players p join Teams t on p.team=t.id where p.team = {}
            '''.format(id)

            cursor.execute(sql)

            
            for r in cursor:            
                name=r[0]
                points=r[1]
            
            try:
                print(name)
            except UnboundLocalError:
                raise Http404
            
            
            
            cursor.execute(sql1)
            
            results_from_cursor=cursor.fetchall()
            
            '''for r in cursor:            
                home_name=r[0]
                away_name=r[1]
                team_away_goals=r[2]
                team_home_goals=r[3]'''
            print (results_from_cursor)
            cursor.execute(sql2)
            
            '''for r in cursor:            
                
                player_name=r[1]
                surname=r[2]
                position=r[3]
                number=r[4]'''
            players_from_cursor=cursor.fetchall()
            
            print (players_from_cursor)    
            print (name)
            #cursor.close()
            #cnx.close()
            
            ctx={'players':players_from_cursor,
                 'results':results_from_cursor,
                 'name':name,
                 'points':points
                 
                 }
            
                
            return render(request, 'teams.html',ctx)
                
def transfer_player(request, player_id, from_club, to_club):
    pass #  nie robie bo to powtorka z baz danych

class SetFavorite(View):
    
    def get(self,request):
        
        club_id=request.GET.get("id")
        try:
            club_id=int(club_id)
        except TypeError:
            raise 'Musi być liczba całkowita'
        
        username= "root"
        passwd= "coderslab"
        hostname= "localhost"
        db_name= "projekt_1"
           
    
        cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
        cursor = cnx.cursor()
            
        sql = '''select name, points, id from Teams where id={}'''.format(club_id)
        
        cursor.execute(sql)
        
        
        for r in cursor:
            club_name=r[2]
            
        try:
            print (club_name)
        except UnboundLocalError:
            raise Http404
        
        cursor.close()
        cnx.close()
        
        when=datetime.now() + timedelta(365)
        response=HttpResponse("dodano cookie")
        response.set_cookie('favorite_team',club_name, expires=when)
        return response
        
        
            
    
                    
                