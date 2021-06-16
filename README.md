# Graph-for-Ursina

Allows to display a small graph for debugging application using ursina.

It takes the argument of an entity and displays it.

## Exemples

The simplest example:
```python
Little_Graph(slider_x, 'value')
```

Second graph at the top left just below the first:
```python
Little_Graph(slider_y, 'value', line=True, point=False, position=2, average=True)
```

## All arguments available:
```python
Little_Graph(

entity, arg,                                                                #Choice of the entity to display and its argument. The argument must be a string

entity2 = False, arg2 = False,                                              #If we want to put a second argument on the graph. Works like the 1st. It is better to stack the graphs, to make two graphs with two different arguments at the same position.

position = (-.5*window.aspect_ratio,.5), scale=(.4, .2),                    #The position on the screen, the origin being at the top left of the graph, ans the scale in x and y. Both can be an int

point=True, line=False, background=True, average=False,                     #If we want to display points, lines, the background and the average

text=True, text_minmax_y=True, text_minmax_x=False,                         #If we want to display text in general, the max, min and middle value of x or y

speed_seconde=1/30, nb_points=50,                                           #The refresh rate in seconds and the number of points to display

back_color=color.black, point_color=color.blue, line_color=color.blue,      #Allows you to choose the colors

limit_axes_x=False, limit_axes_y=False,                                     #If we want to set the min and max value of the axis (ex: (-5, 5))

reset_key='r', pause_key='p', show_key='o',                                 #The keys to reset, pause and display or not the graph

update = True,                                                              #If we want to update the graph

fullscreen = False)                                                         #If we want to display the graph in fullscreen
```
