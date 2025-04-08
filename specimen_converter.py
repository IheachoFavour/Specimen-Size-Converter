def convert_size(size, from_unit, to_unit, magnification=1):
    # Conversion factors to millimeters (mm)
    conversion_factors = {
        'mm': 1,
        'cm': 10,
        'm': 1000,
        'inches': 25.4,
        'feet': 304.8,
        'um': 0.001  # Micrometers to mm
    }
    
    # Check for valid units
    if from_unit not in conversion_factors or to_unit not in conversion_factors:
        return "Invalid unit provided."
    
    # Convert the size to millimeters
    size_in_mm = size * conversion_factors[from_unit]
    
    # Apply magnification as a divisor
    magnified_size_in_mm = size_in_mm / magnification
    
    # Convert the magnified size from mm to the desired unit
    converted_size = magnified_size_in_mm / conversion_factors[to_unit]
    
    return converted_size

def main():
    print("Welcome to the Specimen Size Converter!")
    
    # Input size
    size = float(input("Enter the size of the specimen: "))
    
    # Input units
    from_unit = input("Enter the current unit (mm, cm, m, inches, feet, um): ").lower()
    to_unit = input("Enter the unit to convert to (mm, cm, m, inches, feet, um): ").lower()
    
    # Input magnification
    magnification = input("Enter magnification factor (default is 1 if none): ")
    magnification = float(magnification) if magnification else 1
    
    # Perform conversion
    converted_size = convert_size(size, from_unit, to_unit, magnification)
    
    # Output result
    print(f"The converted size is: {converted_size:.2f} {to_unit}")

if __name__ == "__main__":
    main()