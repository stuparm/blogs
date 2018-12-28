## SAP Data Hub Visualization

I would change the well-known phrase and say:
> “An **animated** picture is worth a **million** words”. 

And, because of that, the animated image below shows the result of this blog post. Later we will go into prerequisites and steps needed to achieve it.

![Example 2](./resources/gif/ex-2.gif)

*More **visual** examples at the end of the blog.*

### Introduction and Prerequisites

I believe that everyone interested in this topic (blog) is already the user of SAP Data Hub, so special introduction is not necessary. In any case, I would recommend the following links if someone is just starting:
- https://blogs.sap.com/2017/12/06/sap-data-hub-developer-edition/
- https://blogs.sap.com/2018/04/26/sap-data-hub-trial-edition/

I personally use **developer edition** and run Data Hub as a docker container on my local machine. All examples are created and tested using this edition, but they work also on any other environment since they use only very basic functionalities of Data Hub.

### Problem

I find Data Hub as a great tool to orchestrate and manage especially IoT sensor data. In general, I am more/less focused on one goal with this tool: extract the meaningful information. For that purpose, I have to create few operators (Javascript, Python, …) that enrich or filter raw data. In this whole process I have to debug my pipeline and for that I usually use well known **Terminal** operator.

![Terminal](./resources/gif/terminal.gif)

Unfortunately, **Terminal** is not so user friendly and it is not always easy to find specific “line” or specific “value”. If we want to monitor single or multiple sensor values, it would be impossible with this console view.

### Solution

For me, the ideal replacement for **Terminal** operator would be something that we can call Chart Operator which will graphically visualize sensor data in real time. For that purpose, I found operator called **HTML Viewer** which will show any html received on input port. If you go to Data Hub Modeler and search for **HTML Viewer**, you will see the description:

![step-0](./resources/steps/step-0.png)

Here, I would like to highlight the comment which says that script tags will be ignored. It means that we are not able to generate some Javasctipt code as part of HTML because this operator will just ignore it. *I suppose that we are all a little bit familiar with Javascript and know that it is responsible for fancy charts available today.*

In other words, we would have to generate pure HTML and CSS code which will be visible as part of **HTML Viewer**, but with provided **Instant Refresh** functionality we could achieve continuous updates of our charts.

In next part of the blog, we will go though step-by-step process and create simple pipeline which start with **Data Generator** and end with **HTML Viewer**.

### Step by Step

#### 1 - Data Generator Operators

First we will create two **Data Generator operators. They will simulate the streaming from two sensors. For simplicity, they will just generate random value in specified range and propagate it further.