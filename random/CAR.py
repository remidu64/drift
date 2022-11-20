import arcade
import math


SPRITE_SCALING = 0.3
TILE_SCALING = 1

SCREEN_HEIGHT = 720
SCREEN_WIDTH = round(SCREEN_HEIGHT * (16/9))
SCREEN_TITLE = "test drift"
CAMERA_SPEED = 0.15

FRICTION = 0
NON_DRIFT_FRICTION = 0.05
DRIFT_FRICTION = 0.1
ACCELERATIONF = 1.8
ACCELERATIONB = 0.3
TEMP_ACCELERATION = 0
TEMP_ACCELERATION_ADD = 0.06
ANGLE_SPEED_MAX = 5
ANGLE_SPEED_MIN = 1E-2
ANGLE_ACCELERATION = 1
MAX_SPEED = 999
MIN_SPEED = 1E-2


position = None

# color
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)



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
        super().__init__(width, height, title, fullscreen = True, vsync=True, resizable=True)

        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

        # Our Scene Object
        self.scene = None

        self.physics_engine = None

        # Set up the player info
        self.player_sprite = None
        self.player_anglerad = None
        self.player_gearing = None
        self.gear = None
        self.state = None
        self.portx = None
        self.porty = None
        self.angleport = None

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
        map_name = "assets/car map.tmj"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Terrain": {
                "use_spatial_hash": True,
            },
            "Water": {
                "use_spatial_hash": True
            },
            "Port":{
              "use_spatial_hash": True
            },
            "Ground": {
                "use_spatial_hash": True,
            },

        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player
        self.car = arcade.load_texture("assets/car.png")
        self.boat = arcade.load_texture("assets/boat.png")
        self.player_sprite = arcade.Sprite("assets/car.png", SPRITE_SCALING)
        self.player_sprite.angle = 0
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_anglerad = math.radians(self.player_sprite.angle)
        self.player_gearing = 3.5
        self.gear = 0
        self.state = 0
        self.portx = 0
        self.porty = 0
        self.angleport = 0
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

        # activate camera
        self.camera.use()

        # Draw our Screen
        self.scene.draw()

        # activate GUI
        self.GUI.use()

        #draw car gearing
        gear_text = ""
        if self.gear == 0:
            gear_text = f'Vitesse: N'
        elif self.gear == -1:
            gear_text = f'Vitesse: R'
        else:
            gear_text = f'Vitesse: {self.gear}'

        arcade.draw_text(gear_text,10, self.height - 20, GREEN, 18)
        """
        #debug
        #draw speed
        speedx_text = f"speed x = {self.player_sprite.change_x}"
        speedy_text = f"speed y = {self.player_sprite.change_y}"
        acceleration= f"acce = {ACCELERATIONF}"
        info = "Tout ce qui est écrit en blanc sert pour le debug"

        arcade.draw_text(info,SCREEN_WIDTH - 10,SCREEN_HEIGHT - 10,WHITE,18)
        arcade.draw_text(speedx_text,10,10,WHITE,18)
        arcade.draw_text(speedy_text,10,30,WHITE, 18)
        arcade.draw_text(acceleration,10,50,WHITE, 18)


        #draw coordonates
        x_text = f"x = {self.player_sprite.center_x}"
        y_text = f"y = {self.player_sprite.center_y}"

        arcade.draw_text(y_text,10,70,WHITE,18)
        arcade.draw_text(x_text,10,90,WHITE,18)

        #draw cam info
        position_text = f'pos = {position}'

        arcade.draw_text(position_text,10,110,WHITE,18)
"""







    def on_update(self, delta_time):
        """ Movement and game logic """
        self.scroll_to_player()
        self.physics_engine.update()


        global ACCELERATIONF
        global ACCELERATIONB
        global TEMP_ACCELERATION
        global TEMP_ACCELERATION_ADD
        global FRICTION
        self.player_anglerad = math.radians(self.player_sprite.angle)

        port_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Port"])
        if len(port_hit_list) > 1:
            if self.state == 0:
                self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene["Ground"])
                self.player_sprite.texture = self.boat
                self.angleport = self.player_sprite.angle
                self.portx = self.player_sprite.center_x
                self.porty = self.player_sprite.center_y
                self.player_sprite.change_y = 0
                self.player_sprite.change_x = 0
                self.player_sprite.center_x = 4850
                self.player_sprite.center_y = 1550
                self.state = 1
            elif self.state == 1:
                self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, walls=self.scene["Terrain"])
                self.player_sprite.angle = self.angleport
                self.player_sprite.center_x = self.portx
                self.player_sprite.center_y = self.porty
                self.player_sprite.change_y = 0
                self.player_sprite.change_x = 0
                self.player_sprite.texture = self.car
                self.player_sprite.forward(-5)
                self.state = 0
            port_hit_list = []






        # Apply acceleration based on the keys pressed


        if self.state == 0:

            ACCELERATIONB = 0.3

            if self.shift_pressed:
                FRICTION = DRIFT_FRICTION
            else:
                FRICTION = NON_DRIFT_FRICTION

            if self.up_pressed and not self.down_pressed:
                if self.gear == -1:
                    self.player_sprite.forward(-ACCELERATIONB / (FRICTION + 1))

                    if TEMP_ACCELERATION - 0.1 <= 0:
                        TEMP_ACCELERATION = 0
                    else:
                        TEMP_ACCELERATION -= 0.1
                else:

                    if TEMP_ACCELERATION + TEMP_ACCELERATION_ADD >= ACCELERATIONF:
                        TEMP_ACCELERATION = ACCELERATIONF
                    else:
                        TEMP_ACCELERATION += TEMP_ACCELERATION_ADD


                if self.player_sprite.change_x + (TEMP_ACCELERATION / self.player_gearing) / (FRICTION + 1) * -math.sin(self.player_anglerad) > MAX_SPEED:
                    self.player_sprite.forward(MAX_SPEED)
                elif self.player_sprite.change_x + (TEMP_ACCELERATION / self.player_gearing) / (FRICTION + 1) * -math.sin(self.player_anglerad) < -MAX_SPEED:
                    self.player_sprite.forward(MAX_SPEED)
                else:
                    self.player_sprite.forward((TEMP_ACCELERATION / self.player_gearing) / (FRICTION + 1))

            elif self.down_pressed and not self.up_pressed:
                self.player_sprite.change_x /= 1.05
                self.player_sprite.change_y /= 1.05

            elif not self.down_pressed and not self.up_pressed:
                if TEMP_ACCELERATION - 0.1 <= 0:
                    TEMP_ACCELERATION = 0
                else:
                    TEMP_ACCELERATION -= 0.1


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
                ACCELERATIONF = 1.5
            else:
                FRICTION = NON_DRIFT_FRICTION
                ACCELERATIONF = 1.2


            if MIN_SPEED > self.player_sprite.change_x > 0:
                self.player_sprite.change_x = 0
            if MIN_SPEED > self.player_sprite.change_y > 0:
                self.player_sprite.change_y = 0
            if -MIN_SPEED < self.player_sprite.change_x < 0:
                self.player_sprite.change_x = 0
            if -MIN_SPEED < self.player_sprite.change_y < 0:
                self.player_sprite.change_y = 0

            if self.gear == 1:
                self.player_gearing = 3.5
                TEMP_ACCELERATION_ADD = 0.05
            elif self.gear == 2:
                self.player_gearing = 2.2
                TEMP_ACCELERATION_ADD = 0.02
            elif self.gear == 3:
                self.player_gearing = 1.8
                TEMP_ACCELERATION_ADD = 0.008
            elif self.gear == 4:
                self.player_gearing = 1.4
                TEMP_ACCELERATION_ADD = 0.004
            elif self.gear == 5:
                self.player_gearing = 1.2
                TEMP_ACCELERATION_ADD = 0.002
            elif self.gear == 6:
                self.player_gearing = 1
                TEMP_ACCELERATION_ADD = 0.001
            elif self.gear == 0:
                TEMP_ACCELERATION = 0
                TEMP_ACCELERATION_ADD = 0
                self.player_gearing = 3.5
            elif self.gear == -1:
                TEMP_ACCELERATION_ADD = 0
                self.player_gearing = 3.5

            water_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Water"])
            for water in water_hit_list:
                self.player_sprite.angle = 0
                self.player_sprite.center_x = 100
                self.player_sprite.center_y = 100
                self.player_anglerad = math.radians(self.player_sprite.angle)
                self.player_gearing = 3.5
                self.gear = 0
                self.state = 0
                self.player_sprite.texture = self.car



        elif self.state == 1:
            if self.up_pressed and not self.down_pressed:
                if self.gear == -1:
                    self.player_sprite.forward(-ACCELERATIONB / (FRICTION + 1))

                    if TEMP_ACCELERATION - 0.1 <= 0:
                        TEMP_ACCELERATION = 0
                    else:
                        TEMP_ACCELERATION -= 0.1
                else:

                    if TEMP_ACCELERATION + TEMP_ACCELERATION_ADD >= ACCELERATIONF:
                        TEMP_ACCELERATION = ACCELERATIONF
                    else:
                        TEMP_ACCELERATION += TEMP_ACCELERATION_ADD

                if self.player_sprite.change_x + (TEMP_ACCELERATION / self.player_gearing) / (
                        FRICTION + 1) * -math.sin(self.player_anglerad) > MAX_SPEED:
                    self.player_sprite.forward(MAX_SPEED)
                elif self.player_sprite.change_x + (TEMP_ACCELERATION / self.player_gearing) / (
                        FRICTION + 1) * -math.sin(self.player_anglerad) < -MAX_SPEED:
                    self.player_sprite.forward(MAX_SPEED)
                else:
                    self.player_sprite.forward((TEMP_ACCELERATION / self.player_gearing) / (FRICTION + 1))

            elif self.down_pressed and not self.up_pressed:
                self.player_sprite.change_x /= 1.05
                self.player_sprite.change_y /= 1.05

            elif not self.down_pressed and not self.up_pressed:
                if TEMP_ACCELERATION - 0.1 <= 0:
                    TEMP_ACCELERATION = 0
                else:
                    TEMP_ACCELERATION -= 0.1

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
                ACCELERATIONF = 1
            else:
                FRICTION = NON_DRIFT_FRICTION
                ACCELERATIONF = 1

            if MIN_SPEED > self.player_sprite.change_x > 0:
                self.player_sprite.change_x = 0
            if MIN_SPEED > self.player_sprite.change_y > 0:
                self.player_sprite.change_y = 0
            if -MIN_SPEED < self.player_sprite.change_x < 0:
                self.player_sprite.change_x = 0
            if -MIN_SPEED < self.player_sprite.change_y < 0:
                self.player_sprite.change_y = 0








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
        global TEMP_ACCELERATION_ADD
        global TEMP_ACCELERATION
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

        if key == arcade.key.UP:
            if self.gear + 1 >= 6:
                self.gear = 6
            else:
                self.gear += 1
                if TEMP_ACCELERATION - 0.5 < 0:
                    TEMP_ACCELERATION = 0
                else:
                    TEMP_ACCELERATION -= 0.5
        if key == arcade.key.DOWN:
            if self.gear - 1 <= -2:
                self.gear = 0
            else:
                self.gear -= 1

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