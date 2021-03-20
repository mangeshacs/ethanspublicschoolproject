import pickle
import maskpass
import os
import hashlib


def get_user_data(param):
    if os.path.exists('user_details'):
        u_details = open('user_details', 'rb')
        db = pickle.load(u_details)
        # for keys in db:
        #     print(db[keys]['name'])
        #     print(keys, '=>', db[keys])
        u_details.close()
        for keys in db:
            if db[keys]['username'] == param and db[keys]['occupation'] == 'teacher':
                return db[keys]
            elif db[keys]['username'] == param and db[keys]['occupation'] == 'student':
                return db[keys]
        else:
            return{}
    else:
        return {}


def get_student_data(stud_roll_no=0, name=''):
    if os.path.exists('student_result_details'):
        with open('student_result_details', 'rb') as stud_result:
            stud_data = pickle.load(stud_result)
        # print(stud_data)
        for keys in stud_data:
            if stud_roll_no != 0:
                if stud_data[keys]['stud_rollno'] == stud_roll_no:
                    return stud_data[keys]
            elif name != '':
                # print(name)
                # print(stud_data[keys]['stud_name'])
                if stud_data[keys]['stud_name'].lower() == name.lower():
                    return stud_data[keys]
        else:
            return {}
    else:
        return {}


def create_user(opts, load_dict):
    teacher = dict()
    stud = dict()
    if opts == 1:
        username = input('Enter Username: ')
        password = hashlib.md5(bytes(maskpass.askpass(), 'utf-8')).hexdigest()
        if len(load_dict) == 0:
            users = get_user_data(username)
            if username not in users.values():
                teacher['username'] = username
                teacher['password'] = password
                teacher['occupation'] = 'teacher'
                return teacher
            else:
                print("\'{}\' username is already present".format(username))
        else:
            if username not in load_dict.values():
                teacher['username'] = username
                teacher['password'] = password
                teacher['occupation'] = 'teacher'
                return teacher
            else:
                print("\'{}\' username is already present".format(username))

    elif opts == 2:
        stud_user = int(input("Enter Roll Number: "))
        stud_pass = hashlib.md5(bytes(maskpass.askpass(), 'utf-8')).hexdigest()
        if len(load_dict) == 0:
            users = get_user_data('student')
            if stud_user not in users.values():
                stud['username'] = stud_user
                stud['password'] = stud_pass
                stud['occupation'] = 'student'
                return stud
            else:
                print("\'{}\' username is already present".format(stud_user))
        else:
            if stud_user not in load_dict.values():
                stud['username'] = stud_user
                stud['password'] = stud_pass
                stud['occupation'] = 'student'
                return stud
            else:
                print("\'{}\' username is already present".format(stud_user))
    else:
        print("Incorrect option")


def enter_result():
    stud_name = input("Enter Student Name:")
    stud_rollno = int(input("Enter Student Roll No:"))
    stud_father_name = input("Enter Student's Father Name:")
    eng_mark = float(input("Enter English Marks:"))
    math_mark = float(input("Enter Maths Marks:"))
    sci_mark = float(input("Enter Science Marks:"))
    stud_details = {'stud_name': stud_name, 'stud_rollno': stud_rollno, 'stud_father_name': stud_father_name,
                    'eng_mark': eng_mark, 'math_mark': math_mark, 'sci_mark': sci_mark
                    }
    return stud_details


def display_roll_number(sname):
    if len(get_student_data(name=sname)) > 0:
        print("{}'s roll number is {}".format(sname.title(), get_student_data(name=sname)['stud_rollno']))
    else:
        print("There is no student having name {}".format(sname.title()))


def display_result(roll_number):
    student_details = get_student_data(stud_roll_no=roll_number)
    if len(student_details) > 0:
        print('='*48, end='\n')
        print('Ethans Public School'.center(47), end='\n')
        print('='*48, end='\n')
        print("Student Name : {}\nFather Name  : {}\nRoll number  : {}".
              format(student_details['stud_name'], student_details['stud_father_name'],
                     student_details['stud_rollno']))
        print('-'*48, end='\n')
        print("English      : {}\nMaths        : {}\nScience      : {}".
              format(student_details['eng_mark'], student_details['math_mark'],
                     student_details['sci_mark']))
        print('-'*48, end='\n')
        print("Total Marks  : {}\nPercentage   : {}\nRank         : {}".
              format(student_details['total'], student_details['percentage'],
                     student_details['rank']))
        print('-'*48, end='\n')
    else:
        print("Please enter correct roll number")


def store_student_result(result):
    students = dict()
    # if os.path.exists('student_result_details'):
    #     with open('student_result_details', 'rb') as stud_result:
    #         stud_data = pickle.load(stud_result)
    for keys in result:
        total = (result[keys]['eng_mark'] + result[keys]['math_mark'] +
                 result[keys]['sci_mark'])
        percentage = total / 300 * 100
        if total not in result[keys]:
            result[keys]['total'] = round(total, 2)
        if percentage not in result[keys]:
            result[keys]['percentage'] = round(percentage, 2)
        students = result
    rank = 1
    for i in sorted(students, key=lambda x: students[x]['percentage'], reverse=True):
        if rank not in students[i]:
            students[i]['rank'] = rank
        rank += 1
    with open('student_result_details', 'wb') as stud_details:
        pickle.dump(students, stud_details)


def login_user():
    student_result = dict()
    num = 1
    ent_op = 1
    login_ops = int(input('1. Teacher\n2. Student\nEnter your option: '))
    if login_ops == 1:
        teacher_user = input("Enter Username:")
        teacher_pass = hashlib.md5(bytes(maskpass.askpass(), 'utf-8')).hexdigest()
        teachers = get_user_data(teacher_user)
        if teachers['username'] == teacher_user and teachers['password'] == teacher_pass\
                and teachers['occupation'] == 'teacher':

            while ent_op != 4:
                teach_ops = int(input('1. Enter Student Result\n2. Display Result\n'
                                      '3. Search Student Roll Number\nEnter your option: '))
                if teach_ops == 1:
                    while teach_ops != 2:
                        student_result[num] = enter_result()
                        teach_ops = int(input('1. Enter Student Result\n2. Exit\nEnter your option: '))
                        num += 1
                    if len(student_result) > 0:
                        store_student_result(student_result)
                elif teach_ops == 2:
                    roll_no = int(input('Enter Roll number:'))
                    display_result(roll_no)
                elif teach_ops == 3:
                    stud_name = input('Enter Student Name:')
                    display_roll_number(stud_name)
                else:
                    ent_op = 4

                    # with open('student_result_details', 'ab') as stud_details:
                    #     pickle.dump(student_result, stud_details)
        else:
            print("Invalid username or password")
    elif login_ops == 2:
        student_user = int(input("Enter Roll no:"))
        student_pass = hashlib.md5(bytes(maskpass.askpass(), 'utf-8')).hexdigest()
        students = get_user_data(student_user)
        if students['username'] == student_user and students['password'] == student_pass \
                and students['occupation'] == 'student':
            while ent_op != 3:
                stud_ops = int(input('1. Display Result\n2. Search Roll Number\nEnter your option: '))
                if stud_ops == 1:
                    display_result(students['username'])
                elif stud_ops == 2:
                    roll_no = int(input('Enter Roll number:'))
                    display_result(roll_no)
                else:
                    ent_op = 3


if __name__ == '__main__':
    opt = 0
    sub_opt = 0
    pickle_dict = dict()
    seq = 0
    while opt != 3:
        login_options = int(input('1. Log In\n2. Create User\n3. Exit\nEnter your option: '))
        if login_options == 1:
            login_user()
        elif login_options == 2:
            while sub_opt != 3:
                user_option = int(input('1. Teacher\n2. Student\nEnter your option: '))
                seq += 1
                if user_option == 1:
                    pickle_dict[seq] = create_user(user_option, pickle_dict)
                elif user_option == 2:
                    pickle_dict[seq] = create_user(user_option, pickle_dict)
                else:
                    sub_opt = 3
            if len(pickle_dict) > 0:
                with open('user_details', 'wb') as login_file:
                    pickle.dump(pickle_dict, login_file)
        elif login_options == 3:
            opt = 3
        else:
            print("Please enter correct option")
