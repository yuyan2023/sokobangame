import tkinter as tk
import tkinter.messagebox
from tkinter import messagebox, filedialog
from typing import Callable
from model import SokobanModel, Tile, Entity
from a2_support import *
from a3_support import *

# Write your classes and functions here
COIN = '$'
COIN_AMOUNT = 5


class FancyGameView(AbstractGrid):
    """
    FancyGameView is inherited from AbstractGrid. The FancyGameView is
    a grid displaying the game map.
    """

    def __init__(self, master: tk.Frame | tk.Tk, dimensions: tuple[int, int], size:
    tuple[int, int], **kwargs) -> None:
        """ 
        Sets up the FancyGameView to be an AbstractGrid
        with the appropriate dimensions and size, and creates an instance attribute 
        of an empty dictionary to be used as an image cache.
        """

        super().__init__(master, dimensions, size)
        self._images = dict()  # create a cache to store images

    def display(self, maze: Grid, entities: Entities, player_position: Position) -> None:
        """
        :param maze: a 2D list maze grid containing tiles
        :param entities: a dictionary where key is position and value is entity
        :param player_position: the tuple of player position
        :return: none
        get every element in maze and entities and get type respectively, then use get_image
        method to render them on the canvas
  """
        self.clear()  # Clears all child widgets off the canvas.

        '''use for loop to fetch all the tiles in maze'''
        for i, row in enumerate(maze):
            for j, tile_type in enumerate(row):
                tile = maze[i][j]  # get tile in maze
                tile_type = str(tile)  # check what type the tile is

                if tile_type == FLOOR:
                    image_floor = get_image("images/Floor.png", self.get_cell_size(), self._images)
                    x, y = self.get_midpoint((i, j))
                    self.create_image(x, y, image=image_floor)

                if tile_type == WALL:
                    image_wall = get_image("images/W.png", self.get_cell_size(), self._images)
                    x, y = self.get_midpoint((i, j))
                    self.create_image(x, y, image=image_wall)

                if tile_type == GOAL:
                    image_goal = get_image("images/G.png", self.get_cell_size(), self._images)
                    x, y = self.get_midpoint((i, j))
                    self.create_image(x, y, image=image_goal)

                if tile_type == FILLED_GOAL:
                    image_filled_goal = get_image("images/X.png", self.get_cell_size(), self._images)
                    x, y = self.get_midpoint((i, j))
                    self.create_image(x, y, image=image_filled_goal)

        '''use for loop to fetch all the entities and their positions in entities'''
        for entity_position, entity in entities.items():  # entities: {(1,1): Crater(5), (1,2): FancyPotion()}
            entity_type = entity.get_type()

            if entity_type == CRATE:
                crate_strength = entity.get_strength()
                image_crate = get_image("images/C.png", self.get_cell_size(), self._images)
                crate_x, crate_y = self.get_midpoint(entity_position)
                self.create_image(crate_x, crate_y, image=image_crate)
                self.create_text(crate_x, crate_y - 20, text=crate_strength, font=CRATE_FONT)

            if entity_type == COIN:
                image_coin = get_image("images/$.png", self.get_cell_size(), self._images)
                coin_x, coin_y = self.get_midpoint(entity_position)
                self.create_image(coin_x, coin_y, image=image_coin)

            if entity_type == STRENGTH_POTION:
                image_strength_potion = get_image("images/S.png", self.get_cell_size(), self._images)
                potion_x, potion_y = self.get_midpoint(entity_position)
                self.create_image(potion_x, potion_y, image=image_strength_potion)

            if entity_type == MOVE_POTION:
                image_move_potion = get_image("images/M.png", self.get_cell_size(), self._images)
                potion_x, potion_y = self.get_midpoint(entity_position)
                self.create_image(potion_x, potion_y, image=image_move_potion)

            if entity_type == FANCY_POTION:
                image_fancy_potion = get_image("images/F.png", self.get_cell_size(), self._images)
                potion_x, potion_y = self.get_midpoint(entity_position)
                self.create_image(potion_x, potion_y, image=image_fancy_potion)

        '''render player image based on its position on maze'''
        image_player = get_image("images/P.png", self.get_cell_size(), self._images)
        x, y = self.get_midpoint(player_position)
        self.create_image(x, y, image=image_player)


class FancyStatsView(AbstractGrid):
    """
    FancyStatsView inherited from AbstractGrid. It is a grid with 3 rows and 3 columns.
    The top row displays the text ‘Player Stats’ in a bold font in the second column.
    The second row displays titles for the stats, and the third row displays the values for
    those stats. Also, it spans the entire width of the game and shop combined.
    """

    def __init__(self, master: tk.Frame):
        """
        Sets up this FancyStatsView to be an AbstractGrid with
        the appropriate number of rows and columns, and the appropriate
        width and height
        """
        super().__init__(master, (3, 3), (MAZE_SIZE + SHOP_WIDTH, STATS_HEIGHT))

    def draw_stats(self, moves_remaining, strength: int, money: int) -> None:
        """
        Clears the FancyStatsView and redraws it to display the provided moves remaining, strength,
        and money
        :param moves_remaining: the moves that player remains
        :param strength: player current strength
        :param money: player's coin
        :return: none
        """
        self.clear()
        self.annotate_position((0, 1), "Player Stats", TITLE_FONT)
        self.annotate_position((1, 0), "Moves remaining:")
        self.annotate_position((1, 1), "Strength:")
        self.annotate_position((1, 2), "Money:")
        self.annotate_position((2, 0), moves_remaining, FONT)
        self.annotate_position((2, 1), strength, FONT)
        self.annotate_position((2, 2), f'{COIN}{money}', FONT)


class Shop(tk.Frame):
    """
    Shop inherited from tk.Frame. The Shop is a frame displaying relevant information and
    buttons for all the buyable items in the game.The Shop should contain a title at the top and a frame
    for each buyable item (each potion). Each item’s frame should contain the following widgets, packed left to right:

    """

    def __init__(self, master: tk.Frame):
        super().__init__(master)
        self.shop_label = tk.Label(self, text="Shop")
        self.shop_label.pack(side=tk.TOP)  # put the shop on top

    def create_buyable_item(self, item: str, amount: int, callback: Callable[[], None]):
        """
        Create a new item in this shop. It creates a new frame within
        the shop frame and then creates a label and button within that child frame. The button
        should be bound to the provided callback.

        :param item: the three different types of potion
        :param amount: the price of item
        :param callback: buy function
        :return: none
        """
        frame_item = tk.Frame(self)
        frame_item.pack()

        # pack the potion item with price
        tk.Label(frame_item, text=f"{item}: ${amount}").pack(side=tk.LEFT)

        # combine the buy button to callback function
        tk.Button(frame_item, text="Buy", command=callback).pack(side=tk.LEFT)


class FancySokobanView:
    """
    The FancySokobanView class provides a wrapper around the smaller GUI components which has been
    built, and provides methods through which the controller can update these components.
    """

    def __init__(self, master: tk.Tk, dimensions: tuple[int, int], size: tuple[int, int]) -> None:
        """
        initialize a new instance, creates the title
        banner, setting the title on the window, and instantiating and packing the three widgets

        :param master: The master frame for this Canvas
        :param dimensions: (#rows, #columns) of maze
        :param size: (maze width in pixels, maze height in pixels)
        :return: none
        """

        # Dictionary to store image references to prevent garbage collection.
        self._images = {}

        # Create and display the banner image.
        self.image_banner = get_image("images/banner.png", (MAZE_SIZE + SHOP_WIDTH, BANNER_HEIGHT), self._images)
        frame_banner = tk.Frame(master, height=BANNER_HEIGHT, width=MAZE_SIZE + SHOP_WIDTH)
        frame_banner.pack(side=tk.TOP)
        frame_banner.pack_propagate(False)
        tk.Label(frame_banner, image=self.image_banner).pack()

        # Create and display the frame that contains both the maze and the shop.
        frame_maze_shop = tk.Frame(master)
        frame_maze_shop.pack(side=tk.TOP)

        # Create and display the shop frame.
        frame_maze = tk.Frame(frame_maze_shop, height=MAZE_SIZE, width=MAZE_SIZE)
        frame_maze.pack(side=tk.LEFT)
        frame_maze.pack_propagate(False)
        self.maze_view = FancyGameView(frame_maze, dimensions, size)
        self.maze_view.pack()

        # Create and display the shop frame.
        frame_shop = tk.Frame(frame_maze_shop, height=MAZE_SIZE, width=SHOP_WIDTH)
        frame_shop.pack(side=tk.RIGHT)
        frame_shop.pack_propagate(False)
        self.maze_shop = Shop(frame_shop)
        self.maze_shop.pack()

        # Create and display the frame that contains player stats.
        frame_stats = tk.Frame(master, height=STATS_HEIGHT, width=MAZE_SIZE + SHOP_WIDTH)
        frame_stats.pack(side=tk.TOP)
        frame_stats.pack_propagate(False)
        self.maze_stats = FancyStatsView(frame_stats)
        self.maze_stats.pack()

    def display_game(self, maze: Grid, entities: Entities, player_position: Position):
        """
        Display the current game state, including the maze layout, entities, and player's position.

        Parameters:
        - maze (Grid): The current maze layout.
        - entities (Entities): All entities within the maze (e.g., monsters, items).
        - player_position (Position): The current position of the player in the maze.
        """
        # Clear the previous state from the maze view.
        self.maze_view.clear()

        # Render the new state of the maze.
        self.maze_view.display(maze, entities, player_position)

    def display_stats(self, moves, strength, money):
        """
        Display the player's stats, including moves made, strength, and money.

        Parameters:
        - moves (int): The number of moves the player has made.
        - strength (int): The player's current strength.
        - money (int): The player's current money amount.
        """
        # Clear the previous state from the stats view.
        self.maze_stats.clear()

        # Draw the new stats.
        self.maze_stats.draw_stats(moves, strength, money)

    def create_shop_items(self, shop_items: dict[str, int], button_callback:
    Callable[[str], None] | None = None):
        """
        Create buyable items in the shop based on the provided dictionary of items and their prices.

        Parameters:
        - shop_items (dict[str, int]): A dictionary where keys are item identifiers and values are their prices.
        - button_callback (Callable[[str], None]): A callback function to be invoked when an item's purchase button
         is pressed. The item's identifier is passed as an argument.
                                                        
        """
        # Iterate over each item and its price in the provided dictionary.
        for item, price in shop_items.items():
            # Assign a user-friendly name based on the item identifier.
            if item == STRENGTH_POTION:
                potion_name = "Strength Potion"
            if item == MOVE_POTION:
                potion_name = "Move Potion"
            if item == FANCY_POTION:
                potion_name = "Fancy Potion"

            # Create a buyable item in the shop with its name, price, and associated callback function.
            self.maze_shop.create_buyable_item(potion_name, price,
                                               lambda potion_name=item: button_callback(potion_name))


class ExtraFancySokoban:
    """
    ExtraFancySokoban represents a graphical implementation of the Sokoban game, including
    an enhanced view and shopping features.

    Attributes:
    - model (SokobanModel): Represents the logic and state of the Sokoban game.
    - view (FancySokobanView): Graphical interface to display the Sokoban game.
    - root (tk.Tk): The main window of the game.
    - _text (tk.Text): A text widget for possibly displaying messages or game info.
    """

    def __init__(self, root: tk.Tk, maze_file: str):
        """
        Initializes the ExtraFancySokoban with a given root window and a maze file.

        Parameters:
        - root (tk.Tk): The main window of the game.
        - maze_file (str): The path to the file containing the maze layout.
         """

        # Initialize the game model with the maze from the provided file.
        self.model = SokobanModel(maze_file)

        # Create a view for the Sokoban game with the required dimensions and size.
        self.view = FancySokobanView(root, self.model.get_dimensions(), (MAZE_SIZE, MAZE_SIZE))

        # Render the initial state of the game.
        self.redraw()

        # Bind keyboard events to the keypress handler.
        self.root = root
        self.root.bind("<Key>", self.handle_keypress)

        # Set focus on the root window to capture keypress events.
        self.root.focus_set()

        # Initialize the shop items in the view using the model's shop items.
        self.view.create_shop_items(
            self.model.get_shop_items(),
            lambda item_id: self.item_attempt(item_id)
        )

        # Create and pack a text widget, which could be used for displaying game messages or other information.
        self._text = tk.Text(self.root)
        self._text.pack(expand=1, fill=tk.BOTH)

        # create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)  # tell master what its menubar is

        # within the menu bar create the file menu
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)  # tell menubar what its menu is

        # within the file menu create the file processing options
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Load", command=self.load_file)
        filemenu.add_command(label="Save", command=self.save_file)
        self._filename = None

    def redraw(self):
        """
        Refresh and display the current game state.
        """
        # Display the current maze, entities, and player's position.
        self.view.display_game(
            self.model.get_maze(),
            self.model.get_entities(),
            self.model.get_player_position()
        )

        # Display the player's remaining moves, strength, and money.
        self.view.display_stats(
            self.model.get_player_moves_remaining(),
            self.model.get_player_strength(),
            self.model.get_player_money()
        )

    def handle_keypress(self, enter: tk.Event):
        """
        Handle keypress events to control player movement and other game mechanics.

        Parameters:
        - enter (tk.Event): The event triggered by a keypress.
        """
        key_input = enter.char

        # Check if the pressed key corresponds to movement keys.
        if key_input in ['w', 'a', 's', 'd']:
            # Attempt to move the player in the given direction.
            self.model.attempt_move(key_input)
            # Refresh the game display.
            self.redraw()
            # Check for game end conditions.
            if self.model.has_won():

                self.redraw()
                self.win_window()

            elif self.model.get_player_moves_remaining() == 0:
                self.redraw()
                self.lose_window()

    def win_window(self):
        """
        Display a winning message and prompt the player to play again or exit.
        """
        message_pop = messagebox.askyesno("", message="You won! Play again?")
        if message_pop:
            # Reset the game state for another round.
            self.model.reset()
        else:
            # Close the game window.
            self.root.destroy()

    def lose_window(self):
        """
        Display a losing message and prompt the player to play again or exit.
        """
        message_pop = messagebox.askyesno("", message="You lost! Play again?")
        if message_pop:
            self.model.reset()
        else:
            self.root.destroy()

    def item_attempt(self, item_id: str):
        """
        Handle the action when a player attempts to purchase an item from the shop.

        Parameters:
        - item_id (str): The identifier of the item being purchased.
        """
        # Make an attempt to purchase the item.
        self.model.attempt_purchase(item_id)

        # Refresh the game display.
        self.redraw()

    def new_file(self):
        """
        Clear the text widget for a new file and update the window title.
        """
        self._text.delete("1.0", tk.END)
        self._filename = None
        self.root.title("New File")

    def save_file(self):
        """
        Save the current content of the text widget to a file.
        """
        # Check if there's an existing filename, if not, prompt the user.
        if self._filename is None:
            filename = filedialog.asksaveasfilename()
            if filename:
                self._filename = filename

        # Save the content to the file.
        if self._filename:
            self.root.title(self._filename)
            fd = open(self._filename, 'w')
            fd.write(self._text.get("1.0", tk.END))
            fd.close()

    def load_file(self):
        """
        Load content from a file into the text widget.
        """
        filename = filedialog.askopenfilename()
        if filename:
            self._filename = filename
            self.root.title(self._filename)
            fd = open(filename, 'r')
            # This assumes the first line of the file has player stats and the rest is the maze.
            lines = filename.readlines()
            maze = [list(line.strip()) for line in lines[1:]]
            player_stats = [int(item) for item in lines[0].strip().split(' ')]

            # Populate the text widget with the file content.
            self._text.insert(tk.INSERT, fd.read())
            fd.close()


def play_game(root: tk.Tk, maze_file: str):
    """
      Launch and display the Extra Fancy Sokoban game in the provided root window using a specified maze file.

      Parameters:
      - root (tk.Tk): The main window in which the game will be displayed.
      - maze_file (str): The path to the file containing the maze layout for the game.
    """
    # set the size of window
    root.geometry('650x600')
    # Set the title of the window
    root.title("Extra Fancy Sokoban")
    ExtraFancySokoban(root, maze_file)
    root.mainloop()


def main() -> None:
    """ The main function. """
    root = tk.Tk()

    play_game(root, "maze_files/maze2.txt")


if __name__ == "__main__":
    main()
