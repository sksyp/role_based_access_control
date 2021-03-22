def view_message(user):
    if 'admin' in user.roles:
        print("You are logged in as admin")
        print("Press 1 to login as another user")
        print("Press 2 to create user")
        print("Press 3 to edit role")
    else:
        print("You are logged in as " + user.name)
        print("Press 1 to login as another user")
        print("Press 2 to view roles")
        print("Press 3 to access resources")


class User:
    def __init__(self, name):
        self.name = name
        self.roles = []

    def add_roles(self, role):
        # check_permission()
        if role not in self.roles:
            self.roles.append(role)
        else:
            print('User already has the entered role')

    def get_roles(self):
        return self.roles

    def get_name(self):
        return self.name

    def remove_role(self, role):
        if role in self.roles:
            self.roles.pop(role)
        else:
            print('User does not have the entered role')
