def plant_status(climate, temperatures):
    try:
        if not isinstance(climate, str):
         raise TypeError("Climate must be a string")
        if not isinstance(temperatures, list):
            raise TypeError("Temperatures should be a list")
        if not all(isinstance(temp, float) for temp in temperatures):
            raise TypeError("All temperatures should be float values")
  
        if climate == "Tropical":
            threshold = 30.0
        elif climate == "Continental":
            threshold = 25.0
        else:
            threshold = 18.0
    
        for temp in temperatures:
            if temp <= threshold:
                print("F")
            else:
                print("U")

    except TypeError as e:
        print("Error:", e)

climate = input("Enter climate: ")
temperatures = input("Enter temperatures as a list of float values: ")
plant_status(climate, temperatures)
