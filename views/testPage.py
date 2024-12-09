import streamlit as st
import pandas as pd
import plotly.express as px
from mlxtend.frequent_patterns import apriori, association_rules

# Streamlit app title
st.title("Interactive Apriori Algorithm for Groceries Dataset")

# Sidebar for parameters
st.sidebar.header("Parameters")
min_support = st.sidebar.slider("Minimum Support", 0.01, 1.0, 0.1)
min_confidence = st.sidebar.slider("Minimum Confidence", 0.01, 1.0, 0.5)
min_lift = st.sidebar.slider("Minimum Lift", 1.0, 10.0, 1.0)  # Additional filter for Lift
top_n = st.sidebar.slider("Top N Associations", 1, 20, 10)  # Filter to display top N associations

# Load the groceries dataset
file_path = "assets/csv/Groceries_dataset.csv"
try:
    data = pd.read_csv(file_path)

    # # Display the raw dataset
    # st.subheader("Raw Dataset")
    # st.dataframe(data.head())

    # Data cleaning
    data = data.dropna(subset=["Member_number", "itemDescription"])
    data["itemDescription"] = data["itemDescription"].str.lower().str.strip()
    data = data.drop_duplicates()

    # Display cleaned dataset
    st.subheader("Cleaned Dataset")
    st.dataframe(data.head())

    # Preprocess the dataset
    transactions = data.groupby("Member_number")["itemDescription"].apply(list)

    # Convert transactions into a one-hot encoded DataFrame
    item_set = set(data["itemDescription"].unique())
    one_hot_encoded = pd.DataFrame(
        [{item: (item in transaction) for item in item_set} for transaction in transactions]
    )

    # Convert date columns to proper format if necessary (e.g., to datetime)
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Group by Month to get monthly sales
    data['Month'] = data['Date'].dt.to_period('M').astype(str)

    # --- Begin Graph Section ---
    st.subheader("Sales Analysis")

    # Items sold per month (bar chart)
    items_per_month = data.groupby('Month')['itemDescription'].count().reset_index()
    items_per_month_fig = px.bar(items_per_month, x='Month', y='itemDescription', title="Items Sold Per Month")
    st.plotly_chart(items_per_month_fig)

    # Items sold per customer (histogram)
    items_per_customer = data.groupby('Member_number')['itemDescription'].count().reset_index()
    items_per_customer_fig = px.histogram(items_per_customer, x='itemDescription', title="Items Sold Per Customer")
    st.plotly_chart(items_per_customer_fig)

    # Customer sales per day (line chart)
    customer_sales_day = data.groupby('Date')['Member_number'].nunique().reset_index()
    customer_sales_day_fig = px.line(customer_sales_day, x='Date', y='Member_number', title="Customer Sales Per Day")
    st.plotly_chart(customer_sales_day_fig)

    # Total sales per day (line chart)
    total_sales_day = data.groupby('Date')['itemDescription'].count().reset_index()
    total_sales_day_fig = px.line(total_sales_day, x='Date', y='itemDescription', title="Total Sales Per Day")
    st.plotly_chart(total_sales_day_fig)

    # --- End Graph Section ---

    # Apply Apriori algorithm
    st.subheader("Frequent Itemsets")
    frequent_itemsets = apriori(one_hot_encoded, min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        st.warning("No frequent itemsets found for the given support level. Try lowering the minimum support.")
    else:
        st.write(frequent_itemsets)

        # Calculate the number of frequent itemsets
        num_itemsets = len(frequent_itemsets)

        # Generate association rules with num_itemsets
        st.subheader("Association Rules")
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence, num_itemsets=num_itemsets)
        if rules.empty:
            st.warning("No association rules found for the given confidence level. Try lowering the minimum confidence.")
        else:
            # Convert frozenset to strings
            rules["antecedents"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
            rules["consequents"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))

            # Display rules with selected columns (antecedent, consequent, support, confidence, lift)
            rules_selected = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
            st.write(rules_selected)

            # Interactive filtering for Lift
            st.subheader("Filter Rules")
            min_lift = st.slider("Minimum Lift", min_value=float(rules["lift"].min()), max_value=float(rules["lift"].max()), value=float(rules["lift"].min()))
            filtered_rules = rules_selected[rules_selected["lift"] >= min_lift]
            st.write(filtered_rules)


            # --- Bar Chart for Top N Associations ---
            top_associations = filtered_rules.sort_values(by="lift", ascending=False).head(top_n)
            bar_chart_fig = px.bar(top_associations, x='antecedents', y='lift', color='lift', title=f"Top {top_n} Associations by Lift")
            st.plotly_chart(bar_chart_fig)

            # Download link for filtered rules
            st.subheader("Download Filtered Rules")
            csv = filtered_rules.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Filtered Rules as CSV",
                data=csv,
                file_name="filtered_association_rules.csv",
                mime="text/csv",
            )

    # --- Scatter Plot for Commonly Bought Together Items ---
    st.subheader("Commonly Bought Together Items")

    # Create a scatter plot of common items from the association rules
    if not rules_selected.empty:
        common_items = rules_selected[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(20)
        fig = px.scatter(common_items, x='support', y='confidence', color='lift', size='lift',
                         hover_data=['antecedents', 'consequents'],
                         title="Commonly Bought Together Items")
        st.plotly_chart(fig)

except FileNotFoundError:
    st.error(f"The file '{file_path}' was not found. Please ensure it is in the correct folder.")
except Exception as e:
    st.error(f"An error occurred: {e}")
