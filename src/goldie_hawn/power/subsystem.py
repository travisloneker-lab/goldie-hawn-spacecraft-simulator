class PowerSubsystem:
    """Simulated spacecraft power subsystem."""

    def __init__(
        self,
        battery_capacity_wh: float = 1000.0,
        battery_energy_wh: float = 800.0,
        power_consumption_w: float = 100.0,
        solar_generation_w: float = 200.0,
    ) -> None:
        """Initialize the power subsystem with the specified configuration."""
        self.battery_capacity_wh = battery_capacity_wh
        self.battery_energy_wh = battery_energy_wh
        self.battery_percent = (self.battery_energy_wh / self.battery_capacity_wh) * 100.0
        self.current_a = 5.0
        self.power_consumption_w = power_consumption_w
        self.solar_generation_w = solar_generation_w
        self.voltage_v = 28.0

    def update(self, dt_seconds: float) -> None:
        """Update the power subsystem state over the given time interval."""
        net_power_w = self.solar_generation_w - self.power_consumption_w
        energy_change_wh = (net_power_w * dt_seconds) / 3600.0
        self.battery_energy_wh = max(0.0, min(self.battery_capacity_wh, self.battery_energy_wh + energy_change_wh))
        self.battery_percent = (self.battery_energy_wh / self.battery_capacity_wh) * 100.0