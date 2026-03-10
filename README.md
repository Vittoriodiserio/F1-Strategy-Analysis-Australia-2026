F1 Strategic Intelligence: Race Strategy Optimization – Australian GP 2026
This project analyses the strategic dynamics of the 2026 Australian Grand Prix, focusing on the management of Charles Leclerc's (Scuderia Ferrari) #16 car in response to the Virtual Safety Car (VSC) on lap 11.
Project Abstract
The analysis shows how a conservative decision by the Ferrari pit wall turned a leading position into a strategic debt of 18.4 seconds. Through the processing of telemetry data, the project isolates real tyre degradation and proposes an "Optimal Strategy" simulation that would have guaranteed victory by a margin of 5.52 seconds.
Key Findings
•	VSC Strategic Debt: Failure to stop below VSC generated an immediate loss of 10.7s of "VSC Gain".
•	Performance Gap: The extension of the stint on Medium C4 exposed the driver to a negative Pace Delta of 0.601s/lap compared to the competition on Hard C3.
•	Tyre Management: Although Leclerc's degradation coefficient was excellent (+0.0225 s/lap), exceeding the performance crossover point made defending the position impossible.
Technical Methodology
The analysis workflow was divided into four main phases:
•	Data Cleaning: Removal of performance outliers above the 107% threshold (VSC, pit lane, traffic) to isolate pure race pace.
•	Linear Regression: Use of NumPy algorithms to determine pneumatic degradation coefficients.
•	Simulation Engine: Development of a simulator in Python to recalculate the race history based on the adoption of the Hard compound on lap 11.
•	Visualization: Professional rendering of time gaps and degradation curves using Matplotlib.
How to perform the analysis
Prerequisites
Make sure you have Python and the necessary libraries installed:
PIP -R requirements.txt Installation
Execution
Launch the main file to generate the analysis and simulation graphs:
Python main.py
