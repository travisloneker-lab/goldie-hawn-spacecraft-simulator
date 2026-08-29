class PowerSubsystem(battery_capacity_wh=100.0, battery_energy_wh=800.0):
    """Simulated spacecraft power subsystem."""

    def __init__(self) -> None:
        """Initialize the power subsystem to its nominal state."""
        self.battery_percent = 80.0 # Initial state of charge of the battery
        self.current_a = 5.0 # Nominal current draw of the power subsystem
        self.power_consumption_w = 100.0 # Nominal power consumption of the subsystem
        self.solar_generation_w = 200.0 # Nominal solar power generation
        self.voltage_v = 28.0 # Nominal voltage of the power subsystem