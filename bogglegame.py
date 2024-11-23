"""Implements the logic of the game of boggle."""

from graphics import GraphWin
from boggleboard import BoggleBoard
from bogglecube import BoggleCube
from brandom import randomize

class BoggleGame:  
    # Description of attributes:
    # _valid_words: the set of all valid Boggle words
    # _board: the BoggleBoard
    # _found_words: a list of strings of all words found so far
    # _selected_cubes: a list of BoggleCubes selected in current turn

    __slots__ = [ "_valid_words", "_board", "_found_words", "_selected_cubes" ]

    def __init__(self, win):
        """
        Create a new Boggle Game and load in our lexicon.
        """
        # set up the set of valid words we can match
        self._valid_words = self.__read_lexicon()

        # initialize and draw a BoggleBoard
        self._board = BoggleBoard(win)
        self._board.draw_board()

        # finish __init__ method
        self._found_words = []
        self._selected_cubes = []

    def __read_lexicon(self, lexicon_name='bogwords.txt'):
        """
        A helper method to read the lexicon and return it as a set.
        """
        # DO NOT MODIFY.
        valid_words = set()
        with open(lexicon_name) as f:
          for line in f:
            valid_words.add(line.strip().upper())

        return valid_words

    def __reset_game(self):
        """
        Updates all game state to reflect the start of a "new" game
        """
        self._found_words.clear()
        self._selected_cubes.clear()
        self._board.reset_grid_graphics()

    def __reset_turn(self):
        """
        Reset current turn by resetting state of selected cubes 
        as well as resetting any associated grid graphics (highlighted 
        letters or colored cells) and text from current word displayed on board
        """
        self._board.reset_grid_graphics()
        self._selected_cubes.clear()
        self._board.set_string_to_lower_text("")


    def __highlight_cube(self, cube, text_color, fill_color):
        """
        Highlights a given cube by setting background grid cell to fill_color
        and text in cell to text_color.
        """
        # DO NOT MODIFY.
        r, c = self._board.get_bogglecube_coords(cube)
        letter = cube.get_letter()
        self._board.set_grid_cell(r, c, letter, text_color, fill_color)

    def __add_cube_to_word(self, cube):
        """
        Extends the current word (displayed on lower text area) by
        adding the visible letter from given cube
        """
        self._selected_cubes.append(cube)
        #get the current word from selected cubes
        current_word = self.__selected_cubes_to_word()
        #update display with the current word
        self._board.set_string_to_lower_text(current_word)
        #highlight selected cube
        self.__highlight_cube(cube, "blue", "light blue")


    def __selected_cubes_to_word(self):
        """
        Returns the word spelled by the visible face of all selected cubes
        """
        return ''.join(cube.get_letter() for cube in self._selected_cubes)

    def do_one_click(self, point):
        """
        Implements the logic for processing one click.
        Returns True if play should continue, and False if the game is over.
        """
        # see handout for a step-by-step guide on how to implement this method
        
        if self._board.in_exit(point):
            return False # Exit the game
        if self._board.in_reset(point):
            self.__reset_game()
        if self._board.in_grid(point):
            cube = self._board.get_bogglecube_at_point(point)

            if not self._selected_cubes:  # First cube clicked
                self.__add_cube_to_word(cube)
            else:
                # Check if cube isn't already selected & if adjecent cube is clicked
                if cube not in self._selected_cubes and self._board.is_adjacent(self._selected_cubes[-1], cube): 
                    self.__highlight_cube(self._selected_cubes[-1], "green", "light green")
                    self.__add_cube_to_word(cube)

                elif cube == self._selected_cubes[-1]: # Same cube selected
                    current_word = self.__selected_cubes_to_word() #get current word
                    
                    # Check if the word is valid
                    if current_word in self._valid_words and current_word not in self._found_words:
                        self._found_words.append(current_word)
                        self._board.set_string_to_text_area("\n".join(self._found_words)) # update found words
                    self.__reset_turn() #Reset for new return
                else:
                    self.__reset_turn() # Reset if non-adjesent cube is clicked
        return True

if __name__ == '__main__':

    # When you are ready to run on different boards,
    # insert a call to randomize() here.  BUT you will
    # find it much easier to test your code without
    # randomizing things!

    win = GraphWin("Boggle", 400, 400)
    game = BoggleGame(win)
    keep_going = True
    while keep_going:
        point = win.getMouse()
        keep_going = game.do_one_click(point)
