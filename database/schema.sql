-- Create the water_samples table
CREATE TABLE water_samples (
    sample_id SERIAL PRIMARY KEY,
    ph NUMERIC(8, 6),
    hardness NUMERIC(10, 4),
    solids NUMERIC(10, 4),
    chloramines NUMERIC(8, 6),
    sulfate NUMERIC(8, 4),
    conductivity NUMERIC(8, 4),
    organic_carbon NUMERIC(8, 6),
    trihalomethanes NUMERIC(8, 6),
    turbidity NUMERIC(8, 6)
);

-- Create the potability_results table
CREATE TABLE potability_results (
    result_id SERIAL PRIMARY KEY,
    sample_id INTEGER REFERENCES water_samples(sample_id),
    potability INTEGER
);