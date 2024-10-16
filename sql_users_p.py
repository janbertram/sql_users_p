import csv
import random

def create_username(first_name, last_name, database):
    first = create_safe_name(first_name)[:3]
    last = create_safe_name(last_name)[:3]
    username = '{}{}{}'.format(database[0].lower(), first, last)
    return username

def create_safe_name(name):
    safe_name = ''
    safe_letters = 'abcdefghijklmnopqrstuvwxyz'
    for letter in name.lower():
        if letter in safe_letters:
            safe_name += letter
        elif letter == 'ä':
            safe_name += 'ae'
        elif letter == 'ö':
            safe_name += 'oe'
        elif letter == 'ü':
            safe_name += 'ue'
    return safe_name

def create_password():
    password = '{}{}{}{}{}{}{}'.format(consonise(),
                                       vocalise(),
                                       consonise(),
                                       consonise(),
                                       vocalise(),
                                       consonise(),
                                       two_digit_numberstring())
    return password

def vocalise():
    return 'aeiou'[random.randint(0, 4)]

def consonise():
    return 'bcdfghjklmnpqrstvwxyz'[random.randint(0, 20)]

def two_digit_numberstring():
    return str(random.randint(10, 99))

def write_files(database, user_data_csv, sender):
    sql_commands = open('users.sql', 'a')
    welcome_msgs = open('welcome.txt', 'a')

    sql_commands.write("CREATE DATABASE IF NOT EXISTS {} COLLATE utf8_german2_ci;\n".format(database))
    welcome_msgs.write('# Nutzer_innen der Datenbank {}:\n\n'.format(database))
    
    with open (user_data_csv, encoding='utf-8-sig') as user_data:
        reader = csv.DictReader(user_data, delimiter=',')
        for row in reader:
            
            user_name = create_username(row['Vorname'], row['Nachname'], database)
            password = create_password()
            salutation = 'Liebe/r'
            if 'Geschlecht' in row:
                if row['Geschlecht'].lower() == 'w':
                    salutation = 'Liebe'
                elif row['Geschlecht'].lower() == 'm':
                    salutation = 'Lieber'
            
            sql_commands.write("CREATE USER '{}'@'%' IDENTIFIED BY '{}';\n"
                               "GRANT SELECT, INSERT, UPDATE, DELETE ON {}.* TO '{}'@'%';\n"
                               "CREATE DATABASE IF NOT EXISTS {};\n"
                               "GRANT ALL PRIVILEGES ON {}.* TO '{}'@'%';\n".format(user_name, password, database, user_name, user_name, user_name, user_name))

            welcome_msgs.write("{} {},\n\n"
                               "Dein Nutzername für den Datenbankzugriff ist:\n"
                               "{}\n"
                               "Das Passwort lautet:\n"
                               "{}\n"
                               "Mit herzlichen Grüßen\n"
                               "\n"
                               "{}\n\n".format(salutation, row['Vorname'], user_name, password, sender))

    sql_commands.close()
    welcome_msgs.write('\n---\n')
    welcome_msgs.close()

def main():
    go_on = True
    while go_on:
        database = input('Name der Datenbank: ')
        user_data_csv = input('Name der csv-Datei (erste Zeile enthält '
                              'die Überschriften "Vorname" und "Nachname"): ')
        sender = input('Name des Absenders: ')
        try:
            write_files(database, user_data_csv, sender)
        except Exception as ex:
            print('Leider hat etwas nicht geklappt.')
            print(ex.__class__, ':', ex)
        user_in = input('Geben Sie "q" ein, um zu beenden. ')
        if user_in == 'q':
            go_on = False

if __name__ == '__main__':
    main()
