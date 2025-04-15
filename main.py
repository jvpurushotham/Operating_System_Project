from PyQt5.QtGui import QColor, QBrush
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QLineEdit, QTabWidget, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsTextItem, QStatusBar
)

# Main application window
class MemoryVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Management Visualizer")  # Window title
        self.setGeometry(100, 100, 1000, 700)  # Window size and position

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.tabs = QTabWidget()  # Tabbed layout
        main_layout.addWidget(self.tabs)

        self.paging_tab = QWidget()  # Paging tab
        self.segmentation_tab = QWidget()  # Segmentation tab
        self.tabs.addTab(self.paging_tab, "Paging")
        self.tabs.addTab(self.segmentation_tab, "Segmentation")

        self.statusBar = QStatusBar()  # Status bar
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        self.setup_paging_tab()  # Setup paging UI
        self.setup_segmentation_tab()  # Setup segmentation UI

    # Setup for paging
    def setup_paging_tab(self):
        layout = QVBoxLayout(self.paging_tab)
        control_layout = QHBoxLayout()

        control_layout.addWidget(QLabel("Algorithm:"))
        self.algorithm_combo = QComboBox()  # Algorithm selection
        self.algorithm_combo.addItems(["LRU", "Optimal"])
        control_layout.addWidget(self.algorithm_combo)

        control_layout.addWidget(QLabel("Frames:"))
        self.frame_spin = QSpinBox()  # Frame size input
        self.frame_spin.setRange(1, 20)
        self.frame_spin.setValue(4)
        control_layout.addWidget(self.frame_spin)

        control_layout.addWidget(QLabel("Reference String:"))
        self.ref_string_input = QLineEdit()  # Reference string input
        self.ref_string_input.setPlaceholderText("e.g. 1,2,3,4,1,2,5")
        control_layout.addWidget(self.ref_string_input)

        self.start_btn = QPushButton("Start")  # Start button
        self.step_btn = QPushButton("Step")  # Step button
        self.reset_btn = QPushButton("Reset")  # Reset button
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.step_btn)
        control_layout.addWidget(self.reset_btn)

        layout.addLayout(control_layout)

        self.paging_view = QGraphicsView()  # Visual display
        self.paging_scene = QGraphicsScene()
        self.paging_view.setScene(self.paging_scene)
        layout.addWidget(self.paging_view)

        self.stats_label = QLabel("Page Faults: 0")  # Faults display
        layout.addWidget(self.stats_label)

        self.frames = []  # Frame storage
        self.ref_list = []  # Reference string list
        self.current_index = 0
        self.page_faults = 0

        self.start_btn.clicked.connect(self.start_paging)
        self.step_btn.clicked.connect(self.step_paging)
        self.reset_btn.clicked.connect(self.reset_paging)

    def start_paging(self):
        self.frames.clear()
        self.page_faults = 0
        self.current_index = 0
        self.paging_scene.clear()

        ref_string = self.ref_string_input.text().strip()
        if not ref_string:
            self.statusBar.showMessage("Error: Enter a reference string!")
            return

        try:
            self.ref_list = [int(x.strip()) for x in ref_string.split(',')]  # Parse input
        except ValueError:
            self.statusBar.showMessage("Error: Invalid input!")
            return

        self.statusBar.showMessage("Paging started!")
        self.step_paging()  # Start first step

    def step_paging(self):
        if self.current_index >= len(self.ref_list):  # End of string
            self.statusBar.showMessage("All references processed.")
            return

        page = self.ref_list[self.current_index]
        algorithm = self.algorithm_combo.currentText()
        frame_limit = self.frame_spin.value()

        if page not in self.frames:
            self.page_faults += 1  # Fault occurred
            if len(self.frames) < frame_limit:
                self.frames.append(page)
            else:
                if algorithm == "LRU":
                    self.frames.pop(0)  # Remove LRU page
                elif algorithm == "Optimal":
                    future = self.ref_list[self.current_index+1:]
                    indices = [future.index(f) if f in future else float('inf') for f in self.frames]
                    to_remove = indices.index(max(indices))  # Optimal replacement
                    self.frames.pop(to_remove)
                self.frames.append(page)
        else:
            if algorithm == "LRU":
                self.frames.remove(page)
                self.frames.append(page)  # Update LRU

        self.current_index += 1
        self.stats_label.setText(f"Page Faults: {self.page_faults}")
        self.visualize_paging()  # Refresh visuals

    def reset_paging(self):
        self.frames.clear()
        self.ref_list.clear()
        self.page_faults = 0
        self.current_index = 0
        self.paging_scene.clear()
        self.stats_label.setText("Page Faults: 0")
        self.statusBar.showMessage("Paging reset!")

    def visualize_paging(self):
        self.paging_scene.clear()
        self.paging_scene.setBackgroundBrush(QBrush(QColor("#1e1e2f")))  # Background color

        for i, frame in enumerate(self.frames):
            rect = QGraphicsRectItem(50, i * 50, 100, 50)  # Frame block
            rect.setBrush(QBrush(QColor("#4CAF50")))
            self.paging_scene.addItem(rect)
            text = QGraphicsTextItem(str(frame))  # Frame text
            text.setPos(85, i * 50 + 12)
            self.paging_scene.addItem(text)

    # Setup for segmentation
    def setup_segmentation_tab(self):
        layout = QVBoxLayout(self.segmentation_tab)
        control_layout = QHBoxLayout()

        control_layout.addWidget(QLabel("Memory Size:"))
        self.mem_size_spin = QSpinBox()  # Total memory input
        self.mem_size_spin.setRange(100, 10000)
        self.mem_size_spin.setValue(1024)
        control_layout.addWidget(self.mem_size_spin)

        control_layout.addWidget(QLabel("Segment Size:"))
        self.seg_size_spin = QSpinBox()  # Segment size input
        self.seg_size_spin.setRange(10, 500)
        self.seg_size_spin.setValue(100)
        control_layout.addWidget(self.seg_size_spin)

        self.alloc_btn = QPushButton("Allocate")  # Allocate memory
        self.dealloc_btn = QPushButton("Deallocate")  # Deallocate memory
        control_layout.addWidget(self.alloc_btn)
        control_layout.addWidget(self.dealloc_btn)

        layout.addLayout(control_layout)

        self.seg_view = QGraphicsView()  # Segmentation view
        self.seg_scene = QGraphicsScene()
        self.seg_view.setScene(self.seg_scene)
        layout.addWidget(self.seg_view)

        self.frag_label = QLabel("Remaining Memory: 1024 KB")  # Memory remaining
        layout.addWidget(self.frag_label)

        self.remaining_memory = self.mem_size_spin.value()
        self.allocated_blocks = []  # Store segments

        self.alloc_btn.clicked.connect(self.allocate_memory)
        self.dealloc_btn.clicked.connect(self.deallocate_memory)
        self.mem_size_spin.valueChanged.connect(self.reset_memory)

    def allocate_memory(self):
        segment_size = self.seg_size_spin.value()
        if segment_size <= self.remaining_memory:
            self.allocated_blocks.append(segment_size)  # Allocate segment
            self.remaining_memory -= segment_size
            self.update_segmentation_visuals()
            self.statusBar.showMessage(f"Allocated {segment_size} KB. Remaining: {self.remaining_memory} KB")
        else:
            self.statusBar.showMessage("Error: Not enough memory available!")

    def deallocate_memory(self):
        if self.allocated_blocks:
            freed_size = self.allocated_blocks.pop()  # Deallocate last
            self.remaining_memory += freed_size
            self.update_segmentation_visuals()
            self.statusBar.showMessage(f"Deallocated {freed_size} KB. Remaining: {self.remaining_memory} KB")
        else:
            self.statusBar.showMessage("Error: No segments to deallocate!")

    def reset_memory(self):
        self.allocated_blocks.clear()  # Clear all segments
        self.remaining_memory = self.mem_size_spin.value()
        self.update_segmentation_visuals()
        self.statusBar.showMessage("Memory reset!")

    def update_segmentation_visuals(self):
        self.seg_scene.clear()
        self.seg_scene.setBackgroundBrush(QBrush(QColor("#1b263b")))  # Background color
        total_memory = self.mem_size_spin.value()
        view_height = 400
        scale_factor = view_height / total_memory
        y_offset = 0
        colors = ["#e63946", "#a8dadc", "#457b9d", "#f36f53", "#ffb703"]  # Segment colors

        for i, segment in enumerate(self.allocated_blocks):
            scaled_height = max(segment * scale_factor, 5)  # Scale block
            rect = QGraphicsRectItem(50, y_offset, 200, scaled_height)
            rect.setBrush(QBrush(QColor(colors[i % len(colors)])))
            self.seg_scene.addItem(rect)

            text = QGraphicsTextItem(f"{segment} KB")  # Segment label
            text.setDefaultTextColor(QColor("#ffffff"))
            text.setPos(125, y_offset + scaled_height / 4)
            self.seg_scene.addItem(text)

            y_offset += scaled_height

        self.frag_label.setText(f"Remaining Memory: {self.remaining_memory} KB")

# Entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemoryVisualizer()
    window.show()
    sys.exit(app.exec_())
