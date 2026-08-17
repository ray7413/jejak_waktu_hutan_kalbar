class Camera:
    def __init__(self, x=0, y=0, zoom=1.0):
        self.x = x
        self.y = y
        self.zoom = zoom

    def set_zoom(self, zoom):
        self.zoom = max(0.6, min(2.0, zoom))

    def world_to_screen(self, wx, wy):
        return (
            self.x + (wx - wy) * 40 * self.zoom,
            self.y + (wx + wy) * 20 * self.zoom,
        )
