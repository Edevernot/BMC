import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image, ImageDraw, ImageFont

class PoseClassificationVisualizer(object):
    def __init__(self,
                 class_name,
                 counter_font_path='Roboto-Regular.ttf',
                 plot_location_y=0.05,
                 plot_max_height=0.4,
                 plot_figsize=(9, 4),
                 plot_x_max=None,
                 plot_y_max=None,
                 counter_location_x=0.85,
                 counter_location_y=0.02,
                 counter_font_color='red',
                 counter_font_size=0.05):
        self._class_name = class_name
        self._plot_location_y = plot_location_y
        self._plot_max_height = plot_max_height
        self._plot_figsize = plot_figsize
        self._plot_x_max = plot_x_max
        self._plot_y_max = plot_y_max
        self._counter_location_x = counter_location_x
        self._counter_location_y = counter_location_y
        self._counter_font_color = counter_font_color
        self._counter_font_size = counter_font_size
        self._counter_font_path = counter_font_path
        self._counter_font = None
        self._pose_classification_history = []
        self._pose_classification_filtered_history = []

    def __call__(self,
                 frame,
                 pose_classification,
                 pose_classification_filtered,
                 repetitions_count):
        # Extend classification history.
        self._pose_classification_history.append(pose_classification)
        self._pose_classification_filtered_history.append(pose_classification_filtered)

        # Output frame with classification plot and counter.
        output_img = Image.fromarray(frame)
        output_width, output_height = output_img.size

        # Draw the plot.
        plot_img = self._plot_classification_history(output_width)
        plot_img_height = int(output_height * self._plot_max_height)
        plot_img = plot_img.resize((output_width, plot_img_height))

        # Combine output_img and plot_img vertically.
        combined_img = Image.new('RGB', (output_width, output_height + plot_img_height))
        combined_img.paste(output_img, (0, 0))
        combined_img.paste(plot_img, (0, output_height))

        # Draw the counter on the original output_img part.
        draw = ImageDraw.Draw(combined_img)
        if self._counter_font is None:
            font_size = int(output_height * self._counter_font_size)
            self._counter_font = ImageFont.truetype(self._counter_font_path, size=font_size)
        counter_x = self._counter_location_x * output_width
        counter_y = self._counter_location_y * output_height
        draw.text((counter_x, counter_y),
                  str(repetitions_count),
                  font=self._counter_font,
                  fill=self._counter_font_color)

        return np.array(combined_img)

    def _plot_classification_history(self, output_width):
        fig = Figure(figsize=self._plot_figsize)
        ax = fig.subplots()
        ax.set_title('Classification history for `{}`'.format(self._class_name))
        ax.set_xlabel('Frame')
        ax.set_ylabel('Confidence')

        # Plot each classification history as a separate line.
        for history in [self._pose_classification_history, self._pose_classification_filtered_history]:
            y = [classification.get(self._class_name, 0) if classification else 0 for classification in history]
            ax.plot(y, linewidth=7)

        ax.grid(axis='y', alpha=0.75)
        if self._plot_y_max is not None:
            ax.set_ylim(top=self._plot_y_max)
        if self._plot_x_max is not None:
            ax.set_xlim(right=self._plot_x_max)

        fig_canvas = FigureCanvas(fig)
        fig_canvas.draw()
        plot_img = np.frombuffer(fig_canvas.tostring_rgb(), dtype=np.uint8)
        plot_img = plot_img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        return Image.fromarray(plot_img)


