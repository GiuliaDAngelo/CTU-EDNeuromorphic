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

## Key Figures in Neuromorphic Engineering  

Here is a list of pioneers and leading researchers in the field of neuromorphic computing along with their affiliations:  

- **Carver Mead** – Professor Emeritus, California Institute of Technology ([Caltech](https://www.caltech.edu/))  
- **Misha Mahowald** – Former researcher, California Institute of Technology  
- **Tobi Delbruck** – Professor, Institute of Neuroinformatics, University of Zurich & ETH Zurich ([INI Zurich](https://www.ini.uzh.ch/))  
- **Kwabena Boahen** – Professor, Stanford University ([Stanford Brains in Silicon](https://brainsinsilicon.stanford.edu/))  
- **Giacomo Indiveri** – Professor, Institute of Neuroinformatics, University of Zurich & ETH Zurich ([INI Zurich](https://www.ini.uzh.ch/))  
- **Shih-Chii Liu** – Professor, Institute of Neuroinformatics, University of Zurich & ETH Zurich ([INI Zurich](https://www.ini.uzh.ch/))  
- **Steve Furber** – Professor, University of Manchester, leader of SpiNNaker project ([SpiNNaker](https://www.cs.manchester.ac.uk/research/expertise/neuromorphic-computing/))  
- **Karlheinz Meier** (1955–2018) – Physicist and co-founder of neuromorphic hardware projects ([BrainScaleS](https://brainscales.kip.uni-heidelberg.de/))  
- **Chris Eliasmith** – Director of the Centre for Theoretical Neuroscience, University of Waterloo ([Waterloo CTN](https://uwaterloo.ca/centre-theoretical-neuroscience/))  

This tutorial provides an introduction to event-driven sensing and neuromorphic computing, highlighting its historical origins and key contributors. The field continues to evolve, driving advancements in robotics, artificial intelligence, and low-power computing for real-world applications. 🚀  

## What are Event-Based Cameras? 📸
Unlike traditional cameras that capture full images at fixed intervals (e.g., 30 or 60 times per second), **event-based cameras** work differently. These cameras are designed to capture **changes** in the scene — pixel by pixel! Instead of taking pictures of the entire scene at once, they only capture what *moves* or *changes* in brightness. 📍✨

![events](https://github.com/GiuliaDAngelo/EDtutorial/blob/main/Images/example.gif)

Copyrigths for the GIF, Arren Glover, Italian Institute of Technology


**Do you want to know more?** Look at my [CTUTalk](https://github.com/GiuliaDAngelo/EDtutorial/blob/main/Images/CTUtalk.pdf)


### How They Work 🧠🔬
- Each pixel in an event-based camera works **independently** and detects changes in brightness 🎥.
- When a pixel detects a change, it sends out an **event** 🚀 (instead of a frame). This means less data is collected for static areas, saving **memory** and **energy** 🔋.

## Why is it so Cool? 😎
- **Ultra-fast** ⚡: They capture events as they happen, with no delay!
- **Efficient** 💡: Only relevant information is collected, making them great for devices with limited resources.
- **Motion detection** 🏃‍♂️: They excel at capturing fast movements like sports, drones in flight, or self-driving cars 🏎️.

## Neuromorphic Vision: What’s That? 🤖🧠
Neuromorphic vision systems mimic the way our **brain** and **eyes** work! 👁️🧠 The idea is to create cameras and chips that process visual information more like human vision, reacting to changes in the environment in **real-time**. 

These systems use **event-based cameras** to collect data and neuromorphic processors to make decisions, just like how our brain reacts to what we see in milliseconds. 🤯

### Benefits of Neuromorphic Vision Systems 🌍🔍
- **Real-time processing**: Instant reactions without waiting for a full image 🎞️.
- **Power efficiency**: By focusing only on changes, these systems save energy and reduce data overload ⚙️.
- **Biologically inspired**: They simulate how **our neurons** work, making them more adaptive and responsive 🧠⚡.

## Cool Applications 🛠️
- **Robotics** 🤖: Robots equipped with event-based cameras can navigate dynamic environments more smoothly!
- **Self-driving cars** 🚗: They use these cameras to react instantly to objects on the road.
- **Sports** 🏀: Capture high-speed sports actions and improve player performance analysis.
- **Healthcare** 💉: Monitoring eye movements for diagnosing medical conditions.

## Want to Learn More? 📚
If you're curious about how the brain 🧠 can inspire technology, **neuromorphic vision** is the perfect place to start! With these futuristic tools, we can create smarter, faster, and more efficient systems. 🌍✨

Check out the for a hands-on introduction!

Do you want to see what events look like? Here you have a tutorial for you: 
- [Real Data](https://github.com/GiuliaDAngelo/EDtutorial/blob/main/realdata.py)

Do you want to create a neuron and see its behaviour?
- [Neuron tutorial](https://github.com/GiuliaDAngelo/EDtutorial/blob/main/neuron.py)

## References 📚
Here are some valuable resources to learn more about event-based cameras and neuromorphic vision:

1. **Papers:**
   - [Event-Based Vision: A Survey](https://ieeexplore.ieee.org/abstract/document/9138762) by Gallego et al. – A comprehensive survey of event-based vision systems.
   - [Neuromorphic Engineering](https://link.springer.com/chapter/10.1007/978-3-662-43505-2_38) by Giacomo Indiveri – An overview of neuromorphic engineering principles and applications.


4. **Websites:**
   - [Event-based Perception for Robotics](https://edpr.iit.it/) – A dedicated resource for event-based vision research and applications.
   - [Neuromorphic Computing and Engineering](https://iopscience.iop.org/journal/2634-4386) – A journal focused on neuromorphic computing research.


🧠 **Stay curious!**
