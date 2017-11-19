from enum import Enum
#--------------------------------------------------------------------------------------------------------------------#
#													   SYSTEM STATES												 #
#--------------------------------------------------------------------------------------------------------------------#

class States(Enum):
	IDLE = 1
	TURN_UP = 2
	TURN_OFF = 3
	FULL = 4

	def get_States_list(self):
		return [States.IDLE, States.TURN_UP, States.TURN_OFF, States.FULL]
