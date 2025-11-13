
USE Customer

-- XEM DỮ LIỆU --
SELECT *FROM data_cleaned

-- Số hóa đơn---
SELECT COUNT(DISTINCT Invoice_Number) AS Total_Invoice
FROM data_cleaned;

-- Số khách hàng---
SELECT COUNT(DISTINCT Customer_ID) AS Total_Customer
FROM data_cleaned;


-- TỔNG DOANH THU --
SELECT SUM(Total_Price) as Revenue FROM data_cleaned

-- Giá trị trung bình trên mỗi đơn hàng
SELECT SUM(Total_Price) * 1.0 / COUNT(DISTINCT Invoice_Number) AS Avg_Revenue_Per_Invoice
FROM data_cleaned;

--- TỔNG DOANH THU THEO NHÓM NAM/NỮ ---
SELECT Gender, SUM(Total_Price) as Revenue FROM data_cleaned
GROUP BY Gender

-- Doanh thu theo tháng - năm ----
SELECT YEAR(Invoice_Date)  AS Year,MONTH(Invoice_Date) AS Month, SUM(Total_Price)    AS Revenue
FROM data_cleaned
GROUP BY YEAR(Invoice_Date), MONTH(Invoice_Date)
ORDER BY Year, Month;

-- Doanh thu theo các ngày trong tuần ----
SELECT DATENAME(WEEKDAY, Invoice_Date)   AS WeekdayName,COUNT(DISTINCT Invoice_Number)  AS Total_Orders
FROM data_cleaned
GROUP BY 
DATENAME(WEEKDAY, Invoice_Date),
DATEPART(WEEKDAY, Invoice_Date)

----Doanh thu theo nhóm tuổi---
SELECT Age_Group,SUM(Total_Price) AS Revenue
FROM data_cleaned
GROUP BY  Age_Group
ORDER BY Age_Group;

-- Phương thức thanh toán theo đơn hàng-- 
SELECT Payment_Method, COUNT(*)  AS Total_Invoice
FROM data_cleaned
GROUP BY Payment_Method;


---TOP 3 Category theo doanh thu---
SELECT TOP 3 Category, SUM(Total_Price) AS Revenue
FROM data_cleaned
GROUP BY Category
ORDER BY Revenue ASC;

---BOTTOM 3 Category theo doanh thu---
SELECT TOP 3 Category, SUM(Total_Price) AS Revenue
FROM data_cleaned
GROUP BY Category
ORDER BY Revenue DESC;

-- TOP 3 Shopping Mall theo doanh thu---
SELECT TOP 3 Shopping_Mall,SUM(Total_Price) AS Revenue
FROM data_cleaned
GROUP BY Shopping_Mall
ORDER BY Revenue DESC;

-- BOTTOM 3 Shopping Mall theo doanh thu----
SELECT TOP 3 Shopping_Mall, SUM(Total_Price) AS Revenue
FROM data_cleaned
GROUP BY Shopping_Mall
ORDER BY Revenue ASC;

-- Top 3 Category by Quantity Sold--
SELECT TOP 3 Category,SUM(Quantity) AS Total_Quantity
FROM data_cleaned
GROUP BY Category
ORDER BY Total_Quantity DESC;

-- BOTTOM 3 Category by Quantity Sold--
SELECT TOP 3 Category, SUM(Quantity) AS Total_Quantity
FROM data_cleaned
GROUP BY Category
ORDER BY Total_Quantity ASC;