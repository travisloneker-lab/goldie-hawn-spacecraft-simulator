import pytest

from goldie_hawn.power import PowerSubsystem


class TestPowerSubsystemInitialization:
    """Tests for the initial power subsystem state."""

    def test_power_initializes(self):
        """Verify the power subsystem starts in a known state."""
        power = PowerSubsystem()

        assert power.voltage_v == 28.0
        assert power.battery_percent == 80.0

    def test_power_tracks_electrical_state(self):
        """Verify the power subsystem tracks electrical state."""
        power = PowerSubsystem()

        assert power.current_a == 5.0
        assert power.solar_generation_w == 200.0
        assert power.power_consumption_w == 100.0


class TestPowerSubsystemUpdate:
    """Tests for battery-energy updates over a timestep."""

    def test_power_charges_battery(self):
        """Verify the battery charges when net power is positive."""
        power = PowerSubsystem(
            battery_capacity_wh=1000.0,
            battery_energy_wh=800.0,
            solar_generation_w=200.0,
            power_consumption_w=100.0,
        )

        power.update(dt_seconds=3600)

        assert power.battery_energy_wh == 900.0
        assert power.battery_percent == 90.0

    def test_power_discharges_battery(self):
        """Verify the battery discharges when net power is negative."""
        power = PowerSubsystem(
            battery_capacity_wh=1000.0,
            battery_energy_wh=800.0,
            solar_generation_w=50.0,
            power_consumption_w=150.0,
        )

        power.update(dt_seconds=3600)

        assert power.battery_energy_wh == 700.0
        assert power.battery_percent == 70.0

    def test_power_clamps_at_full_capacity(self):
        """Verify the battery cannot exceed its maximum capacity."""
        power = PowerSubsystem(
            battery_capacity_wh=1000.0,
            battery_energy_wh=950.0,
            solar_generation_w=500.0,
            power_consumption_w=100.0,
        )

        power.update(dt_seconds=3600)

        assert power.battery_energy_wh == 1000.0
        assert power.battery_percent == 100.0

    def test_power_clamps_at_zero_capacity(self):
        """Verify the battery cannot discharge below zero."""
        power = PowerSubsystem(
            battery_capacity_wh=1000.0,
            battery_energy_wh=50.0,
            solar_generation_w=50.0,
            power_consumption_w=250.0,
        )

        power.update(dt_seconds=3600)

        assert power.battery_energy_wh == 0.0
        assert power.battery_percent == 0.0

    def test_power_zero_timestep_does_not_change_state(self):
        """Verify a zero timestep does not change battery state."""
        power = PowerSubsystem()

        initial_energy_wh = power.battery_energy_wh
        initial_percent = power.battery_percent

        power.update(dt_seconds=0)

        assert power.battery_energy_wh == initial_energy_wh
        assert power.battery_percent == initial_percent


class TestPowerSubsystemValidation:
    """Tests for invalid power subsystem inputs."""

    def test_power_rejects_zero_battery_capacity(self):
        """Verify the power subsystem rejects zero battery capacity."""
        with pytest.raises(
            ValueError,
            match="Battery capacity must be greater than zero.",
        ):
            PowerSubsystem(battery_capacity_wh=0.0)

    def test_power_rejects_negative_battery_capacity(self):
        """Verify the power subsystem rejects negative battery capacity."""
        with pytest.raises(
            ValueError,
            match="Battery capacity must be greater than zero.",
        ):
            PowerSubsystem(battery_capacity_wh=-100.0)

    def test_power_rejects_negative_battery_energy(self):
        """Verify the power subsystem rejects negative battery energy."""
        with pytest.raises(
            ValueError,
            match="Battery energy must be greater than or equal to zero.",
        ):
            PowerSubsystem(battery_energy_wh=-100.0)

    def test_power_rejects_battery_energy_above_capacity(self):
        """Verify the power subsystem rejects battery energy above capacity."""
        with pytest.raises(
            ValueError,
            match="Battery energy cannot exceed battery capacity.",
        ):
            PowerSubsystem(battery_capacity_wh=1000.0, battery_energy_wh=1200.0)

    def test_power_rejects_negative_solar_generation(self):
        """Verify the power subsystem rejects negative solar generation."""
        with pytest.raises(
            ValueError,
            match="Solar generation must be greater than or equal to zero.",
        ):
            PowerSubsystem(solar_generation_w=-100.0)

    def test_power_rejects_negative_power_consumption(self):
        """Verify the power subsystem rejects negative power consumption."""
        with pytest.raises(
            ValueError,
            match="Power consumption must be greater than or equal to zero.",
        ):
            PowerSubsystem(power_consumption_w=-100.0)

    def test_power_rejects_negative_timestep(self):
        """Verify the power subsystem rejects negative timestep."""
        power = PowerSubsystem()

        with pytest.raises(
            ValueError,
            match="Timestep must be greater than or equal to zero.",
        ):
            power.update(dt_seconds=-3600)
