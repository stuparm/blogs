# CONFIGURATION
# --------------------------------------------------------------------------------------------
y_min = 0                           # minimum value displayed on y axis
y_max = 100                         # maximum value displayed on y axis (maximum must be greater (not greater or equal) than minimum)
x_min = 0                           # minimum value displayed on x axis
x_max = 100                         # maximum value displayed on x axis (maximum must be greater (not greater or equal) than minimum)
inputs = ["input1","input2"]        # name of the input ports. It cooresponds to x and y axis
output = "output"                   # name of the output port 
chart_color = "#2E86C1"             # point chart color. blue = 2E86C1 , yellow = F4D03F, orange = E67E22
chart_height = 500                  # height of the chart in pixels 
chart_width = 500                   # width of the chart in pixel
num_y_labels = 4                    # number of labels dispyed on y axis. min and max values are not displayed 
num_x_labels = 4                    # number of labels dispyed on x axis. min and max values are not displayed
label_decimals = 0                  # number of decimal places used for displaying labels on y axis - 0 means, integers are displayed
graph_name = "Resource Consumption" # title/graph name
# -------------------------------------------------------------------------------------------

# INTERNAL CONFIGURATION - CHANGE ONLY IF YOU KNOW WHAT ARE YOU DOING
# ------------------------------------------------------------------------------------------
line_offset = 15                    # chart line starts from x_zero position. it is a shift left on the chart for y axis labels
font_size = 12                      # font size
background_color = "#212F3C"        # dark blue
# ------------------------------------------------------------------------------------------

# INTERNAL CONFIGURATION - DO NOT CHANGE
# -------------------------------------------------------------------------------------------
y_range = y_max - y_min             # range of y values calculated from configuration parameters.
x_range = x_max - x_min             # range of x values calculated from configuration parameters.
font_size_px = font_size * 0.6667   # font size in pixels, important for indentation on y axis
label_pattern = "{0:."+str(label_decimals)+"f}"     # pattern which is used to format values on y axis


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
        
        #y_labels   
        #x_labels
        #points
        
    </svg>
  </div>
</div>
'''

point = '''<circle cx="#x_coord" cy="#y_coord" r="3" stroke="none" fill="#color" />
'''

horizontal_line = '''
<polyline fill="none" stroke="#989898" stroke-width="0.3" points=" '''+str(line_offset)+''', #y_pos, '''+str(chart_width)+''', #y_pos "/>
'''
y_axis_text = '''
<text font-family="verdana" font-size="'''+str(font_size)+'''px" fill="white" y="#y_pos" >#y_value</text>
'''
vertical_line = '''
<polyline fill="none" stroke="#989898" stroke-width="0.3" points=" #x_pos, 0, #x_pos, '''+str(chart_height - line_offset)+''' "/>
'''

x_axis_text = '''
<text font-family="verdana" font-size="'''+str(font_size)+'''px" fill="white" y="'''+str(chart_height - 2)+'''" x="#x_pos" >#x_value</text>
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

# create html which draws horizontal axis and corresponding values
def create_y_labels_html(num_y_labels):
    global y_min
    global y_max
    global y_range
    
    html_labels = ""
    if (num_y_labels <= 0):
        return html_labels;
    n_y_steps = num_y_labels + 1
    y_step = y_range / (n_y_steps)
    
    for curr in range(1,n_y_steps):
        y_value = y_min + (y_step * curr)
        y_value_display = label_pattern.format(y_value)
        y_pos = calculate_y(y_value)
        
        html_labels += horizontal_line.replace("#y_pos",str(y_pos))
        html_labels += y_axis_text.replace("#y_pos",str(y_pos + font_size_px/2)).replace("#y_value",y_value_display)
        
    return html_labels 


def create_x_labels_html(num_x_labels):
    global x_min
    global x_max
    global x_range
    
    html_labels = ""
    if (num_x_labels <= 0):
        return html_labels;
    n_x_steps = num_x_labels + 1
    x_step = x_range / (n_x_steps)
    
    for curr in range(1,n_x_steps):
        x_value = x_min + (x_step * curr)
        x_value_display = label_pattern.format(x_value)
        x_pos = calculate_x(x_value)
        
        html_labels += vertical_line.replace("#x_pos",str(x_pos))
        html_labels += x_axis_text.replace("#x_pos",str(x_pos - 8)).replace("#x_value", x_value_display)
        
    return html_labels



# function which will be triggered when new data are received on port
# input: value (string encoded number)
def on_input(value1, value2):
    global html
    global point
    global points
    global chart_color

    val1 = float(value1)   # value x
    val2 = float(value2)   # value y
    
    x_val = calculate_x(val1)
    y_val = calculate_y(val2)
    
    circle = point.replace("#x_coord",str(x_val)).replace("#y_coord", str(y_val)).replace("#color", chart_color)
    points += circle
    
    html_tmp = html.replace("#points", points)
    
    api.send(output, html_tmp)

api.set_port_callback(inputs, on_input)

# generate x and y labels on start
html = html.replace("#y_labels", create_y_labels_html(num_y_labels))
html = html.replace("#x_labels", create_x_labels_html(num_x_labels))


