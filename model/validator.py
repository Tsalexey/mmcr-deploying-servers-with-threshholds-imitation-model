__author__ = 'tsarev alexey'
#--------------------------------------------------------------------------------------------------------------------#
#													  Validator 												  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Validator:
	'''
		Static class for input parameters validation
	'''

	def validate_main():
		is_valid = False
		# TODO: implement
		return is_valid

	def validate_range(input_list):
		'''
			Validate range parameter in format 'parameter=1-10'
		'''
		validation_result = False if len(input_list) != 2 else True
		has_range = True if len(input_list[1].split('-')) == 2 else False
		return [has_range, validation_result]

	def validate_single(input_list):
		'''
			Validate single parameter in format 'parameter=123'
		'''
		validation_result = False if len(input_list) != 2 else True	
		has_range = True if len(input_list.split("-")) != 1 else False
		return [has_range, validation_result]

	def validate_stat_generator(args):
		'''
			Validate input for stat_generator
		'''
		has_range = False
		validation_result = False

		if len(args) < 12 or len(args) > 13:
			print("\nInput parameters must be: 'filename step='%' lambda='%' mu='%' C='%' c0='%' Q='%' theta='%' L='%' H='%' simulation_time is_debug repeats(optionally)'")

		for i in [2, 5]:
			[has_range, validation_result] = validate_single( args[i].split("=") )
			if not validation_result:
				print("Wrong parameter format: ", args[i].split("="))
			if not has_range:
				print("Wron single parameter. Found: ", args[i].split("-"))

		for i in [3, 4, 6, 7, 8, 9, 10]:
			[has_range, validation_result] = validate_range( args[i].split("=") )
			if not validation_result: 
				print("Wrong: ", args[i].split("="))

		if not validation_result: 
			print("\nValidation failed!")
		if not has_range:
			print("\nOne of the following parameters = {lambda, mu, c0, Q, theta, L, H} must be inputed as range in format: parameter='%'-'%'")

