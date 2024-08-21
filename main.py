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

    selected_drugs = st.multiselect("Select the drugs:", list(drug_database.keys()))
    weight_kg = st.number_input("Enter the animal weight (kg):", min_value=0.0, step=0.1)

    dose = {}
    for name in selected_drugs:
        dose[name] = st.number_input(f"Enter the dose (ml per kg) for {name}. "
                                     "If no value is entered, the default is used:", min_value=0.0, step=0.1, key=name)

    df_contents = []
    if st.button("Calculate"):
        for name in selected_drugs:

            if dose[name] < 1.e-8:
                dose[name] = drug_database[name]['dose']
                st.write(f'Using the default dose for {name} of {dose[name]} (ml/kg)')

            vol = volume_dose(drug_database, name, weight_kg, dose[name])
            # st.write(f'Administer {vol} (ml) for {name}')

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
