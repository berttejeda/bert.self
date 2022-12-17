class Female_Grandparent:
    def __init__(self):
        self.grandma_name = 'Grandma'

class Male_Grandparent:
    def __init__(self):
        self.grandpa_name = 'Grandpa'

class Parent(Female_Grandparent, Male_Grandparent):
    def __init__(self):
        Female_Grandparent.__init__(self)
        Male_Grandparent.__init__(self)

        self.parent_name = 'Parent Class'

class Child(Parent):
    def __init__(self):
        Parent.__init__(self)
#---------------------------------------------------------------------------------------#
        for cls in Parent.__bases__: # This block grabs the classes of the child
             cls.__init__(self)      # class (which is named 'Parent' in this case),
                                     # and iterates through them, initiating each one.
                                     # The result is that each parent, of each child,
                                     # is automatically handled upon initiation of the
                                     # dependent class. WOOT WOOT! :D
#---------------------------------------------------------------------------------------#



g = Female_Grandparent()
print(g.grandma_name)

p = Parent()
print(p.grandma_name)

child = Child()

print(child.grandma_name)

class Yellow:

    yellows_name = "Mr. Yellow"
    my_color = 'Yellow'

    def show_yellow_message(self):
        return(f'This is a message from the color {self.yellows_name}')

    def show_my_color(self):
        return(f'The color is {self.my_color}')


class Red:

    reds_name = "Mr. Red"
    my_color = 'Red'

    def show_red_message(self):
        return(f'This is a message from the color {self.reds_name}')

    def show_my_color(self):
        return (f'The color is {self.my_color}')

class Orange(Yellow, Red):

    my_color = 'Orange'

    def show_my_color(self):
        message = f'The color is Red & Yellow, which makes {self.my_color}'
        return (message)


def test():

    print(Yellow().show_my_color())
    print(Red().show_my_color())
    print(Orange().show_my_color())

    print("Now let's show that Orange can call methods from Yellow and Red")
    print(Orange().show_yellow_message())
    print(Orange().show_red_message())

if __name__ == "__main__":
  test()