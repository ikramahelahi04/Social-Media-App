x-- Table for photos
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

-- Insert data into photos table
SET IDENTITY_INSERT dbo.photos ON;

INSERT INTO dbo.photos (id, image_url, user_id, created_at)
VALUES
(1, 'http://elijah.biz', 1, '2024-04-06 05:45:26'),
(2, 'https://shanon.org', 1, '2024-04-06 05:45:26'),
(3, 'http://vicky.biz', 1, '2024-04-06 05:45:26'),
(4, 'http://oleta.net', 1, '2024-04-06 05:45:26'),
(5, 'https://jennings.biz', 1, '2024-04-06 05:45:26'),
(6, 'https://quinn.biz', 2, '2024-04-06 05:45:26'),
(7, 'https://selina.name', 2, '2024-04-06 05:45:26'),
(8, 'http://malvina.org', 2, '2024-04-06 05:45:26'),
(9, 'https://branson.biz', 2, '2024-04-06 05:45:26'),
(10, 'https://elenor.name', 3, '2024-04-06 05:45:26'),
(11, 'https://marcelino.com', 3, '2024-04-06 05:45:26'),
(12, 'http://felicity.name', 3, '2024-04-06 05:45:26'),
(13, 'https://fred.com', 3, '2024-04-06 05:45:26'),
(14, 'https://gerhard.biz', 4, '2024-04-06 05:45:26'),
(15, 'https://sherwood.net', 4, '2024-04-06 05:45:26'),
(16, 'https://maudie.org', 4, '2024-04-06 05:45:26'),
(17, 'http://annamae.name', 6, '2024-04-06 05:45:26'),
(18, 'https://mac.org', 6, '2024-04-06 05:45:26'),
(19, 'http://miracle.info', 6, '2024-04-06 05:45:26'),
(20, 'http://emmet.com', 6, '2024-04-06 05:45:26'),
(21, 'https://lisa.com', 6, '2024-04-06 05:45:26'),
(22, 'https://brooklyn.name', 8, '2024-04-06 05:45:26'),
(23, 'http://madison.net', 8, '2024-04-06 05:45:26'),
(24, 'http://annie.name', 8, '2024-04-06 05:45:26'),
(25, 'http://darron.info', 8, '2024-04-06 05:45:26'),
(26, 'http://saige.com', 9, '2024-04-06 05:45:26'),
(27, 'https://reece.net', 9, '2024-04-06 05:45:26'),
(28, 'http://vance.org', 9, '2024-04-06 05:45:26'),
(29, 'http://ignacio.net', 9, '2024-04-06 05:45:26'),
(30, 'http://kenny.com', 10, '2024-04-06 05:45:26'),
(31, 'http://remington.name', 10, '2024-04-06 05:45:26'),
(32, 'http://kurtis.info', 10, '2024-04-06 05:45:26'),
(33, 'https://alisha.com', 11, '2024-04-06 05:45:26'),
(34, 'https://henderson.com', 11, '2024-04-06 05:45:26'),
(35, 'http://bonnie.info', 11, '2024-04-06 05:45:26'),
(36, 'http://kennith.net', 11, '2024-04-06 05:45:26'),
(37, 'http://camille.name', 11, '2024-04-06 05:45:26'),
(38, 'http://alena.net', 12, '2024-04-06 05:45:26'),
(39, 'http://ralph.name', 12, '2024-04-06 05:45:26'),
(40, 'https://tyshawn.com', 12, '2024-04-06 05:45:26'),
(41, 'https://adella.net', 12, '2024-04-06 05:45:26'),
(42, 'https://cielo.info', 13, '2024-04-06 05:45:26'),
(43, 'https://easter.net', 13, '2024-04-06 05:45:26'),
(44, 'http://golden.org', 13, '2024-04-06 05:45:26'),
(45, 'http://kendall.biz', 13, '2024-04-06 05:45:26'),
(46, 'https://glenda.info', 13, '2024-04-06 05:45:26'),
(47, 'http://dominic.biz', 15, '2024-04-06 05:45:26'),
(48, 'http://tressie.info', 15, '2024-04-06 05:45:26'),
(49, 'http://estevan.org', 15, '2024-04-06 05:45:26'),
(50, 'http://zena.com', 15, '2024-04-06 05:45:26');

ALTER TABLE dbo.photos
ADD caption NVARCHAR(255);

UPDATE dbo.photos
SET caption = CONCAT('Caption for photo', 1);

UPDATE dbo.photos
SET image_url = 'https://upload.wikimedia.org/wikipedia/commons/f/fa/Dubai_International_Airport_interior_of_Terminal_3%2C_2019%2C_14.jpg'
WHERE user_id = 15;

select * from photos
select * from users

select * from follow

SET IDENTITY_INSERT dbo.photos OFF;

select * from photos
select * from likes
select * from comments

-- Table for likes
IF OBJECT_ID('dbo.likes', 'U') IS NOT NULL
    DROP TABLE dbo.likes;
GO

CREATE TABLE dbo.likes (
    user_id INT NOT NULL,
    photo_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES dbo.users(id),
    FOREIGN KEY (photo_id) REFERENCES dbo.photos(id)
);

-- Create indexes for better performance
CREATE INDEX idx_user_id ON dbo.likes(user_id);
CREATE INDEX idx_photo_id ON dbo.likes(photo_id);

-- Inserting data into likes table (Ensure user_id exists in dbo.users and photo_id exists in dbo.photos)
INSERT INTO dbo.likes (user_id, photo_id, created_at)
VALUES
(1, 1, '2024-04-06 05:56:14'),
(2, 1, '2024-04-06 05:56:14'),
(3, 1, '2024-04-06 05:56:14'),
(4, 1, '2024-04-06 05:56:14'),
(5, 2, '2024-04-06 05:56:14'),
(6, 2, '2024-04-06 05:56:14'),
(7, 2, '2024-04-06 05:56:14'),
(8, 2, '2024-04-06 05:56:14'),
(9, 3, '2024-04-06 05:56:14'),
(10, 3, '2024-04-06 05:56:14'),
(11, 3, '2024-04-06 05:56:14'),
(12, 3, '2024-04-06 05:56:14'),
(13, 4, '2024-04-06 05:56:14'),
(14, 4, '2024-04-06 05:56:14'),
(15, 4, '2024-04-06 05:56:14'),
(16, 4, '2024-04-06 05:56:14'),
(17, 5, '2024-04-06 05:56:14'),
(18, 5, '2024-04-06 05:56:14'),
(19, 5, '2024-04-06 05:56:14'),
(20, 5, '2024-04-06 05:56:14'),
(21, 6, '2024-04-06 05:56:14'),
(22, 6, '2024-04-06 05:56:14'),
(23, 6, '2024-04-06 05:56:14'),
(24, 6, '2024-04-06 05:56:14'),
(25, 7, '2024-04-06 05:56:14'),
(26, 7, '2024-04-06 05:56:14'),
(27, 7, '2024-04-06 05:56:14'),
(28, 7, '2024-04-06 05:56:14'),
(29, 8, '2024-04-06 05:56:14'),
(30, 8, '2024-04-06 05:56:14'),
(31, 8, '2024-04-06 05:56:14'),
(32, 8, '2024-04-06 05:56:14'),
(33, 9, '2024-04-06 05:56:14'),
(34, 9, '2024-04-06 05:56:14'),
(35, 9, '2024-04-06 05:56:14'),
(36, 9, '2024-04-06 05:56:14'),
(37, 10, '2024-04-06 05:56:14'),
(38, 10, '2024-04-06 05:56:14'),
(39, 10, '2024-04-06 05:56:14'),
(40, 10, '2024-04-06 05:56:14'),
(41, 11, '2024-04-06 05:56:14'),
(42, 11, '2024-04-06 05:56:14'),
(43, 11, '2024-04-06 05:56:14'),
(44, 11, '2024-04-06 05:56:14'),
(45, 12, '2024-04-06 05:56:14'),
(46, 12, '2024-04-06 05:56:14'),
(47, 12, '2024-04-06 05:56:14'),
(48, 12, '2024-04-06 05:56:14'),
(49, 13, '2024-04-06 05:56:14'),
(50, 13, '2024-04-06 05:56:14');



-- Table for comments
IF OBJECT_ID('dbo.comments', 'U') IS NOT NULL
    DROP TABLE dbo.comments;
GO

CREATE TABLE dbo.comments (
    id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    comment_text VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    photo_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES dbo.users(id),
    FOREIGN KEY (photo_id) REFERENCES dbo.photos(id)
);

-- Create indexes
CREATE INDEX idx_user_id ON dbo.comments(user_id);
CREATE INDEX idx_photo_id ON dbo.comments(photo_id);

-- Insert sample data into comments table
INSERT INTO dbo.comments (comment_text, user_id, photo_id, created_at)
VALUES
    ('Amazing photo!', 1, 1, '2024-04-06 05:55:58'),
    ('Great shot!', 2, 1, '2024-04-06 05:55:58'),
    ('Beautiful!', 3, 1, '2024-04-06 05:55:58'),
    ('Love this!', 4, 1, '2024-04-06 05:55:58'),
    ('Stunning!', 5, 1, '2024-04-06 05:55:58'),
    ('Incredible!', 6, 1, '2024-04-06 05:55:58'),
    ('Wow!', 7, 1, '2024-04-06 05:55:58'),
    ('Fantastic!', 8, 1, '2024-04-06 05:55:58'),
    ('Nice capture!', 9, 1, '2024-04-06 05:55:58'),
    ('Lovely!', 10, 1, '2024-04-06 05:55:58'),
    ('Great colors!', 11, 1, '2024-04-06 05:55:58'),
    ('Perfect!', 12, 1, '2024-04-06 05:55:58'),
    ('So cool!', 13, 1, '2024-04-06 05:55:58'),
    ('Epic!', 14, 1, '2024-04-06 05:55:58'),
    ('Impressive!', 15, 1, '2024-04-06 05:55:58'),
    ('Great angle!', 16, 1, '2024-04-06 05:55:58'),
    ('So beautiful!', 17, 1, '2024-04-06 05:55:58'),
    ('Amazing work!', 18, 1, '2024-04-06 05:55:58'),
    ('Incredible shot!', 19, 1, '2024-04-06 05:55:58'),
    ('Love the colors!', 20, 1, '2024-04-06 05:55:58'),
    ('Great light!', 21, 1, '2024-04-06 05:55:58'),
    ('Awesome!', 22, 1, '2024-04-06 05:55:58'),
    ('Perfect shot!', 23, 1, '2024-04-06 05:55:58'),
    ('Wonderful!', 24, 1, '2024-04-06 05:55:58'),
    ('So artistic!', 25, 1, '2024-04-06 05:55:58'),
    ('Nice composition!', 26, 1, '2024-04-06 05:55:58'),
    ('Superb!', 27, 1, '2024-04-06 05:55:58'),
    ('Fantastic work!', 28, 1, '2024-04-06 05:55:58'),
    ('Amazing detail!', 29, 1, '2024-04-06 05:55:58'),
    ('So sharp!', 30, 1, '2024-04-06 05:55:58'),
    ('Great focus!', 31, 1, '2024-04-06 05:55:58'),
    ('Beautiful composition!', 32, 1, '2024-04-06 05:55:58'),
    ('Amazing clarity!', 33, 1, '2024-04-06 05:55:58'),
    ('Nice perspective!', 34, 1, '2024-04-06 05:55:58'),
    ('Well done!', 35, 1, '2024-04-06 05:55:58'),
    ('Excellent!', 36, 1, '2024-04-06 05:55:58'),
    ('So creative!', 37, 1, '2024-04-06 05:55:58'),
    ('Stunning shot!', 38, 1, '2024-04-06 05:55:58'),
    ('Beautifully done!', 39, 1, '2024-04-06 05:55:58'),
    ('Great job!', 40, 1, '2024-04-06 05:55:58'),
    ('Nicely captured!', 41, 1, '2024-04-06 05:55:58'),
    ('Amazing angle!', 42, 1, '2024-04-06 05:55:58'),
    ('Awesome shot!', 43, 1, '2024-04-06 05:55:58'),
    ('Beautiful colors!', 44, 1, '2024-04-06 05:55:58'),
    ('Great capture!', 45, 1, '2024-04-06 05:55:58'),
    ('Wonderful composition!', 46, 1, '2024-04-06 05:55:58'),
    ('Love this shot!', 47, 1, '2024-04-06 05:55:58'),
    ('So sharp!', 48, 1, '2024-04-06 05:55:58'),
    ('Stunning colors!', 49, 1, '2024-04-06 05:55:58'),
    ('Impressive capture!', 50, 1, '2024-04-06 05:55:58'),
    ('Excellent composition!', 1, 2, '2024-04-06 05:55:58'),
    ('Amazing colors!', 2, 2, '2024-04-06 05:55:58'),
    ('So detailed!', 3, 2, '2024-04-06 05:55:58'),
    ('Great shot!', 4, 2, '2024-04-06 05:55:58'),
    ('Incredible photo!', 5, 2, '2024-04-06 05:55:58'),
    ('Beautiful!', 6, 2, '2024-04-06 05:55:58'),
    ('Amazing shot!', 7, 2, '2024-04-06 05:55:58'),
    ('Fantastic!', 8, 2, '2024-04-06 05:55:58'),
    ('Wow!', 9, 2, '2024-04-06 05:55:58'),
    ('Great capture!', 10, 2, '2024-04-06 05:55:58'),
    ('Love it!', 11, 2, '2024-04-06 05:55:58'),
    ('So cool!', 12, 2, '2024-04-06 05:55:58'),
    ('Perfect shot!', 13, 2, '2024-04-06 05:55:58'),
    ('Awesome!', 14, 2, '2024-04-06 05:55:58'),
    ('Beautiful capture!', 15, 2, '2024-04-06 05:55:58'),
    ('Nice colors!', 16, 2, '2024-04-06 05:55:58'),
    ('Stunning detail!', 17, 2, '2024-04-06 05:55:58'),
    ('Incredible angle!', 18, 2, '2024-04-06 05:55:58'),
    ('Amazing!', 19, 2, '2024-04-06 05:55:58'),
    ('Fantastic shot!', 20, 2, '2024-04-06 05:55:58'),
    ('Love the detail!', 21, 2, '2024-04-06 05:55:58'),
    ('Awesome capture!', 22, 2, '2024-04-06 05:55:58'),
    ('Beautiful colors!', 23, 2, '2024-04-06 05:55:58'),
    ('Nice work!', 24, 2, '2024-04-06 05:55:58'),
    ('Perfect composition!', 25, 2, '2024-04-06 05:55:58'),
    ('Incredible!', 26, 2, '2024-04-06 05:55:58'),
    ('So artistic!', 27, 2, '2024-04-06 05:55:58'),
    ('Great job!', 28, 2, '2024-04-06 05:55:58'),
    ('So sharp!', 29, 2, '2024-04-06 05:55:58'),
    ('Love the perspective!', 30, 2, '2024-04-06 05:55:58');

	select * from comments
	select * from likes
	select * from photos
	select * from users

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