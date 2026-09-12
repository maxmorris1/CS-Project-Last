CREATE TABLE IF NOT EXISTS Staff (
  StaffID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  StaffFirstName TEXT NOT NULL,
  StaffLastName TEXT NOT NULL,
  StaffPosition TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Customers (
  CustomerID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  CustomerFirstName TEXT NOT NULL,
  CustomerLastName TEXT NOT NULL,
  CustomerPhone INTEGER UNIQUE NOT NULL,
  CustomerEmail TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS CustomerOrder (
  OrderID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  StaffID INTEGER NOT NULL,
  CustomerID INTEGER NOT NULL,
  OrderPrice REAL NOT NULL,
  OrderDate TEXT NOT NULL,
  OrderTime INTEGER NOT NULL,
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
  FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);

CREATE TABLE IF NOT EXISTS MenuItems (
  ItemID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  ItemName TEXT UNIQUE NOT NULL,
  ItemPrice REAL NOT NULL,
  ItemCostToMake REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS Ingredients (
  IngredientID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  IngrName TEXT NOT NULL,
  IngrPrice REAL NOT NULL,
  IngrStock INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS OrderMenuItems (
  OrderID INTEGER NOT NULL,
  ItemID INTEGER NOT NULL,
  ItemAmount INTEGER NOT NULL,
  PRIMARY KEY (OrderID, ItemID),
  FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID),
  FOREIGN KEY (ItemID) REFERENCES MenuItems(ItemID)
);

CREATE TABLE IF NOT EXISTS MenuIngredients (
  ItemID INTEGER NOT NULL,
  IngredientID INTEGER NOT NULL,
  IngrAmount REAL NOT NULL,
  PRIMARY KEY (ItemID, IngredientID),
  FOREIGN KEY (ItemID) REFERENCES MenuItems(ItemID),
  FOREIGN KEY (IngredientID) REFERENCES Ingredients(IngredientID)
);

CREATE TABLE IF NOT EXISTS CustomersLogin (
  CustomerLoginID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  CustomerID INTEGER NOT NULL,
  CustomerUsername TEXT UNIQUE NOT NULL,
  CustomerPassHex TEXT NOT NULL,
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE IF NOT EXISTS StaffLogin (
  StaffLoginID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  StaffID INTEGER NOT NULL,
  StaffUsername TEXT UNIQUE NOT NULL,
  StaffPassHex TEXT NOT NULL,
  FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);











INSERT OR IGNORE INTO Staff
    (StaffID, StaffFirstName, StaffLastName, StaffPosition)
VALUES
    (1, 'Alice', 'Morgan', 'Manager'),
    (2, 'Ben', 'Carter', 'Cashier');

INSERT OR IGNORE INTO Customers
    (CustomerID, CustomerFirstName, CustomerLastName, CustomerPhone, CustomerEmail)
VALUES
    (1, 'Jamie', 'Lee', 5551001, 'jamie.lee@example.com'),
    (2, 'Taylor', 'Smith', 5551002, 'taylor.smith@example.com');

INSERT OR IGNORE INTO StaffLogin
    (StaffLoginID, StaffID, StaffUsername, StaffPassHex)
VALUES
    (1, 1, 'alice.manager',
     '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
    (2, 2, 'ben.cashier',
     '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

INSERT OR IGNORE INTO CustomersLogin
    (CustomerLoginID, CustomerID, CustomerUsername, CustomerPassHex)
VALUES
    (1, 1, 'jamie.lee',
     '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
    (2, 2, 'taylor.smith',
     '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

INSERT OR IGNORE INTO MenuItems
    (ItemID, ItemName, ItemPrice, ItemCostToMake)
VALUES
    (1, 'Latte', 4.50, 1.20),
    (2, 'Cappuccino', 4.25, 1.10),
    (3, 'Blueberry Muffin', 3.00, 0.85),
    (4, 'Ham Sandwich', 7.50, 3.25);

INSERT OR IGNORE INTO Ingredients
    (IngredientID, IngrName, IngrPrice, IngrStock)
VALUES
    (1, 'Coffee Beans', 18.00, 100),
    (2, 'Milk', 3.50, 50),
    (3, 'Blueberries', 6.00, 30),
    (4, 'Flour', 4.00, 40),
    (5, 'Ham', 12.00, 25),
    (6, 'Bread', 3.00, 35);

INSERT OR IGNORE INTO MenuIngredients
    (ItemID, IngredientID, IngrAmount)
VALUES
    (1, 1, 18),
    (1, 2, 250),
    (2, 1, 18),
    (2, 2, 180),
    (3, 3, 40),
    (3, 4, 100),
    (4, 5, 80),
    (4, 6, 2);

INSERT OR IGNORE INTO CustomerOrder
    (OrderID, StaffID, CustomerID, OrderPrice, OrderDate, OrderTime)
VALUES
    (1, 1, 1, 7.50, '2026-09-12', 1030),
    (2, 2, 2, 11.50, '2026-09-12', 1145);

INSERT OR IGNORE INTO OrderMenuItems
    (OrderID, ItemID, ItemAmount)
VALUES
    (1, 1, 1),
    (1, 3, 1),
    (2, 2, 1),
    (2, 4, 1);
