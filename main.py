
import pymysql
from app import app
from db_config import mysql
from flask import flash, render_template, request, redirect

@app.route('/new_user')
def add_user_view():
	return render_template('add.html')

# Permite guardar un registro		
@app.route('/add', methods=['POST'])
def add_user():
	try:		
		# Obtiene parametros
		_nombre = request.form['inputName']
		_email = request.form['inputEmail']

		# Valida los valores recibidos
		if _nombre and _email and request.method == 'POST':
			
			# Crea string de query
			sql = "INSERT INTO usuarios(nombre, email) VALUES(%s, %s)"
			data = (_nombre, _email)

			# Permite conectarse a la BD y ejecutar query
			conn = mysql.connect()
			cursor = conn.cursor()
			
			# Ejecuta la query
			cursor.execute(sql, data)
			conn.commit()

			# Si guarda todo OK, devuelve vista con mensaje
			flash('User added successfully!')
			return redirect('/')

		else:
			return 'Error while adding user'

	except Exception as e:
		print(e)

	finally:
		cursor.close() 
		conn.close()

# Obtiene todos los usuarios y devuelve vista		
@app.route('/')
def users():	
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM usuarios")
		rows = cursor.fetchall()		
		return render_template('users.html', usuarios=rows, total= 5000)

	except Exception as e:
		print(e)

	finally:
		cursor.close() 
		conn.close()

# Obtiene el usuario y lo entrega a la vista
@app.route('/edit/<int:id>')
def edit_view(id):
	
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM usuarios WHERE id=%s", id)
		row = cursor.fetchone()

		if row:
			return render_template('edit.html', row = row)
		else:
			return 'Error loading #{id}'.format(id=id)
			
	except Exception as e:
		print(e)

	finally:
		cursor.close()
		conn.close()

@app.route('/update', methods=['POST'])
def update_user():
	try:				
		_nombre = request.form['inputName']
		_email = request.form['inputEmail']
		_id = request.form['id']
				
		# validate the received values
		if _id and _nombre and _email and request.method == 'POST':

			# save edits
			sql = "UPDATE usuarios SET nombre=%s, email=%s WHERE id=%s"
			data = (_nombre, _email, _id)					
			
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()

			flash('User updated successfully!')
			return redirect('/')

		else:
			return 'Error while updating user'

	except Exception as e:
		print(e)

	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<int:id>')
def delete_user(id):

	try:		
		conn = mysql.connect()		
		cursor = conn.cursor()
		cursor.execute("DELETE FROM usuarios WHERE id=%s", (id))
		conn.commit()
		flash('User deleted successfully!')
		return redirect('/')

	except Exception as e:
		print(e)
		
	finally:
		cursor.close() 
		conn.close()
		
if __name__ == "__main__":
    app.run()