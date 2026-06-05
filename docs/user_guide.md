# PerMix User Guide

Welcome to PerMix! PerMix is a graphical user interface (GUI) designed to standardize and accelerate the process of calculating precursor masses for perovskite synthesis. This guide provides a comprehensive overview of how to navigate the application and perform precise stoichiometric calculations.

---

## 1. Main Menu and Navigation

Upon launching PerMix, the main window opens, dedicated to the core calculation workflow. The top navigation bar features several key tabs:

* **Viewing:** Provides access to a set of Data Viewers that allow you to manage the local database. You can browse, add, or delete entries to tailor the software to your needs:
  * *Solvents:* Displays all the solvents and antisolvents currently available in the database, detailing properties like density and boiling point.
  * *Ion Radii:* Manages the database of chemical species and their physical properties, essential for calculating geometric stability factors.
  * *Phase Templates:* Allows you to manage structural blueprints, which define a crystal structure's stoichiometry and its constituent cation sites.
  * *Compositions:* A central hub for managing reference materials. It contains both a database of "Literature compositions" and your personal saved calculations under "My compositions" (Favorite compositions).
* **Language:** Toggles the interface language between English and Russian.
* **About Program:** Contains comprehensive information about the software's purpose, operational guidelines, and citation details.
* **Exit:** Closes the application.

---

## 2. Step-by-Step Calculation Workflow

The main interface is designed to guide you logically from top to bottom through the input panel.

### Step 1: Define the Crystal Structure and Composition
1. **Phase Template:** Choose a Phase Template from the dropdown menu to define the fundamental crystal structure (e.g., 3D ABX3 or 2D A2BX4). Click the **Submit** button to generate the corresponding input fields.
2. **Structure:** Define the precise chemical composition of your target material.
    * Select the number of components for each site (A, B, X).
    * Choose the specific ion and enter its molar fraction.
    * **Important:** The sum of fractions for all components on a single site must strictly equal **1.0**. The application features an auto-completion tool that automatically calculates the final fraction field to ensure this sum is met.

### Step 2: Define the Solution Properties
1. **Antisolvents:** If your method requires an antisolvent, check the "Presence of antisolvents" box. Click **Submit composition** to proceed.
2. **Solvents/Antisolvents Configuration:** Specify the number of liquid components, select their names, and define their volume fractions. The sum of all solvent fractions must equal **1.0**.
3. **Solution Parameters:** Enter the total intended **Solution Volume** (in mL) and the final **Solution Concentration** (Molarity, mol/L). If using an antisolvent, enter its total volume as well.

### Step 3: Apply K-Factors (Reagent Purity)
The "K-factors" section allows you to apply correction factors to account for real-world impurities or to intentionally introduce excess amounts of precursors. To compensate for a precursor that is not perfectly pure (e.g., 98% purity), input a multiplier greater than 1.0 (e.g., 1.02) to automatically increase the calculated mass and ensure exact stoichiometry.

---

## 3. Running Calculations and Analyzing Results

Once all inputs are configured, click the **Start Calculations** button. The high-precision engine (utilizing the `Decimal` data type and `periodictable` library to prevent rounding errors down to $10^{-6}\text{ g}$) will process the data and display the results in the right-hand output console.

### Output Features
* **Geometric Factors:** The application automatically calculates the Goldschmidt Tolerance Factor (t) and Octahedral Factor ($\mu$) to check the structural stability of your defined composition.
* **Calculated Equations:** Generates a list of all valid, balanced synthesis pathways based on your available precursor salts.
* **Mass Table:** Presents a detailed table with the precise precursor masses in grams required for each specific synthesis equation. You can retrieve a condensed overview of a specific reaction by using the **Get the equation summary** option.

### Sorting and Visualization
When multiple synthesis equations are generated, use the "Sorting Equations" frame to rank them. You can hierarchically sort the equations based on:

* Total combined mass.
* Number of required precursors.
* Mass of a specific precursor salt. 
The interface also renders a **mass histogram** to visually distribute and compare the required weights of the reagents.

### Saving Configurations
If you want to archive a successful setup, click the **Save the configuration** button located in the left-hand panel. After providing a name and optional description, the setup is saved locally and instantly accessible via **Viewing -> Viewing compositions -> My compositions**, where it can be loaded back at any time.