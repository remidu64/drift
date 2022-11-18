import arcade
import math


SPRITE_SCALING = 0.2
TILE_SCALING = 1

SCREEN_HEIGHT = 720
SCREEN_WIDTH = round(SCREEN_HEIGHT * (16/9))
SCREEN_TITLE = "test drift"
CAMERA_SPEED = 0.15

FRICTION = 0
NON_DRIFT_FRICTION = 0.06
DRIFT_FRICTION = 0.1
ACCELERATIONF = 1.2
ACCELERATIONB = 0.3
ANGLE_SPEED_MAX = 5
ANGLE_SPEED_MIN = 1E-2
ANGLE_ACCELERATION = 1
MAX_SPEED = 999
MIN_SPEED = 1E-2


position = None

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
        super().__init__(width, height, title, fullscreen = True)

        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

        # Our Scene Object
        self.scene = None

        self.physics_engine = None

        # Set up the player info
        self.player_sprite = None
        self.player_speed = None
        self.player_anglerad = None
        self.player_tempx = None
        self.player_tempy = None
        self.player_gearing = None
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
        self.shift_pressed = False

        # camera
        self.camera = None

        # Our TileMap Object
        self.tile_map = None



    def setup(self):
        """ Set up the game and initialize the variables. """


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
        self.player_speed = 0
        self.player_anglerad = 0
        self.player_gearing = 3.5
        self.scene.add_sprite("Player", self.player_sprite)

        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, walls=self.scene["Terrain"])

    def on_draw(self):
        global position
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Get viewport dimensions
        left, screen_width, bottom, screen_height = self.get_viewport()

        # Draw our Screen
        self.scene.draw()

        # activate camera
        self.camera.use()


        # activate GUI
        #self.GUI.use()

        # debug only

        #draw speed
        """
        speedx_text = f"speed x = {self.player_sprite.change_x}"
        speedy_text = f"speed y = {self.player_sprite.change_y}"
        speed_text = f"speed = {self.player_speed}"
        oldspeedx_text = f"old speed x = {self.player_vecspeedold_x}"
        oldspeedy_text = f"old speed y = {self.player_vecspeedold_y}"

        arcade.draw_text(speedx_text,10,10,WHITE,18)
        arcade.draw_text(speedy_text,10,30,WHITE, 18)
        arcade.draw_text(speed_text,10,50,WHITE,18)
        arcade.draw_text(speed_text, 10, 50, WHITE, 18)
        arcade.draw_text(oldspeedx_text, 10, 70, WHITE, 18)
        arcade.draw_text(oldspeedy_text, 10, 90, WHITE, 18)


        #draw coordonates
        x_text = f"x = {self.player_sprite.center_x}"
        y_text = f"y = {self.player_sprite.center_y}"

        arcade.draw_text(y_text,10,110,WHITE,18)
        arcade.draw_text(x_text,10,130,WHITE,18)

        #draw cam info
        position_text = f'pos = {position}'

        arcade.draw_text(position_text,10,150,WHITE,18)
        """



    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_anglerad = math.radians(self.player_sprite.angle)

        if self.shift_pressed:
            FRICTION = DRIFT_FRICTION
        else:
            FRICTION = NON_DRIFT_FRICTION


        # Apply acceleration based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            if self.player_sprite.change_x + (ACCELERATIONF / self.player_gearing) / (FRICTION + 1) * -math.sin(self.player_anglerad) > MAX_SPEED:
                self.player_sprite.change_x = MAX_SPEED
            elif self.player_sprite.change_x + (ACCELERATIONF / self.player_gearing) / (FRICTION + 1) * -math.sin(self.player_anglerad) < -MAX_SPEED:
                self.player_sprite.change_x = -MAX_SPEED
            else:
                self.player_sprite.change_x += (ACCELERATIONF / self.player_gearing) / (FRICTION + 1) * -math.sin(self.player_anglerad)

            if self.player_sprite.change_y + (ACCELERATIONF / self.player_gearing) / (FRICTION + 1) * math.cos(self.player_anglerad) > MAX_SPEED:
                self.player_sprite.change_y = MAX_SPEED
            elif self.player_sprite.change_y + (ACCELERATIONF / self.player_gearing) / (FRICTION + 1) * math.cos(self.player_anglerad) < -MAX_SPEED:
                self.player_sprite.change_y = -MAX_SPEED
            else:
                self.player_sprite.change_y += (ACCELERATIONF / self.player_gearing) / (FRICTION + 1) * math.cos(self.player_anglerad)
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_x -= ACCELERATIONB / (FRICTION + 1) * -math.sin(self.player_anglerad)
            self.player_sprite.change_y -= ACCELERATIONB/ (FRICTION + 1) * math.cos(self.player_anglerad)
        self.player_sprite.change_x /= FRICTION + 1
        self.player_sprite.change_y /= FRICTION + 1


        if self.left_pressed:
            self.player_sprite.change_angle += ANGLE_ACCELERATION
        elif self.right_pressed:
            self.player_sprite.change_angle -= ANGLE_ACCELERATION

        if self.player_sprite.change_angle > ANGLE_SPEED_MAX:
            self.player_sprite.change_angle = ANGLE_SPEED_MAX
        elif self.player_sprite.change_angle < -ANGLE_SPEED_MAX:
            self.player_sprite.change_angle = -ANGLE_SPEED_MAX

        if not self.left_pressed and not self.right_pressed:
            self.player_sprite.change_angle /= 5

        if ANGLE_SPEED_MIN > self.player_sprite.change_angle > 0:
            self.player_sprite.change_angle = 0
        elif -ANGLE_SPEED_MIN < self.player_sprite.change_angle < 0:
            self.player_sprite.change_angle = 0

        if self.shift_pressed:
            FRICTION = DRIFT_FRICTION
        else:
            FRICTION = NON_DRIFT_FRICTION


        if MIN_SPEED > self.player_sprite.change_x > 0:
            self.player_sprite.change_x = 0
        if MIN_SPEED > self.player_sprite.change_y > 0:
            self.player_sprite.change_y = 0
        if -MIN_SPEED < self.player_sprite.change_x < 0:
            self.player_sprite.change_x = 0
        if -MIN_SPEED < self.player_sprite.change_y < 0:
            self.player_sprite.change_y = 0


        self.scroll_to_player()
        self.physics_engine.update()

    def scroll_to_player(self):
        global position
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = self.player_sprite.center_x - (self.width / 2), self.player_sprite.center_y - (self.height / 2)
        self.camera.move_to(position, CAMERA_SPEED)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.Z:
            self.up_pressed = True
        if key == arcade.key.S:
            self.down_pressed = True
        if key == arcade.key.Q:
            self.left_pressed = True
        if key == arcade.key.D:
            self.right_pressed = True
        if key == arcade.key.LSHIFT:
            self.shift_pressed = True

        if key == arcade.key.NUM_1:
            self.player_gearing = 3.5
        elif key == arcade.key.NUM_2:
            self.player_gearing = 2.2
        elif key == arcade.key.NUM_3:
            self.player_gearing = 1.8
        elif key == arcade.key.NUM_4:
            self.player_gearing = 1.4
        elif key == arcade.key.NUM_5:
            self.player_gearing = 1.2
        elif key == arcade.key.NUM_6:
            self.player_gearing = 1


        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

        #quit game
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.Z:
            self.up_pressed = False
        if key == arcade.key.S:
            self.down_pressed = False
        if key == arcade.key.Q:
            self.left_pressed = False
        if key == arcade.key.D:
            self.right_pressed = False
        if key == arcade.key.LSHIFT:
            self.shift_pressed = False



def main():
    """ Main function """
    window = Drift(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


main()