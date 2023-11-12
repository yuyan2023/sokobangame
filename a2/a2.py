from a2_support import *


# Write your classes here
class Tile(object):
    """An abstract class from which all instantiable types of tiles inherit."""

    def is_blocking(self) -> bool:
        """Returns True only when this tile is blocking.
        A tile is blocking if an entity would not be able to move onto that tile.
        """
        return False

    def get_type(self) -> str:
        """return the tile type"""
        return 'Abstract Tile'

    def __str__(self):
        """return get_type result"""
        result = self.get_type()
        return result

    def __repr__(self):
        """return __str__ result"""
        tile_str = self.__str__()
        return tile_str


class Floor(Tile):
    """Inherited from Tile

    Floor is a basic type of tile that represents an empty
    space on which entities can freely move. It is non-blocking
    and is represented by a single space character.
    """

    def is_blocking(self) -> bool:
        """Returns False only when the floor is not blocking"""
        return False

    def get_type(self) -> str:
        """return FLOOR 'F' """
        return FLOOR


class Wall(Tile):
    """Inherited from Tile

    Wall is a type of tile that represents a wall through
    which entities cannot pass. Wall tiles are blocking,
    and are represented by the character ‘W’.
    """

    def is_blocking(self) -> bool:
        """Returns True because wall blocks everything by default"""
        return True

    def get_type(self) -> str:
        """return WALL 'W' """
        return WALL


class Goal(Tile):
    """Inherits from Tile

    Goal is a type of tile that represents a goal location for a crate.
    Goal tiles are non-blocking, and the type is represented by ‘G’.
    Goal tiles can either be filled or unfilled.

    Goal tiles start unfilled, nd become filled throughout gameplay
    as the player pushes crates onto them. If a goal tile is unfilled,
    the __str__ and __repr__ methods return ‘G’. However, when a goal tile
    becomes filled, the __str__ and __repr__ methods should instead return ‘X’
    to denote that this goal tile is filled.
    """

    def __init__(self) -> None:
        """use a value self._place to show goal not realized"""
        self._place = False

    def get_type(self) -> str:
        """return GOAL """
        return GOAL

    def unfill(self) -> None:
        """unfilled the goal"""
        self._place = False

    def is_filled(self) -> bool:
        """return self._place which is a bool type when the goal is filled"""
        return self._place

    def fill(self) -> None:
        """modify self._place to true showing filled"""
        self._place = True

    def __str__(self):
        """use is_filled method
        if is filled return filled_goal, else return goal
        """
        if self.is_filled():
            return FILLED_GOAL
        else:
            return GOAL


class Entity:
    """Entities exist on top of the grid,including the player, all crates, and all potions.
       Entities may or may not be movable.Abstract base class from which all entities inherit.
    """

    def __init__(self):
        """ the __init__ method doesn't take any arguments."""
        pass

    def get_type(self) -> str:
        """Returns a string representing the type of this entity.
        For the abstract Entity class, this method returns the string ‘Abstract Entity’.
        For instantiable subclasses, this method should return the single letter constant
        corresponding to that class.
        """
        return 'Abstract Entity'

    def is_movable(self) -> bool:
        """Returns True if this entity is movable. By default, entities are not movable"""
        return False

    def __str__(self):
        """return get_type result"""
        return self.get_type()

    def __repr__(self):
        """return __str__ result"""
        return self.__str__()


class Crate(Entity):
    """Inherits from Entity

    Crate is a movable entity, represented by the letter ‘C’. Crates are constructed with a strength
    value, which represents the strength a player is required to have in order to move that crate.
    The string representation of a crate should be the string version of its strength value.
    """

    def __init__(self, strength: int):
        """create self._strength show how much strength the crate is required """
        super().__init__()
        self._strength = strength

    def get_type(self) -> str:
        """return crate type"""
        return CRATE

    def __str__(self):
        """convert the crate strength to string and return"""
        return str(self._strength)

    def __repr__(self):
        """return the result of __str__()"""
        return self.__str__()

    def is_movable(self) -> bool:
        """Crate returns True meaning movable by default"""
        return True

    def get_strength(self) -> int:
        """return the requirement of crate strength"""
        return self._strength


class Potion(Entity):
    """Inherits from Entity

    This is an abstract class which provides a simple interface which all instances of potions
    must implement. The __init__ method for all potions do not take any arguments besides self.
    Since this class inherits from Entity, it should also provide all methods available from
    the Entity class. Potions are not movable. An abstract potion is represented by ‘Potion’
    and has no effect.
    """

    def effect(self) -> dict[str, int]:
        """The method returns an empty dictionary, since it has no effect"""
        return {}

    def get_type(self) -> str:
        """returns potion"""
        return 'Potion'


class StrengthPotion(Potion):
    """Inherits from Potion

    A StrengthPotion is represented by the string ‘S’ and provides the player with an additional 2 strength.
    """

    def get_type(self) -> str:
        """return strength potion"""
        return STRENGTH_POTION

    def effect(self) -> dict[str, int]:
        """return {strength: 2}"""
        return {'strength': 2}


class MovePotion(Potion):
    """Inherits from Potion

    A MovePotion is represented by the string ‘M’ and provides the player with an additional 5 moves.
    """

    def get_type(self) -> str:
        """return move_potion"""
        return MOVE_POTION

    def effect(self) -> dict[str, int]:
        """return {move: 5}"""
        return {'moves': 5}


class FancyPotion(Potion):
    """Inherits from Potion

    A FancyPotion is represented by the string ‘F’ and provides the player with 3 strength and 3 moves.
    """

    def get_type(self) -> str:
        """return fancy_potion """
        return FANCY_POTION

    def effect(self) -> dict[str, int]:
        """return {strength: 2, move: 2}"""
        return {'strength': 2, 'moves': 2}


class Player(Entity):
    """Inherits from Entity

    Player is a movable entity, represented by the letter ‘P’. A player instance is
    constructed with a starting strength and an initial number of moves remaining.
    These two values can change throughout regular gameplay, or through the use of
    potions,via methods provided by the Player class. A player is only movable if
    they have a positive number of moves remaining.

    """

    def __init__(self, start_strength: int, moves_remaining: int) -> None:
        """Initializes a Player object with the given initial strength and moves remaining.
        Args:
        start_strength (int): The initial strength of the player.
        moves_remaining (int): The initial number of moves remaining for the player.

        Attributes:
        self._strength (int): The current strength of the player.
        self._moves (int): The current number of moves remaining for the player.
        """
        super().__init__()
        self._strength = start_strength
        self._moves = moves_remaining

    def is_movable(self) -> bool:
        """Checks if the player is movable based on their remaining moves.
        Returns True if the player has more than 0 moves remaining, False otherwise.
        """
        if self._moves > 0:
            return True
        else:
            return False

    def get_type(self) -> str:
        """return player 'P'"""
        return PLAYER

    def get_strength(self) -> int:
        """RETURN PLAYER strength"""
        return self._strength

    def add_strength(self, amount: int) -> None:
        """Adds the specified amount to the player's strength.
        Args:
        amount (int): The amount to be added to the player's strength.
        """
        self._strength = self._strength + amount

    def get_moves_remaining(self) -> int:
        """Returns the current number of moves remaining for the player."""
        return self._moves

    def add_moves_remaining(self, amount: int) -> None:
        """Adds the specified amount to the player's moves remaining and ensures it doesn't go below 0.
        Args:
        amount (int): The amount to be added to the player's moves remaining.
        """
        self._moves = self._moves + amount
        if self._moves < 0:  # the position is always positive
            self._moves = 0

    def apply_effect(self, potion_effect: dict[str, int]) -> None:
        """Applies the effects of a potion to the player's attributes (strength and moves).
        Args:
        potion_effect (dict[str, int]): A dictionary containing the potion effects.
        strength (int): The amount by which to increase the player's strength.
        moves (int): The amount by which to increase the player's moves remaining.
        """
        if 'strength' in potion_effect:
            self.add_strength(potion_effect['strength'])

        if 'moves' in potion_effect:
            self.add_moves_remaining(potion_effect['moves'])


def convert_maze(game: list[list[str]]) -> tuple[Grid, Entity, Position]:
    """Converts a game represented as a 2D list of strings into a maze, entity dictionary, and player position.
        Args:
        game (list[list[str]]): A list of lists representing the game grid.

        Returns:
        tuple[Grid, Entity, Position]: A tuple containing:
        Grid: The game grid represented as a list of lists of tiles.
        Entity: A dictionary representing the entities with their positions.
        Position: A tuple representing the initial position of the player on the grid.

        The function iterates through the 'game' list and converts each element into corresponding
        tile objects like Wall, Floor and entities like Crates, Potions because all the entities
        standing on a tile. It builds the 'entities' list, populates the 'rows' with entities
        and their positions, and determines the player position.

        Note: The Grid and Entity types used in the return annotation are assumed to be previously defined.
              The Entities are on floors which should be recorded on the list.
        """
    entities = {}  # Dictionary to store entities and positions.
    maze_rows = []  # a list stores game rows.
    i = 0  # Row index.

    for row in game:  # find every row in the game grid using for loop
        maze_tiles = []  # a list storing tiles on the grid
        j = 0  # Column index

        # find every cell in the row using for loop
        for cell in row:

            # if the cell is a wall, create a new wall 'W', insert 'W' to maze_tiles list
            if cell == WALL:
                tile_wall = Wall()
                maze_tiles.append(tile_wall)

            # if the cell is a floor, create a new floor 'F', insert 'F' to maze_tiles list
            if cell == FLOOR:
                tile_floor = Floor()
                maze_tiles.append(tile_floor)

            # if the entity is a potion, create a new potion and insert it to entities with its position
            if cell == STRENGTH_POTION:
                entity_potion = StrengthPotion()
                entity_position = (i, j)  # get potion position
                entities[entity_position] = entity_potion
                tile_floor = Floor()  # below the potion is a floor, append floor to the maze list
                maze_tiles.append(tile_floor)

            if cell == FANCY_POTION:
                entity_potion = FancyPotion()
                entity_position = (i, j)
                entities[entity_position] = entity_potion
                tile_floor = Floor()
                maze_tiles.append(tile_floor)

            if cell == MOVE_POTION:
                entity_potion = MovePotion()
                entity_position = (i, j)
                entities[entity_position] = entity_potion
                tile_floor = Floor()
                maze_tiles.append(tile_floor)

            # if the cell is a goal, create a new goal and append it to maze tile list
            if cell == GOAL:
                tile_goal = Goal()
                maze_tiles.append(tile_goal)

            if cell == FILLED_GOAL:
                tile_goal = Goal()
                tile_goal.fill()  # fill the goal, turn 'G' to 'X'
                maze_tiles.append(tile_goal)

            # if the entity is a crate, create a new crate and append it to entities with its position
            if cell.isdigit():  # check if it can be turned to int
                entity_crate = Crate(int(cell))
                entity_crate.is_movable()  # make crate movable because by default the crate is unmovable
                crate_position = (i, j)
                entities[crate_position] = entity_crate
                tile_floor = Floor()
                maze_tiles.append(tile_floor)

            # if the cell is a player, record its position
            if cell == PLAYER:
                player_position = (i, j)
                tile_floor = Floor()
                maze_tiles.append(tile_floor)

            j += 1
        i += 1
        maze_rows.append(maze_tiles)
    return maze_rows, entities, player_position


class SokobanModel:
    """Represents the game model for Sokoban, including the maze, entities, and player state.

           Args:
           maze_file (str): The path to the maze file to initialize the game model.

           Attributes:
           self._maze (Grid): The game grid represented as a list of lists of tiles.
           self._entities (Entities): A dictionary representing entities (e.g., Crates, Potions) with their positions.
           self._player_place (Position): A tuple representing the initial position of the player on the grid.
           self._strength (int): The initial strength of the player.
           self._moves (int): The initial number of moves remaining for the player.
           self._player (Player): The player instance representing the player character in the game.

           self._maze_undo (Grid): The previous game grid before any change.
           self._entities_undo (Entities): A dictionary saves entities with their positions before any change.
           self._player_place_undo (Position): The previous position of the player on the grid before any move.
           self._strength_undo (int): The previous strength of the player before applying potion.
           self._moves_undo (int): The previous number of moves remaining for the player before any change.
           self._player_undo (Player): The previous player before any change.
           self.undo_stack (list): The storage saves undo attributes

           The game model is responsible for managing the state of the Sokoban game, including the grid, entities,
           player attributes, and game logic.
           """

    def __init__(self, maze_file: str) -> None:
        """Initializes the SokobanModel by reading a maze file and setting up the initial game state.

        Args:
        maze_file (str): The path to the maze file to initialize the game model.
        return: None.
        """
        # maze_raw is a 2D list game grid, player_stats is a list storing moves and strength
        maze_raw, player_stats = read_file(maze_file)
        maze, entities, player_place = convert_maze(maze_raw)
        self._maze = maze
        self._entities = entities
        self._player_position = player_place
        self._strength = player_stats[0]
        self._moves = player_stats[1]
        self._player = Player(player_stats[0], player_stats[1])

        self.undo_stack = []  # a list storing previous elements
        self.maze_undo = maze
        self.entities_undo = entities
        self.player_position_undo = player_place
        self.strength_undo = player_stats[0]
        self.moves_undo = player_stats[1]
        self.player_undo = Player(player_stats[0], player_stats[1])

    def get_entities(self) -> Entities:
        """Returns the dictionary of entities and their positions."""
        return self._entities

    def get_maze(self) -> Grid:
        """Returns the game grid which is a 2D list."""
        return self._maze

    def get_player_position(self) -> tuple[int, int]:
        """ Returns A tuple representing the position of the player on the grid."""
        return self._player_position

    def get_player_moves_remaining(self) -> int:
        """Returns the number of moves remaining for the player."""
        return self._player.get_moves_remaining()

    def get_player_strength(self) -> int:
        """Returns the current strength of the player."""
        return self._player.get_strength()

    def attempt_move(self, direction: str) -> bool:
        """Attempts to move the player character in the specified direction.

        Args:
        direction (str): The direction in which the player wants to move ('up', 'down', 'left', or 'right').

        This method handles the player's movement within the game. It checks if the specified direction is valid,
        considering the game grid and entity positions. If the move is valid, it updates the player's position and
        modifies the game state accordingly. The method returns True if the move was successful, indicating that
        the player's position has changed, and False otherwise if the move is invalid or blocked.

        return: bool
        """

        # Check if the given direction is valid
        if direction not in DIRECTION_DELTAS:
            return False

        # Get the current player position from the game state
        position_player = self.get_player_position()

        # Get current player strength and remaining moves
        player_strength = self.get_player_strength()
        player_moves = self.get_player_moves_remaining()

        # movement (tuple[int, int]): The coordinate deltas for the specified movement direction.
        movement = DIRECTION_DELTAS[direction]

        # position_next_move: The next position of the player after the move.
        position_next_move = (position_player[0] + movement[0], position_player[1] + movement[1])
        x, y = position_next_move  # x is row and y is column

        # Fetch maze dimensions
        maze = self.get_maze()
        maze_height = len(maze)
        maze_width = len(maze[0])

        # Check if the potential move is within the maze boundary
        if y >= maze_height or x >= maze_width:
            return False

        # Check if the potential move is blocked by maze tiles
        maze_tile = self.get_maze()[x][y]
        if maze_tile.is_blocking():
            return False

        # Store all entities in a dictionary
        entities = self.get_entities()

        # Check if the next position has an entity and handle accordingly
        if position_next_move in entities:
            entity_object = entities[position_next_move]  # The entity object at the potential new position.

            # Check if the entity is a crate
            if entity_object.get_type() == CRATE:
                crate_strength = entity_object.get_strength()  # The strength of the crate

                # position_crate_move: The potential new position of the crate if the carte be pushed by player
                position_crate_move = (position_next_move[0] + movement[0], position_next_move[1] + movement[1])

                # a,b coordinates of the potential new crate position
                a, b = position_crate_move

                # Check if the crate move is within the maze boundary
                if a >= maze_height or b >= maze_width:
                    return False

                # The new tile which will be occupied by crate in the next move
                maze_tile_new = self.get_maze()[a][b]

                # if the tile is a wall return False if not return True
                if maze_tile_new.is_blocking():
                    return False

                # return False if the strength of player is less than the crate
                if player_strength < crate_strength:
                    return False

                # return False when position_crate_move is an entity
                if position_crate_move in entities:
                    return False

                # create a new dictionary to store all the entities before making any move for undo step
                entities_undo = {}
                for h, j in entities.items():  # copy keys and values from original entities
                    entities_undo[h] = j
                self.entities_undo = entities_undo

                # make the crate movable
                entity_object.is_movable()

                # delete old position of crate
                entities.pop(position_next_move)

                # update new position of crate
                entities[position_crate_move] = entity_object

                # if the tile at the new position is a GOAL
                if maze_tile_new.get_type() == GOAL:

                    # fill the goal, turn 'G' to 'X'
                    maze_tile_new.fill()

                    # delete crate because it has filled the goal
                    entities.pop(position_crate_move)

            else:
                # if player next move is a potion
                potion = entities[position_next_move]
                effect = potion.effect()

                # create a new dictionary to store all the entities before making any move for undo step
                entities_undo = {}
                for h, j in entities.items():
                    entities_undo[h] = j
                self.entities_undo = entities_undo

                # save the player strength before apply the effect
                self.strength_undo = player_strength

                # save the player remaining moves before apply the effect
                self.moves_undo = player_moves

                # player use the potion and delete the potion
                entities.pop(position_next_move)
                self._player.apply_effect(effect)

        # save maze, player position, strength and moves, entities before any change
        self.moves_undo = player_moves
        self.player_undo = Player(player_strength, player_moves)
        self.maze_undo = maze
        self.player_position_undo = self._player_position
        self.undo_stack.append({
            '_maze': self.maze_undo,
            '_entities': self.entities_undo,
            '_player_position': self.player_position_undo,
            '_strength': self.strength_undo,
            '_moves': self.moves_undo,
            '_player': self.player_undo
        })

        # player move to new position
        self._player_position = position_next_move

        # the moves of player minus 1
        self._player.add_moves_remaining(-1)
        return True

    def has_won(self) -> bool:
        """ Checks if the player has won the game by completing all goals
        Returns True if the player has won, False otherwise
        """
        #  store all the unfilled goal in a list
        goals = []
        for i in self.get_maze():
            for j in i:
                if j.get_type() == GOAL:
                    if not j.is_filled():  # if the goal is not filled
                        goals.append(j)

        # return True if there are no unfilled goal which means all goals are filled
        if len(goals) == 0:
            return True

        return False

    def undo(self) -> None:
        """ Reverts the game state to the last saved state.

        This method pops the last saved state from the undo stack and reverts all game-related attributes
        to their values in that state.
        """

        # if the list stores nothing, undo method is not usable
        if len(self.undo_stack) == 0:
            return

        last_state = self.undo_stack.pop()

        # Revert to the last state
        self._maze = last_state['_maze']
        self._entities = last_state['_entities']

        # find the filled goal and unfill it
        for i in self.get_maze():
            for j in i:
                if j.get_type() == GOAL:
                    j.unfill()

        # assign the values of last step to attributes
        self._player_position = last_state['_player_position']
        self._strength = last_state['_strength']
        self._moves = last_state['_moves']
        self._player = last_state['_player']


class Sokoban:
    """A class representing a Sokoban game.

    Attributes:
        _model (SokobanModel): The game model, which contains the maze, entities, and game state.
        _view (SokobanView): The view responsible for displaying the game and statistics.
    """

    def __init__(self, maze_file):
        """Initialize a new Sokoban game instance.

        Args:maze_file (str): The path to the maze file used to initialize the game.
        Returns:None
        """
        self._model = SokobanModel(maze_file)
        self._view = SokobanView()

    def display(self) -> None:
        """Display the current state of the Sokoban game.

        This method displays the game board, player's position, and other relevant information.
        Returns:None
        """
        # the 2D list of game grid
        maze = self._model.get_maze()

        # the dictionary containing all the entities
        entity = self._model.get_entities()

        # player current position
        position = self._model.get_player_position()

        # player strength
        strength = self._model.get_player_strength()

        # player remaining moves
        moves_remaining = self._model.get_player_moves_remaining()

        self._view.display_game(maze, entity, position)  # game grid
        self._view.display_stats(moves_remaining, strength)  # player stats

    def play_game(self):
        """ Start playing the Sokoban game.

        This method allows the player to make moves and plays the game until the player wins,
        loses, or quits the game. when player moves > 0, the game continues, otherwise the game ends.
        Returns:None
        """
        while self._model.get_player_moves_remaining() > 0:  # the game continues when the moves are more than 0
            self.display()  # display the current state of game and player

            if self._model.has_won():  # check if the game won
                print("You won!")
                return

            result = input("Enter move: ")  # Prompt the player for a move.
            if result == 'q':  # If the player enters 'q',quit the game
                return

            if result == 'u':  # if the player enter 'u', back to previous status
                self._model.undo()

            elif not self._model.attempt_move(result):  # If the move is invalid, inform the player.
                print("Invalid move\n")

        if self._model.has_won():  # If the player wins after all moves, display victory message.
            self.display()
            print("You won!")
            return

        if self._model.get_player_moves_remaining() == 0:  # If the player runs out of moves, display defeat message.
            print("You lost!")
            return


def main() -> None:
    # uncomment the lines below once you've written your Sokoban class
    game = Sokoban('maze_files/maze3.txt')
    game.play_game()
    pass


if __name__ == '__main__':
    main()
