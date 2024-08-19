#!/usr/bin/python3
""" Admin console """

import cmd
from backend.models import storage
from backend.models.user import User
from backend.models.shoe import Shoe
import shlex  # for splitting the line along spaces except in double quotes
# from backend.models.cart import Cart


classes = {"Shoe": Shoe, "User": User}


class JWS(cmd.Cmd):
    """ JWS console """
    prompt = '[JWS]:\t'

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    
    def do_exit(self, arg):
        """Save as quit"""
        return True

    def do_create(self, arg):
        """Creates a new instance of a class"""
        exclude = (
            'id', 'created_at', 'updated_at', '__class__'
        )
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if len(args) > 1:
            print("Error: Available Models: {User, Shoe}")
        if args[0] in classes:
            temp = {}
            obj = classes[args[0]]
            data = obj().to_dict()
            for i in data:
                if i not in exclude:
                    value = input(f'{i} ?: ')
                    temp[i] = value
            obj = obj(**temp)
            obj.save()
            print(obj.id)
            print('done')
        else:
            print("** class doesn't exist **")
            return False

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in storage.all():
                    print(storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in storage.all():
                    storage.all().pop(key)
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = storage.all()
        elif args[0] in classes:
            obj_dict = storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Updates an instance of a class
        
        Can only update one instance at a time
        """
        args = shlex.split(arg)
        if len(args) < 4:
            print("** insufficient arguments **")
            return False

        k = args[0] + "." + args[1]
        if k in storage.all():
            obj = storage.all()[k]
            attr_name = args[2]
            attr_value = args[3]
            
            # Check if the attribute exists on the object
            if hasattr(obj, attr_name):
                setattr(obj, attr_name, attr_value)
                obj.save()
                print(f"Updated {attr_name} to {attr_value}")
            else:
                print(f"** attribute {attr_name} doesn't exist **")
        else:
            print("** instance not found **")
            return False



if __name__ == '__main__':
    JWS().cmdloop()
