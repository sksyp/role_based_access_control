from src.classes.Registry import Registry
from src.classes.User import User, view_message


def main():
    user_list = []
    register = Registry()
    register.add_role('admin')
    register.add_resource('design', 'python')
    register.allow('admin', 'view', 'design')
    register.allow('admin', 'create', 'design')
    register.allow('admin', 'update', 'design')
    register.allow('admin', 'delete', 'design')
    admin_user = User('admin')
    admin_user.add_roles('admin')
    user_list.append(admin_user)
    current_user = admin_user
    while True:
        view_message(current_user)

        print("Press 4 to quit")
        s = int(input())
        if s == 4:
            exit(0)
        if s == 1:
            print("Enter user name")
            name = input()
            flag = True
            for user in user_list:
                if user.name == name:
                    current_user = user
                    flag = False
            if flag:
                print("User does not exist")
        if 'admin' in current_user.get_roles():
            if s == 2:
                print("Enter User Name")
                name = input()
                user_list.append(User(name))

            if s == 3:
                print("Enter role name")
                s = input()
                register.add_role(s)
        else:
            if s == 2:
                print(current_user.get_roles())

            if s == 3:
                print(register.get_resources())


if __name__ == '__main__':
    main()
