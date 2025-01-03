# Online Retail Interactive Dashboard

## Overview

This project involves the creation of an **interactive dashboard** for an online retail dataset targeted at younger adults aged 18-35 years. The dashboard summarizes sales trends, customer segmentation, and geographical sales distribution, offering a visually appealing and user-friendly experience.

## Additional Resources

- More Information: For a detailed explanation of the project structure, methodologies, and findings, refer to the Full Project Report.[Full Project Report](https://github.com/federicoariton/Project-3-Dashboard-with-python-/blob/main/Dashboard%20with%20Python%20Report%20pdf.pdf)


---

## Features

### Interactivity
- **Date Range Slider**: Allows users to filter data by time periods.
- **Country Dropdown**: Enables exploration of sales data by specific countries.

### Visualizations
- **Sales Over Time**: Line chart for identifying trends and seasonal patterns.
- **Sales by Country**: Bar chart highlighting geographical performance.
- **Top Products**: Displays the top 10 best-performing products by sales.
- **Sales Map**: Choropleth map showing global sales distribution.
- **Customer Segmentation**: Pie chart identifying key customer groups.
- **Monthly Sales**: Bar chart summarizing sales performance per month.

---

## Data Preparation

1. **Data Cleaning**
   - Removed rows with null values in `CustomerID` and `Description`.
   - Filtered out invalid transactions (non-positive `Quantity` values).

2. **Feature Engineering**
   - Created `TotalPrice` by multiplying `Quantity` and `UnitPrice`.
   - Extracted time-based features like `YearMonth`, `DayOfWeek`, and `Day` from `InvoiceDate`.

---

## Deployment

The dashboard is built using **Dash**, a Python framework for creating analytical web applications.

### Prerequisites
Install the required libraries using the command below:

```bash
pip install dash dash-bootstrap-components plotly pandas openpyxl
