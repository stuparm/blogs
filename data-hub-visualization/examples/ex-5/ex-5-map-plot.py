# CONFIGURATION
# --------------------------------------------------------------------------------------------
y_min = 48.14430                    # minimum value displayed on y axis (min latitude)
y_max = 48.15026                    # maximum value displayed on y axis (max latitude)
x_min = 11.55723                    # minimum value displayed on x axis (min longitude)
x_max = 11.57143                    # maximum value displayed on x axis (max longitude)
inputs = "input1"                   # name of the input port. It cooresponds to longitude,latitude. Important that longitude is first value
output = "output"                   # name of the output port 
chart_color = "#DC143C"             # point chart color. blue = 2E86C1 , yellow = F4D03F, orange = E67E22, red = DC143C
chart_height = 652                  # height of the chart in pixels 
chart_width = 975                   # width of the chart in pixel
graph_name = "Map - Munich"         # title/graph name
map_url="https://raw.githubusercontent.com/stuparmihailo/blogs/master/data-hub-visualization/examples/ex-5/ex-5-map.png"    #url with location of the map
# -------------------------------------------------------------------------------------------

# INTERNAL CONFIGURATION - CHANGE ONLY IF YOU KNOW WHAT ARE YOU DOING
# ------------------------------------------------------------------------------------------
background_color = "#212F3C"        # dark blue
# ------------------------------------------------------------------------------------------

# INTERNAL CONFIGURATION - DO NOT CHANGE
# -------------------------------------------------------------------------------------------
y_range = y_max - y_min             # range of y values calculated from configuration parameters.
x_range = x_max - x_min             # range of x values calculated from configuration parameters.


# HTML TEMPLATES
# ------------------------------------------------------------------------------------------
html = '''
<style>
  body, html { height: 100%; background-color: '''+background_color+'''}
  .graph-container { width: 100%; height: 90%; padding-top: 20px;   }
  .chart { background: '''+background_color+'''; width: '''+str(chart_width)+'''px; height: '''+str(chart_height)+'''px; }
</style>
<br>
<div align="center" ><font face="verdana" color="white">'''+graph_name+'''</font></div> 
<div align="center" class="graph-container"> 
  <div class="chart-box">
    <svg viewBox="0 0 '''+str(chart_width)+''' '''+str(chart_height)+'''" class="chart">
        
        <image xlink:href="'''+map_url+'''" x="0" y="0" height="'''+str(chart_height)+'''px" width="'''+str(chart_width)+'''px"/>

        #points
        
    </svg>
  </div>
</div>
'''

point = '''<circle cx="#x_coord" cy="#y_coord" r="5" stroke="none" fill="#color" />
'''
# ------------------------------------------------------------------------------------------


# DRAWING CODE
# ------------------------------------------------------------------------------------------
points = ""


# calculate y value for input value. Input value is received from input port and must be integer or float. 
# input: value (float or integer)
# return: y value in pixels (integer)
def calculate_y(value):
    global y_range
    
    y_relative = (value - y_min) / y_range
    y_absolute = y_relative * chart_height
    y = chart_height - y_absolute
    return y
    
def calculate_x(value):
    global x_range
    
    x_relative = (value - x_min) / x_range
    x_absolute = x_relative * chart_width
    x = x_absolute
    return x

# function which will be triggered when new data are received on port
# input: value (longityde,latitude)
def on_input(value):
    global html
    global point
    global points
    global chart_color

    values = value.split(",")

    val1 = float(values[0])   # value x
    val2 = float(values[1])   # value y
    
    x_val = calculate_x(val1)
    y_val = calculate_y(val2)
    
    circle = point.replace("#x_coord",str(x_val)).replace("#y_coord", str(y_val)).replace("#color", chart_color)
    points += circle
    
    html_tmp = html.replace("#points", points)
    
    api.send(output, html_tmp)

api.set_port_callback(inputs, on_input)
