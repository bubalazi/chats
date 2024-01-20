#!/usr/bin/env python

import argparse

def calculate_biogas_storage(volume, pressure, compressor_efficiency, ambient_temperature):
    # Constants
    molar_mass_methane = 16  # g/mol for CH4
    molar_mass_co2 = 44  # g/mol for CO2
    proportion_methane = 0.60  # 60% of biogas
    proportion_co2 = 0.40  # remaining significant component
    average_molar_mass_biogas = (molar_mass_methane * proportion_methane) + (molar_mass_co2 * proportion_co2)
    R = 0.08314  # L·bar/K·mol (Universal gas constant)
    energy_content_methane_MJ_per_m3 = 35.8  # MJ/m³ at STP for methane
    MJ_to_kWh = 0.277778  # conversion factor from MJ to kWh
    
    # Energy content of biogas per cubic meter at STP
    energy_content_biogas_MJ_per_m3 = energy_content_methane_MJ_per_m3 * proportion_methane

    # Calculating the number of moles in the cylinder
    number_of_moles = (volume * pressure) / (R * ambient_temperature)

    # Total energy content in kWh
    volume_at_STP_m3 = number_of_moles * R * ambient_temperature / 1  # 1 bar
    total_energy_kWh = (energy_content_biogas_MJ_per_m3 * volume_at_STP_m3) * MJ_to_kWh

    # Energy required to compress the gas (considering efficiency)
    work_done_kWh = total_energy_kWh * (pressure - 1) / compressor_efficiency

    # Losses due to compression
    losses_kWh = work_done_kWh - total_energy_kWh

    return total_energy_kWh, work_done_kWh, losses_kWh

def main():
    parser = argparse.ArgumentParser(description="Calculate biogas storage and compression details.")
    parser.add_argument("volume", type=float, help="Volume of the cylinder in liters")
    parser.add_argument("pressure", type=float, help="Final pressure in the cylinder in bar")
    parser.add_argument("--compressor_efficiency", type=float, default=1.0, help="Efficiency of the compressor")
    parser.add_argument("--ambient_temperature", type=float, default=293, help="Ambient temperature in Kelvin")
    
    args = parser.parse_args()

    total_energy, energy_used, losses = calculate_biogas_storage(args.volume, args.pressure, args.compressor_efficiency, args.ambient_temperature)

    # Printing results in a tabular format
    print("\nReport for Biogas Storage:")
    header = ["Parameter", "Value", "Unit"]
    data = [
        ["Volume of Cylinder", f"{args.volume}", "liters"],
        ["Final Pressure", f"{args.pressure}", "bar"],
        ["Compressor Efficiency", f"{args.compressor_efficiency}", ""],
        ["Ambient Temperature", f"{args.ambient_temperature}", "K"],
        ["Total Energy Stored", f"{total_energy:.2f}", "kWh"],
        ["Energy Used to Compress", f"{energy_used:.2f}", "kWh"],
        ["Losses due to Compression", f"{losses:.2f}", "kWh"]
    ]

    # Print the header
    print(f"{header[0]:<25} {header[1]:<15} {header[2]:<5}")
    print("-" * 45)

    # Print each data row
    for row in data:
        print(f"{row[0]:<25} {row[1]:<15} {row[2]:<5}")

if __name__ == "__main__":
    main()

