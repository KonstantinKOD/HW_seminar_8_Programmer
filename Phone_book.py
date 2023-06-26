from os import path

all_data = []
last_id = 0
file_base = 'base.txt'

if not path.exists(file_base):
    with open(file_base, 'w', encoding='utf-8') as f:
        pass


def read_records():
    global all_data, last_id

    with open(file_base, encoding='utf-8') as f:
        all_data = [i.strip() for i in f]
        if all_data:
            last_id = int(all_data[-1].split()[0])
            return all_data
    return []


def show_all():
    if all_data:
        print()
        print(*all_data, sep='\n')
        print()
    else:
        print()
        print('Empty data!\n')


def exist_contact(rec_id, data):
    if rec_id:
        record_in_all_data = [i for i in all_data if rec_id in i.split()[0]]
    else:
        record_in_all_data = [i for i in all_data if data in i]
    return record_in_all_data


def add_new_record():
    global last_id

    array = ['surname', 'name', 'patronymic', 'phone number']
    answers = []
    for i in array:
        answers.append(data_verification(i))

    if not exist_contact(0, ' '.join(answers)):
        last_id += 1
        answers.insert(0, str(last_id))

        with open(file_base, 'a', encoding='utf-8') as f:
            f.write(f'{" ".join(answers)}\n')
        print('The entry has been successfully added to the phone book!\n')
    else:
        print('The data already exists!')


def ipm_bd(name):
    global file_base
    if path.exists(name):
        file_base = name
        read_records()


def exp_bd(name):

    symbol = '\n'

    change_name = f'{name}.txt'
    if not path.exists(change_name):
        with open(change_name, 'w', encoding='utf-8') as f:
            f.write(f'{symbol.join(all_data)}\n')
    else:
        print('The data already exists!')


def exp_imp_menu():
    # 1. Как я понял для импорт/экспорт должен быть указан файл?
    while True:
        print('\nExp/Imp menu:')
        move = input('1. Import\n'
                     '2. Export\n'
                     '3. exit\n')

        match move:
            case '1':
                ipm_bd(input('Enter the name of the file: '))
            case '2':
                exp_bd(input('Enter the name of the file: '))
            case '3':
                return 0
            case _:
                print('The data is not recognized, repeat the input.')


def search_contact():
    search_data = exist_contact(0, input('Enter the search data: '))
    if search_data:
        print(*search_data, sep='\n')
    else:
        print('The data is not correct!')


def edit_menu():
    add_dict = {'1': 'surname', '2': 'name', '3': 'patronymic', '4': 'phone number'}

    show_all()
    print('Enter the record id: ')
    record_id = input()

    if exist_contact(record_id, ''):
        while True:
            print('\nChanging:')
            change = input('1. surname\n'
                           '2. name\n'
                           '3. patronymic\n'
                           '4. phone number\n'
                           '5. exit\n')

            match change:
                case '1' | '2' | '3' | '4':
                    return record_id, change, data_verification(add_dict[change])
                case '5':
                    return 0
                case _:
                    print('The data is not recognized, repeat the input')

    else:
        print('The data is not correct!')


def data_verification(num):
    answer = input(f'Enter a {num}: ')
    while True:
        if num in "surname name patronymic":
            if answer.isalpha():
                break
        if num == 'phone number':
            if answer.isdigit() and len(answer) == 11:
                break
        print(f'Data is incorrect!\n'
              f'Use only the letters'
              f' of the alphabet, the length'
              f' of the number is 11 digits\n'
              f'Enter a {num}: ')
        answer = input()
    return answer


def delete():
    global all_data

    symbol = '\n'  # 2. Почему вы записали перенос на новую строку в этой переменной?
    show_all()
    del_recorde = input('Enter the record id: ')

    if exist_contact(del_recorde, ''):
        all_data = [k for k in all_data if
                    k.split()[0] != del_recorde]  # 3. почему использовалась 'k', а не привычная 'i'?

        with open(file_base, 'w', encoding='utf-8') as f:
            f.write(f'{symbol.join(all_data)}\n')
        print('Record deleted!\n')
    else:
        print('The data is not correct!')


def change_contact(data_tuple):
    global all_data
    symbol = '\n' # 4. Для чего в переменную присваивается перенос на новую строку?

    record_id, num_data, data = data_tuple

    for i, v in enumerate(all_data):
        if v.split()[0] == record_id:
            v = v.split()
            v[int(num_data)] = data
            if exist_contact(0, ' '.join(v[1:])):
                print('The data already exists!')
                return
            all_data[i] = ' '.join(v)
            break

    with open(file_base, 'w', encoding='utf-8') as f:
        f.write(f'{symbol.join(all_data)}\n')
    print('Record changed!\n')


def main_menu():
    play = True
    while play:
        read_records()
        answer = input('Phone book:\n'
                       '1. Show all records\n'
                       '2. Add a record\n'
                       '3. Search a record\n'
                       '4. Change\n'
                       '5. Delete\n'
                       '6. Imp\Exp\n'
                       '7. Exit\n')
        match answer:
            case '1':
                show_all()
            case '2':
                add_new_record()
            case '3':
                search_contact()
            case '4':
                work = edit_menu()
                if work:
                    change_contact(work)
            case '5':
                delete()
            case '6':
                exp_imp_menu()
            case '7':
                play = False
            case _:
                print("Try again!\n")


main_menu()
