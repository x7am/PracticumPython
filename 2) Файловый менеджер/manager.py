from options import root_folder
import os, shutil, sys
import zipfile
import time

def cdr(*args):
    '''
    Change directory. Смена директории.ss Для шага вверх по директориям нужно ввести две точки. Для текущей директории одна точка (как и во всех файловых менеджерах.)
    '''
    global current_path
    if len(args) == 0 or len(args) > 1:
        print('Введите путь, по которому перемещаемся.')
    else:
        if args[0] == '..':
            if current_path[1] != '/':
                prevdir = current_path[1].rfind('/')
                try:
                    if prevdir == 0:
                        os.chdir(current_path[0])
                        current_path = [current_path[0], '/'+os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                    else:
                        os.chdir(current_path[0]+current_path[1][:prevdir])
                        current_path = [current_path[0], os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                except PermissionError:
                    print(f'Недостаточно прав.')
            else:
                print('Вы достигли корневого раздела.')
        elif args[0] == '.':
            pass
        elif args[0][0] == '/':
            if os.path.exists(current_path[0]+args[0]):
                try:
                    os.chdir(current_path[0]+args[0])
                    if len(args[0]) == 1:
                        current_path = [current_path[0], '/'+os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                    else:
                        current_path = [current_path[0], os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                except PermissionError:
                    print(f'Недостаточно прав.')
            else:
                print('Указанной директории не существует.')
        else:
            if os.path.exists(current_path[0]+current_path[1]+'/'+args[0]):
                try:
                    os.chdir(current_path[0]+current_path[1]+'/'+args[0])
                    current_path = [current_path[0], os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                except PermissionError:
                    print(f'Недостаточно прав.')
            else:
                print('Указанной директории не существует.')

def adr(*args):
    '''
    Add directory. Функция создания директории. Можно создать несколько директорий, если ввести несколько аргументов.
    '''
    if len(args) == 0:
        print('Введите название создаваемой папки.')
    else:
        if len(args) > 1: 
            if input('Вы ввели несколько параметров, хотите создать несколько папок? (Y/n) ').lower() not in ['y', 'д']:
                return
        for name in args:
            try:
                os.mkdir(name)
            except FileExistsError:
                print(f'Создаваемая папка уже существует [{name}].')
            except PermissionError:
                print(f'Недостаточно прав.')

def ddr(*args):
    '''
    Delete directory. Удаление директории. Можно удалить несколько папок, если ввести несколько аргументов.
    '''
    if len(args) == 0:
        print('Введите название удаляемой папки.')
    else:
        if len(args) > 1: 
            if input('Вы ввели несколько параметров, хотите удалить несколько папок? (Y/n) ').lower() not in ['y', 'д']:
                return
        for name in args:
            try:
                os.rmdir(name)
            except FileNotFoundError:
                print(f'Указанной папки не существует [{name}].')
            except PermissionError:
                print(f'Недостаточно прав.')

def afl(*args):
    '''
    Add file. Создание файла. Можно создать несколько файлов, если ввести несколько аргументов.
    '''
    if len(args) == 0:
        print('Введите название создаваемого файла (с расширением).')
    else:
        if len(args) > 1: 
            if input('Вы ввели несколько параметров, хотите создать несколько файлов? (Y/n) ').lower() not in ['y', 'д']:
                return
        for name in args:
            if os.path.exists(current_path[0]+current_path[1]+'/'+name):
                print(f'Создаваемый файл уже существует [{name}].')
            else:
                try:
                    open(name, "w")
                except PermissionError:
                    print(f'Недостаточно прав.')

def dfl(*args):
    '''
    Delete file. Удаление файла. Можно удалить несколько файлов, если ввести несколько аргументов.
    '''
    if len(args) == 0:
        print('Введите название удаляемого файла (с расширением).')
    else:
        if len(args) > 1: 
            if input('Вы ввели несколько параметров, хотите удалить несколько файлов? (Y/n) ').lower() not in ['y', 'д']:
                return
        for name in args:
            try:
                os.remove(name)
            except FileNotFoundError:
                print(f'Указанного файла не существует [{name}].')
            except PermissionError:
                print(f'Недостаточно прав.')

def efl(*args):
    '''
    Edit file. Редактирование файла. Для выхода из редактора нужно написать 'closefile' в отдельной строке.
    '''
    if len(args) == 1:
        print("Введите 'closefile', чтобы закрыть редактор")
        try:
            with open(args[0], 'w') as file:
                while True:
                    inp = input()
                    if inp == 'closefile':
                        break
                    file.write(inp+'\n')
                    
        except FileExistsError:
            print(f'Указанный файл не существует [{args[0]}].')
        except PermissionError:
            print(f'Недостаточно прав.')
    else:
        print('Введите название файла для редактирования')

def pfl(*args):
    '''
    Print file. Вывести содержимое файла.
    '''
    if len(args) == 1:
        try:
            with open(args[0], 'r') as file:
                for line in file.readlines():
                    print(line, end = '')
            if gui:
                time.sleep(5) # чтобы увидеть содержимое файла в режиме с псевдоинтерфейсом
        except FileNotFoundError:
            print(f'Указанный файл не существует [{args[0]}].')
        except PermissionError:
            print(f'Недостаточно прав.')
    else:
        print('Введите название файла для вывода.')

def cpfl(*args):
    '''
    Copy file. Копирование файла в указанную директорию.
    '''
    if len(args) == 2:
        try:
            if args[0][0] == '/' and args[1][0] == '/':
                shutil.copy2(current_path[0]+'/'+args[0], current_path[0]+'/'+args[1]) 
            elif args[0][0] == '/':
                shutil.copy2(current_path[0]+'/'+args[0], current_path[0]+current_path[1]+'/'+args[1]) 
            elif args[1][0] == '/':
                shutil.copy2(current_path[0]+current_path[1]+'/'+args[0], current_path[0]+'/'+args[1]) 
            else:
                shutil.copy2(current_path[0]+current_path[1]+'/'+args[0], current_path[0]+current_path[1]+'/'+args[1])  
        except FileNotFoundError:
            print(f'Указанный файл не существует [{args[0]}].')
        except PermissionError:
            print(f'Недостаточно прав.')
    else:
        print('Введите старое расположение файла и новое.')
    pass

def mfl(*args):
    '''
    Move file. Перемещение файла в указанную директорию.
    '''
    if len(args) == 2:
        try:
            if args[0][0] == '/' and args[1][0] == '/':
                os.replace(current_path[0]+'/'+args[0], current_path[0]+'/'+args[1]) 
            elif args[0][0] == '/':
                os.replace(current_path[0]+'/'+args[0], current_path[0]+current_path[1]+'/'+args[1]) 
            elif args[1][0] == '/':
                os.replace(current_path[0]+current_path[1]+'/'+args[0], current_path[0]+'/'+args[1]) 
            else:
                os.replace(current_path[0]+current_path[1]+'/'+args[0], current_path[0]+current_path[1]+'/'+args[1])    
        except FileNotFoundError:
            print(f'Указанный файл не существует [{args[0]}].')
        except PermissionError:
            print(f'Недостаточно прав.')
        except:
            print(f'Неизвестная ошибка. Попробуйте ввести не просто путь до конечной директории, а путь до создаваемого нового файла.')
    else:
        print('Введите старое расположение файла и новое.')
    pass

def rfl(*args):
    '''
    Rename file. Переименовывание указанной директори или указанного файла. Напишите путь к файлу и новый путь к файлу (не новое имя).
    '''
    if len(args) == 2:
        try:
            if args[0][0] == '/':
                pass
            else:
                os.rename(current_path[0]+current_path[1]+'/'+args[0], current_path[0]+current_path[1]+'/'+args[1])
        except FileNotFoundError:
            print(f'Указанный файл не существует [{args[0]}].')
        except PermissionError:
            print(f'Недостаточно прав.')
    else:
        print('Введите текущее имя файла, а также новое имя файла.')

def zfl(*args):
    '''
    Zip file. Архивирование указанной директории или указанного файла. Введите путь к файлу/директории, а также путь к создаваемогу архиву.
    '''
    if len(args) == 2:
        try:
            if args[1][0] == '/':
                cur_zip = zipfile.ZipFile(current_path[0]+'/'+args[1], 'w')
                v = 1
            else:   
                cur_zip = zipfile.ZipFile(current_path[0]+current_path[1]+'/'+args[1], 'w')
                v = 2
            if args[0][0] == '/':
                if os.path.isdir(current_path[0]+'/'+args[0]):
                    for folder, subfolders, files in os.walk(current_path[0]+'/'+args[0]):
                        for file in files:
                            if '.' in file and file != args[1]:
                                cur_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), current_path[0]+'/'+args[0]), compress_type = zipfile.ZIP_DEFLATED)
                else:
                    cur_zip.write(current_path[0]+'/'+args[0], compress_type=zipfile.ZIP_DEFLATED)
            else:
                if os.path.isdir(current_path[0]+current_path[1]+'/'+args[0]):
                   for folder, subfolders, files in os.walk(current_path[0]+current_path[1]+'/'+args[0]):
                        for file in files:
                            if '.' in file and file != args[1]:
                                cur_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), current_path[0]+current_path[1]+'/'+args[0]), compress_type = zipfile.ZIP_DEFLATED) 
                else:
                    cur_zip.write(current_path[0]+current_path[1]+'/'+args[0], compress_type=zipfile.ZIP_DEFLATED)
            cur_zip.close()
        except FileNotFoundError:
            print(f'Указанный файл не существует [{args[0]}].')
            cur_zip.close()
            os.remove(current_path[0]+'/'+args[1]) if v == 1 else os.remove(current_path[0]+current_path[1]+'/'+args[1])
        except PermissionError:
            print(f'Недостаточно прав.')
    else:
        print('Введите путь до файла/директории, а также путь создаваемого архива.')

def uzfl(*args):
    '''
    Zip file. Архивирование указанной директории или указанного файла. Введите путь к файлу/директории, а также путь к создаваемогу архиву.
    '''
    if len(args) == 2:
        try:
            if args[1][0] == '/':
                cur_zip = zipfile.ZipFile(current_path[0]+'/'+args[0])
                v = 1
            else:   
                cur_zip = zipfile.ZipFile(current_path[0]+current_path[1]+'/'+args[0])
                v = 2
            if args[0][0] == '/':
                cur_zip.extractall(current_path[0]+'/'+args[1])
            else:
                cur_zip.extractall(current_path[0]+current_path[1]+'/'+args[1])
            cur_zip.close()
        except FileNotFoundError:
            print(f'Указанный файл не существует [{args[0]}].')
            cur_zip.close()
            os.remove(current_path[0]+'/'+args[1]) if v == 1 else os.remove(current_path[0]+current_path[1]+'/'+args[1])
        except PermissionError:
            print(f'Недостаточно прав.')
    else:
        print('Введите путь к архиву, а также папку для разархивации.')

def printHelp():
    print('''main functions:
adr [folder_path] - Создание папки (с указанием имени);
ddr [folder_path] - Удаление папки по имени;
cdr [folder_path] - Перемещение между папками (в пределах рабочей папки) - заход в папку по имени, выход на уровень вверх;
afl [file_path] - Создание пустых файлов с указанием имени;
efl [file_path] - Запись текста в файл;
pfl [file_path] - Просмотр содержимого текстового файла;
dfl [file_path] - Удаление файлов по имени;
cpfl [file/folder_path_from] [file/folder_path_to] - Копирование файлов из одной папки в другую;
mfl [file/folder_path] [new_file/folder_path] - Перемещение файлов;
rfl [file_path] [new_file_path] - Переименование файлов.
other functions:
zfl [file/folder_path] [zip_path] - Архивирование файлов;
uzfl [zip_path] [file/folder_path] - Разархивирование архива.
напишите exit или close, чтобы выйти из программы
напишите chuser, чтобы поменять пользователя''')

def main():
    global current_path
    while True:
        command = input(f'FileManager:{current_path[1]}$ ').split()
        if len(command) != 0:
            if command[0] == 'exit' or command[0] == 'close':
                break
            if command[0] == 'chuser':
                authorization(login, passw)
                print(f'логин: {login}')
                current_path = [root_folder+'/'+login, '/'+os.getcwd()[len(root_folder+'/'+login):].replace('\\', '/')]
                os.chdir(current_path[0])
            elif command[0] == 'help':
                printHelp()
            else:
                try:
                    commands[command[0]](*command[1:])
                except KeyError:
                    print('Неправильная команда. Команды можно посмотреть, написав "help".')
                except TypeError:
                    print('Неправильный формат ввода.')
        print()

def gui_main():
    global current_path
    while True:
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
        print('Текущая директория: '+current_path[1])
        print(f'Логин: {login}')
        if sys.platform == 'win32':
            os.system('dir /X /OG /A')
        else:
            os.system('ls -l')
        print()
        command = input(f'FileManager:{current_path[1]}$ ').split()
        if len(command) != 0:
            if command[0] == 'exit' or command[0] == 'close':
                break
            if command[0] == 'chuser':
                authorization(login, passw)
                print(f'логин: {login}')
                current_path = [root_folder+'/'+login, '/'+os.getcwd()[len(root_folder+'/'+login):].replace('\\', '/')]
                os.chdir(current_path[0])
            elif command[0] == 'help':
                printHelp()
            else:
                try:
                    commands[command[0]](*command[1:])
                except KeyError:
                    print('Неправильная команда. Команды можно посмотреть, написав "help".')
                except TypeError:
                    print('Неправильный формат ввода.')


def authorization(prevlogin='', prevpassw=''):
    global login, passw, current_path
    logged = False
    isreg = False
    err = False
    while not logged:
        if not isreg:
            login = input('enter your login (enter "reg" for registration): ')
        if "reg" in login or isreg == True:
            isreg = True
            login = input('choose login: ')
            if login in userinfo:
                print('Имя пользователя занято.')
                continue
            passw = input('choose password: ')
            userinfo[login] = passw
            with open('users.txt', 'w') as file:
                print(userinfo, file = file)
            try:
                os.mkdir(root_folder+'/'+login)
            except:
                print('Имя пользователя не занято, но папка уже существует. Обратитесь к администратору.')
                err = True
            if not err:
                print('successful registration.')
            logged = True
        else:
            passw = input ('enter your password: ')
            if login in userinfo:
                for userl, userp in userinfo.items():
                    if login == userl and passw == userp:
                        print('logged in.')
                        logged = True
            if not logged:
                print('wrong login or password')
                for i in range(3,0, -1):
                    print(f'timeout {i} sec')
                    time.sleep(1)
    if err:
        if prevlogin != '':
            login = prevlogin
            passw = prevpassw
            print('Возвращен предыдущий пользователь.')
        else:
            print('Попробуйте снова.')
            sys.exit()

if __name__ == '__main__':
    commands = {'adr': adr, 'ddr': ddr, 'cdr': cdr, 'afl': afl, 'efl': efl, 'pfl': pfl, 'dfl': dfl, 'cpfl': cpfl, 'mfl': mfl, 'rfl': rfl, 'zfl': zfl, 'uzfl': uzfl}
    userinfo = {}
    with open('users.txt', 'r') as file:
        for line in file.readlines():
            userinfo = eval(line)

    authorization()
    print()

    current_path = [root_folder+'/'+login]
    os.chdir(current_path[0])
    current_path.append('/'+os.getcwd()[len(root_folder+'/'+login):].replace('\\', '/'))
    if 'gui' in input('gui or console version? '):
        gui = True
        gui_main()
    else:
        gui = False
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
        print(f'логин: {login}', end = '\n\n')
        main()