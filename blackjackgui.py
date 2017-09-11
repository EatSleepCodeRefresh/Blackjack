"""
File: blackjackgui.py
Project 9-4
Author: Roland
"""
from tkinter import *
from blackjack import Blackjack

class BlackjackGUI(Frame):
	def __init__(self):
		Frame.__init__(self)
		self._model = Blackjack()
		self.master.title("Blackjack")
		self.grid()
		
		#Add the command buttons
		self._hitButton = Button(self, text = "HIT", command = self._hit)
		self._hitButton.grid(row = 0, column = 0)
		self._stayButton = Button(self, text = "STAY", command = self._stay)
		self._stayButton.grid(row = 0, column = 1)
		self._newGameButton = Button(self, text = "NEW GAME", command = self._newGame)
		self._newGameButton.grid(row = 0, column = 2)
		
		#Add the status field
		self._statusVar = StringVar()
		self._statusField = Entry(self, textvariable = self._statusVar)
		self._statusField.grid(row = 1, column = 0, columnspan = 3)
		
		#Add the panes for the player and dealer cards
		self._playerPane = Frame(self)
		self._playerPane.grid(row = 2, column = 0)
		self._dealerPane = Frame(self)
		self._dealerPane.grid(row = 3, column = 0, columnspan = 3)
		self._newGame()
		
	#Create the event handler methods
	def _newGame(self):
		"""Instantiates the model and establishes the GUI."""
		self._model = Blackjack()
		
		#Refresh the cards pane
		self._playerImages = list(map(lambda card: PhotoImage(file = card.getFilename()), self._model.getPlayerCards()))
		self._playerLabels = list(map(lambda i: Label(self._playerPane, image = i), self._playerImages))
		for col in range(len(self._playerLabels)):
			self._playerLabels[col].grid(row = 0, column = col)
			
		#Dealer Cards
		self._dealerImages = list(map(lambda card: PhotoImage(file = card.getFilename()), self._model.getDealerCards()))
		self._dealerLabels = list(map(lambda i: Label(self._dealerPane, image = i), self._dealerImages))
		for col in range(len(self._dealerLabels)):
			self._dealerLabels[col].grid(row = 0, column = col)
			
		#Re-enable the buttons and clear the status field
		self._hitButton["state"] = NORMAL
		self._stayButton["state"] = NORMAL
		self._statusVar.set("")
	
	
	def _hit(self):
		"""Hits the player in the data model and updates the card pane. If the player points reach or exceed 21, hits the dealer too."""
		(card, points) = self._model.hitPlayer()
		cardImage = PhotoImage(file = card.getFilename())
		self._playerImages.append(cardImage)
		label = Label(self._playerPane, image = cardImage)
		self._playerLabels.append(label)
		label.grid(row = 0, column = len(self._playerLabels) - 1)
		if points >= 21:
			self._stay()	#Hits the dealer to finish
			
	def _stay(self):
		"""Hits the dealer in the data model, updates its card pane, and displays the outcome of the game."""
		self._hitButton["state"] = DISABLED
		self._stayButton["state"] = DISABLED
		
		#Hit dealer and refresh card pane
		outcome = self._model.hitDealer()
		self._dealerImages = list(map(lambda card: PhotoImage(file = card.getFilename()), self._model.getDealerCards()))
		self._dealerLabels = list(map(lambda i: Label(self._dealerPane, image = i), self._dealerImages))
		for col in range(len(self._dealerLabels)):
			self._dealerLabels[col].grid(row = 0, column = 0)
		self._statusVar.set(outcome)
		
def main():
	BlackjackGUI().mainloop()
	
main()