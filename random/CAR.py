import arcade
import math

SPRITE_SCALING = 0.3
TILE_SCALING = 1

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "test drift"

FRICTION = 0.08
ACCELERATIONF = 1
ACCELERATIONB = 0.5
ANGLE_SPEED = 3.5
MAX_SPEED = 15
MIN_SPEED = 1E-2
STARTPOSX = 100
STARTPOSY = 100

anglerad = 0

# color
WHITE = (255, 255, 255)



class Drift(arcade.Window):
    global anglerad
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Our Scene Object
        self.scene = None

        self.physics_engine = None

        # Set up the player info
        self.player_sprite = None
        self.player_list = None


        # background
        self.background = None

        # GUI
        self.GUI = None

        # camera
        self.camera = None

        # MOOV
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # camera
        self.camera = None

        # Our TileMap Object
        self.tile_map = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.player_list = arcade.SpriteList()

        # setup GUI
        self.GUI = arcade.Camera(self.width, self.height)

        # setup camera
        self.camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = "resource/car map.tmj"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Terrain": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player
        self.player_sprite = arcade.Sprite("resource/car.png", SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, walls=None)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # activate camera
        self.camera.use()

        # activate GUI
        self.GUI.use()

        # Draw our Screen
        self.scene.draw()
        self.player_list.draw()


        # debug only
        """
        #draw speed
        speedx_text = f"speed x = {self.player_sprite.speedx}"
        speedy_text = f"speed y = {self.player_sprite.speedy}"

        arcade.draw_text(speedx_text,10,10,WHITE,18)
        arcade.draw_text(speedy_text,10,30,WHITE, 18)

        #draw coordonates
        x_text = f"x = {self.player_sprite.center_x}"
        y_text = f"y = {self.player_sprite.center_y}"

        arcade.draw_text(y_text,10,50,WHITE,18)
        arcade.draw_text(x_text,10,70,WHITE,18)
        """



    def on_update(self, delta_time):
        """ Movement and game logic """

        anglerad = math.radians(self.player_sprite.angle)

        # Apply acceleration based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_x -= ACCELERATIONF * math.sin(anglerad)
            self.player_sprite.change_y += ACCELERATIONF * math.cos(anglerad)
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_x -= ACCELERATIONB * math.sin(anglerad)
            self.player_sprite.change_y += ACCELERATIONB * math.cos(anglerad)

        self.player_sprite.change_x /= FRICTION + 1
        self.player_sprite.change_y /= FRICTION + 1

        if self.player_sprite.change_x > MAX_SPEED:
            self.player_sprite.change_x = MAX_SPEED
        if self.player_sprite.change_y > MAX_SPEED:
            self.player_sprite.change_y = MAX_SPEED
        if self.player_sprite.change_x < -MAX_SPEED:
            self.player_sprite.change_x = -MAX_SPEED
        if self.player_sprite.change_y < -MAX_SPEED:
            self.player_sprite.change_y = -MAX_SPEED

        if MIN_SPEED > self.player_sprite.change_x > 0:
            self.player_sprite.change_x = 0
        elif -MIN_SPEED < self.player_sprite.change_x < 0:
            self.player_sprite.change_x = 0

        if MIN_SPEED > self.player_sprite.change_y > 0:
            self.player_sprite.change_y = 0
        elif -MIN_SPEED < self.player_sprite.change_y < 0:
            self.player_sprite.change_y = 0

        if self.left_pressed:
            self.player_sprite.change_angle = ANGLE_SPEED
        if self.right_pressed:
            self.player_sprite.change_angle = -ANGLE_SPEED

        if not self.left_pressed and not self.right_pressed:
            self.player_sprite.change_angle = 0

        self.physics_engine.update()
        self.center_camera_to_player()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x
        screen_center_y = self.player_sprite.center_y

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.Z:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.Q:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.Z:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.Q:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False


def main():
    """ Main function """
    window = Drift(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


main()