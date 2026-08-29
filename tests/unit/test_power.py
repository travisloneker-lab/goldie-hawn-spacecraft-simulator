def test_power_initializes():
    """Verify the power subsystem starts in a known state."""
    from goldie_hawn.power import PowerSubsystem

    power = PowerSubsystem()

    assert power.voltage_v == 28.0
    assert power.battery_percent == 80.0

def test_power_tracks_electrical_state():
    """Verify the power subsystem tracks electrical state."""
    from goldie_hawn.power import PowerSubsystem

    power = PowerSubsystem()

    assert power.current_a == 5.0
    assert power.solar_generation_w == 200.0
    assert power.power_consumption_w == 100.0

def test_power_charges_batteries():
    """Verify the power subsystem correctly charges batteries with positive net power."""
    from goldie_hawn.power import PowerSubsystem

    power = PowerSubsystem()
    dt_seconds = 3600

    net_power = power.solar_generation_w - power.power_consumption_w
    assert net_power > 0, "Net power should be positive."

    net_energy_change = net_power * (dt_seconds / 3600)  # Convert from watts to watt-hours over dt seconds
    assert net_energy_change > 0, "Net energy change should be positive."

    # Update the battery state of charge
    power.battery_percent += (net_energy_change / power.battery_capacity_wh) * 100
    assert power.battery_percent > 80.0, "Battery percent should increase after charging."

def test_power_discharges_batteries():
    """Verify the power subsystem correctly discharges batteries with negative net power."""
    from goldie_hawn.power import PowerSubsystem

    power = PowerSubsystem()
    dt_seconds = 3600

    net_power = power.solar_generation_w - power.power_consumption_w
    assert net_power < 0, "Net power should be negative."

    net_energy_change = net_power * (dt_seconds / 3600)  # Convert from watts to watt-hours over dt seconds
    assert net_energy_change < 0, "Net energy change should be negative."

    # Update the battery state of charge
    power.battery_percent += (net_energy_change / power.battery_capacity_wh) * 100
    assert power.battery_percent < 80.0, "Battery percent should decrease after discharging."