import numpy as np

def calculate_pile_capacity(layer_number, table_data, diameter_pile, factor_of_safety, k_value):
    cumulative_Qs = 0
    results = []

    radius_pile = diameter_pile / 2
    A_b = np.pi * (radius_pile) ** 2  # Base area of the pile

    for i in range(layer_number):
        soil_type = table_data[i, 0]
        current_depth = float(table_data[i, 1])
        previous_depth = float(table_data[i - 1, 1]) if i > 0 else 0
        layer_depth = current_depth - previous_depth  # Calculate layer depth

        field_spt = float(table_data[i, 2])

        # Correct the SPT N value
        if field_spt > 15:
            N_corrected = 15 + 0.5 * (field_spt - 15)
        else:
            N_corrected = field_spt

        # Calculate cohesion from corrected N value using the user-defined k_value
        cohesion = k_value * N_corrected  # in kPa

        # Convert cohesion from kPa to ton/ft² using the multiplier 0.0093
        cohesion_ton_ft2 = cohesion * 0.0093  # 1 kPa = 0.0093 ton/ft²

        # Calculate skin friction and end bearing based on soil type
        if soil_type.lower() == "cohesionless":
            fsu = 4 * N_corrected / 200  # in ton/ft²
            qpu = 4 * N_corrected  # in ton/ft²
        elif soil_type.lower() == "cohesive":
            alpha = 0.55  # Example value, adjust as needed
            fsu = alpha * cohesion_ton_ft2  # in ton/ft²
            qpu = 9 * cohesion_ton_ft2  # in ton/ft²
        else:
            raise ValueError("Invalid soil type. Please enter 'Cohesionless' or 'Cohesive'.")

        # Convert fsu and qpu from ton/ft² to kN/m²
        fsu_kN_m2 = fsu * 95.76  # 1 ton/ft² = 95.76 kN/m²
        qpu_kN_m2 = qpu * 95.76  # 1 ton/ft² = 95.76 kN/m²

        A_s = np.pi * diameter_pile * layer_depth  # Surface area of the pile shaft
        Q_s = A_s * fsu_kN_m2  # Skin friction capacity for the layer
        cumulative_Qs += Q_s  # Cumulative skin friction capacity

        Q_b = A_b * qpu_kN_m2  # End bearing capacity for the layer

        # Ultimate bearing capacity (Qu) for this layer
        Q_u = Q_b + cumulative_Qs  # Correct calculation for Qu

        # Allowable capacity (Qa)
        Q_a = Q_u / factor_of_safety

        results.append([current_depth, Q_s, Q_b, Q_a])

    return results