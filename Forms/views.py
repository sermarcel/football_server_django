from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from mysql.connector import connect
from django.http import HttpResponseRedirect
from mysql.connector.errors import ProgrammingError
from pip._vendor.requests.sessions import session
from django.views import View


@csrf_exempt
def degrees (request):
	form='''
		 <html>
			<form action="#" method="POST">
			    <label>
			        Temperatura:
			        <input type="number" min="0.00" step="0.01" name="degrees" value=%s>
			    </label>
			    <input type="submit" name="convertionType" value="celcToFahr">
			    <input type="submit" name="convertionType" value="FahrToCelc">
			</form>
	 	 </html>
	 	'''

	if request.method=="POST":
		temp=request.POST.get("degrees") # pobieramy temperaturę
		temp = float(temp)
		convertionType = request.POST.get ("convertionType") # ktory przycisk
		if convertionType == "celcToFahr":
			new_temp = 32 + 9/5 * temp
		else:
			new_temp = 5/8 * (temp - 32)

		print (new_temp)
		new_temp = "%.2f" % new_temp
		return HttpResponse (form % new_temp)

	return HttpResponse(form % "")
				



def name_surname(request):
	html="""<html><body>
                    %s <form action="/forms1" method="POST">
                       <label>
                           Imię:
                           <input type="text" name="name">
                       </label>
                       <label>
                           Nazwisko:
                           <input type="text" name="surname">
                       </label>
                       <label>
                           <input type="submit">Wyślij</input>
                       </label>
                       </form></body></html>"""      
	if request.method == "POST":
		name = request.POST.get("name")# sprawdza czy metoda post przesłała taka zmienna, jesli nie przesłała to zwróci None(bezpieczniej)
		surname = request.POST["surname"]# sprawdza czy metoda post przesłała taka zmienna, jesli nie przesłała to wywali program
		hello = "Hello %s %s"  %(name, surname)
		return HttpResponse(html % hello)
	else:
		return HttpResponse(html % "") 

@csrf_exempt
def add_game(request):


	sql = '''select id,name from Teams;'''
	username= "root"
	passwd= "coderslab"
	hostname= "localhost"
	db_name= "projekt_1"
  
	cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
	cursor = cnx.cursor()
	cursor.execute(sql)
	

	form='''
			 <html>
				<form action="#" method="POST">
				    <label>
				        Klub piłkarski grający u siebie:
				        <select name="played_home">'''
	for row in cursor:
		form += "<option value={}>{}</option>".format(row[0],row[1])
	form+=''' 	</select></label>
				<label>Liczba bramek
					<input type"name" name="wynik_home">
				</label>
					<br>
				'''
	cursor.execute(sql)
				
	form+='''	
				<label>
					Klub piłkarski grający na wyjeżdzie:
				    <select name="played_away">''' # zamykać selecta przy tworzeniu html
	for row in cursor:
		form += "<option value={}>{}</option>".format(row[0],row[1])
	form+=''' 	</select></label>
				
				<label>
					Liczba bramek:
					<input type"name" name="wynik_away">
				</label>
				<br><br>
				<label>
				<input type="submit" value="Wyślij"</input>
				</label>

				</form>

		 	 </html>'''
	
	if request.method=="POST":

		w_a=request.POST.get("wynik_away") # pobieramy
		w_h=request.POST.get("wynik_home") # pobieramy
		try:
			w_a=int(w_a)
			w_h=int(w_h)
		except ValueError:
			return HttpResponse ("Musi być liczba całkowita")
			
		d_a=request.POST.get("played_away")
		d_h=request.POST.get("played_home")
		
		sql1= '''INSERT INTO `Games` (`id`, `team_home`, `team_home_goals`, `team_away`, `team_away_goals`) VALUES (0, {}, {}, {}, {});'''.format(d_h,w_h, d_a, w_a)
	
		
		print(sql1)
		
		cursor.execute(sql1)
		return HttpResponseRedirect("/games?id={}".format(w_h))
	
	cnx.commit()
	cursor.close()
	cnx.close()

	return HttpResponse(form)

@csrf_exempt
def add_player2(request):
	
	
	sql = 'select id,position from Player_Position;'
	sql2= "select id,name from Teams;"
	username= "root"
	passwd= "coderslab"
	hostname= "localhost"
	db_name= "projekt_1"
  
	cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
	cursor = cnx.cursor()
	cursor.execute(sql)
	is_ok='<h2>Dziękujemy!</h2>'
	not_ok='<h2>Nie udało się przesłac danych. Błędnie wypełniony formularz</h2>'
	
	
	form='''	
				<form action="#" method="POST">
					<label>
						<h2>Dodaj zawodnika do klubu:</h2>
					</label>
					<label>Imię</label>
						<input type="text" name="name">
					<label>Nazwisko</label>
						<input type="text" name="surname">
					<label>Numer</label>
						<input type="text" name="number">
					
					<label>Pozycja</label>
						<select name="pozycja">'''
	for row in cursor:
		form +='<option value={}>{}</option>'.format(row[1], row[1])
							
	cursor.execute(sql2)

	form+=''' 	</select>
				<br><br><br>
				<label> Klub </label>
					<select name="klub">'''
	for row in cursor:
		form +='<option value={}>{}</option>'.format(row[0], row[1])
	form+='''	</select>
				<input type="submit" value="Dodaj"</input>
				</form>
				'''
	
	if request.method=="POST":
		player_name=request.POST.get('name')
		player_surname=request.POST.get('surname')
		player_number=request.POST.get('number')
		player_position=request.POST.get('pozycja')
		player_club=request.POST.get('klub')
		
		sql3='''INSERT INTO `Players` (`name`, `surname`, `position`, `number`,`team`) 
VALUES ('{}', '{}', '{}', {}, {});'''.format(player_name,player_surname,player_position, \
											player_number, player_club)
		print(sql3)
		try:
			cursor.execute(sql3)
			cnx.commit()
			return HttpResponse(is_ok)
		except ProgrammingError:
			return HttpResponse(not_ok)
			
		
		finally:
			cursor.close()
			cnx.close()
		
		
	return HttpResponse(form)



#player_session='player_session'
	
class AddPlayer(View):

	def get(self,request):
	
	
		sql = 'select id,position from Player_Position;'
		sql2= "select id,name from Teams;"
		username= "root"
		passwd= "coderslab"
		hostname= "localhost"
		db_name= "projekt_1"
	  
		cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
		cursor = cnx.cursor()
		cursor.execute(sql)
		
		
		
		positon_from_cursor=cursor.fetchall()
		cursor.execute(sql2)
		teams_from_cursor=cursor.fetchall()
					
		
		if 'player_session' in request.session:
			player_session=request.session.get('player_session')
		
			player_session=int(player_session)
		print(player_session)
			
		ctx={'position':positon_from_cursor,
				'teams': teams_from_cursor,
				'default_klub': player_session
				}	
	
		return render(request, "add_player.html",ctx)
	
	
	def post(self,request):			
		
		username= "root"
		passwd= "coderslab"
		hostname= "localhost"
		db_name= "projekt_1"
		cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
		cursor = cnx.cursor()
		
		is_ok='<h2>Dziękujemy!</h2>'
		not_ok='<h2>Nie udało się przesłac danych. Błędnie wypełniony formularz</h2>'
		
		
		player_name=request.POST.get('name')
		player_surname=request.POST.get('surname')
		player_number=request.POST.get('number')
		player_position=request.POST.get('pozycja')
		player_club=request.POST.get('klub')
		
		print(player_club)
		
		#  dodanie sesji
		
		request.session["player_session"]=player_club
		
		
		sql3='''INSERT INTO `Players` (`name`, `surname`, `position`, `number`,`team`) 
		VALUES ('{}', '{}', '{}', {}, {});'''.format(player_name,player_surname,player_position, \
											player_number, player_club)
		#print(sql3)
			
			
		try:
			cursor.execute(sql3)
			cnx.commit()
			return HttpResponse(is_ok)
		except ProgrammingError:
			return HttpResponse(not_ok)
			
	
		finally:
			cursor.close()
			cnx.close()

	
