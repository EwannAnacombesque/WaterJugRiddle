class bottleState():
	def __init__(self,state,action,previous_path,previous_action_path):
		self.state = state
		self.state_path = [*previous_path,state]
		self.action_path = [*previous_action_path,action] if action else []

class bottleSolver():
	def __init__(self,bottles_restrictions):
		self.bottles_restrictions = bottles_restrictions
		self.bottles_amount = len(self.bottles_restrictions)
	
	def set_up(self,initial_state):
		self.initial_state = bottleState(initial_state,"",[],[])
		
		assert len(initial_state) == len(self.bottles_restrictions), "Restrictions and initial state must have the same size"
		assert not sum([initial_state[i]>self.bottles_restrictions[i] for i in range(self.bottles_amount)]), "Initial state violate restrictions"
		
		self.visited_states = set()
		self.states_queue = [self.initial_state]

	def get_actions(self,head_state):
		
		bottles_indices = range(self.bottles_amount)
		state = head_state.state
		
		# Get each pourer possible
		for pourer_index in bottles_indices:
			# Get each container possible
			for container_index in [i for i in bottles_indices if i!=pourer_index]:
				
				# Verify if pourer isn't empty	
				if not state[pourer_index]:
					continue
				
				# Pour the pourer bottle into the container, make sure it doesn't overflow
				new_container_state = min(state[container_index]+state[pourer_index],self.bottles_restrictions[container_index])
				
				# Get the remaining quantity in the pourer 
				new_pourer_state = state[pourer_index] + state[container_index] - new_container_state

				new_state = [state[i] for i in bottles_indices]
				# Change pourer and container state 
				new_state[pourer_index] = new_pourer_state 
				new_state[container_index] = new_container_state

				# Don't check a state that is actually already checked
				if str(new_state) in self.visited_states:
					continue 
				
				self.visited_states.add(str(new_state))
				
				# Add the new state to the queue
				self.states_queue.append(bottleState(new_state,
													f"{pourer_index} → {container_index}", # action that has been done
													head_state.state_path, 
													head_state.action_path)) 

	def solve(self,initial_state,searched_quantity,permutable=False):
		self.set_up(initial_state)
		
		# Case disjunction in function of what is searched 
	
		if type(searched_quantity) == type(5):
			# Only searching for a quantity  
			searching = "single_quantity"
		else:
			# Searching for a specific state / permutation of it 
			searching = "list_quantity"
			
			if permutable:
				searched_quantity.sort()
			
			assert sum(searched_quantity) == sum(self.initial_state.state), "Can't obtain less or more than initial state total quantity"		

		# Breadth-first search
		while self.states_queue:
			head_state = self.states_queue.pop(0)

			# Verify the head of the queue
			if searching == "single_quantity":
				if searched_quantity in head_state.state:
					return True,head_state
			if searching == "list_quantity":
				verification_state = sorted(head_state.state) if permutable else head_state.state
				if searched_quantity == verification_state:
					return True, head_state	


			self.get_actions(head_state)

		return False,None
			
solver_example = bottleSolver(bottles_restrictions=[8,5,3])

# Illustration #

success,solution = solver_example.solve(initial_state=[8,0,0],searched_quantity=[7,1,0],permutable=True)
if success:
	print(solution.state_path)
	print(solution.action_path)
	print(f"State found : {solution.state}")
else:
	print(solver_example.visited_states)
	
success,solution = solver_example.solve(initial_state=[8,0,0],searched_quantity=4)
print(solution.state_path)
print(solution.action_path)
print(f"State found : {solution.state}")