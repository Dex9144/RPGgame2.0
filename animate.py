class Animate:
    def __init__(self, textures):
        """
        Initialize the Animate class.

        :param textures: A list of surfaces (frames) that will be used for animation.
        """
        self.textures = textures  # List of frames for the animation
        self.i = 0  # The current frame index
        self.timer = 0  # Timer to keep track of time between frames

    def update_animation(self, dt):
        """
        Update the animation frame based on the time delta (dt).

        :param dt: The time between frames, controlling the animation speed.
        """
        self.timer += dt  # Increment the timer by the delta time
        if self.timer >= 1:  # If enough time has passed, go to the next frame
            self.i += 1
            if self.i >= len(self.textures):  # If we've reached the last frame, loop back to the first
                self.i = 0
            self.timer = 0  # Reset the timer for the next frame
