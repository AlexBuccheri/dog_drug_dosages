from typing import Optional

import streamlit as st
import yaml


def volume_dose(database, name: str, weight: float, dose: Optional[float] = None) -> float:
    """ Return the total volume of a drug dosage to administer, given the weight of the dog and
    the drug concentration, and dose per kg.

    :param database: Dict of default drug doses and concentrations
    :param name: Drug name
    :param weight: Dog weight (kg)
    :param dose: Optional drug dose (mg/kg). If not passed, the default is used.
    :return: Drug dosage volume, in ml
    """
    if name not in database.keys():
        raise ValueError(f'Drug {name} is not currently in the database')

    if not dose:
        dose = database[name]['dose']
        st.write(f'Using the default dose for {name} of {dose} (ml/kg)')

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
        dose[name] = st.number_input(f"Enter the dose (ml per kg) for {name}."
                                     f"If no value is entered, the default is used:", min_value=0.0, step=0.1, key=name)

    if st.button("Calculate"):
        for name in selected_drugs:
            result = volume_dose(drug_database, name, weight_kg, dose[name])
            st.write(f'Administer {result} (ml) for {name}')


if __name__ == "__main__":
    main()
