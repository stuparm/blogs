# CONFIGURATION
# --------------------------------------------------------------------------------------------
y_min = 0           # minimum value displayed on y axis
y_max = 100         # maximum value displated on y axis (maximum must be greater (not greater or equal) than minimum)
input = "input1"    # name of the input port
output = "output1"  # name of the output port 
step = 10           # in pixels. Defines how many pixels is next pooint moved to the right on x axis
chart_height = 500  # height of the chart in pixels 
# -------------------------------------------------------------------------------------------


# INRTERNAL PARAMETERS - USUALLY THIS PARAMETERS ARE NOT CHANGED
# -------------------------------------------------------------------------------------------
x_last = None       # x coordinate of last drawn point, in pixels. Depends on step value.
y_last = None       # y coordinate of last drawn point, in pixels
y_range = y_max - y_min     # range of values calculated from configuration parameters.
y_px = chart_height         # amount of pixels used to display y axis (the height of the chart in pixels)
# ------------------------------------------------------------------------------------------


# DRAWING CODE
# ------------------------------------------------------------------------------------------
points = ""
fill_start = "#x_start,"+str(y_px)+","
fill_row = "#x_start,#y_start,#x_end,#y_end,"
fill_end = "#x_last,"+str(y_px)
fill = ""

# calculate y value for input value. Input value is received from input port and must be integer or float. 
# input: value (float or integer)
# return: y value in pixels (integer)
def calculate_y(value):
    global y_range
    
    y_relative = (value - y_min) / y_range
    y_absolute = y_relative * y_px
    y = y_px - y_absolute
    return y

# function which will be triggered when new data are received on port
# input: value (string encoded number)
def on_input(value):
    global message
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
        x_last = 0                  # First point
        fill_start = fill_start.replace("#x_start", str(x_last))
        fill += fill_start
    else :    
        x_start = x_last
        y_start = y_last
        x_end = x_start + step
        y_end = calculate_y(val)
        
        # === points ===
        point_tmp = point.replace("#x_start", str(x_start))
        point_tmp = point_tmp.replace("#y_start", str(y_start))
        point_tmp = point_tmp.replace("#x_end", str(x_end))
        point_tmp = point_tmp.replace("#y_end", str(y_end))
        points += point_tmp
        message_tmp = message.replace("#points", points)
        
        # === fill ===
        fill_tmp = fill_row.replace("#x_start", str(x_start))
        fill_tmp = fill_tmp.replace("#y_start", str(y_start))
        fill_tmp = fill_tmp.replace("#x_end", str(x_end))
        fill_tmp = fill_tmp.replace("#y_end", str(y_end))
        fill_end_tmp = fill_end.replace("#x_last",str(x_end))
        fill += fill_tmp
        fill_all = fill + fill_end_tmp
        
        # === apply ===
        message_tmp = message_tmp.replace("#fill", fill_all)
        
        # === set new values ===
        x_last = x_end
        y_last = y_end
        
        # === send html to the output ===
        api.send(output, message_tmp)


api.set_port_callback(input, on_input)

# HTML
# ------------------------------------------------------------------------------
message = '''
<style>
  body, html { height: 100%; }
  .graph-container { width: 90%; height: 90%; position: relative; padding-left: 20px; padding-top: 20px }
  .chart { background: white; width: 5000px; height: '''+str(y_px)+'''px; border-left: 1px dotted #555; border-bottom: 1px dotted #555; }
</style>

<div class="graph-container"> 
  <div class="chart-box">
    <!-- Size of the graph in pixes (5000 pixels in width and 500 in height). These values have to match the values from css definition for .chart class -->
    <svg viewBox="0 0 5000 '''+str(y_px)+'''" class="chart">
      <!-- definition of the circle(s) -->
      <defs>
        <marker id="circle" markerWidth="4" markerHeight="4" refx="2" refy="2">
          <circle cx="2" cy="2" r="2" stroke="none" fill="#3887cc"/>
        </marker>
      </defs>
    
      <!-- fill polygon -->
      <polygon fill="#eef3f7" stroke="none" stroke-width="4"
        points="#fill" />
      
      <!-- point polygon -->
      #points


      <!-- y labels 
      <text y="500" textLength="10" >0</text>
      <text y="12" textLength="25" >100</text>
      <text y="256" textLength="17" >50</text> -->
    </svg>
  </div>
</div>
'''

point = '''
<polyline fill="none" stroke="#cad7e3" stroke-width="2" marker-start="url(#circle)" marker-end="url(#circle)"
    points="#x_start, #y_start, #x_end, #y_end"/>
'''

