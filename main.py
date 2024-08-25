from typing import Optional

import pandas as pd
import streamlit as st
import yaml

"""
Drug  Concentration (mg/ml)  
"""


def volume_dose(database, name: str, weight: float, dose: float) -> float:
    """ Return the total volume of a drug dosage to administer, given the weight of the dog and
    the drug concentration, and dose per kg.

    :param database: Dict of default drug doses and concentrations
    :param name: Drug name
    :param weight: Dog weight (kg)
    :param dose: Drug dose (mg/kg)
    :return: Drug dosage volume, in ml
    """
    if name not in database.keys():
        raise ValueError(f'Drug {name} is not currently in the database')

    total_dose = dose * weight
    return total_dose / database[name]['concentration']


# Streamlit app
def main():
    st.title("Drug Dose Calculator for Doggos")

    with open('database.yaml', 'r') as fid:
        drug_database = yaml.safe_load(fid)

    weight_kg = st.number_input("Enter the animal weight (kg):", min_value=0.0, step=0.1)
    selected_drugs = st.multiselect("Select the drugs:", list(drug_database.keys()))
    dose = {}

    # TODO. Need to prune drugs_with_dose_ranges, such that it's the intersection of drugs_with_dose_ranges and selected_drugs
    # But do not know how to do this, when selected_drugs is a streamlit object

    # Assign drugs with a dosage options
    drugs_with_dose_ranges = set()
    for name in drug_database.keys():
        if drug_database[name]['dose_options'] is not None:
            drugs_with_dose_ranges.add(name)

    for name in drugs_with_dose_ranges:
        min_val = min(drug_database[name]['dose_options'])
        max_val = max(drug_database[name]['dose_options'])
        # Note, this assumes that the value spacing is linear!
        dx = drug_database[name]['dose_options'][1] - drug_database[name]['dose_options'][0]
        dose[name] = st.number_input(f"Enter the dose (ml per kg) for {name}. "
                                     "If no value is entered, the default is used:",
                                     min_value=min_val,
                                     max_value=max_val,
                                     step=dx,
                                     key=name)

    # TODO. Need to prune drugs_with_fixed_dose, such that it's the intersection of drugs_with_fixed_dose and selected_drugs
    # But do not know how to do this, when selected_drugs is a streamlit object

    # Assign drugs with a fixed dose
    drugs_with_fixed_dose = {name for name in drug_database.keys()} - drugs_with_dose_ranges

    for name in drugs_with_fixed_dose:
        dose[name] = st.number_input(f"Enter the dose (ml per kg) for {name}. "
                                     "Default dosage supplied:",
                                     value=drug_database[name]['default_dose'],
                                     key=name)

    df_contents = []
    if st.button("Calculate"):
        for name in selected_drugs:

            # If no dose is specified by the user, use the default
            if dose[name] < 1.e-8:
                dose[name] = drug_database[name]['default_dose']
                st.write(f'Using the default dose for {name} of {dose[name]} (ml/kg)')

            # Exception for Atipam
            if name is 'Atipam':
                current_names = [entry['Drug'] for entry in df_contents]
                if not 'Medetomidine' in current_names:
                    raise ValueError('User must specify Medetomidine before Atipam')
                i = current_names.index('Medetomidine')
                vol = df_contents[i]['Volume to Give (ml)']
            else:
                vol = volume_dose(drug_database, name, weight_kg, dose[name])

            # Package for table view in ST
            df_contents.append(
                {'Drug': name,
                 'Concentration (mg/ml)': drug_database[name]['concentration'],
                 'Dose (mg/kg)': dose[name],
                 'Volume to Give (ml)': vol}
            )

        st.dataframe(pd.DataFrame(df_contents), use_container_width=True)


if __name__ == "__main__":
    main()
