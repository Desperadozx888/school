name = 'John Snow'  # (1) REPLACE THE STRING VARIABLE WITH YOUR NAME in string type
student_num = '1234567' # (2) REPLACE THIS STRING VARIABLE WITH YOUR UOW ID in string type
subject_code = 'CSIT110' # do not comment the first 4 lines. 
someone_who_inspires_you = ''

#=========insert solution to question 1 here=============#
class SalesStaff:
    def __init__(self, param):
        self.name = param["name"]
        self.presents_wrapped = param["presents_wrapped"]
    
    @classmethod
    def dict_to_cls_obj(cls, param): #[{},{},{},...]
        return_val = []
        # for each_dict in the list
        for each_dict in param:
            #create an instance with each_dict
            instance = cls(each_dict)
            #append instance to list
            return_val.append(instance)
        # return list of instances
        return return_val
    
    def get_weighted_stats(self, weights):
        weighted_results = 0
        for each_key in weights:
            if each_key in self.presents_wrapped:
                weighted_results += weights[each_key]*self.presents_wrapped[each_key]
            else:
                raise RecordNotFoundError(each_key, self.name)
        return weighted_results
    

#============end of solution to question 1===============#
#=========insert solution to question 2 here=============#
class RecordNotFoundError(Exception):
    def __init__(self, name_present, name_staff):
        self.name_present = name_present
        self.name_staff = name_staff
    def __str__(self):
        return f"There is no record of {self.name_present} in {self.name_staff}'s results"


#============end of solution to question 2===============#
#=========insert solution to question 3 here=============#
def count_presents_unit_test(cls_ref):
    try:
        obj = cls_ref()
        val = obj.count_presents()
        # return val
        # return obj.count_presents()
    except AttributeError:
        return 400
    except ValueError:
        return -1
    except:
        return 404
    else:
        return val

#============end of solution to question 3===============#
#=========insert solution to question 4 here=============#
class InvalidDepthError(Exception):
    def __str__(self):
        return "Invalid Depth"


class WaterBody:
    RHO = 997
    G = 9.81

    def __init__(self, vol):
        self.volume = vol

    @classmethod
    def get_hydrostatic_pressure(cls, depth: float):
        if depth < 0:
            raise InvalidDepthError()
        return cls.RHO*cls.G*depth

    @staticmethod
    def compute_density(mass, volume):
        return mass/volume

    def get_water_mass(self):
        return WaterBody.RHO*self.volume


#============end of solution to question 4===============#


def myClass_demo_unit_test(inputClass):
    """ This example takes in a class definition as input,
        then instantiates a class object and test its method
        in a try except system. 
    """
    try:
        obj = inputClass()
        obj.demo()
    except ValueError as e:
        print('A ValueError was raised because ' + str(e))


def example():
    # A class with one method
    class MyClass(): 
        def __init__(self):
            pass
        def demo(self):
            raise ValueError('Wrong input given!')
    # test the demo method
    myClass_demo_unit_test(MyClass)


def main():
    print("Assignment4")

    list_instances = SalesStaff.dict_to_cls_obj(
        [
            { "name": "Alfie",
                "presents_wrapped": {
                    "toys": 3,
                    "gadgets": 5,
                    "clothes": 4,
                },
            },{
                "name": "Jafarine",
                "presents_wrapped": {
                    "cosmetics": 1,
                    "clothes": 5,
                },
            }]
    )
    for each_instance in list_instances:
        print( each_instance.name)
        print(each_instance.presents_wrapped)
   
    example()
    """an example function that creates a class and feeds into
    the class into the myClass_demo_unit_test for testing
    You are free to create your own test subjects that raise
    errors to test your code here."""
    staff = SalesStaff(
        {"name":"John", "presents_wrapped": {}})
    try:
        staff.get_weighted_stats({"key":3})
    except RecordNotFoundError as e:
        print(" raised correct error")
        if str(e) == "Number of key wrapped is not found in John's record":
            print('string is ok')
        else:
            print("__str__ not ok")


    class AttrErrorTester(): 
        def __init__(self):
            pass
        def count_presents(self):
            raise AttributeError('Wrong input given!')
    
    class OtherErrorTester(): 
        def __init__(self):
            pass
        def count_presents(self):
            raise SyntaxError('Wrong input given!')

    class NoErrorTester(): 
        def __init__(self):
            pass
        def count_presents(self):
            return 8

    if(count_presents_unit_test(AttrErrorTester)==400):
        print("ok")
    else:
        count_presents_unit_test(AttrErrorTester)
    print(count_presents_unit_test(OtherErrorTester)==404)
    print(count_presents_unit_test(NoErrorTester)==8)

    
if __name__ == '__main__':  ## DO NOT EDIT THESE TWO LINES.Y
    main()
    def print_dict(param, lvl=1):
        print('{')
        for key in param:
            print("\t"*lvl, end="")
            print(repr(key), end=": ")
            val = param[key]
            if isinstance(val, dict):
                print_dict(val, lvl+1)
            elif isinstance(val, str):
                print(f'"{val}"', end= "")
            else:
                print(val, end="")
            if key != list(param.keys())[-1]:
                print(",")
        print("}")
    
    print_dict({"a":1, "b":3, "c": {4:"2", 5: "2"}})

