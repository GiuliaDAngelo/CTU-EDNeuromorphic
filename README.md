# CTU: Event-driven sensing and Neuromorphic computing

## Introduction 

Robotics is entering a new era of intelligence, where traditional approaches to perception 
and computation are no longer sufficient to meet the demands of real-time, energy-efficient,
and adaptive systems. To enable more complex behaviours and facilitate the seamless integration 
of robots into daily human environments, it is imperative to significantly reduce the power 
consumption of robotic applications.

Event-driven sensing and neuromorphic computing offer disruptive solutions to these challenges 
by mimicking how biological brains perceive and process their surroundings, a critical step toward
the next generation of robotic autonomy. Unlike conventional systems that process data at fixed
intervals, event-driven systems react only when a change occurs in the environment. 
Event-driven sensing encompasses a range of event-based sensors for [vision](https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/), 
[audio](https://link.springer.com/referenceworkentry/10.1007/978-1-4614-7320-6_118-1), and [touch](https://link.springer.com/referenceworkentry/10.1007/978-981-16-5540-1_117), 
seamlessly integrating with neuromorphic platforms ([SpiNNaker](https://www.humanbrainproject.eu/en/collaborate-hbp/innovation-industry/technology-catalogue/spinnaker/),
[Speck](https://www.synsense.ai/products/speck-2/), [BrainScaleS](https://brainscales.kip.uni-heidelberg.de/), [Loihi](https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html), [Akida](https://brainchip.com/akida-neural-processor-soc/)) 
to enable the construction of spiking neural networks for efficient computation.
This shift enables low-latency, low-power, and highly efficient processing, essential for autonomous
robots, smart city infrastructure, and space exploration — fields where quick adaptation, energy 
efficiency, and data reduction are key.

Event-based information processing has gained significant [attention](https://www.eetimes.com/what-does-neuromorphic-mean-today/) from the scientific community 
(and worldwide media such as [EE Times](https://www.eetimes.com/tag/neuromorphic/)) due to the promising results of early studies at 
[Caltech University in the late 1980s](http://www.carvermead.caltech.edu/). The concept of neuromorphic computing has evolved, with its meaning changing 
based on the level of emulation of neuron dynamics. This technology has attracted interest because 
of the fundamental belief that nature and biology possess superior characteristics for solving daily
tasks. 

## A Bit of History  

### Carver Mead  

[Carver Mead](http://www.carvermead.caltech.edu/), a professor at Caltech, is widely recognized as the founder of neuromorphic engineering. In the late 1980s, he introduced the concept of using analog VLSI circuits to mimic neuro-biological architectures present in the nervous system. His seminal work, *A Silicon Model of Early Visual Processing*, co-authored with Misha Mahowald in 1988, demonstrated the potential of silicon-based neural systems. In 2024, Mead was honored with a lifetime contribution award by the Misha Mahowald Prize committee for his foundational work in the field.  
[Read more at Caltech](https://www.caltech.edu/about/news/carver-mead-earns-lifetime-contribution-award-for-neuromorphic-engineering/)  

[![Carver Mead - Neuromorphic Engineering](https://img.youtube.com/vi/vznthE_AsVM/0.jpg)](https://www.youtube.com/watch?v=vznthE_AsVM)

### Misha Mahowald  

[Misha Mahowald](https://direct.mit.edu/neco/article/35/3/343/113812/Neuromorphic-Engineering-In-Memory-of-Misha), one of Mead's doctoral students, made significant contributions to neuromorphic engineering. She developed the first silicon retina, an analog VLSI system that emulated the early visual processing of the human retina. Her groundbreaking work in the early 1990s on a silicon model of stereoscopic vision provided a foundation for future neuromorphic vision systems. In her honor, the Misha Mahowald Prize was established to recognize outstanding achievements in neuromorphic engineering.  

[![Misha Mahowald - Event-Based Vision](https://img.youtube.com/vi/dh8O5PuxyTk/0.jpg)](https://www.youtube.com/watch?v=dh8O5PuxyTk)


### Tobi Delbruck  

[Tobi Delbruck](https://www.eetimes.com/podcasts/tobi-delbruck-talks-caltech-cameras-and-neural-control/) is a professor at the Institute of Neuroinformatics at the University of Zurich and ETH Zurich. He has played a crucial role in advancing neuromorphic engineering, particularly in the development of event-based vision sensors. Collaborating with Mead and Mahowald, Delbruck has contributed significantly to silicon retinas and event-driven cameras, shaping the design of modern low-latency, low-power vision systems.  

[![Tobi Delbruck - Neuromorphic Vision](https://img.youtube.com/vi/Y1KBAFM1Iuc/0.jpg)](https://www.youtube.com/watch?v=Y1KBAFM1Iuc)

### Giacomo Indiveri  


[Giacomo Indiveri](https://ee.ethz.ch/the-department/people-a-z/person-detail.Nzk0NzU=.TGlzdC8zMjc5LC0xNjUwNTg5ODIw.html) is a prominent figure in neuromorphic engineering, making significant advancements in the development of bio-inspired computational architectures. His research focuses on creating hardware that mimics the brain's neural processes, particularly in sensory processing and perception. Indiveri has been instrumental in designing neuromorphic chips and systems capable of real-time processing of sensory data, which has important implications for robotics and artificial intelligence. His contributions have fostered collaboration across disciplines, further advancing the field of neuromorphic computing.

[![Giacomo Indiveri - Neuromorphic Engineering](https://img.youtube.com/vi/eTbd8JXcf3Y/0.jpg)](https://www.youtube.com/watch?v=eTbd8JXcf3Y&ab_channel=UCBerkeleyEvents)


## Key Figures in Neuromorphic Engineering  

Here is a list of pioneers and leading researchers in the field of neuromorphic computing along with their affiliations:  

- **Carver Mead** – Professor Emeritus, California Institute of Technology ([Caltech](https://www.caltech.edu/))  
- **Misha Mahowald** – Former researcher, California Institute of Technology  
- **Tobi Delbruck** – Professor, Institute of Neuroinformatics, University of Zurich & ETH Zurich ([INI Zurich](https://www.ini.uzh.ch/))  
- **Kwabena Boahen** – Professor, Stanford University ([Stanford Brains in Silicon](https://web.stanford.edu/group/brainsinsilicon/))  
- **Giacomo Indiveri** – Professor, Institute of Neuroinformatics, University of Zurich & ETH Zurich ([INI Zurich](https://www.ini.uzh.ch/))  
- **Shih-Chii Liu** – Professor, Institute of Neuroinformatics, University of Zurich & ETH Zurich ([INI Zurich](https://www.ini.uzh.ch/))  
- **Steve Furber** – Professor, University of Manchester, leader of SpiNNaker project ([SpiNNaker](https://www.cs.manchester.ac.uk/research/expertise/neuromorphic-computing/))  
- **Karlheinz Meier** (1955–2018) – Physicist and co-founder of neuromorphic hardware projects ([BrainScaleS](https://brainscales.kip.uni-heidelberg.de/))  
- **Chris Eliasmith** – Director of the Centre for Theoretical Neuroscience, University of Waterloo ([Waterloo CTN](https://uwaterloo.ca/))  

This tutorial provides an introduction to event-driven sensing and neuromorphic computing, highlighting its historical origins and key contributors. The field continues to evolve, driving advancements in robotics, artificial intelligence, and low-power computing for real-world applications. 🚀  

## What Are Event-Based Cameras?

Unlike traditional cameras that capture full frames at fixed intervals—such
as 30 or 60 frames per second—**event-based cameras** operate on a 
fundamentally different principle. These innovative cameras are 
engineered to detect and record **changes** in the scene on a pixel-by-pixel
basis. Instead of capturing a complete image of the entire scene at once, 
they only respond to what *moves* or *changes* in brightness, providing a
more dynamic representation of the visual environment.

In an event-based camera, each pixel functions independently. This means
that when a pixel detects a change in brightness—whether due to motion, 
lighting shifts, or other factors—it reacts immediately. Upon detecting a 
change, the pixel emits an **event** instead of a traditional frame. This
event contains information about the time and location of the change. As a
result, static areas of the scene do not generate events, leading to a 
significant reduction in the amount of data collected. This characteristic
is particularly advantageous for conserving **memory** and **energy**.

Event-based cameras are notable for their ultra-fast response time. They
capture changes as they occur, enabling real-time processing with virtually
no delay. This rapid response is crucial for applications that require 
immediate feedback. Additionally, by focusing only on relevant changes in
the scene, event-based cameras collect significantly less information than
traditional cameras, making them highly efficient and suitable for devices
with limited processing power and storage capacity.

These cameras excel at capturing rapid movements, making them ideal
for scenarios such as sports, aerial drones in flight, and autonomous
vehicles navigating complex environments. Their ability to track fast-moving 
objects with precision sets them apart from conventional imaging systems,
allowing for more advanced applications in robotics and beyond.

![events](Images/example.gif)  
*Copyright for the GIF: Arren Glover, Italian Institute of Technology*

Event-based cameras[1], which mimic the initial 
layers of the mammalian retina and react to pixel-level illumination 
changes, offer a solution to the limitations of the frame-based cameras. 
Unlike frame-based cameras, event-based sensors improve dynamic range,
reduce latency, and generate an
asynchronous event stream providing information of spatial coordinates, 
polarity, and timestamps. This results in a significant reduction in data
processing, making event-based cameras highly relevant for robotic 
applications[2,3,4,5]. 
Their inherent real-time response to luminance changes provides 
an ideal sensory input for guiding subsequent visual attention actions.


### References: 
- [1] Lichtsteiner, P., Posch, C., & Delbruck, T. (2008). A 128x128 120dB 15us Latency Asynchronous Temporal Contrast Vision Sensor. IEEE Journal of Solid-State Circuits, 43(2), 566-576.**
- [2] Monforte, Marco, et al. "Exploiting event cameras for spatio-temporal prediction of fast-changing trajectories." 2020 2nd IEEE International Conference on Artificial Intelligence Circuits and Systems (AICAS). IEEE, 2020.
- [3] Mueggler, Elias, et al. "Continuous-time visual-inertial odometry for event cameras." IEEE Transactions on Robotics 34.6 (2018): 1425-1440.
- [4] Iacono, Massimiliano, et al. "Towards event-driven object detection with off-the-shelf deep learning." 2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2018.
- [5] Glover, Arren, and Chiara Bartolozzi. "Robust visual tracking with a freely-moving event camera." 2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2017.
- [6] Bartolozzi, Chiara, et al. "Embedded neuromorphic vision for humanoid robots." CVPR 2011 workshops. IEEE, 2011.


![bm](Images/bmlogo.png)  

If you want to know more about the history and advancements in neuromorphic 
engineering and event-based sensing, check out the ["Brains and Machines"](https://brainsandmachines.net/) 
podcast.  This podcast delves into the intersection of neuroscience, robotics, and artificial intelligence, featuring discussions with influential leading experts in the field and exploring the latest research and innovations.

![bm](Images/bm.png)  


# Tutorial Overview
## Tutorial 1 (A) - Time Window for Event-Based Data Visualization  

This script demonstrates how to load and visualize event-based data from a Dynamic Vision Sensor (DVS). Unlike conventional cameras, a DVS detects brightness changes at each pixel asynchronously, providing high temporal resolution. Using the `importIitYarp` function from the Bimvee library, the script extracts event coordinates, timestamps, and polarities. Events are processed within fixed time windows, and the visualization updates dynamically in real time with OpenCV, showcasing the benefits of event-based vision for dynamic scene analysis.  

[Tutorial1-EventBasedDataTimeWindow.py](Tutorial1-EventBasedDataTimeWindow.py)  

![DVSdata](Images/attdata.png)  
---

## Tutorial 1 (B) - Sliding Window for Event-Based Data Visualization  

This script extends time-windowed visualization by continuously updating the displayed events using a sliding window approach. Events from a DVS are loaded with Bimvee, processed within an initial time window, and updated dynamically by removing outdated events while adding new ones. ON and OFF events are tracked separately, and OpenCV provides real-time visualization. This approach is useful for understanding motion encoding and scene changes in neuromorphic cameras.  

[Tutorial1-EventBasedDataSlidingWindow.py](Tutorial1-EventBasedDataSlidingWindow.py)  

---

## Tutorial 1 (C) - Fixed Event Count for Event-Based Data Visualization  

Instead of a time-based window, this script processes a fixed number of events per visualization cycle. It loads DVS data, extracts event properties, and updates the display in real time, ensuring a consistent event sampling rate. This method is useful for applications requiring precise event control, such as neuromorphic computing, object tracking, and motion analysis.  

[Tutorial1-EventBasedDataNumberEvents.py](Tutorial1-EventBasedDataNumberEvents.py)  

---

## Tutorial 2: Loading IBM DVS Gesture Dataset  

This tutorial explores and visualizes event-based data from the DVSGesture dataset, captured by a DVS. The sensor records scene changes with high temporal resolution, enabling detection of rapid movements. The script converts event data into frames representing positive and negative polarities, providing insight into the sensor's response to different stimuli. The final output displays these frames side by side for a comprehensive analysis of event-based vision systems.  

[Tutorial2-EventBasedData.py](Tutorial2-EventBasedData.py)  

![ibmdvs](Images/IBMDVS.png)  
