from pyfluids import Fluid, FluidsList

water_vapour = Fluid(FluidsList.Water).dew_point_at_pressure(101325)
print(water_vapour.specific_heat)  # 2079.937085633241
