## Examples

This folder contains five examples that can be separated into three categories:
1) Line Charts
    - [Example 1 - Single Line Chart](#Example-1---Single-Line-Chart) 
    - [Example 2 - Multiple Line Chart](#Example-2---Multiple-Line-Chart) 
2) Scatter Plots 
    - [Example 3 - Single Cluster Scatter Plot](#Example-3---Single-Cluster-Scatter-Plot)
    - [Example 4 - Two Clusters Scatter Plot](#Example-4---Two-Clusters-Scatter-Plot)
3) Map Visualization 
    - Example 5 - Map Visualization - Single Input of GPS points
---
---

#### Example 1 - Single Line Chart
 
![Example 1 - Single Line Chart ](../resources/ex-1.gif)

This type of chart is useful for displaying single input (single value). Entry point is just ```y value``` and in this case, ```y value``` is in range [20,40]. The code for generating such a value is in file [ex-1-generator.js](../examples/ex-1-generator.js). As shown in the diagram, there are no ```x values```. This is because, this diagram is timestamp oriented, which means every time the ```y value``` arrives, it is shown in the diagram (in our case it is generated every 500ms).

The code for html chart creation is in file [ex-1-line-plot-1.py](../examples/ex-1-line-plot-1.py). The code is more/less generic and external user should only be focused on ```configuration``` part.

```python
# CONFIGURATION
# --------------------------------------------------------------------------------------------
y_min = 0                           # minimum value displayed on y axis
y_max = 100                         # maximum value displayed on y axis (maximum must be greater (not greater or equal) than minimum)
input = "input1"                    # name of the input port
output = "output1"                  # name of the output port 
x_step = 10                         # distance in pixels on x axis between two consecutive values/measures (movement/shift to the right)
chart_height = 500                  # height of the chart in pixels 
chart_width = 1500                  # width of the chart in pixel
chart_color = "#E67E22"             # Color of the line/chart. blue = 2E86C1, yellow = F4D03F, orange = E67E22
num_y_labels = 4                    # number of labels dispyed on y axes. y_min and y_max values are displayed by default on y axis. Total number of labels is num_y_labels + 2 
y_label_decimals = 0                # number of decimal places used for displaying labels on y axis - 0 means, integers are displayed
graph_name = "Memory Consumption"   # title/graph name
# -------------------------------------------------------------------------------------------
```

All components mentioned above are part of the diagram:
the diagram looks as follows:

![Example 1 - Single Line Data Hub ](../resources/ex-1.png)

---
---
#### Example 2 - Multiple Line Chart

![Example 2 - Multiple Line Chart ](../resources/ex-2.gif)

If two values should be displayed in a single diagram, than this type of chart can be used. It accepts two values from two input port and displayes it simultaniously. ```y value``` generators can be found in files [ex-2-1-generator.js](../examples/ex-2-1-generator.js) and [ex-2-2-generator.js](../examples/ex-2-2-generator.js). They are connected to single python component which generates html with the chart. Python code can be found in [ex-2-line-plot-2.py](../examples/ex-2-line-plot-2.py) with coresponding configuration:

```python
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
```
Finally, the diagram looks as follows:

![Example 2 - Multiple Line Data Hub ](../resources/ex-2.png)

---
---
#### Example 3 - Single Cluster Scatter Plot

![Example 3 - Single Cluster Scatter Plot ](../resources/ex-3.gif)

Sometimes, data are organized in clusters and it can be useful to represent them. This example represents single point (single input) in 2D coordinate system.

Altough, the python script that generates html accepts two inputs, semantically they represent one point with two coordinates. First generator [ex-3-1-generator.js](../examples/ex-3-1-generator.js) generates ```x-value``` and second one [ex-3-2-generator.js](../examples/ex-3-2-generator.js) is responsible for ```y value```.

Then, html creator merges these two inputs and creates single html file (output), which is described in [ex-3-scatter-plot-1.py](../examples/ex-3-scatter-plot-1.py). Configuration is listed at the begining of the file:
```python
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
label_decimals = 0                  # number of decimal places used for displaying labels on y axis.label_decimals = 0 -> integers are displayed
graph_name = "User Segmentation"    # title/graph name
# -------------------------------------------------------------------------------------------
```
At the end, the the look of the pipeline is shown in image below.

![Example 3 - Single Cluster Scatter Plot ](../resources/ex-3.png)

---
---

#### Example 4 - Two Clusters Scatter Plot

#### Example 5 - Map Visualization


