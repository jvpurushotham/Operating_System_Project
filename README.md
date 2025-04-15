Virtual Memory Management Tool

🧠 Overview

The Virtual Memory Management Tool is a simulation-based educational application that allows users to understand and visualize how operating systems manage memory using paging and segmentation techniques. It provides hands-on interaction with critical concepts such as page faults, demand paging, and memory fragmentation, and supports page replacement algorithms like LRU (Least Recently Used) and Optimal.

This tool is ideal for students, educators, and developers who want to explore the internal workings of memory management in operating systems.

🚀 Features

Paging Simulation
Visualize memory allocation via pages and frames.
Track page faults and simulate demand paging behavior.
Segmentation Simulation
Explore how logical memory is divided into segments.
Visualize segment tables and fragmented memory space.
Page Replacement Algorithms
Choose between LRU and Optimal algorithms.
Visualize page replacement decisions dynamically.
Custom Memory Input
Users can enter custom page references, memory size, and allocation settings.
Simulate multiple scenarios for better understanding.
Memory Fragmentation Visualization
See how fragmentation occurs over time.
Compare paging vs segmentation in real-time.
Interactive GUI
Built using PyQt5, offering an intuitive and dynamic graphical interface.
GraphicsView-based memory layout rendering.
🛠️ Technologies Used

Python Libraries
PyQt5: For building the GUI.
QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox, QLineEdit, QTabWidget
QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
QStatusBar, QColor, QBrush
📦 Installation

Prerequisites
Python 3.x
PyQt5
pip install PyQt5
Clone the Repository
git clone https://github.com/yourusername/virtual-memory-tool.git
cd virtual-memory-tool
Run the App
python main.py
📷 Screenshots



🧪 How to Use

Launch the application.
Select Paging or Segmentation from the tab menu.
Enter memory configuration values (e.g., frame size, number of pages, etc.).
Choose a page replacement algorithm.
Click Simulate to begin the visualization.
Observe the graphical memory representation and statistics shown in the status bar.
📚 Educational Goals

Understand the difference between paging and segmentation.
Learn how page replacement algorithms work.
Visualize how memory fragmentation affects allocation.
Gain insight into how demand paging reduces memory load.
🙌 Contribution

Contributions are welcome! Please open issues or pull requests to enhance functionality, fix bugs, or improve visual design.

📄 License

This project is open-source and licensed under the MIT License.

👨‍💻 Author

Developed by [J V Purushotham]
Contact: jvpurushotham31@gmail.com
