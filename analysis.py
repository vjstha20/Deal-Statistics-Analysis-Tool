import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    # Load the data from CSV files
    combined_data = pd.read_csv('combined_data.csv')
    deal_statistics_data = pd.read_csv('deal_statistics_data.csv')
    industry_averages = pd.read_csv('industry_averages.csv')
    macroeconomics = pd.read_csv('macroeconomics.csv')

    # Data Cleaning and Transformation
    # Forward fill missing values
    combined_data.ffill(inplace=True)
    deal_statistics_data.ffill(inplace=True)
    macroeconomics.ffill(inplace=True)
    
    # Remove duplicates
    combined_data.drop_duplicates(inplace=True)
    deal_statistics_data.drop_duplicates(inplace=True)
    macroeconomics.drop_duplicates(inplace=True)
    
    # Convert date columns to datetime format
    combined_data['deal_date'] = pd.to_datetime(combined_data['deal_date'])
    deal_statistics_data['deal_date'] = pd.to_datetime(deal_statistics_data['deal_date'])
    macroeconomics['date'] = pd.to_datetime(macroeconomics['date'])
    
    # Calculate debt-equity ratio
    deal_statistics_data['debt_equity_ratio'] = deal_statistics_data['debt_amount'] / deal_statistics_data['equity_amount']
    
    # Ensure the 'data/processed' directory exists
    os.makedirs('data/processed', exist_ok=True)
    
    # Save cleaned data
    combined_data.to_csv('data/processed/cleaned_combined_data.csv', index=False)
    deal_statistics_data.to_csv('data/processed/cleaned_deal_statistics_data.csv', index=False)
    macroeconomics.to_csv('data/processed/cleaned_macroeconomics.csv', index=False)

    # Analysis Tool Development
    # Merge deal statistics data with industry averages
    analysis_data = pd.merge(deal_statistics_data, industry_averages, on='industry', suffixes=('', '_industry_avg'))
    
    # Calculate peers multiple
    analysis_data['peers_multiple'] = analysis_data['debt_equity_ratio'] / analysis_data['average_debt_equity_ratio']
    
    # Save analysis results
    analysis_data.to_csv('data/processed/analysis_results.csv', index=False)

    # Ensure the 'reports' directory exists
    os.makedirs('reports', exist_ok=True)

    # Visualization Creation
    # Create and save line plot of debt-equity ratio over time
    plt.figure(figsize=(12, 10))
    sns.lineplot(data=analysis_data, x='deal_date', y='debt_equity_ratio')
    plt.title('Debt-Equity Ratio Over Time')
    plt.xlabel('Date')
    plt.ylabel('Debt-Equity Ratio')
    plt.savefig('reports/debt_equity_ratio_over_time.png')
    plt.show()
    
    # Create and save bar plot of peers multiples by industry
    plt.figure(figsize=(12, 10))
    sns.barplot(data=analysis_data, x='industry', y='peers_multiple')
    plt.title('Peers Multiples by Industry')
    plt.xlabel('Industry')
    plt.ylabel('Peers Multiple')
    plt.xticks(rotation=45)
    plt.savefig('reports/peers_multiples_by_industry.png')
    plt.show()

if __name__ == "__main__":
    main()
