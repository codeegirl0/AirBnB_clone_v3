#!/usr/bin/python3
"""
the Command interpreter 
"""
import os
import cmd
from models import base_model, user, storage, CNC

BaseModel = base_model.BaseModel
User = user.User

class HBNBCommand(cmd.Cmd):
    """
        the inerpreter class
    """
    prompt = '(hbnb) '
    ERR = [
        '** class name missing **',
        '** class doesn\'t exist **',
        '** instance id missing **',
        '** no instance found **',
        '** attribute name missing **',
        '** value missing **',
        ]

    def preloop(self):
        """
            get intro of interpreter
        """
        print('.----------------------------.')
        print('|    Welcome to hbnb CLI!    |')
        print('|   for help, input \'help\'   |')
        print('|   for quit, input \'quit\'   |')
        print('.----------------------------.')

    def postloop(self):
        """
            get exit to  interpreter
        """
        print('.----------------------------.')
        print('|  Well, that sure was fun!  |')
        print('.----------------------------.')

    def default(self, line):
        """
            the response of commands
        """
        pass

    def emptyline(self):
        """
             empty line  prompt.
        """
        pass

    def __class_err(self, arg):
        """
            private: missing  or unknown 
        """
        error = 0
        if len(arg) == 0:
            print(HBNBCommand.ERR[0])
            error = 1
        else:
            if isinstance(arg, list):
                arg = arg[0]
            if arg not in CNC.keys():
                print(HBNBCommand.ERR[1])
                error = 1
        return error

    def __id_err(self, arg):
        """
            private missing ID 
        """
        error = 0
        if (len(arg) < 2):
            error += 1
            print(HBNBCommand.ERR[2])
        if not error:
            file_storage_objs = storage.all()
            for key, value in file_storage_objs.items():
                temp_id = key.split('.')[1]
                if temp_id == arg[1] and arg[0] in key:
                    return error
            error += 1
            print(HBNBCommand.ERR[3])
        return error

    def do_airbnb(self, arg):
        """airbnb: airbnb do def
        """
        print("                      __ ___                        ")
        print("    _     _  _ _||\ |/  \ | _  _  _|_|_     _  _ _| ")
        print("|_||_)\)/(_|| (_|| \|\__/ || )(_)| |_| )\)/(_|| (_| ")
        print("   |                                                ")
        if HBNBCommand.prompt == '(hbnb) ':
            HBNBCommand.prompt = " /_ /_ _  /_\n/ //_// //_/ "
        else:
            HBNBCommand.prompt = '(hbnb) '
        arg = arg.split()
        error = self.__class_err(arg)

    def do_quit(self, line):
        """quit: do quit
        """
        return True

    def do_EOF(self, line):
        """handle EOF"""
        print()
        return True

    def __parse_string(self, value):
        """ get attribute value passed """
        value = value.strip('"').replace('_', ' ')
        index = 0
        while index < len(value):
            index = value.find('\\', index)
            if index == -1:
                break
            if value[index+1] == '"':
                value_list = list(value)
                del value_list[index]
                value = ''.join(value_list)
                index += 2
        return value

    def __parse_number(self, value):
        """ get attribute value passed  """
        if value.find('.') != -1:
            try:
                value = float(value)
            except:
                pass
        else:
            try:
                value = int(value)
            except:
                pass
        return value

    def do_create(self, arg):
        """create: do the create 
        """
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            for k, v in CNC.items():
                if k == arg[0]:
                    my_obj = v()
                    for param in arg[1:]:
                        attribute = param.split('=')
                        value = attribute[1]
                        if value[0] == '"' and value[-1] == '"':
                            value = self.__parse_string(value)
                        else:
                            value = self.__parse_number(value)
                        my_obj.bm_update(attribute[0], value)
                    my_obj.save()
                    print(my_obj.id)

    def do_show(self, arg):
        """show: showing
        """
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if not error:
            file_storage_objs = storage.all()
            for k, v in file_storage_objs.items():
                if arg[1] in k and arg[0] in k:
                    print(v)

    def do_all(self, arg):
        """all: do all
       """
        error = 0
        if arg:
            arg = arg.split()
            arg = str(arg[0])
            error = self.__class_err(arg)
        if not error:
            file_storage_objs = storage.all(arg)
            l = 0
            if arg:
                for v in file_storage_objs.values():
                    if isinstance(arg, str):
                        if type(v).__name__ == CNC[arg].__name__:
                            l += 1
                    else:
                        if type(v).__name__ == CNC[arg[0]].__name__:
                            l += 1
                c = 0
                for v in file_storage_objs.values():
                    if isinstance(arg, str):
                        if type(v).__name__ == CNC[arg].__name__:
                            c += 1
                            print(v, end=(', ' if c < l else ''))
                    else:
                        if type(v).__name__ == CNC[arg[0]].__name__:
                            c += 1
                            print(v, end=(', ' if c < l else ''))
            else:
                l = len(file_storage_objs)
                c = 0
                for v in file_storage_objs.values():
                    print(v, end=(', ' if c < l else ''))
            print()

    def do_destroy(self, arg):
        """destroy: remove
       """
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
            
        if not error:
            file_storage_objs = storage.all()
            for k in file_storage_objs.keys():
                if arg[1] in k and arg[0] in k:
                    del file_storage_objs[k]
                    storage.save()

    def __rreplace(self, s, l):
        for c in l:
            s = s.replace(c, '')
        return s

    def __check_dict(self, arg):
        """dictionary for args"""
        if '{' and '}' in arg:
            l = arg.split('{')[1]
            l = l.split(', ')
            l = list(s.split(':') for s in l)
            d = {}
            for subl in l:
                k = subl[0].strip('"\' {}')
                v = subl[1].strip('"\' {}')
                d[k] = v
            return d
        else:
            return None

    def __handle_update_err(self, arg):
        """get errors update"""
        d = self.__check_dict(arg)
        arg = self.__rreplace(arg, [',', '"'])
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)

        if not error:
            valid_id = 0
            file_storage_objs = storage.all()
            for k in file_storage_objs.keys():
                if arg[1] in k and arg[0] in k:
                    key = k
            if len(arg) < 3:
                print(HBNBCommand.ERR[4])
            elif len(arg) < 4:
                print(HBNBCommand.ERR[5])
            else:
                return [1, arg, d, file_storage_objs, key]
        return [0]

    def do_update(self, arg):
        """update: updating
        """
        arg_inv = self.__handle_update_err(arg)
        if arg_inv[0]:
            arg = arg_inv[1]
            d = arg_inv[2]
            file_storage_objs = arg_inv[3]
            key = arg_inv[4]
            if not d:
                avalue = arg[3].strip('"')
                if avalue.isdigit():
                    avalue = int(avalue)
                file_storage_objs[key].bm_update(arg[2], avalue)
            else:
                for k, v in d.items():
                    if v.isdigit():
                        v = int(v)
                    file_storage_objs[key].bm_update(k, v)

    def do_BaseModel(self, arg):
        """class method 
        """
        self.__parse_exec('BaseModel', arg)

    def do_Amenity(self, arg):
        """class method """
        self.__parse_exec('Amenity', arg)

    def do_City(self, arg):
        """class method """
        self.__parse_exec('City', arg)

    def do_Place(self, arg):
        """class method """
        self.__parse_exec('Place', arg)

    def do_Review(self, arg):
        """class method """
        self.__parse_exec('Review', arg)

    def do_State(self, arg):
        """class method """
        self.__parse_exec('State', arg)

    def do_User(self, arg):
        """class method"""
        self.__parse_exec('User', arg)

    def __count(self, arg):
        args = arg.split()
        file_storage_objs = storage.all()
        count = 0
        for k in file_storage_objs.keys():
            if args[0] in k:
                count += 1
        print(count)

    def __parse_exec(self, c, arg):
        CMD_MATCH = {
            '.all': self.do_all,
            '.count': self.__count,
            '.show': self.do_show,
            '.destroy': self.do_destroy,
            '.update': self.do_update,
            '.create': self.do_create,
        }
        if '(' and ')' in arg:
            check = arg.split('(')
            new_arg = "{} {}".format(c, check[1][:-1])
            for k, v in CMD_MATCH.items():
                if k == check[0]:
                    if ((',' or '"' in new_arg) and k != '.update'):
                        new_arg = self.__rreplace(new_arg, ['"', ','])
                    v(new_arg)
                    return
        self.default(arg)
if __name__ == '__main__':
    HBNBCommand().cmdloop()
