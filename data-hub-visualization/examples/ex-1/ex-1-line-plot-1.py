# CONFIGURATION
# --------------------------------------------------------------------------------------------
y_min = 0                           # minimum value displayed on y axis
y_max = 100                         # maximum value displayed on y axis (maximum must be greater (not greater or equal) than minimum)
input = "input1"                    # name of the input port
output = "output1"                  # name of the output port 
x_step = 10                         # distance in pixels on x axis between two consecutive values/measures (movement/shift ti the right)
chart_height = 500                  # height of the chart in pixels 
chart_width = 1500                  # width of the chart in pixel
chart_color = "#E67E22"             # Color of the line/chart. blue = 2E86C1, yellow = F4D03F, orange = E67E22
num_y_labels = 4                    # number of labels dispyed on y axes. y_min and y_max values are displayed by default on y axis. Total number of labels is num_y_labels + 2 
y_label_decimals = 0                # number of decimal places used for displaying labels on y axis - 0 means, integers are displayed
graph_name = "Memory Consumption"   # title/graph name
# -------------------------------------------------------------------------------------------

# INTERNAL CONFIGURATION - CHANGE ONLY IF YOU KNOW WHAT ARE YOU DOING
# ------------------------------------------------------------------------------------------
x_zero = 15                         # chart line starts from x_zero position. it is a shift left on the chart for y axis labels
font_size = 12                      # font size
background_color = "#212F3C"        # dark blue
# ------------------------------------------------------------------------------------------

# INTERNAL CONFIGURATION - DO NOT CHANGE
# -------------------------------------------------------------------------------------------
x_last = None                       # x coordinate of last drawn point, in pixels. Depends on x_step value.
y_last = None                       # y coordinate of last drawn point, in pixels
y_range = y_max - y_min             # range of values calculated from configuration parameters.
font_size_px = font_size * 0.6667   # font size in pixels, important for indentation on y axis
y_label_pattern = "{0:."+str(y_label_decimals)+"f}"     # pattern which is used to format values on y axis


# HTML TEMPLATES
# ------------------------------------------------------------------------------------------
html = '''
<style>
  body, html { height: 100%; background-color: '''+background_color+''';}
  .graph-container { width: 90%; height: 90%; position: relative; padding-left: 20px; padding-top: 20px }
  .chart { background: '''+background_color+'''; width: '''+str(chart_width)+'''px; height: '''+str(chart_height)+'''px; border-left: 1px dotted #555; border-bottom: 1px dotted #555; }
</style>
<div class="graph-container"> 
  <div align="center" ><font face="verdana" color="white">'''+graph_name+'''</font></div>     
  <div class="chart-box">
    <svg viewBox="0 0 '''+str(chart_width)+''' '''+str(chart_height)+'''" class="chart">
        
        <text font-family="verdana" font-size="'''+str(font_size)+'''" fill="white" y="'''+str(chart_height)+'''" >'''+ y_label_pattern.format(y_min)+'''</text>
        <text font-family="verdana" font-size="'''+str(font_size)+'''" fill="white" y="'''+str(font_size)+'''" >'''+ y_label_pattern.format(y_max)+'''</text>
        #y_labels   

        <polygon fill="'''+chart_color+'''" stroke="none" stroke-width="4" fill-opacity="0.4" points="#fill" />
        #points
        
    </svg>
  </div>
</div>
'''

point = '''
<polyline fill="none" stroke="'''+chart_color+'''" stroke-width="2"
    points="#x_start, #y_start, #x_end, #y_end"/>
'''

horizontal_line = '''
<polyline fill="none" stroke="#989898" stroke-width="0.3" points=" '''+str(x_zero)+''', #y_pos, '''+str(chart_width)+''', #y_pos "/>
'''

y_axis_text = '''
<text font-family="verdana" font-size="'''+str(font_size)+'''px" fill="white" y="#y_pos" >#y_value</text>
'''
# ------------------------------------------------------------------------------------------


# DRAWING CODE
# ------------------------------------------------------------------------------------------
points = ""
fill_start = "#x_start,"+str(chart_height)+","
fill_row = "#x_start,#y_start,#x_end,#y_end,"
fill_end = "#x_last,"+str(chart_height)
fill = ""

# calculate y value for input value. Input value is received from input port and must be integer or float. 
# input: value (float or integer)
# return: y value in pixels (integer)
def calculate_y(value):
    global y_range
    
    y_relative = (value - y_min) / y_range
    y_absolute = y_relative * chart_height
    y = chart_height - y_absolute
    return y

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
        y_value_display = y_label_pattern.format(y_value)
        y_pos = calculate_y(y_value)
        
        html_labels += horizontal_line.replace("#y_pos",str(y_pos))
        html_labels += y_axis_text.replace("#y_pos",str(y_pos + font_size_px/2)).replace("#y_value",y_value_display)
        
    return html_labels 

# function which will be triggered when new data are received on port
# input: value (string encoded number)
def on_input(value):
    global html
    global y_last
    global x_last
    global point
    global points
    global fill_start
    global fill_row
    global fill
    
    val = float(value)
    
    if y_last == None:              # => x_last == None, as well
        y = calculate_y(val)
        y_last = y
        x_last = x_zero                  # First point
        fill_start = fill_start.replace("#x_start", str(x_last))
        fill += fill_start
    else :    
        x_start = x_last
        y_start = y_last
        x_end = x_start + x_step
        y_end = calculate_y(val)
        
        # === points ===
        point_tmp = point.replace("#x_start", str(x_start)).replace("#y_start", str(y_start)).replace("#x_end", str(x_end)).replace("#y_end", str(y_end))
        points += point_tmp
        html_tmp = html.replace("#points", points)
        
        # === fill ===
        fill_tmp = fill_row.replace("#x_start", str(x_start)).replace("#y_start", str(y_start)).replace("#x_end", str(x_end)).replace("#y_end", str(y_end))
        fill_end_tmp = fill_end.replace("#x_last",str(x_end))
        fill += fill_tmp
        fill_all = fill + fill_end_tmp
        html_tmp =html_tmp.replace("#fill", fill_all)
        
        # === set new values ===
        x_last = x_end
        y_last = y_end
        
        # === send html to the output ===
        api.send(output, html_tmp)

api.set_port_callback(input, on_input)

html = html.replace("#y_labels", create_y_labels_html(num_y_labels))