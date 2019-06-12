import pygame


class SpriteSheet:
    def __init__(self, filename, rows, cols):
        self.sheet = pygame.image.load(filename)
        self.cols = cols
        self.rows = rows
        self.total_cells = cols*rows
        self.size = self.sheet.get_rect()
        self.cell_width = self.size.width / cols
        self.cell_height = self.size.height / rows
        self.cell_rects = self.split_sheet()

    def split_sheet(self):
        # gets the area of each individual cell in the sheet, one row at a time from left to right
        lefts = [(x % self.cols) * self.cell_width for x in range(self.total_cells)]
        tops = [(x // self.cols) * self.cell_height for x in range(self.total_cells)]
        widths = [self.cell_width] * self.total_cells
        heights = [self.cell_height] * self.total_cells
        return tuple(zip(lefts, tops, widths, heights))