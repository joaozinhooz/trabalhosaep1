import sqlite3

conn = sqlite3.connect('atividades.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM turma")
turmas = cursor.fetchall()
print(turmas)

cursor.execute("SELECT * FROM atividade")
atividades = cursor.fetchall()
print(atividades)

conn.close()
