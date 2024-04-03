"""
Clock App Program.

Input:
- None.

Output:
- Displays a clock app with time, stopwatch, and buttons for start/stop and reset.

Features:
1. Display time, stopwatch, and buttons for start/stop and reset.
2. Light and dark mode color schemes.
3. Click sound for buttons.
4. Alarm functionality with sound.
5. Set, snooze, and stop alarm features.
6. Lap time recording for the stopwatch.
7. Toggle between light and dark modes.

Usage:
- Run the script to launch the clock app with the specified features.

"""

import time
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.lang import Builder
from time import strftime
import os

# Define colors for light and dark mode
light_mode_colors = {
    'background': '#FFFFFF',
    'text': '#000000',
    'button_normal': '#4CAF50',
    'button_down': '#45A049',
}

dark_mode_colors = {
    'background': '#121212',
    'text': '#FFFFFF',
    'button_normal': '#333333',
    'button_down': '#585858',
}

class AlarmPopup(Popup):
    def __init__(self, set_alarm_callback, **kwargs):
        super(AlarmPopup, self).__init__(**kwargs)
        self.set_alarm_callback = set_alarm_callback
        self.title = 'Set Alarm'
        self.content = self._build_content()

    def _build_content(self):
        layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10),
            size_hint=(None, None),
            size=(dp(350), dp(400)),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )

        inner_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(350),
            pos_hint={'center_x': 1.0, 'center_y': 1.0}
        )

        alarm_label = Label(
            text='Time for alarm:',
            size_hint=(None, None),
            height=dp(45),
            font_size=dp(24),
            pos_hint={'center_x': 1.0, 'center_y': 1.0}
        )
        inner_layout.add_widget(alarm_label)

        self.hour_input = TextInput(
            hint_text='Hour',
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            pos_hint={'center_x': 1.0, 'center_y': 1.0}
        )
        self.minute_input = TextInput(
            hint_text='Minute',
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            pos_hint={'center_x': 1.0, 'center_y': 1.0}
        )

        inner_layout.add_widget(self.hour_input)
        inner_layout.add_widget(self.minute_input)

        set_alarm_button = Button(
            text='Set Alarm',
            on_press=self.set_alarm,
            size_hint_y=None,
            height=dp(45),
            font_size=dp(18),
            pos_hint={'center_x': 1.0, 'center_y': 1.0}
        )
        inner_layout.add_widget(set_alarm_button)

        layout.add_widget(inner_layout)

        return layout

    def set_alarm(self, instance):
        try:
            hour = int(self.hour_input.text)
            minute = int(self.minute_input.text)

            if 0 <= hour <= 23 and 0 <= minute <= 59:
                self.set_alarm_callback(hour, minute)
                self.dismiss()
            else:
                Popup(title='Invalid Input', content=Label(text='Please enter valid hour (0-23) and minute (0-59).'),
                      size_hint=(None, None), size=(dp(400), dp(200))).open()
        except ValueError:
            Popup(title='Invalid Input', content=Label(text='Please enter valid numerical values for hour and minute.'),
                  size_hint=(None, None), size=(dp(400), dp(200))).open()

class ClockApp(App):
    sw_started = False
    sw_seconds = 0
    lap_times = ListProperty([])
    dark_mode = True

    def __init__(self, **kwargs):
        super(ClockApp, self).__init__(**kwargs)
        self.audio_folder = 'audio'
        self.image_folder = 'images'
        self.click_sound = SoundLoader.load(os.path.join(self.audio_folder, 'click.wav'))
        self.alarm_sound = None
        self.alarm_hour = 0
        self.alarm_minute = 0
        self.alarm_triggered = False

    def play_click_sound(self):
        if self.click_sound:
            self.click_sound.play()

    def play_alarm_sound(self):
        if self.alarm_sound:
            self.alarm_sound.play()

    def play_timer_expired_sound(self):
        timer_expired_sound = SoundLoader.load(os.path.join(self.audio_folder, 'timer_expired.wav'))
        if timer_expired_sound:
            timer_expired_sound.play()

    def update_time(self, nap):
        try:
            if self.sw_started:
                self.sw_seconds += nap
            self.check_alarm_trigger()

            minutes, seconds = divmod(self.sw_seconds, 60)
            milliseconds = int(seconds * 100 % 100)

            if self.root:
                self.root.ids.stopwatch.text = (
                    '[size=40]%02d[/size]:[size=40]%02d[/size].[size=20]%02d[/size]' %
                    (int(minutes), int(seconds), milliseconds)
                )
                self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')

        except Exception as e:
            print(f"Error updating time: {e}")

    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)

    def start_stop(self):
        if self.root:
            self.root.ids.start_stop.text = (
                'Start' if self.sw_started else 'Stop'
            )
        self.sw_started = not self.sw_started
        self.play_click_sound()

    def reset(self):
        if self.sw_started:
            if self.root:
                self.root.ids.start_stop.text = 'Start'
            self.sw_started = False
            self.lap_times = []
        self.sw_seconds = 0
        self.play_click_sound()

    def mark_lap(self):
        if self.sw_started:
            minutes, seconds = divmod(self.sw_seconds, 60)
            milliseconds = int(seconds * 100 % 100)
            lap_time = f'{int(minutes):02d}:{int(seconds):02d}.{milliseconds:02d}'
            self.lap_times.insert(0, lap_time)  # Insert lap time at the beginning of the list
            if self.root:
                self.root.ids.lap_times.text = '\n'.join(self.lap_times)
            self.play_click_sound()

    def set_alarm(self, hour, minute):
        try:
            print(f'Setting alarm for {hour:02d}:{minute:02d}')
            self.alarm_hour = hour
            self.alarm_minute = minute
            self.alarm_sound = SoundLoader.load(os.path.join(self.audio_folder, 'alarm.wav'))
            print(f"Alarm set: {self.alarm_hour:02d}:{self.alarm_minute:02d}")
        except Exception as e:
            print(f"Error setting alarm: {e}")

    def check_alarm_trigger(self):
        if not self.alarm_triggered:
            # Get the current time
            current_time = time.localtime()
            current_hour = current_time.tm_hour
            current_minute = current_time.tm_min
            current_second = current_time.tm_sec

            if self.alarm_hour == current_hour and self.alarm_minute == current_minute and current_second == 0:
                print("Alarm triggered!")
                self.play_alarm_sound()
                self.alarm_triggered = True
                self.show_alarm_popup()

    def snooze_alarm(self):
        self.alarm_triggered = False
        self.reset()
        self.play_alarm_sound()

    def stop_alarm(self):
        self.alarm_triggered = False
        if self.alarm_sound:
            self.alarm_sound.stop()

    def show_alarm_settings_popup(self):
        alarm_popup = AlarmPopup(self.set_alarm)
        alarm_popup.open()

    def show_alarm_popup(self):
        alarm_popup = Popup(title='Alarm!', content=self._build_alarm_popup_content(),
                            size_hint=(None, None), size=(dp(400), dp(200)))
        alarm_popup.open()

    def _build_alarm_popup_content(self):
        layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10),
            size_hint=(None, None),
            size=(dp(300), dp(150))  # Adjust the size of the Popup
        )

        alarm_label = Label(
            text='Alarm Time Reached!',
            size_hint=(None, None),
            height=dp(45),
            font_size=dp(18)  # Adjust the font size of the Label
        )
        layout.add_widget(alarm_label)

        snooze_button = Button(
            text='Snooze',
            on_press=lambda instance: self.snooze_alarm(),
            size_hint_y=None,
            height=dp(40),
            font_size=dp(16),
            accessibility_hint='Snooze the alarm'
        )
        stop_button = Button(
            text='Stop',
            on_press=lambda instance: self.stop_alarm(),
            size_hint_y=None,
            height=dp(40),
            font_size=dp(16)  # Adjust the font size of the Button
        )

        button_layout = BoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(80)
        )
        button_layout.add_widget(snooze_button)
        button_layout.add_widget(stop_button)

        layout.add_widget(button_layout)

        return layout

    def build(self):
        self.apply_color_scheme(self.dark_mode)
        return Builder.load_file('clock.kv')
    
    def apply_color_scheme(self, dark_mode=False):
        colors = dark_mode_colors if dark_mode else light_mode_colors
        
        Window.clearcolor = get_color_from_hex(colors['background'])

        LabelBase.register(name='Roboto',
                        fn_regular='Roboto-Thin.ttf' if dark_mode else 'Roboto-Regular.ttf',
                        fn_bold='Roboto-Medium.ttf')

        # Set text color for specific labels
        text_labels = ['time', 'stopwatch', 'lap_times']
        for label_id in text_labels:
            label = self.root.ids[label_id] # type: ignore
            if label:
                label.color = get_color_from_hex(colors['text'])
        
        # Set text color for buttons
        button_ids = ['start_stop', 'reset', 'toggle_dark_mode']
        for button_id in button_ids:
            button = self.root.ids[button_id] # type: ignore
            if button:
                button.color = get_color_from_hex(colors['text'])

        if hasattr(self, 'alarm_popup') and self.alarm_popup:
            self.alarm_popup.content.apply_color_scheme(dark_mode)

    def toggle_dark_mode(self):
        try:
            self.dark_mode = not self.dark_mode
            self.apply_color_scheme(self.dark_mode)
        except Exception as e:
            print(f"Error toggling dark mode: {e}")

if __name__ == '__main__':
    ClockApp().run()