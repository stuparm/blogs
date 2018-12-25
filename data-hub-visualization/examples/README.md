## Examples

This folder contains five examples that can be separated into three categories:
1) Line Charts
    - [Example 1 - Single Line Chart](#Example-1---Single-Line-Chart) - Single Input
    - [Example 2 - Multiple Line Chart](#Example-2---Multiple-Line-Chart) - Two Inputs
2) Scatter Plots 
    - [Example 3 - Single Type Scatter Plot](#Example-3---Single-Type-Scatter-Plot) - Single Input
    - Example 4 - Two Types  - Two Inputs
3) Map Visualization 
    - Example 5 - Map Visualization - Single Input of GPS points
---
#### Example 1 - Single Line Chart

![Example 1 - Single Line Chart ](../resources/ex-1.gif)

This type of chart is useful for displaying single input (single value). Entry point is just ```y value``` and in this case, ```y value``` is in range [20,40]. The code for generating such a value is in file [examples/ex-1-generator.js](../examples/ex-1-generator.js). As shown in the diagram, there are no ```x values```. This is because, this diagram is timestamp oriented, which means every time the ```y value``` arrives, it is shown in the diagram (in our case it is generated every 500ms).

The code for html chart creation is in file [examples/ex-1-line-plot-1.py](../examples/ex-1-line-plot-1.py). The code is more/less generic and external user should only be focused on ```configuration``` part.

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






#### Example 2 - Multiple Line Chart

#### Example 3 - Single Cluster Scatter Plot

#### Example 4 - Two Types Scatter Plot

#### Example 5 - Map Visualization


