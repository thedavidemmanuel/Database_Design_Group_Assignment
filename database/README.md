# Water Quality Database Schema

This project defines a PostgreSQL database schema for storing water quality measurements and potability data.

## Schema Overview

The schema consists of two main tables:

### `WaterQuality`

This table stores various measurements related to water quality.

- `id`: Primary key for the water quality entry.
- `ph`: pH level of the water.
- `Hardness`: Hardness of the water.
- `Solids`: Amount of dissolved solids in the water.
- `Chloramines`: Chloramines content in the water.
- `Sulfate`: Sulfate content in the water.
- `Conductivity`: Conductivity of the water.
- `Organic_carbon`: Organic carbon content in the water.
- `Trihalomethanes`: Trihalomethanes content in the water.
- `Turbidity`: Turbidity level of the water.

### `WaterPotability`

This table stores the potability status associated with each water quality entry.

- `id`: Primary key for the potability entry.
- `water_quality_id`: Foreign key referencing the `id` column in the `WaterQuality` table.
- `Potability`: Indicates whether the water is potable (1) or not (0).

## Implementation Details

### Requirements

- PostgreSQL database server.
- pgAdmin or any PostgreSQL client tool for executing SQL scripts.

### Usage

1. **Setting Up the Database:**

   - Create a new PostgreSQL database named `water_quality_db`.
   - Execute the SQL script `create_water_quality_db.sql` to create the schema.

2. **Running the SQL Script:**

   - Open pgAdmin and connect to your PostgreSQL server.
   - Select the `water_quality_db` database.
   - Open the Query Tool and paste the contents of `create_water_quality_db.sql`.
   - Execute the script to create the `WaterQuality` and `WaterPotability` tables.

3. **Understanding the Schema:**

   - `WaterQuality` table stores detailed measurements of water quality.
   - `WaterPotability` table links each quality measurement to its potability status.

4. **Contributing**
   - Feel free to fork this repository, make improvements, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
