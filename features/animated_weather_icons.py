import time

class AnimatedWeatherIcon:
    def __init__(self, label_widget):
        # Store the label where we'll show the animated icon
        self.label = label_widget
        # Keep track of whether animation is running
        self.animation_active = False
        # Store the timer job so we can cancel it later
        self.animation_job = None
        # Remember what weather type we're animating
        self.current_weather = None
        # Count which frame of animation we're on
        self.animation_frame = 0
        
    def start_animation(self, weather_main):
        # Begin animating for this weather type
        self.current_weather = weather_main
        self.animation_active = True
        self.animation_frame = 0
        self._animate()
    
    def stop_animation(self):
        # Turn off the animation
        self.animation_active = False
        if self.animation_job:
            self.label.after_cancel(self.animation_job)
            self.animation_job = None
    
    def _animate(self):
        # This runs over and over to create the animation
        if not self.animation_active:
            return
            
        # Figure out what icon to show right now
        icon = self._get_animated_frame()
        self.label.config(text=icon)
        
        # Move to the next frame
        self.animation_frame += 1
        
        # Set up the next frame to happen later
        delay = self._get_animation_delay()
        self.animation_job = self.label.after(delay, self._animate)
    
    def _get_animated_frame(self):
        # Pick which animation to run based on weather type
        weather = self.current_weather.lower()
        
        if weather == 'clear':
            return self._animate_sun()
        elif weather == 'clouds':
            return self._animate_clouds()
        elif weather == 'rain':
            return self._animate_rain()
        elif weather == 'drizzle':
            return self._animate_drizzle()
        elif weather == 'thunderstorm':
            return self._animate_thunderstorm()
        elif weather == 'snow':
            return self._animate_snow()
        elif weather in ['mist', 'fog', 'haze']:
            return self._animate_fog()
        else:
            return '🌤️'  # Just show this if we don't know the weather
    
    def _animate_sun(self):
        # Make the sun pulse bigger and smaller
        cycle = self.animation_frame % 20
        if cycle < 10:
            # Sun is growing
            intensity = cycle / 9.0
            if intensity < 0.3:
                return '☀️'
            elif intensity < 0.6:
                return '🌟'
            else:
                return '✨☀️✨'
        else:
            # Sun is shrinking
            intensity = (19 - cycle) / 9.0
            if intensity < 0.3:
                return '☀️'
            elif intensity < 0.6:
                return '🌟'
            else:
                return '✨☀️✨'
    
    def _animate_clouds(self):
        # Make clouds drift across the screen
        cycle = self.animation_frame % 12
        cloud_states = [
            '☁️    ',
            ' ☁️   ',
            '  ☁️  ',
            '   ☁️ ',
            '    ☁️',
            '   ☁️ ',
            '  ☁️  ',
            ' ☁️   ',
            '☁️    ',
            '☁️☁️  ',
            ' ☁️☁️ ',
            '  ☁️☁️'
        ]
        return cloud_states[cycle]
    
    def _animate_rain(self):
        # Show rain falling down
        cycle = self.animation_frame % 8
        rain_states = [
            '🌧️',
            '☔',
            '🌧️💧',
            '☔💧',
            '🌧️',
            '💧🌧️',
            '☔',
            '💧☔'
        ]
        return rain_states[cycle]
    
    def _animate_drizzle(self):
        # Light rain animation
        cycle = self.animation_frame % 6
        drizzle_states = [
            '🌦️',
            '🌦️💧',
            '🌦️',
            '🌦️ ',
            '🌦️💧',
            '🌦️'
        ]
        return drizzle_states[cycle]
    
    def _animate_thunderstorm(self):
        # Show lightning flashes randomly
        cycle = self.animation_frame % 16
        if cycle < 12:
            return '⛈️'
        elif cycle == 12:
            return '⚡⛈️⚡'
        elif cycle == 13:
            return '⛈️'
        elif cycle == 14:
            return '⚡⛈️'
        else:
            return '⛈️'
    
    def _animate_snow(self):
        # Show snowflakes falling
        cycle = self.animation_frame % 10
        snow_states = [
            '🌨️',
            '❄️🌨️',
            '🌨️❄️',
            '❄️🌨️❄️',
            '🌨️',
            '🌨️❄️',
            '❄️🌨️',
            '🌨️❄️🌨️',
            '❄️🌨️',
            '🌨️'
        ]
        return snow_states[cycle]
    
    def _animate_fog(self):
        # Show fog drifting slowly
        cycle = self.animation_frame % 8
        fog_states = [
            '🌫️',
            '🌫️ ',
            ' 🌫️',
            '  🌫️',
            ' 🌫️ ',
            '🌫️  ',
            ' 🌫️',
            '🌫️'
        ]
        return fog_states[cycle]
    
    def _get_animation_delay(self):
        # How fast should each weather type animate?
        weather = self.current_weather.lower()
        
        if weather == 'clear':
            return 150  # Sun pulses slowly
        elif weather == 'clouds':
            return 300  # Clouds drift slowly
        elif weather == 'rain':
            return 200  # Rain falls at medium speed
        elif weather == 'drizzle':
            return 250  # Light rain is a bit slower
        elif weather == 'thunderstorm':
            return 100  # Lightning flashes quickly
        elif weather == 'snow':
            return 400  # Snow falls slowly
        elif weather in ['mist', 'fog', 'haze']:
            return 350  # Fog drifts very slowly
        else:
            return 200  # Default speed


# Simple function to get regular (non-animated) weather icons
def get_weather_icon(weather_main):
    # Just returns one emoji for each weather type
    icons = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '🌨️',
        'Mist': '🌫️',
        'Fog': '🌫️',
        'Haze': '🌫️'
    }
    return icons.get(weather_main, '🌤️')


def get_animated_weather_icon(label_widget, weather_main):
    # Easy way to create and start an animated icon
    animator = AnimatedWeatherIcon(label_widget)
    animator.start_animation(weather_main)
    return animator