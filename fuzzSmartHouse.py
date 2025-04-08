!pip install numpy scikit-fuzzy matplotlib

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import datetime

class SmartHomeLightingSystem:
    def __init__(self):
        # Define input and output variables
        self.time_of_day = ctrl.Antecedent(np.arange(0, 24, 0.1), 'time_of_day')
        self.occupancy = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'occupancy')
        self.lighting = ctrl.Consequent(np.arange(0, 101, 1), 'lighting')
        
        # Define membership functions for time of day
        self.time_of_day['morning'] = fuzz.trapmf(self.time_of_day.universe, [6, 8, 10, 12])
        self.time_of_day['afternoon'] = fuzz.trapmf(self.time_of_day.universe, [12, 13, 16, 18])
        self.time_of_day['evening'] = fuzz.trapmf(self.time_of_day.universe, [18, 19, 20, 21])
        self.time_of_day['night'] = fuzz.trapmf(self.time_of_day.universe, [21, 22, 5, 6])
        
        # Define membership functions for occupancy
        self.occupancy['unoccupied'] = fuzz.trimf(self.occupancy.universe, [0, 0, 0.5])
        self.occupancy['occupied'] = fuzz.trimf(self.occupancy.universe, [0.5, 1, 1])
        
        # Define membership functions for lighting intensity
        self.lighting['off'] = fuzz.trimf(self.lighting.universe, [0, 0, 25])
        self.lighting['low'] = fuzz.trimf(self.lighting.universe, [0, 25, 50])
        self.lighting['medium'] = fuzz.trimf(self.lighting.universe, [25, 50, 75])
        self.lighting['high'] = fuzz.trimf(self.lighting.universe, [50, 100, 100])
        
        # Define fuzzy rules
        self.rules = []
        self.setup_default_rules()
        
        # Create fuzzy control system
        self.lighting_ctrl = ctrl.ControlSystem(self.rules)
        self.lighting_simulation = ctrl.ControlSystemSimulation(self.lighting_ctrl)
        
        # User preferences dictionary (can be modified by users)
        self.user_preferences = {
            'morning': 'medium',
            'afternoon': 'low',
            'evening': 'high',
            'night': 'off'
        }
    
    def setup_default_rules(self):
        # Default rules based on requirements
        rule1 = ctrl.Rule(self.time_of_day['morning'] & self.occupancy['occupied'], 
                         self.lighting['medium'])
        rule2 = ctrl.Rule(self.time_of_day['afternoon'] & self.occupancy['occupied'], 
                         self.lighting['low'])
        rule3 = ctrl.Rule(self.time_of_day['evening'] & self.occupancy['occupied'], 
                         self.lighting['high'])
        rule4 = ctrl.Rule(self.time_of_day['night'] & self.occupancy['occupied'], 
                         self.lighting['low'])
        rule5 = ctrl.Rule(self.occupancy['unoccupied'], self.lighting['off'])
        
        self.rules = [rule1, rule2, rule3, rule4, rule5]
    
    def update_rules_from_preferences(self):
        # Clear existing rules
        self.rules = []
        
        # Create rules based on user preferences
        if self.user_preferences['morning'] == 'medium':
            self.rules.append(ctrl.Rule(self.time_of_day['morning'] & self.occupancy['occupied'], 
                                      self.lighting['medium']))
        elif self.user_preferences['morning'] == 'low':
            self.rules.append(ctrl.Rule(self.time_of_day['morning'] & self.occupancy['occupied'], 
                                      self.lighting['low']))
        elif self.user_preferences['morning'] == 'high':
            self.rules.append(ctrl.Rule(self.time_of_day['morning'] & self.occupancy['occupied'], 
                                      self.lighting['high']))
        
        if self.user_preferences['afternoon'] == 'medium':
            self.rules.append(ctrl.Rule(self.time_of_day['afternoon'] & self.occupancy['occupied'], 
                                      self.lighting['medium']))
        elif self.user_preferences['afternoon'] == 'low':
            self.rules.append(ctrl.Rule(self.time_of_day['afternoon'] & self.occupancy['occupied'], 
                                      self.lighting['low']))
        elif self.user_preferences['afternoon'] == 'high':
            self.rules.append(ctrl.Rule(self.time_of_day['afternoon'] & self.occupancy['occupied'], 
                                      self.lighting['high']))
        
        if self.user_preferences['evening'] == 'medium':
            self.rules.append(ctrl.Rule(self.time_of_day['evening'] & self.occupancy['occupied'], 
                                      self.lighting['medium']))
        elif self.user_preferences['evening'] == 'low':
            self.rules.append(ctrl.Rule(self.time_of_day['evening'] & self.occupancy['occupied'], 
                                      self.lighting['low']))
        elif self.user_preferences['evening'] == 'high':
            self.rules.append(ctrl.Rule(self.time_of_day['evening'] & self.occupancy['occupied'], 
                                      self.lighting['high']))
        
        if self.user_preferences['night'] == 'medium':
            self.rules.append(ctrl.Rule(self.time_of_day['night'] & self.occupancy['occupied'], 
                                      self.lighting['medium']))
        elif self.user_preferences['night'] == 'low':
            self.rules.append(ctrl.Rule(self.time_of_day['night'] & self.occupancy['occupied'], 
                                      self.lighting['low']))
        elif self.user_preferences['night'] == 'high':
            self.rules.append(ctrl.Rule(self.time_of_day['night'] & self.occupancy['occupied'], 
                                      self.lighting['high']))
        elif self.user_preferences['night'] == 'off':
            self.rules.append(ctrl.Rule(self.time_of_day['night'] & self.occupancy['occupied'], 
                                      self.lighting['off']))
        
        # Always turn off lights when room is unoccupied
        self.rules.append(ctrl.Rule(self.occupancy['unoccupied'], self.lighting['off']))
        
        # Update the control system with new rules
        self.lighting_ctrl = ctrl.ControlSystem(self.rules)
        self.lighting_simulation = ctrl.ControlSystemSimulation(self.lighting_ctrl)
    
    def set_user_preference(self, time_period, lighting_level):
        """
        Set user preference for a specific time period
        time_period: 'morning', 'afternoon', 'evening', 'night'
        lighting_level: 'off', 'low', 'medium', 'high'
        """
        if time_period not in ['morning', 'afternoon', 'evening', 'night']:
            raise ValueError("Time period must be morning, afternoon, evening, or night")
        
        if lighting_level not in ['off', 'low', 'medium', 'high']:
            raise ValueError("Lighting level must be off, low, medium, or high")
        
        self.user_preferences[time_period] = lighting_level
        self.update_rules_from_preferences()
    
    def get_time_period(self, hour):
        """Determine the time period based on the hour (0-23)"""
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 21:
            return 'evening'
        else:
            return 'night'
    
    def adjust_lighting(self, hour, is_occupied):
        """
        Adjust lighting based on time and occupancy
        hour: int (0-23)
        is_occupied: bool
        """
        try:
            # Handle possible sensor errors
            if not isinstance(hour, (int, float)) or hour < 0 or hour >= 24:
                raise ValueError(f"Invalid hour: {hour}. Must be between 0 and 23.")
            
            # Convert boolean to fuzzy value
            occupancy_value = 1 if is_occupied else 0
            
            # Set inputs
            self.lighting_simulation.input['time_of_day'] = hour
            self.lighting_simulation.input['occupancy'] = occupancy_value
            
            # Compute result
            self.lighting_simulation.compute()
            
            # Get the defuzzified value
            lighting_intensity = self.lighting_simulation.output['lighting']
            
            # Map numerical result to linguistic terms for reporting
            if lighting_intensity < 20:
                linguistic_result = "Off"
            elif lighting_intensity < 40:
                linguistic_result = "Low"
            elif lighting_intensity < 70:
                linguistic_result = "Medium"
            else:
                linguistic_result = "High"
            
            return {
                'numeric_value': lighting_intensity,
                'linguistic_value': linguistic_result,
                'time_period': self.get_time_period(hour),
                'occupancy': "Occupied" if is_occupied else "Unoccupied"
            }
            
        except Exception as e:
            print(f"Error adjusting lighting: {e}")
            # Return a safe default in case of errors
            return {
                'numeric_value': 0,
                'linguistic_value': "Off",
                'time_period': "unknown",
                'occupancy': "unknown",
                'error': str(e)
            }
    
    def visualize_membership_functions(self):
        """Visualize the fuzzy membership functions"""
        # Time of day membership functions
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 10))
        
        self.time_of_day.view(ax=ax0)
        ax0.set_title('Time of Day')
        ax0.legend()
        
        self.occupancy.view(ax=ax1)
        ax1.set_title('Occupancy')
        ax1.legend()
        
        self.lighting.view(ax=ax2)
        ax2.set_title('Lighting Intensity')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()


# Example usage
if __name__ == "__main__":
    # Create an instance of the smart home lighting system
    smart_lighting = SmartHomeLightingSystem()
    
    # Test the system with the example data
    test_data = [
        {'time': 7, 'occupancy': 1},  # 7 AM, Occupied
        {'time': 13, 'occupancy': 0},  # 1 PM, Unoccupied
        {'time': 19, 'occupancy': 1},  # 7 PM, Occupied
        {'time': 23, 'occupancy': 0}   # 11 PM, Unoccupied
    ]
    
    print("=== Smart Home Lighting Control System ===")
    print("\nDefault user preferences:")
    for period, level in smart_lighting.user_preferences.items():
        print(f"  {period.capitalize()}: {level.capitalize()}")
    
    print("\nTesting with example data:")
    for data in test_data:
        result = smart_lighting.adjust_lighting(data['time'], data['occupancy'])
        print(f"\n  Time: {data['time']}:00 ({result['time_period'].capitalize()})")
        print(f"  Occupancy: {result['occupancy']}")
        print(f"  Lighting Level: {result['linguistic_value']} ({result['numeric_value']:.1f}%)")
    
    # Example of updating user preferences
    print("\n=== Updating User Preferences ===")
    smart_lighting.set_user_preference('night', 'low')
    print("Updated 'night' preference to 'low'")
    
    # Test with updated preferences
    night_result = smart_lighting.adjust_lighting(23, 1)  # 11 PM, Occupied
    print(f"\n  Time: 23:00 ({night_result['time_period'].capitalize()})")
    print(f"  Occupancy: {night_result['occupancy']}")
    print(f"  Lighting Level: {night_result['linguistic_value']} ({night_result['numeric_value']:.1f}%)")