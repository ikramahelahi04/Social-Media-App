-- Drop the table if it exists
IF OBJECT_ID('dbo.users', 'U') IS NOT NULL
    DROP TABLE dbo.users;
GO

-- Create the users table
CREATE TABLE dbo.users (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    pass VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,  
    dob DATETIME NOT NULL
);

-- Insert new test data with unique passwords, email addresses, and varied DOBs
SET IDENTITY_INSERT dbo.users ON;

INSERT INTO dbo.users (id, username, pass, email, dob)
VALUES
(1, 'Alice_Wonder24', 'aW24!secure', 'alice.wonder24@example.com', '1995-05-14'),
(2, 'Bob_Smith45', 'bSmith#2023', 'bob.smith45@example.com', '1988-03-22'),
(3, 'Charlie_Brown18', 'cBrown$4589', 'charlie.brown18@example.com', '2001-11-10'),
(4, 'Daisy_Ridley07', 'dRidley#309', 'daisy.ridley07@example.com', '1992-07-29'),
(5, 'Ethan_Hunt33', 'ethanHunt!84', 'ethan.hunt33@example.com', '1980-09-17'),
(6, 'Fiona_Glenanne89', 'fGlenanne_1!', 'fiona.glenanne89@example.com', '1994-02-14'),
(7, 'George_Clooney76', 'gClooney76#', 'george.clooney76@example.com', '1976-10-10'),
(8, 'Helen_Parr22', 'hParr_2022!', 'helen.parr22@example.com', '1989-08-19'),
(9, 'Ian_Fleming54', 'iFleming$2024', 'ian.fleming54@example.com', '1974-01-04'),
(10, 'Jane_Doe99', 'jDoe#77!', 'jane.doe99@example.com', '1999-12-12'),
(11, 'Kara_Thrace11', 'kThrace!08', 'kara.thrace11@example.com', '1985-06-23'),
(12, 'Lara_Croft28', 'lCroft_22!', 'lara.croft28@example.com', '1993-04-15'),
(13, 'Mike_Ross63', 'mRoss#33!', 'mike.ross63@example.com', '2000-01-27'),
(14, 'Nancy_Drew47', 'nDrew#009', 'nancy.drew47@example.com', '1990-05-02'),
(15, 'Oscar_Wilde31', 'oWilde$93!', 'oscar.wilde31@example.com', '1979-03-15'),
(16, 'Penny_Wise77', 'pWise#35!', 'penny.wise77@example.com', '1988-08-09'),
(17, 'Quincy_Adams84', 'qAdams%44!', 'quincy.adams84@example.com', '1991-09-30'),
(18, 'Rachel_Green02', 'rGreen#82!', 'rachel.green02@example.com', '1992-06-01'),
(19, 'Sam_Winchester65', 'sWinchester*75!', 'sam.winchester65@example.com', '1986-11-13'),
(20, 'Tina_Fey43', 'tFey_99!', 'tina.fey43@example.com', '1977-12-03'),
(21, 'Uma_Thurman36', 'uThurman_20!', 'uma.thurman36@example.com', '1985-02-08'),
(22, 'Vince_Vaughn58', 'vVaughn#40!', 'vince.vaughn58@example.com', '1981-03-24'),
(23, 'Wanda_Maximoff12', 'wMaximoff%99!', 'wanda.maximoff12@example.com', '1997-07-16'),
(24, 'Xander_Harris91', 'xHarris$08!', 'xander.harris91@example.com', '1993-01-01'),
(25, 'Yara_Greyjoy70', 'yGreyjoy#11!', 'yara.greyjoy70@example.com', '1989-10-25'),
(26, 'Zach_Galifianakis39', 'zGalifianakis#77!', 'zach.galifianakis39@example.com', '1986-12-20'),
(27, 'Amy_Pond27', 'aPond_20!', 'amy.pond27@example.com', '1993-07-05'),
(28, 'Bruce_Wayne48', 'bWayne$89!', 'bruce.wayne48@example.com', '1980-02-19'),
(29, 'Clark_Kent56', 'cKent#02!', 'clark.kent56@example.com', '1984-03-11'),
(30, 'Diana_Prince67', 'dPrince_77!', 'diana.prince67@example.com', '1992-04-29'),
(31, 'Eric_Northman30', 'eNorthman$55!', 'eric.northman30@example.com', '1979-05-22'),
(32, 'Frodo_Baggins77', 'fBaggins#44!', 'frodo.baggins77@example.com', '1990-06-13'),
(33, 'Gordon_Ramsay50', 'gRamsay_99!', 'gordon.ramsay50@example.com', '1966-11-08'),
(34, 'Hugh_Jackman32', 'hJackman%72!', 'hugh.jackman32@example.com', '1968-10-12'),
(35, 'Isabella_Swann71', 'iSwann#33!', 'isabella.swann71@example.com', '1994-01-09'),
(36, 'Jack_Sparrow88', 'jSparrow$66!', 'jack.sparrow88@example.com', '1987-12-25'),
(37, 'Katniss_Everdeen13', 'kEverdeen_18!', 'katniss.everdeen13@example.com', '1995-08-11'),
(38, 'Legolas_Greenleaf55', 'lGreenleaf_90!', 'legolas.greenleaf55@example.com', '1983-09-17'),
(39, 'Mickey_Mouse64', 'mMouse#75!', 'mickey.mouse64@example.com', '1928-11-18'),
(40, 'Nathan_Drake82', 'nDrake_99!', 'nathan.drake82@example.com', '1981-05-20'),
(41, 'Olivia_Benson25', 'oBenson_13!', 'olivia.benson25@example.com', '1985-07-07'),
(42, 'Peter_Pan46', 'pPan$45!', 'peter.pan46@example.com', '1988-02-29'),
(43, 'Quinn_Fabray17', 'qFabray%77!', 'quinn.fabray17@example.com', '1993-12-19'),
(44, 'Ron_Weasley99', 'rWeasley#08!', 'ron.weasley99@example.com', '1990-03-01'),
(45, 'Sherlock_Holmes03', 'sHolmes$55!', 'sherlock.holmes03@example.com', '1970-06-23'),
(46, 'Tony_Stark15', 'tStark#20!', 'tony.stark15@example.com', '1975-05-29'),
(47, 'Ursula_Andress23', 'uAndress_44!', 'ursula.andress23@example.com', '1936-03-19'),
(48, 'Victor_Creed79', 'vCreed$77!', 'victor.creed79@example.com', '1982-10-03'),
(49, 'Walter_White52', 'wWhite%20!', 'walter.white52@example.com', '1956-09-07'),
(50, 'Xena_Warrior66', 'xWarrior_88!', 'xena.warrior66@example.com', '1991-01-31');

select * from users

SET IDENTITY_INSERT dbo.users OFF;

ALTER TABLE dbo.users
ADD profilepic NVARCHAR(1000);

UPDATE dbo.users
SET profilepic = 'https://static.wikia.nocookie.net/phineasandferb/images/6/6c/Phineas_says_in_two_weeks.jpg/revision/latest?cb=20150213031420'
WHERE id = 1;

UPDATE dbo.users
SET profilepic = 'https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small_2x/default-avatar-profile-icon-of-social-media-user-vector.jpg'
WHERE id = 7;

select * from users;
select * from follow

-- Table for following relationships
IF OBJECT_ID('dbo.follow', 'U') IS NOT NULL
    DROP TABLE dbo.follow;
GO

CREATE TABLE dbo.follow (
    follower_id INT NOT NULL,
    followee_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (follower_id, followee_id),
    FOREIGN KEY (follower_id) REFERENCES dbo.users(id),
    FOREIGN KEY (followee_id) REFERENCES dbo.users(id)
);

-- Create index on followee_id for performance optimization
CREATE INDEX idx_followee_id ON dbo.follow(followee_id);

-- Insert valid test data into follow table
INSERT INTO dbo.follow (follower_id, followee_id, created_at)
VALUES
(1, 2, '2024-04-06 05:55:19'),
(2, 3, '2024-04-06 05:55:19'),
(3, 4, '2024-04-06 05:55:19'),
(4, 5, '2024-04-06 05:55:19'),
(5, 6, '2024-04-06 05:55:19'),
(6, 7, '2024-04-06 05:55:19'),
(7, 8, '2024-04-06 05:55:19'),
(8, 9, '2024-04-06 05:55:19'),
(9, 10, '2024-04-06 05:55:19'),
(10, 11, '2024-04-06 05:55:19'),
(11, 12, '2024-04-06 05:55:19'),
(12, 13, '2024-04-06 05:55:19'),
(13, 14, '2024-04-06 05:55:19'),
(14, 15, '2024-04-06 05:55:19'),
(15, 16, '2024-04-06 05:55:19'),
(16, 17, '2024-04-06 05:55:19'),
(17, 18, '2024-04-06 05:55:19'),
(18, 19, '2024-04-06 05:55:19'),
(19, 20, '2024-04-06 05:55:19'),
(20, 21, '2024-04-06 05:55:19'),
(21, 22, '2024-04-06 05:55:19'),
(22, 23, '2024-04-06 05:55:19'),
(23, 24, '2024-04-06 05:55:19'),
(24, 25, '2024-04-06 05:55:19'),
(25, 26, '2024-04-06 05:55:19'),
(26, 27, '2024-04-06 05:55:19'),
(27, 28, '2024-04-06 05:55:19'),
(28, 29, '2024-04-06 05:55:19'),
(29, 30, '2024-04-06 05:55:19'),
(30, 31, '2024-04-06 05:55:19'),
(31, 32, '2024-04-06 05:55:19'),
(32, 33, '2024-04-06 05:55:19'),
(33, 34, '2024-04-06 05:55:19'),
(34, 35, '2024-04-06 05:55:19'),
(35, 36, '2024-04-06 05:55:19'),
(36, 37, '2024-04-06 05:55:19'),
(37, 38, '2024-04-06 05:55:19'),
(38, 39, '2024-04-06 05:55:19'),
(39, 40, '2024-04-06 05:55:19'),
(40, 41, '2024-04-06 05:55:19'),
(41, 42, '2024-04-06 05:55:19'),
(42, 43, '2024-04-06 05:55:19'),
(43, 44, '2024-04-06 05:55:19'),
(44, 45, '2024-04-06 05:55:19'),
(45, 46, '2024-04-06 05:55:19'),
(46, 47, '2024-04-06 05:55:19'),
(47, 48, '2024-04-06 05:55:19'),
(48, 49, '2024-04-06 05:55:19'),
(49, 50, '2024-04-06 05:55:19');

INSERT INTO dbo.follow (follower_id, followee_id, created_at)
VALUES
(34, 51, getdate())

INSERT INTO dbo.follow (follower_id, followee_id, created_at)
VALUES
(51, 6, getdate()),
(51, 7, getdate()),
(51, 8, getdate()),
(51, 9, getdate())

INSERT INTO dbo.follow (follower_id, followee_id, created_at)
VALUES
(1, 51, getdate()),
(2, 51, getdate()),
(3, 51, getdate()),
(4, 51, getdate())

INSERT INTO dbo.follow (follower_id, followee_id, created_at)
VALUES
(51, 1, getdate())

select * from follow

-- Table for photos
IF OBJECT_ID('dbo.photos', 'U') IS NOT NULL
    DROP TABLE dbo.photos;
GO

CREATE TABLE dbo.photos (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    image_url VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES dbo.users(id)
);

CREATE TABLE dbo.admins (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Insert new test data with unique passwords, email addresses, and varied DOBs
SET IDENTITY_INSERT dbo.admins ON;

INSERT INTO dbo.admins (id, username, password)
VALUES
(1, 'admin1', '12345678'),
(2, 'admin2', '87654321');

select * from admins

SET IDENTITY_INSERT dbo.admin OFF;