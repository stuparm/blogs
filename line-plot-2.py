# CONFIGURATION
# --------------------------------------------------------------------------------------------
y_min = 0                           # minimum value displayed on y axis
y_max = 100                         # maximum value displayed on y axis (maximum must be greater (not greater or equal) than minimum)
inputs = ["input1","input2"]        # name of the input ports
output = "output"                   # name of the output port 
chart_colors = ["#2E86C1","#E67E22"]# chart colors. First element in chart_colors array matches the first value in inputs array. blue = 2E86C1 , yellow = F4D03F, orange = E67E22
x_step = 10                         # distance in pixels on x axis between two consecutive values/measures (movement/shift ti the right)
chart_height = 500                  # height of the chart in pixels 
chart_width = 1500                  # width of the chart in pixel
num_y_labels = 4                    # number of labels dispyed on y axes. y_min and y_max values are displayed by default on y axis. Total number of labels is num_y_labels + 2 
y_label_decimals = 0                # number of decimal places used for displaying labels on y axis - 0 means, integers are displayed
graph_name = "Resource Consumption" # title/graph name
input_names = ["cpu", "memory"]     # 
# -------------------------------------------------------------------------------------------

# INTERNAL CONFIGURATION - CHANGE ONLY IF YOU KNOW WHAT ARE YOU DOING
# ------------------------------------------------------------------------------------------
x_zero = 15                         # chart line starts from x_zero position. it is a shift left on the chart for y axis labels
font_size = 12                      # font size
background_color = "#212F3C"        # dark blue
# ------------------------------------------------------------------------------------------

# INTERNAL CONFIGURATION - DO NOT CHANGE
# -------------------------------------------------------------------------------------------
x_last_1 = None                       # x coordinate of last drawn point, in pixels. Depends on x_step value.
y_last_1 = None                       # y coordinate of last drawn point, in pixels
x_last_2 = None
x_last_2 = None

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

        <polygon fill="'''+chart_colors[0]+'''" stroke="none" stroke-width="4" fill-opacity="0.2" points="#fill_1" />
        <polygon fill="'''+chart_colors[1]+'''" stroke="none" stroke-width="4" fill-opacity="0.2" points="#fill_2" />
        
        #points_1
        #points_2
        
    </svg>
        <div align="center" >
        <font color="'''+chart_colors[0]+'''" font-size="24px">&#8213;</font>
        <font face="verdana" color="white">'''+input_names[0]+'''</font>&ensp;
        <font color="'''+chart_colors[1]+'''" font-size="24px">&#8213;</font>
        <font face="verdana" color="white">'''+input_names[1]+'''</font>
        </div>
  </div>
</div>
'''

point = '''
<polyline fill="none" stroke="#chart_color" stroke-width="2"
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
points_1 = ""
points_2 = ""
fill_start_1 = "#x_start,"+str(chart_height)+","
fill_start_2 = "#x_start,"+str(chart_height)+","
fill_row = "#x_start,#y_start,#x_end,#y_end,"
fill_end = "#x_last,"+str(chart_height)
fill_1 = ""
fill_2 = ""

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
def on_input(value1, value2):
    global html
    global y_last_1
    global x_last_1
    global y_last_2
    global x_last_2
    global point
    global points_1
    global points_2
    global fill_start_1
    global fill_start_2
    global fill_row
    global fill_1
    global fill_2
    
    
    val1 = float(value1)
    val2 = float(value2)
    
    if y_last_1 == None:              # => y_last_2 == None
        y_1 = calculate_y(val1)
        y_last_1 = y_1
        x_last_1 = x_zero
        fill_start_1 = fill_start_1.replace("#x_start", str(x_last_1))
        fill_1 += fill_start_1
        
        y_2 = calculate_y(val2)
        y_last_2 = y_2
        x_last_2 = x_zero
        fill_start_2 = fill_start_2.replace("#x_start", str(x_last_2))
        fill_2 += fill_start_2
        
    else :    
        x_start_1 = x_last_1
        y_start_1 = y_last_1
        x_end_1 = x_start_1 + x_step
        y_end_1 = calculate_y(val1)
        point_tmp_1 = point.replace("#x_start", str(x_start_1)).replace("#y_start", str(y_start_1)).replace("#x_end", str(x_end_1)).replace("#y_end", str(y_end_1)).replace("#chart_color", chart_colors[0])
        points_1 += point_tmp_1
        html_tmp_1 = html.replace("#points_1", points_1)
        fill_tmp_1 = fill_row.replace("#x_start", str(x_start_1)).replace("#y_start", str(y_start_1)).replace("#x_end", str(x_end_1)).replace("#y_end", str(y_end_1))
        fill_end_tmp_1 = fill_end.replace("#x_last",str(x_end_1))
        fill_1 += fill_tmp_1
        fill_all_1 = fill_1 + fill_end_tmp_1
        html_tmp_1 =html_tmp_1.replace("#fill_1", fill_all_1)
        x_last_1 = x_end_1
        y_last_1 = y_end_1
        
        x_start_2 = x_last_2
        y_start_2 = y_last_2
        x_end_2 = x_start_2 + x_step
        y_end_2 = calculate_y(val2)
        point_tmp_2 = point.replace("#x_start", str(x_start_2)).replace("#y_start", str(y_start_2)).replace("#x_end", str(x_end_2)).replace("#y_end", str(y_end_2)).replace("#chart_color", chart_colors[1])
        points_2 += point_tmp_2
        html_tmp_2 = html_tmp_1.replace("#points_2", points_2)
        fill_tmp_2 = fill_row.replace("#x_start", str(x_start_2)).replace("#y_start", str(y_start_2)).replace("#x_end", str(x_end_2)).replace("#y_end", str(y_end_2))
        fill_end_tmp_2 = fill_end.replace("#x_last",str(x_end_2))
        fill_2 += fill_tmp_2
        fill_all_2 = fill_2 + fill_end_tmp_2
        html_tmp_2 =html_tmp_2.replace("#fill_2", fill_all_2)
        x_last_2 = x_end_2
        y_last_2 = y_end_2
        
        # === send html to the output ===
        api.send(output, html_tmp_2)

api.set_port_callback(inputs, on_input)

html = html.replace("#y_labels", create_y_labels_html(num_y_labels))


