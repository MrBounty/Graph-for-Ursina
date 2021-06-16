from ursina import *

class Little_Graph(Entity):
    def __init__(self,
     entity, arg,
     entity2 = False, arg2 = False,
     position = (-.5*window.aspect_ratio,.5), scale=(.4, .2),
     point=True, line=False, background=True, average=False,
     text=True, text_minmax_y=True, text_minmax_x=False,
     speed_seconde=1/30, nb_points=50,
     back_color=color.black, point_color=color.blue, line_color=color.blue,
     limit_axes_x=False, limit_axes_y=False,
     reset_key='r', pause_key='p', show_key='o',
     update = True,
     fullscreen = False,
     **kwargs):

        super().__init__(
            parent = camera.ui,                                         
            origin = (-.5, .5),
            **kwargs,
            )

        #region initializing a whole bunch of crap
        self.back_color = back_color
        self.plot_update = update
        self.points_nb_max = nb_points
        self.vitesse_sec = speed_seconde
        self.points_activ = point
        self.lignes_activ = line
        self.text_activ = text
        self.text_minmax_x_activ = text_minmax_x
        self.text_minmax_y_activ = text_minmax_y
        self.points_color = point_color
        self.lignes_color = line_color
        self.entity = entity
        self.v_str = 'self.entity.' + arg
        self.t = 0

        self.entity2 = entity2
        self.arg2 = arg2

        if arg2==False: self.arg2_act = False
        else: 
            self.arg2_act = True
            self.v_str2 = 'self.entity2.' + arg2

        #Graph size
        if type(scale)==tuple:self.scale = scale
        else: self.scale = (.4*scale, .2*scale)

        #Graph position
        if type(position)==int:
            for i in range(2, 10):
                if position == i:
                    self.position = (-.5*window.aspect_ratio,.5-(i-1)*self.scale[1])
        else: self.position = position

        self.background_activ = background
        self.text_average_activ = average
        self.reset_key = reset_key
        self.pause_key = pause_key
        self.show_key = show_key
        self.limit_axes_x = limit_axes_x
        self.limit_axes_y = limit_axes_y
        self.x_graph=[]
        self.y_graph=[]

        self.text_minmax_y_print = False
        self.text_minmax_x_print = False

        self.text_values_print = False
        self.can_plot = False
        #endregion

        #region parents initialization
        if self.points_activ: 
            self.points = Entity(parent=self)
            self.points_list = []
        if self.lignes_activ: 
            self.lignes = Entity(parent=self)
            self.lines_list = []
        self.text = Entity(parent=self)
        self.text_value = Entity(parent=self.text)
        if self.text_activ: self.text_minmax = Entity(parent=self.text)
        if self.text_average_activ: self.text_average = Entity(parent=self.text)
        if self.background_activ: self.add_background()
        #endregion

        #base text size
        Text.default_resolution = 1080 * Text.size

        if fullscreen: 
            self.position = (-.5*window.aspect_ratio,.5) 
            self.scale=(window.aspect_ratio*1.001, 1)

    def add_background(self):
    #add background
        self.background_ent = Entity(model='quad', color=self.back_color, scale=(1,1), position=(.5, -.5), z=1, parent=self)
        if self.text_average_activ: Entity(model='quad', color=self.back_color, scale=(1,self.scale[0]*0.7),origin=(-.5, .5), position=(0, -1), z=1, parent=self)

    def add_text_value(self):
    #add the value in the middle if the value is always the same
        v = max(self.y_graph)
        text_desc = self.float_to_scientific(v)
        text_scale = (1/Text.get_width(text_desc))*0.8
        #if it does not exist
        if len(self.text_value.children) == 0: self.text_value_y = Text(text=text_desc, parent=self.text_value, scale=text_scale, origin=(0, 0),position=(0.5, -.5)) 
        else: 
            self.text_value_y.text = text_desc
            self.text_value_y.scale = text_scale

    def add_text_minmax(self):
    #Add the three text that corresponds to the min, max and the average
        if self.text_minmax_x_activ: #if we want some for x
            if not self.text_minmax_x_print: #Initialisation
                avr_x = (self.max_x+self.min_x)/2
                str_max_x, str_min_x, str_avr_x = self.float_to_scientific(self.max_x), self.float_to_scientific(self.min_x), self.float_to_scientific(avr_x)
                text_scale = (1/Text.get_width(str_max_x))*0.1
                self.entity_text_max_x = entity_text_max_x = Text(text=str_max_x, parent=self.text_minmax, origin=(.5,-.5), position=(1, -1), scale=text_scale)
                self.entity_text_min_x = entity_text_min_x = Text(text=str_min_x, parent=self.text_minmax, origin=(-.5,-.5), position=(0, -1), scale=text_scale)
                self.entity_text_avr_x = entity_text_avr_x = Text(text=str_avr_x, parent=self.text_minmax, origin=(0,-.5), position=(.5, -1), scale=text_scale)
                self.text_minmax_x_print = True
            else: #Update
                avr_x = (self.max_x+self.min_x)/2
                str_max_x, str_min_x, str_avr_x = self.float_to_scientific(self.max_x), self.float_to_scientific(self.min_x), self.float_to_scientific(avr_x)
                self.entity_text_max_x.text = str_max_x
                self.entity_text_min_x.text = str_min_x
                self.entity_text_avr_x.text = str_avr_x
        if self.text_minmax_y_activ: #if we want some for y
            if not self.text_minmax_y_print: #Initialisation
                avr_y = (self.max_y+self.min_y)/2
                str_max_y, str_min_y, str_avr_y = self.float_to_scientific(self.max_y), self.float_to_scientific(self.min_y), self.float_to_scientific(avr_y)
                text_scale = (1/Text.get_width(str_max_y))*0.1
                self.entity_text_max_y = Text(text=str_max_y, parent=self.text_minmax, origin=(-.5,.5), position=(0, 0), scale=text_scale)
                self.entity_text_min_y = Text(text=str_min_y, parent=self.text_minmax, origin=(-.5,-.5), position=(0, -1), scale=text_scale)
                self.entity_text_avr_y = Text(text=str_avr_y, parent=self.text_minmax, origin=(-.5,0), position=(0, -.5), scale=text_scale)
                self.text_minmax_y_print = True
            else: #Update
                avr_y = (self.max_y+self.min_y)/2
                str_max_y, str_min_y, str_avr_y = self.float_to_scientific(self.max_y), self.float_to_scientific(self.min_y), self.float_to_scientific(avr_y)
                self.entity_text_max_y.text = str_max_y
                self.entity_text_min_y.text = str_min_y
                self.entity_text_avr_y.text = str_avr_y

    def add_average(self):
    #Add an average value below the graph
        somme = 0
        for i in self.y_graph:
            somme +=i
        avr = somme/len(self.y_graph)
        text_desc = self.float_to_scientific(avr)
        text_scale = self.scale[1]*50
        #if it does not exist
        if len(self.text_average.children) == 0: self.text_average_y = Text(text=text_desc, parent=self.text_average, scale=text_scale, origin=(-.5,.5), position=(0, -1))
        else: 
            self.text_average_y.text = text_desc
            self.text_average_y.scale = text_scale

    def float_to_scientific(self, v):
    #Round off the value and turn it into a scientist if it is too big or small
        if (.001 < v < 10000) or (-.001 > v > -10000) or v==0: text = str(round(v,2))
        else: text = "{:.2e}".format(v)
        return text
    
    def max_min(self):
    #update the max and min values ​​for the axes
        if not self.limit_axes_x: self.max_x, self.min_x = max(self.x_graph), min(self.x_graph)
        else: self.min_x, self.max_x = self.limit_axes_x[0], self.limit_axes_x[1]
        if not self.limit_axes_y: self.max_y, self.min_y = max(self.y_graph), min(self.y_graph)
        else: self.min_y, self.max_y = self.limit_axes_y[0], self.limit_axes_y[1]

    def add_points(self):
    #Allows you to draw points with two vectors x and y
        #if the points are already all create
        if len(self.points_list) == len(self.x_graph):
            self.update_points()
        #if entity points are missing
        else:
            points_size = 1/len(self.x_graph)
            for i in range(len(self.points_list), len(self.x_graph)):
                x_cur = round(((self.x_graph[i]-self.min_x)/(self.max_x-self.min_x))*(.95/1.1)+0.1, 5)
                y_cur = round(((self.y_graph[i]-self.min_y)/(self.max_y-self.min_y))*(.95/1.05)+.05, 5)-1
                self.points_list.append(Entity(model='circle', position=(x_cur,y_cur), scale=points_size, color=self.points_color, parent=self.points))
                if not (0<x_cur<1) or not (-1<y_cur<0):
                    self.points_list[-1].visible = False
                    
            self.update_points()

    def update_points(self):
    #change the position and size of the points to update them
        points_size = 1/len(self.x_graph)
        for i in range(0, len(self.x_graph)):
                x_cur = round(((self.x_graph[i]-self.min_x)/(self.max_x-self.min_x))*(.95/1.1)+0.1, 5)
                y_cur = round(((self.y_graph[i]-self.min_y)/(self.max_y-self.min_y))*(.95/1.05)+.05, 5)-1
                self.points_list[i].x = x_cur
                self.points_list[i].y = y_cur
                self.points_list[i].scale = points_size
                if not 0<x_cur<1 or not -1<y_cur<1:
                    self.points_list[i].visible = False
                else: self.points_list[i].visible = True
                    
    def add_lignes(self):
    #Allows you to draw lines with two vectors x and y
        #if the lines are already all create
        if len(self.lines_list) == len(self.x_graph) - 1:
            self.update_lines()
        #if entity lines are missing
        else:
            lignes_size = 0.3/len(self.x_graph)
            for i in range(len(self.lines_list), len(self.x_graph) - 1):
                x_cur1 = round(((self.x_graph[i]-self.min_x)/(self.max_x-self.min_x))*(.95/1.1)+0.1, 5)
                y_cur1 = round(((self.y_graph[i]-self.min_y)/(self.max_y-self.min_y))*(.95/1.05)+.05, 5)-1
                x_cur2 = round(((self.x_graph[i+1]-self.min_x)/(self.max_x-self.min_x))*(.95/1.1)+0.1, 5)
                y_cur2 = round(((self.y_graph[i+1]-self.min_y)/(self.max_y-self.min_y))*(.95/1.05)+.05, 5)-1
                x_cur = x_cur1 - x_cur2
                y_cur = y_cur1 - y_cur2
                dist = math.sqrt((math.pow(x_cur, 2)) + math.pow(y_cur, 2))
                rot = math.degrees(math.atan2(y_cur, x_cur))
                self.lines_list.append(Entity(model='quad', position=(x_cur1-x_cur/2,y_cur1-y_cur/2), scale=(dist, lignes_size),rotation_z=-rot, color=self.lignes_color, parent=self.lignes))
                if not 0<x_cur1-x_cur/2<1 or not -1<y_cur1-y_cur/2<0:
                    self.lines_list[-1].visible = False
                    
            self.update_lines()

    def update_lines(self):
    #change the position, size and rotation of the lines to update them
        lignes_size = 0.3/len(self.x_graph)
        if lignes_size<.005: lignes_size = .006
        for i in range(0, len(self.x_graph)-1):
            x_cur1 = round(((self.x_graph[i]-self.min_x)/(self.max_x-self.min_x))*(.95/1.1)+0.1, 5)
            y_cur1 = round(((self.y_graph[i]-self.min_y)/(self.max_y-self.min_y))*(.95/1.05)+.05, 5)-1
            x_cur2 = round(((self.x_graph[i+1]-self.min_x)/(self.max_x-self.min_x))*(.95/1.1)+0.1, 5)
            y_cur2 = round(((self.y_graph[i+1]-self.min_y)/(self.max_y-self.min_y))*(.95/1.05)+.05, 5)-1
            x_cur = x_cur1 - x_cur2
            y_cur = y_cur1 - y_cur2
            dist = math.sqrt((math.pow(x_cur, 2)) + math.pow(y_cur, 2))
            rot = math.degrees(math.atan2(y_cur, x_cur))
            self.lines_list[i].x = x_cur1-x_cur/2
            self.lines_list[i].y = y_cur1-y_cur/2
            self.lines_list[i].rotation_z = -rot
            self.lines_list[i].scale = (dist, lignes_size)
            if not 0<x_cur1-x_cur/2<1 or not -1<y_cur1-y_cur/2<0:
                self.lines_list[i].visible = False
            else: self.lines_list[i].visible = True

    def add_values(self, v):
    #Allows you to add a value to the list x and y (if v is a single value, we add 1 to the last x otherwise if v is a list of size 2, we add the value x and y)
        if isinstance(v, int) or isinstance(v, float):
            if len(self.x_graph) == 0: 
                self.x_graph.append(0)
            else: 
                self.x_graph.append(self.x_graph[-1]+1)
            self.y_graph.append(v)
        elif len(v) == 2:
            self.x_graph.append(v[0])
            self.y_graph.append(v[1])

    def delete_for_reset(self):
        if self.points_activ: 
            destroy(self.points)
            self.points = Entity(parent=self)
            self.points_list = []
        if self.lignes_activ: 
            destroy(self.lignes)
            self.lignes = Entity(parent=self)
            self.lines_list = []

    def input(self, key):
    #to reset, pause and see the graph
        if key == self.reset_key:
            self.delete_for_reset()
            self.x_graph = []
            self.y_graph = []
        if key == self.pause_key:
            self.plot_update = not self.plot_update
        if key == self.show_key:
            self.visible = not self.visible

    def update(self):
        self.t += time.dt
        if self.plot_update and (self.t > self.vitesse_sec): #If we want to update
            self.t = 0
            if not self.arg2_act: self.add_values(eval(self.v_str))
            else: self.add_values((eval(self.v_str), eval(self.v_str2)))

            #If all the values ​​are equal, we do not draw the graph and we make the graph invisible
            if (max(self.x_graph)-min(self.x_graph) == 0) or (max(self.y_graph)-min(self.y_graph) == 0): 
                self.can_plot = False
                if self.points_activ:self.points.visible = False
                if self.lignes_activ:self.lignes.visible = False
                if self.text_activ: self.text_minmax.visible = False
                if self.text_activ: self.text_value.visible = True
            else: 
                self.can_plot = True
                if self.points_activ:self.points.visible = True
                if self.lignes_activ:self.lignes.visible = True
                if self.text_activ: self.text_minmax.visible = True
                if self.text_activ:self.text_value.visible = False

            if self.can_plot: #If we draw the graph, we update the position and value
                self.max_min()
                if self.points_activ: self.add_points()
                if self.lignes_activ: self.add_lignes()
                if self.text_activ: self.add_text_minmax()
                if self.text_average_activ: self.add_average()
            else: #else we just update the value in the middle
                if self.text_activ:
                    if not self.text_values_print: self.add_text_value()

            #we remove the first values ​​of x and y if we have too many
            if len(self.x_graph) > self.points_nb_max:
                for i in range(0, len(self.x_graph) - self.points_nb_max):
                    self.x_graph.pop(i)
                    self.y_graph.pop(i)

if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    slider_x = ThinSlider(text = 'x', min=0, max=100, default=.5, dynamic=True, y = 0.1)
    slider_y = ThinSlider(text = 'y',min=0, max=100, dynamic=True)

    #the simplest example is the graph at the top left
    Little_Graph(slider_x, 'value')

    #for the second graph at the top left just below the first
    Little_Graph(slider_y, 'value', line=True, point=False, position=2, average=True)

    #an example with many usable arguments
    Little_Graph(slider_y, 'value',
    line=True, point=True, 
    position=(-.6, -.01), scale=(.3, .3), 
    speed_seconde=0.5, nb_points=5,
    back_color=color.pink, point_color=color.green, line_color=color.red,
    text_minmax_x=True)


    def slider_x_changed(slider=slider_x):
        global dx
        dx = slider.value
    slider_x.on_value_changed = slider_x_changed

    def slider_y_changed(slider=slider_y):
        global dy
        dy = slider.value
    slider_y.on_value_changed = slider_y_changed

    app.run()