__author__ = 'tsarev alexey'
#--------------------------------------------------------------------------------------------------------------------#
#													  Validator 												  	 #
#--------------------------------------------------------------------------------------------------------------------#
class Validator:
	"""
		Static class for input parameters validation
	"""

	def validate_main(self):
		is_valid = False
		# TODO: implement
		return is_valid

	def validate_range(self, input_list):
		"""
			Validate range parameter in format 'parameter=1-10'
		"""
		validation_result = False if len(input_list) != 2 else True
		has_range = True if len(input_list[1].split('-')) == 2 else False
		return [has_range, validation_result]

	def validate_single(self, input_list):
		"""
			Validate single parameter in format 'parameter=123'
		"""
		validation_result = False if len(input_list) != 2 else True	
		has_range = True if len(input_list[1].split("-")) == 1 else False
		return [has_range, validation_result]

	def validate_stat_generator(self, args):
		"""
			Validate input for stat_generator
		"""
		has_range = False
		validation_result = False
		range_parameters_count = 0

		if len(args) < 13 or len(args) > 14:
			print("Wrong count of parameters!")
			print("\nInput parameters must be: 'filename step='%' lambda='%' mu='%' C='%' c0='%'",
			 	  "Q='%' theta='%' L='%' H='%' simulation_time is_debug repeats(optionally)'\n")			
			return False
		list_args = [x.split("=") for x in args];
		if not self.validate_parameters_order([x[0] for x in list_args]):
			print("\nInput parameters must be: 'filename step='%' lambda='%' mu='%' C='%' c0='%'",
			 	  "Q='%' theta='%' L='%' H='%' simulation_time is_debug repeats(optionally)'\n")
			return False

		for i in [2, 5, 11, 12, len(args)-1]:
			[has_range, validation_result] = self.validate_single( args[i].split("=") )
			if not validation_result:
				print("Wrong parameter format: ", args[i].split("="))
			if not has_range:
				print("Wron single parameter. Found: ", args[i].split("-"))

		for i in [3, 4, 6, 7, 8, 9, 10]:
			[has_range, validation_result] = self.validate_range( args[i].split("=") )
			if has_range:
				range_parameters_count += 1
			if not validation_result: 
				print("Wrong: ", args[i].split("="))

		if not validation_result: 
			print("\nValidation failed!")
			return False
		if range_parameters_count > 1:
			print("\nThere is more then 1 range parameter!")
			return False
		if range_parameters_count < 1:
			print("\nOne of the following parameters = {lambda, mu, c0, Q, theta, L, H} must be inputed as range in format: parameter='%'-'%'")
			return False
		return True

	def validate_parameters_order(self, args):
		"""
			Validate input parameter names
			filename step=% lambda=% mu=% C=% c0=% Q=% theta=% L=% H=% simulation_time=% is_debug=% repeats(optionally)=%
		"""
		is_valid = True
		if self.get_name(args[2]) != "step": 
			print("2nd parameter must be step")
			is_valid = False
		if self.get_name(args[3]) != "lambda": 
			print("3ndrd parameter must be lambda")
			is_valid = False
		if self.get_name(args[4]) != "mu": 
			print("4th parameter must be mu")
			is_valid = False	
		if self.get_name(args[5]) != "C": 
			print("5th parameter must be C")
			is_valid = False
		if self.get_name(args[6]) != "c0": 
			print("6th parameter must be c0")
			is_valid = False
		if self.get_name(args[7]) != "Q": 
			print("7th parameter must be Q")
			is_valid = False
		if self.get_name(args[8]) != "theta": 
			print("8th parameter must be theta")
			is_valid = False			
		if self.get_name(args[9]) != "L": 
			print("9th parameter must be L")
			is_valid = False
		if self.get_name(args[10]) != "H": 
			print("10th parameter must be H")
			is_valid = False
		if self.get_name(args[11]) != "simulation_time":
			print("11th parameter must be simulation_time") 
			is_valid = False
		if self.get_name(args[12]) != "is_debug": 
			print("11th parameter must be is_debug")
			is_valid = False
		if len(args) == 13:
			if self.get_name(args[13]) != "repeats": 
				print("12th parameter must be is_debug")
				is_valid = False	
		return is_valid	

	def get_name(self, str):
		"""
			Return name of inputed tuple
		"""
		l = str.split("=")
		if len(l) != 1: return ""
		return l[0]