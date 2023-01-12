import pygame
import numpy as np
import sys, pygame
import random
from tablesChess import tables
import math

pygame.init()
pygame.display.set_caption('Chess')
size = width, height = 1004, 812

screen = pygame.display.set_mode(size)

beige = (201, 168, 126)
brown = (113, 94, 69)
beigeD = (171, 143, 108)
brownD = (98, 82, 60)
selectedColor = (74, 62, 46)
bgColor = (139, 139, 139)


def scoreText(score, x, y, txt):
    black = (0, 0, 0)
    font = pygame.font.Font('freesansbold.ttf', 28)
    text = font.render(txt + str(score), True, black)
    textRect = text.get_rect()
    textRect.center = (x, y)
    textRect.left = x
    return [text, textRect]


class Game:
    def __init__(self):

        self.screen = screen
        self.board = Board()
        self.score = 1
        self.selectedSquare = None
        self.selectedSquareIndex = None
        self.timerDisUpdate = 0
        self.allPieces = []
        pieceTypes = [4, 3, 2, 1, 0, 2, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5]
        pieceTypes2 = [5, 5, 5, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0, 2, 3, 4]

        # self.allPieces.append(Piece(1, 0))
        # self.allPieces.append(Piece(4, 1))
        # self.allPieces.append(Piece(3, 0))
        # self.allPieces.append(Piece(3, 1))

        for pieceType in pieceTypes:
            self.allPieces.append(Piece(pieceType, 0))

        for pieceType in pieceTypes2:
            self.allPieces.append(Piece(pieceType, 1))

        self.allPiecesPos = []

        # self.allPiecesPos.append(43)
        # self.allPiecesPos.append(12)
        # self.allPiecesPos.append(44)
        # self.allPiecesPos.append(55)

        for i in range(16):
            self.allPiecesPos.append(i)

        for i in range(48, 64):
            self.allPiecesPos.append(i)

    def main(self):
        clock = pygame.time.Clock()
        frametime = clock.tick()
        self.score = 1
        run = True
        self.drawObjects()
        pygame.display.update()
        while run == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()

            self.drawObjects()

            clock.tick(10)

    def moveOrEat(self, boardPieceIndex, boardPiece, eat=False):
        if eat:
            if self.selectedSquareIndex > self.allPiecesPos.index(boardPieceIndex):
                self.selectedSquareIndex -= 1

            self.allPieces.pop(self.allPiecesPos.index(boardPieceIndex))
            self.allPiecesPos.pop(self.allPiecesPos.index(boardPieceIndex))

            pygame.draw.rect(screen,
                             self.board.boardColors[boardPieceIndex],
                             self.board.boardRect[boardPieceIndex])

        self.allPieces[self.selectedSquareIndex].drawPiece(boardPiece)
        pygame.draw.rect(screen, self.board.boardColors[
            self.allPiecesPos[self.selectedSquareIndex]],
                         self.board.boardRect[
                             self.allPiecesPos[self.selectedSquareIndex]])
        self.allPiecesPos[self.selectedSquareIndex] = boardPieceIndex
        self.selectedSquare = None
        self.selectedSquareIndex = None
        pygame.display.update()

    def drawObjects(self):
        self.screen.fill(bgColor)
        # scoreFunc = scoreText(self.timerDisUpdate, 20, 30, "Size: ")
        # self.screen.blit(scoreFunc[0], scoreFunc[1])
        self.board.drawBoard(self.screen)

        if self.timerDisUpdate > 0:
            self.timerDisUpdate -= 1

        for i in range(len(self.allPieces)):
            self.allPieces[i].drawPiece(self.board.boardRect[self.allPiecesPos[i]])

        if pygame.mouse.get_pressed()[0]:
            mousePos = pygame.mouse.get_pos()
            for pieceIndex, piece in enumerate(self.allPieces):
                if piece.pieceRect.collidepoint(mousePos):
                    if self.selectedSquare is None:
                        self.timerDisUpdate = 4
                        pygame.draw.rect(screen, selectedColor, piece.pieceRect)
                        self.selectedSquare = piece
                        self.selectedSquareIndex = pieceIndex
                        self.allPieces[pieceIndex].drawPiece(self.board.boardRect[self.allPiecesPos[pieceIndex]])
                        pygame.display.update()
                    elif self.selectedSquare is not None and self.selectedSquare != piece:
                        if self.selectedSquare.pieceColor == piece.pieceColor:
                            self.timerDisUpdate = 4
                            pygame.draw.rect(screen, selectedColor, piece.pieceRect)
                            self.selectedSquare = piece
                            self.selectedSquareIndex = pieceIndex
                            self.allPieces[pieceIndex].drawPiece(self.board.boardRect[self.allPiecesPos[pieceIndex]])
                            pygame.display.update()
                    elif self.timerDisUpdate == 0 and self.selectedSquare == piece:
                        self.selectedSquare = None
                        self.selectedSquareIndex = None
                        pygame.display.update()

            for boardPieceIndex, boardPiece in enumerate(self.board.boardRect):
                if boardPiece.collidepoint(mousePos):
                    if self.selectedSquare is not None and self.selectedSquareIndex is not None and boardPieceIndex != \
                            self.allPiecesPos[self.selectedSquareIndex]:
                        if self.selectedSquare.pieceType == 5:
                            tableIndex = self.allPiecesPos[self.selectedSquareIndex] / 8
                            colorOperator = 1
                            if self.selectedSquare.pieceColor == 1:
                                colorOperator = -1
                            if 0 < math.floor(tableIndex) < 7 and boardPieceIndex not in self.allPiecesPos:
                                if (boardPieceIndex == tables[0][math.floor(tableIndex) + colorOperator][
                                    math.floor((tableIndex % 1) * 8)] or
                                    (boardPieceIndex == tables[0][math.floor(tableIndex) + colorOperator * 2][
                                        math.floor((tableIndex % 1) * 8)] and
                                     (((self.selectedSquare.pieceRect.y == self.board.boardRect[
                                         10].y and self.selectedSquare.pieceColor == 0) or
                                       (self.selectedSquare.pieceRect.y == self.board.boardRect[
                                           50].y and self.selectedSquare.pieceColor == 1))))) and \
                                        boardPieceIndex not in self.allPiecesPos:
                                    self.moveOrEat(boardPieceIndex, boardPiece)
                            elif math.floor(tableIndex) == 0 or math.floor(tableIndex) == 7:
                                pass  # TODO: cambiar a pieza que quieran
                            elif boardPieceIndex in self.allPiecesPos and \
                                    self.allPieces[self.allPiecesPos.index(
                                        boardPieceIndex)].pieceColor != self.selectedSquare.pieceColor:
                                if ((tableIndex) - math.floor(tableIndex)) * 8 != 7 and boardPieceIndex == \
                                        tables[0][math.floor(tableIndex) + colorOperator][
                                            math.floor((tableIndex % 1) * 8) + 1]:
                                    self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                elif ((tableIndex) - math.floor(tableIndex)) * 8 != 0 and boardPieceIndex == \
                                        tables[0][math.floor(tableIndex) + colorOperator][
                                            math.floor((tableIndex % 1) * 8) - 1]:
                                    self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                        elif self.selectedSquare.pieceType == 4:
                            tableIndex = self.allPiecesPos[self.selectedSquareIndex] / 8
                            if boardPieceIndex in tables[1][math.floor((tableIndex % 1) * 8)]:
                                matches = list(
                                    set(tables[1][math.floor((tableIndex % 1) * 8)]).intersection(self.allPiecesPos))
                                tableMainIndex = tables[1][math.floor((tableIndex % 1) * 8)].index(
                                    self.allPiecesPos[self.selectedSquareIndex])
                                if boardPieceIndex > tables[1][math.floor((tableIndex % 1) * 8)][
                                    math.floor(tableIndex)]:
                                    beforeLast = None
                                    for match in matches:
                                        if match > self.allPiecesPos[self.selectedSquareIndex] and beforeLast is None:
                                            beforeLast = match
                                        elif match > self.allPiecesPos[
                                            self.selectedSquareIndex] and beforeLast is not None and match < beforeLast:
                                            beforeLast = match

                                    for match in matches.copy():
                                        if match < self.allPiecesPos[self.selectedSquareIndex]:
                                            matches.remove(match)

                                    if beforeLast is None:
                                        beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                    beforeLastIndex = tables[1][math.floor((tableIndex % 1) * 8)].index(beforeLast) + 1
                                    rangePossible = tables[1][math.floor((tableIndex % 1) * 8)][
                                                    tableMainIndex:beforeLastIndex]
                                    if len(matches) == 1:
                                        rangePossible = tables[1][math.floor((tableIndex % 1) * 8)][
                                                        tableMainIndex:]

                                    if rangePossible[-1] > boardPieceIndex:
                                        self.moveOrEat(boardPieceIndex, boardPiece)
                                    elif rangePossible[-1] == boardPieceIndex:
                                        if rangePossible[-1] in self.allPiecesPos:
                                            if self.allPieces[self.allPiecesPos.index(
                                                    rangePossible[-1])].pieceColor != self.selectedSquare.pieceColor:
                                                self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                        else:
                                            self.moveOrEat(boardPieceIndex, boardPiece)

                                elif boardPieceIndex < tables[1][math.floor((tableIndex % 1) * 8)][
                                    math.floor(tableIndex)]:
                                    beforeLast = None
                                    for match in matches:
                                        if match < self.allPiecesPos[self.selectedSquareIndex] and beforeLast is None:
                                            beforeLast = match
                                        elif match < self.allPiecesPos[
                                            self.selectedSquareIndex] and beforeLast is not None and match > beforeLast:
                                            beforeLast = match

                                    for match in matches.copy():
                                        if match > self.allPiecesPos[self.selectedSquareIndex]:
                                            matches.remove(match)

                                    if beforeLast is None:
                                        beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                    beforeLastIndex = tables[1][math.floor((tableIndex % 1) * 8)].index(beforeLast)
                                    rangePossible = tables[1][math.floor((tableIndex % 1) * 8)][
                                                    beforeLastIndex:tableMainIndex]
                                    if len(matches) == 1:
                                        rangePossible = tables[1][math.floor((tableIndex % 1) * 8)][
                                                        :tableMainIndex]

                                    if rangePossible[0] < boardPieceIndex:
                                        self.moveOrEat(boardPieceIndex, boardPiece)
                                    elif rangePossible[0] == boardPieceIndex:
                                        if rangePossible[0] in self.allPiecesPos:
                                            if self.allPieces[self.allPiecesPos.index(
                                                    rangePossible[0])].pieceColor != self.selectedSquare.pieceColor:
                                                self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                        else:
                                            self.moveOrEat(boardPieceIndex, boardPiece)

                            elif boardPieceIndex in tables[0][math.floor(tableIndex)]:
                                matches = list(
                                    set(tables[0][math.floor(tableIndex)]).intersection(self.allPiecesPos))
                                tableMainIndex = tables[0][math.floor(tableIndex)].index(
                                    self.allPiecesPos[self.selectedSquareIndex])
                                if boardPieceIndex > tables[0][math.floor(tableIndex)][
                                    math.floor((tableIndex % 1) * 8)]:
                                    beforeLast = None
                                    for match in matches:
                                        if match > self.allPiecesPos[self.selectedSquareIndex] and beforeLast is None:
                                            beforeLast = match
                                        elif match > self.allPiecesPos[
                                            self.selectedSquareIndex] and beforeLast is not None and match < beforeLast:
                                            beforeLast = match

                                    for match in matches.copy():
                                        if match < self.allPiecesPos[self.selectedSquareIndex]:
                                            matches.remove(match)

                                    if beforeLast is None:
                                        beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                    beforeLastIndex = tables[0][math.floor(tableIndex)].index(beforeLast) + 1
                                    rangePossible = tables[0][math.floor(tableIndex)][
                                                    tableMainIndex:beforeLastIndex]
                                    if len(matches) == 1:
                                        rangePossible = tables[0][math.floor(tableIndex)][
                                                        tableMainIndex:]

                                    if rangePossible[-1] > boardPieceIndex:
                                        self.moveOrEat(boardPieceIndex, boardPiece)
                                    elif rangePossible[-1] == boardPieceIndex:
                                        if rangePossible[-1] in self.allPiecesPos:
                                            if self.allPieces[self.allPiecesPos.index(
                                                    rangePossible[-1])].pieceColor != self.selectedSquare.pieceColor:
                                                self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                        else:
                                            self.moveOrEat(boardPieceIndex, boardPiece)

                                elif boardPieceIndex < tables[0][math.floor(tableIndex)][
                                    math.floor((tableIndex % 1) * 8)]:
                                    beforeLast = None
                                    for match in matches:
                                        if match < self.allPiecesPos[self.selectedSquareIndex] and beforeLast is None:
                                            beforeLast = match
                                        elif match < self.allPiecesPos[
                                            self.selectedSquareIndex] and beforeLast is not None and match > beforeLast:
                                            beforeLast = match

                                    for match in matches.copy():
                                        if match > self.allPiecesPos[self.selectedSquareIndex]:
                                            matches.remove(match)

                                    if beforeLast is None:
                                        beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                    beforeLastIndex = tables[0][math.floor(tableIndex)].index(beforeLast)
                                    rangePossible = tables[0][math.floor(tableIndex)][
                                                    beforeLastIndex:tableMainIndex]
                                    if len(matches) == 1:
                                        rangePossible = tables[0][math.floor(tableIndex)][
                                                        :tableMainIndex]

                                    if rangePossible[0] < boardPieceIndex:
                                        self.moveOrEat(boardPieceIndex, boardPiece)
                                    elif rangePossible[0] == boardPieceIndex:
                                        if rangePossible[0] in self.allPiecesPos:
                                            if self.allPieces[self.allPiecesPos.index(
                                                    rangePossible[0])].pieceColor != self.selectedSquare.pieceColor:
                                                self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                        else:
                                            self.moveOrEat(boardPieceIndex, boardPiece)
                        elif self.selectedSquare.pieceType == 3:
                            currentPos = self.allPiecesPos[self.selectedSquareIndex]
                            tableIndex = currentPos / 8

                            if boardPieceIndex in tables[4][self.allPiecesPos[self.selectedSquareIndex]]:
                                if boardPieceIndex in self.allPiecesPos:
                                    if self.allPieces[self.allPiecesPos.index(
                                            boardPieceIndex)].pieceColor != self.selectedSquare.pieceColor:
                                        self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                else:
                                    self.moveOrEat(boardPieceIndex, boardPiece)
                        elif self.selectedSquare.pieceType == 2:
                            whichTable = None
                            rowTableIndex = None
                            indexInTable = None
                            piecePos = self.allPiecesPos[self.selectedSquareIndex]
                            for indexR, rowT3 in enumerate(tables[2]):
                                if boardPieceIndex in rowT3 and piecePos in rowT3:
                                    whichTable = 2
                                    rowTableIndex = indexR
                                    indexInTable = rowT3.index(piecePos)
                                    break

                            for indexR, rowT4 in enumerate(tables[3]):
                                if boardPieceIndex in rowT4 and piecePos in rowT4:
                                    whichTable = 3
                                    rowTableIndex = indexR
                                    indexInTable = rowT4.index(piecePos)
                                    break

                            if indexInTable is not None:
                                matches = list(
                                    set(tables[whichTable][rowTableIndex]).intersection(self.allPiecesPos))

                                if boardPieceIndex > piecePos:
                                    beforeLast = None
                                    for match in matches:
                                        if match > self.allPiecesPos[self.selectedSquareIndex] and beforeLast is None:
                                            beforeLast = match
                                        elif match > self.allPiecesPos[
                                            self.selectedSquareIndex] and beforeLast is not None and match < beforeLast:
                                            beforeLast = match

                                    for match in matches.copy():
                                        if match < self.allPiecesPos[self.selectedSquareIndex]:
                                            matches.remove(match)

                                    if beforeLast is None:
                                        beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                    beforeLastIndex = tables[whichTable][rowTableIndex].index(beforeLast)
                                    rangePossible = tables[whichTable][rowTableIndex][
                                                    beforeLastIndex:indexInTable]
                                    if len(matches) == 1:
                                        rangePossible = tables[whichTable][rowTableIndex][
                                                        :indexInTable]

                                    if rangePossible[0] > boardPieceIndex:
                                        self.moveOrEat(boardPieceIndex, boardPiece)
                                    elif rangePossible[0] == boardPieceIndex:
                                        if rangePossible[0] in self.allPiecesPos:
                                            if self.allPieces[self.allPiecesPos.index(
                                                    rangePossible[0])].pieceColor != self.selectedSquare.pieceColor:
                                                self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                        else:
                                            self.moveOrEat(boardPieceIndex, boardPiece)

                                elif boardPieceIndex < piecePos:
                                    beforeLast = None

                                    for match in matches:
                                        if match < self.allPiecesPos[self.selectedSquareIndex] and beforeLast is None:
                                            beforeLast = match
                                        elif match < self.allPiecesPos[
                                            self.selectedSquareIndex] and beforeLast is not None and match > beforeLast:
                                            beforeLast = match

                                    for match in matches.copy():
                                        if match > self.allPiecesPos[self.selectedSquareIndex]:
                                            matches.remove(match)

                                    if beforeLast is None:
                                        beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                    beforeLastIndex = tables[whichTable][rowTableIndex].index(beforeLast) + 1
                                    rangePossible = tables[whichTable][rowTableIndex][
                                                    indexInTable:beforeLastIndex]

                                    if len(matches) == 1:
                                        rangePossible = tables[whichTable][rowTableIndex][
                                                        indexInTable:]

                                    if rangePossible[-1] < boardPieceIndex:
                                        self.moveOrEat(boardPieceIndex, boardPiece)
                                    elif rangePossible[-1] == boardPieceIndex:
                                        if rangePossible[-1] in self.allPiecesPos:
                                            if self.allPieces[self.allPiecesPos.index(
                                                    rangePossible[-1])].pieceColor != self.selectedSquare.pieceColor:
                                                self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                        else:
                                            self.moveOrEat(boardPieceIndex, boardPiece)
                        elif self.selectedSquare.pieceType == 1:
                            whichTable = None
                            rowTableIndex = None
                            indexInTable = None
                            piecePos = self.allPiecesPos[self.selectedSquareIndex]
                            for indexR, rowT3 in enumerate(tables[2]):
                                if boardPieceIndex in rowT3 and piecePos in rowT3:
                                    whichTable = 2
                                    rowTableIndex = indexR
                                    indexInTable = rowT3.index(piecePos)
                                    break

                            for indexR, rowT4 in enumerate(tables[3]):
                                if boardPieceIndex in rowT4 and piecePos in rowT4:
                                    whichTable = 3
                                    rowTableIndex = indexR
                                    indexInTable = rowT4.index(piecePos)
                                    break

                            if indexInTable is not None:
                                matches = list(
                                    set(tables[whichTable][rowTableIndex]).intersection(self.allPiecesPos))

                                if boardPieceIndex > piecePos:
                                    beforeLast = None

                                    for match in matches:
                                        if match > self.allPiecesPos[self.selectedSquareIndex] and beforeLast is None:
                                            beforeLast = match
                                        elif match > self.allPiecesPos[
                                            self.selectedSquareIndex] and beforeLast is not None and match < beforeLast:
                                            beforeLast = match

                                    for match in matches.copy():
                                        if match < self.allPiecesPos[self.selectedSquareIndex]:
                                            matches.remove(match)

                                    if beforeLast is None:
                                        beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                    beforeLastIndex = tables[whichTable][rowTableIndex].index(beforeLast)
                                    rangePossible = tables[whichTable][rowTableIndex][
                                                    beforeLastIndex:indexInTable]
                                    if len(matches) == 1:
                                        rangePossible = tables[whichTable][rowTableIndex][
                                                        :indexInTable]

                                    if rangePossible[0] > boardPieceIndex:
                                        self.moveOrEat(boardPieceIndex, boardPiece)
                                    elif rangePossible[0] == boardPieceIndex:
                                        if rangePossible[0] in self.allPiecesPos:
                                            if self.allPieces[self.allPiecesPos.index(
                                                    rangePossible[0])].pieceColor != self.selectedSquare.pieceColor:
                                                self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                        else:
                                            self.moveOrEat(boardPieceIndex, boardPiece)

                                elif boardPieceIndex < piecePos:
                                    beforeLast = None

                                    for match in matches:
                                        if match < self.allPiecesPos[self.selectedSquareIndex] and beforeLast is None:
                                            beforeLast = match
                                        elif match < self.allPiecesPos[
                                            self.selectedSquareIndex] and beforeLast is not None and match < beforeLast:
                                            beforeLast = match

                                    for match in matches.copy():
                                        if match > self.allPiecesPos[self.selectedSquareIndex]:
                                            matches.remove(match)

                                    if beforeLast is None:
                                        beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                    beforeLastIndex = tables[whichTable][rowTableIndex].index(beforeLast) + 1
                                    rangePossible = tables[whichTable][rowTableIndex][
                                                    indexInTable:beforeLastIndex]
                                    if len(matches) == 1:
                                        rangePossible = tables[whichTable][rowTableIndex][
                                                        indexInTable:]

                                    if rangePossible[-1] < boardPieceIndex:
                                        self.moveOrEat(boardPieceIndex, boardPiece)
                                    elif rangePossible[-1] == boardPieceIndex:
                                        if rangePossible[-1] in self.allPiecesPos:
                                            if self.allPieces[self.allPiecesPos.index(
                                                    rangePossible[-1])].pieceColor != self.selectedSquare.pieceColor:
                                                self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                        else:
                                            self.moveOrEat(boardPieceIndex, boardPiece)
                            else:
                                tableIndex = self.allPiecesPos[self.selectedSquareIndex] / 8
                                if boardPieceIndex in tables[1][math.floor((tableIndex % 1) * 8)]:
                                    matches = list(
                                        set(tables[1][math.floor((tableIndex % 1) * 8)]).intersection(
                                            self.allPiecesPos))
                                    tableMainIndex = tables[1][math.floor((tableIndex % 1) * 8)].index(
                                        self.allPiecesPos[self.selectedSquareIndex])
                                    if boardPieceIndex > tables[1][math.floor((tableIndex % 1) * 8)][
                                        math.floor(tableIndex)]:
                                        beforeLast = None
                                        for match in matches:
                                            if match > self.allPiecesPos[
                                                self.selectedSquareIndex] and beforeLast is None:
                                                beforeLast = match
                                            elif match > self.allPiecesPos[
                                                self.selectedSquareIndex] and beforeLast is not None and match < beforeLast:
                                                beforeLast = match

                                        for match in matches.copy():
                                            if match < self.allPiecesPos[self.selectedSquareIndex]:
                                                matches.remove(match)

                                        if beforeLast is None:
                                            beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                        beforeLastIndex = tables[1][math.floor((tableIndex % 1) * 8)].index(
                                            beforeLast) + 1
                                        rangePossible = tables[1][math.floor((tableIndex % 1) * 8)][
                                                        tableMainIndex:beforeLastIndex]
                                        if len(matches) == 1:
                                            rangePossible = tables[1][math.floor((tableIndex % 1) * 8)][
                                                            tableMainIndex:]

                                        if rangePossible[-1] > boardPieceIndex:
                                            self.moveOrEat(boardPieceIndex, boardPiece)
                                        elif rangePossible[-1] == boardPieceIndex:
                                            if rangePossible[-1] in self.allPiecesPos:
                                                if self.allPieces[self.allPiecesPos.index(
                                                        rangePossible[
                                                            -1])].pieceColor != self.selectedSquare.pieceColor:
                                                    self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                            else:
                                                self.moveOrEat(boardPieceIndex, boardPiece)

                                    elif boardPieceIndex < tables[1][math.floor((tableIndex % 1) * 8)][
                                        math.floor(tableIndex)]:
                                        beforeLast = None
                                        for match in matches:
                                            if match < self.allPiecesPos[
                                                self.selectedSquareIndex] and beforeLast is None:
                                                beforeLast = match
                                            elif match < self.allPiecesPos[
                                                self.selectedSquareIndex] and beforeLast is not None and match > beforeLast:
                                                beforeLast = match

                                        for match in matches.copy():
                                            if match > self.allPiecesPos[self.selectedSquareIndex]:
                                                matches.remove(match)

                                        if beforeLast is None:
                                            beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                        beforeLastIndex = tables[1][math.floor((tableIndex % 1) * 8)].index(beforeLast)
                                        rangePossible = tables[1][math.floor((tableIndex % 1) * 8)][
                                                        beforeLastIndex:tableMainIndex]
                                        if len(matches) == 1:
                                            rangePossible = tables[1][math.floor((tableIndex % 1) * 8)][
                                                            :tableMainIndex]

                                        if rangePossible[0] < boardPieceIndex:
                                            self.moveOrEat(boardPieceIndex, boardPiece)
                                        elif rangePossible[0] == boardPieceIndex:
                                            if rangePossible[0] in self.allPiecesPos:
                                                if self.allPieces[self.allPiecesPos.index(
                                                        rangePossible[0])].pieceColor != self.selectedSquare.pieceColor:
                                                    self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                            else:
                                                self.moveOrEat(boardPieceIndex, boardPiece, )

                                elif boardPieceIndex in tables[0][math.floor(tableIndex)]:
                                    matches = list(
                                        set(tables[0][math.floor(tableIndex)]).intersection(self.allPiecesPos))
                                    tableMainIndex = tables[0][math.floor(tableIndex)].index(
                                        self.allPiecesPos[self.selectedSquareIndex])
                                    if boardPieceIndex > tables[0][math.floor(tableIndex)][
                                        math.floor((tableIndex % 1) * 8)]:
                                        beforeLast = None
                                        for match in matches:
                                            if match > self.allPiecesPos[
                                                self.selectedSquareIndex] and beforeLast is None:
                                                beforeLast = match
                                            elif match > self.allPiecesPos[
                                                self.selectedSquareIndex] and beforeLast is not None and match < beforeLast:
                                                beforeLast = match

                                        for match in matches.copy():
                                            if match < self.allPiecesPos[self.selectedSquareIndex]:
                                                matches.remove(match)

                                        if beforeLast is None:
                                            beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                        beforeLastIndex = tables[0][math.floor(tableIndex)].index(beforeLast) + 1
                                        rangePossible = tables[0][math.floor(tableIndex)][
                                                        tableMainIndex:beforeLastIndex]
                                        if len(matches) == 1:
                                            rangePossible = tables[0][math.floor(tableIndex)][
                                                            tableMainIndex:]

                                        if rangePossible[-1] > boardPieceIndex:
                                            self.moveOrEat(boardPieceIndex, boardPiece)
                                        elif rangePossible[-1] == boardPieceIndex:
                                            if rangePossible[-1] in self.allPiecesPos:
                                                if self.allPieces[self.allPiecesPos.index(
                                                        rangePossible[
                                                            -1])].pieceColor != self.selectedSquare.pieceColor:
                                                    self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                            else:
                                                self.moveOrEat(boardPieceIndex, boardPiece)

                                    elif boardPieceIndex < tables[0][math.floor(tableIndex)][
                                        math.floor((tableIndex % 1) * 8)]:
                                        beforeLast = None
                                        for match in matches:
                                            if match < self.allPiecesPos[
                                                self.selectedSquareIndex] and beforeLast is None:
                                                beforeLast = match
                                            elif match < self.allPiecesPos[
                                                self.selectedSquareIndex] and beforeLast is not None and match > beforeLast:
                                                beforeLast = match

                                        for match in matches.copy():
                                            if match > self.allPiecesPos[self.selectedSquareIndex]:
                                                matches.remove(match)

                                        if beforeLast is None:
                                            beforeLast = self.allPiecesPos[self.selectedSquareIndex]

                                        beforeLastIndex = tables[0][math.floor(tableIndex)].index(beforeLast)
                                        rangePossible = tables[0][math.floor(tableIndex)][
                                                        beforeLastIndex:tableMainIndex]
                                        if len(matches) == 1:
                                            rangePossible = tables[0][math.floor(tableIndex)][
                                                            :tableMainIndex]

                                        if rangePossible[0] < boardPieceIndex:
                                            self.moveOrEat(boardPieceIndex, boardPiece)
                                        elif rangePossible[0] == boardPieceIndex:
                                            if rangePossible[0] in self.allPiecesPos:
                                                if self.allPieces[self.allPiecesPos.index(
                                                        rangePossible[0])].pieceColor != self.selectedSquare.pieceColor:
                                                    self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                            else:
                                                self.moveOrEat(boardPieceIndex, boardPiece)
                        elif self.selectedSquare.pieceType == 0:
                            currentPos = self.allPiecesPos[self.selectedSquareIndex]
                            tableIndex = currentPos / 8
                            rowTableIndex = math.floor(tableIndex)
                            indexInTable = math.floor((tableIndex % 1) * 8)

                            available = []

                            if rowTableIndex == 0:
                                if indexInTable == 0:
                                    available = [1, 8, 9]
                                    available = [i + currentPos for i in available]
                                elif indexInTable == 7:
                                    available = [-1, 7, 8]
                                    available = [i + currentPos for i in available]
                                else:
                                    available = [1, 8, 9, -1, 7]
                                    available = [i + currentPos for i in available]
                            elif rowTableIndex == 7:
                                if indexInTable == 0:
                                    available = [-8, -7, 1]
                                    available = [i + currentPos for i in available]
                                elif indexInTable == 7:
                                    available = [-9, -8, -1]
                                    available = [i + currentPos for i in available]
                                else:
                                    available = [-1, 1, -9, -8, -7]
                                    available = [i + currentPos for i in available]
                            else:
                                if indexInTable == 0:
                                    available = [-8, -7, 1, 8, 9]
                                    available = [i + currentPos for i in available]
                                elif indexInTable == 7:
                                    available = [-9, -8, -1, 7, 8]
                                    available = [i + currentPos for i in available]
                                else:
                                    available = [-9, -8, -7, -1, 1, 7, 8, 9]
                                    available = [i + currentPos for i in available]

                            if boardPieceIndex in available:
                                if boardPieceIndex in self.allPiecesPos:
                                    if self.allPieces[self.allPiecesPos.index(
                                            boardPieceIndex)].pieceColor != self.selectedSquare.pieceColor:
                                        self.moveOrEat(boardPieceIndex, boardPiece, eat=True)
                                else:
                                    self.moveOrEat(boardPieceIndex, boardPiece)


class Board:
    def __init__(self):
        self.boardRect = []
        self.startXY = 100
        self.yDif = 40
        self.xWidth = 100
        self.yWidth = 80
        self.separation = 5
        self.border = 5
        self.boardColors = []
        for y in range(8):
            r = range(8)
            xMinus = 0
            if y % 2 == 0 or y == 0:
                xMinus = 1
                r = range(1, 9)
            for x in r:
                color = brown
                if x % 2 == 0 or x == 0:
                    color = beige
                rect = pygame.rect.Rect((self.startXY + (self.xWidth * (x - xMinus)),
                                         self.startXY - self.yDif + (self.yWidth * y),
                                         self.xWidth,
                                         self.yWidth))
                self.boardRect.append(rect)
                self.boardColors.append(color)

    def drawBoard(self, screen):

        rect1 = pygame.rect.Rect((self.startXY - self.border,
                                  self.startXY - self.border - self.yDif,
                                  self.xWidth * 8 + self.border * 2,
                                  self.yWidth * 8 + (self.yWidth - self.yDif) + self.border * 2 + self.separation))
        pygame.draw.rect(screen, selectedColor, rect1)

        for b in range(8):
            color = beigeD
            if b % 2 == 0 or b == 0:
                color = brownD
            rect = pygame.rect.Rect(
                (self.startXY + (self.xWidth * b), self.startXY - self.yDif + (self.yWidth * 8) + self.separation,
                 self.xWidth, self.yWidth - self.yDif))
            pygame.draw.rect(screen, color, rect)

        for i in range(len(self.boardRect)):
            pygame.draw.rect(screen, self.boardColors[i], self.boardRect[i])


class Piece:
    def __init__(self, pieceType, color):
        self.pieceColor = color
        self.pieceType = pieceType
        spriteSheet = pygame.image.load('chess_pieces_fullBrown.png').convert_alpha()
        separation = 200
        spritePieceRect = pygame.Rect(
            (14 + (separation * self.pieceType), 18 + (separation * self.pieceColor), 173, 172))
        self.image = pygame.Surface(spritePieceRect.size).convert_alpha()
        self.image.blit(spriteSheet, (0, 0), spritePieceRect)
        self.pieceRect = pygame.rect.Rect((0, 0, 100, 80))

    def drawPiece(self, coor):
        xWidth = 100
        yWidth = 80
        self.pieceRect = pygame.rect.Rect((coor[0], coor[1], xWidth, yWidth))
        screen.blit(pygame.transform.scale(self.image, (xWidth, yWidth)), self.pieceRect)


game1 = Game()

game1.main()
