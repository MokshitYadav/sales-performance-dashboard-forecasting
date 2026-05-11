-- 1. Total Sales, Profit and Orders
SELECT 
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore;

-- 2. Sales and Profit by Category
SELECT 
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore
GROUP BY Category
ORDER BY Total_Sales DESC;

-- 3. Top 10 Products by Sales
SELECT 
    Product_Name,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM superstore
GROUP BY Product_Name
ORDER BY Total_Sales DESC
LIMIT 10;

-- 4. Sales by Region
SELECT 
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore
GROUP BY Region
ORDER BY Total_Sales DESC;

-- 5. Monthly Sales Trend
SELECT 
    Order_Year,
    Order_Month,
    ROUND(SUM(Sales), 2) AS Monthly_Sales
FROM superstore
GROUP BY Order_Year, Order_Month
ORDER BY Order_Year, Order_Month;

-- 6. Most Profitable Sub-Categories
SELECT 
    Sub_Category,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore
GROUP BY Sub_Category
ORDER BY Total_Profit DESC;