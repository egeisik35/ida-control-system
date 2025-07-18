from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy_garden.mapview import MapView, MapMarker
import requests

class WaypointSelector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.mapview = MapView(zoom=17, lat=40.0, lon=29.0)
        self.add_widget(self.mapview)

        self.waypoints = []
        self.waypoint_list = Label(text="Waypoints:\n", size_hint_y=None, height=150)
        self.add_widget(self.waypoint_list)

        self.save_btn = Button(text="Save and Close", size_hint_y=None, height=50)
        self.save_btn.bind(on_release=self.save_and_close)
        self.add_widget(self.save_btn)

        self.mapview.bind(on_touch_down=self.on_map_touch)

    def on_map_touch(self, instance, touch):
        if self.mapview.collide_point(*touch.pos) and touch.button == 'left':
            lat, lon = self.mapview.get_latlon_at(*touch.pos)
            # Altitude lookup
            alt = self.get_altitude(lat, lon)
            marker = MapMarker(lat=lat, lon=lon)
            self.mapview.add_widget(marker)
            self.waypoints.append((lat, lon, alt))
            self.update_waypoint_list()
        return False

    def get_altitude(self, lat, lon):
        try:
            r = requests.get(f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}", timeout=3)
            if r.status_code == 200:
                data = r.json()
                return data['results'][0]['elevation']
        except Exception as e:
            print(f"[ERROR] Altitude fetch failed: {e}")
        return 10.0  # fallback

    def update_waypoint_list(self):
        txt = "Waypoints:\n"
        for idx, wp in enumerate(self.waypoints, 1):
            txt += f"{idx}: {wp[0]:.6f}, {wp[1]:.6f}, {wp[2]:.1f}m\n"
        self.waypoint_list.text = txt

    def save_and_close(self, *args):
        with open("waypoints.txt", "w") as f:
            for wp in self.waypoints:
                f.write(f"{wp[0]},{wp[1]},{wp[2]}\n")
        App.get_running_app().stop()

class WaypointApp(App):
    def build(self):
        return WaypointSelector()

if __name__ == "__main__":
    WaypointApp().run()
