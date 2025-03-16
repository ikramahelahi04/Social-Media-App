import sys
import hashlib
import pyodbc
from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import requests
from io import BytesIO

server = 'DESKTOP-IO55A14'
database = 'ikramah'  # Name of your database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'DESKTOP-IO55A14/DELL'  # Specify a username if not using Windows Authentication
password = 'your_password'  # Specify a password if not using Windows Authentication
global connection_string

# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Function to register a new user
def register_user(username, password, email, dob):
    try:
        dob = datetime.strptime(dob, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        print("Invalid date format")
        return False  # Invalid date format

    conn = pyodbc.connect(connection_string)
    c = conn.cursor()
    
    # Check if the username already exists
    c.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    count = c.fetchone()[0]
    print(f"Username check count: {count}")
    if count > 0:
        conn.close()
        print("Username already exists")
        return False  # Username already exists

    try:
        c.execute("INSERT INTO users (username, pass, email, dob) VALUES (?, ?, ?, ?)", 
                  (username, password, email, dob))
        conn.commit()
        conn.close()
        print("User registered successfully")
        return True
    except pyodbc.IntegrityError as e:  # Handle any other integrity errors
        conn.close()
        print(f"Integrity error: {e}")
        return False
    except Exception as e:
        conn.close()
        print(f"Error: {e}")
        return False

# Function to validate sign-in credentials
def validate_user(username, password):
    conn = pyodbc.connect(connection_string)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND pass = ?", (username, password))
    user = c.fetchone()
    conn.close()
    
    return user is not None  # Returns True if user exists

class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('LogInFINAL.ui', self)

        self.pushButton_3.clicked.connect(self.handle_login)
        self.pushButton_5.clicked.connect(self.open_signup)
        self.pushButton.clicked.connect(self.open_admin_login)  # Map pushButton to open AdminLoginFINAL

    def handle_login(self):
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        if validate_user(username, password):
            QMessageBox.information(self, "Login Success", f"Welcome, {username}!")
            self.open_main_page(username)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")

    def open_signup(self):
        self.signup_screen = SignUpScreen()
        self.signup_screen.show()

    def open_main_page(self, username):
        self.main_window = MainWindow(username)
        self.main_window.show()
        self.close()

    def open_admin_login(self):
        self.admin_login_screen = AdminLoginScreen()
        self.admin_login_screen.show()

class AdminLoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('AdminLoginFINAL.ui', self)

        self.pushButton_3.clicked.connect(self.handle_admin_login)  # Map pushButton_3 to handle admin login

    def handle_admin_login(self):
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        if self.validate_admin(username, password):
            QMessageBox.information(self, "Login Success", "Welcome, Admin!")
            self.open_admin_portal()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid admin username or password. Please try again.")

    def validate_admin(self, username, password):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
        admin = cursor.fetchone()
        connection.close()
        return admin is not None

    def open_admin_portal(self):
        self.admin_portal_screen = AdminPortalScreen()
        self.admin_portal_screen.show()
        self.close()

class AdminPortalScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('AdminPortalFINAL.ui', self)
        self.populate_user_list()
        self.pushButton.clicked.connect(self.delete_user)  # Map pushButton to delete user
        self.pushButton_2.clicked.connect(self.close_and_open_login)  # Map pushButton_2 to close and open LogInFINAL

    def populate_user_list(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()
        connection.close()

        self.listWidget.clear()
        for user in users:
            list_item = QListWidgetItem(user[0])
            self.listWidget.addItem(list_item)

    def delete_user(self):
        selected_item = self.listWidget.currentItem()
        if selected_item:
            username = selected_item.text()
            reply = QMessageBox.question(self, 'Delete Account', f"Are you sure you want to delete the account '{username}'?", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                connection = pyodbc.connect(connection_string)
                cursor = connection.cursor()
                # Delete related records in the follow table
                cursor.execute("DELETE FROM follow WHERE follower_id = (SELECT id FROM users WHERE username = ?) OR followee_id = (SELECT id FROM users WHERE username = ?)", (username, username))
                # Delete related records in the likes table
                cursor.execute("DELETE FROM likes WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
                # Delete related records in the photos table
                cursor.execute("DELETE FROM photos WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
                # Delete related records in the comments table
                cursor.execute("DELETE FROM comments WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
                # Delete the user
                cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                connection.commit()
                connection.close()
                self.populate_user_list()
                QMessageBox.information(self, "Account Deleted", f"The account '{username}' has been deleted successfully.")

    def close_and_open_login(self):
        self.close()
        self.login_screen = LoginScreen()
        self.login_screen.show()

class SignUpScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('SignUpFINAL.ui', self)

        self.pushButton_3.clicked.connect(self.handle_signup)

    def handle_signup(self):
        email = self.lineEdit.text().strip()
        dob = self.lineEdit_2.text().strip()
        username = self.lineEdit_3.text().strip()
        password = self.lineEdit_4.text().strip()

        if not email or not dob or not username or not password:
            QMessageBox.warning(self, "Sign-Up Failed", "Please fill in all fields.")
            return

        if register_user(username, password, email, dob):
            QMessageBox.information(self, "Sign-Up Success", "Your account has been created successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Sign-Up Failed", "Username already exists or there was an error. Please choose another.")

class ProfilePage(QMainWindow):
    def __init__(self, current_user_id):
        super().__init__()
        uic.loadUi("MyProfileFINAL.ui", self)
        self.current_user_id = current_user_id
        self.pushButton_5.clicked.connect(self.open_following_page)
        self.pushButton.clicked.connect(self.open_followers_page)  # Map pushButton to open followers page
        self.home.clicked.connect(self.close_profile_page)
        self.editprofile.clicked.connect(self.open_edit_profile_page)
        self.listWidget.itemClicked.connect(self.open_post_screen)  # Map listWidget item click to open post screen
        self.populate_profile()
        self.populate_posts()

    def populate_profile(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("SELECT username, profilepic FROM dbo.users WHERE id = ?", (self.current_user_id,))
        result = cursor.fetchone()
        if result:
            self.username.setText(result[0])
            self.current_username = result[0]  # Store the current username
            profilepic_url = result[1]
            self.display_profile_picture(profilepic_url)

        cursor.execute("SELECT COUNT(*) FROM dbo.photos WHERE user_id = ?", (self.current_user_id,))
        result = cursor.fetchone()
        if result:
            self.label.setText(f"Posts: {result[0]}")

        cursor.execute("SELECT COUNT(*) FROM dbo.follow WHERE followee_id = ?", (self.current_user_id,))
        result = cursor.fetchone()
        if result:
            self.label_3.setText(f"Followers: {result[0]}")

        cursor.execute("SELECT COUNT(*) FROM dbo.follow WHERE follower_id = ?", (self.current_user_id,))
        result = cursor.fetchone()
        if result:
            self.label_23.setText(f"Following: {result[0]}")

        connection.close()

    def populate_posts(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("SELECT id, caption, created_at FROM dbo.photos WHERE user_id = ? ORDER BY created_at DESC", (self.current_user_id,))
        posts = cursor.fetchall()
        connection.close()

        self.listWidget.clear()
        for post in posts:
            post_id, caption, created_at = post
            list_item = QListWidgetItem(f"{caption} - {created_at}")
            list_item.setData(Qt.ItemDataRole.UserRole, post_id)
            self.listWidget.addItem(list_item)

    def open_post_screen(self, item):
        post_id = item.data(Qt.ItemDataRole.UserRole)
        self.post_screen_window = AltPostScreenWindow(post_id, self.current_user_id, self.current_username)
        self.post_screen_window.show()

    def display_profile_picture(self, image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            image = QPixmap()
            image.loadFromData(BytesIO(response.content).read())
            # Resize the image to fit the label while maintaining aspect ratio
            label_size = self.profilepic.size()
            side_length = min(label_size.width(), label_size.height())
            scaled_image = image.scaled(side_length, side_length, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.profilepic.setPixmap(scaled_image)
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Image Load Failed", f"Failed to load profile picture: {e}")
            # Set a default image or placeholder
            self.profilepic.setPixmap(QPixmap("path/to/default/profilepic.png"))

    def open_following_page(self):
        self.following_page = FollowingPage(self.current_user_id, label_text="Following")
        self.following_page.show()

    def open_followers_page(self):
        self.followers_page = FollowersPage(self.current_user_id, label_text="Followers")
        self.followers_page.show()

    def open_edit_profile_page(self):
        self.edit_profile_window = EditProfileWindow(self.current_user_id)
        self.edit_profile_window.show()

    def close_profile_page(self):
        self.close()

class AltPostScreenWindow(QMainWindow):
    def __init__(self, post_id, current_user_id, current_username):
        super(AltPostScreenWindow, self).__init__()
        uic.loadUi("AltPostScreenFINAL.ui", self)
        self.post_id = post_id
        self.current_user_id = current_user_id
        self.current_username = current_username
        self.pushButton.clicked.connect(self.close_window)

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT p.image_url, p.caption FROM dbo.photos p WHERE p.id = ?", (self.post_id,))
        result = cursor.fetchone()
        if result:
            image_url = result[0]
            caption = result[1]
            self.display_image(image_url)
            self.label_5.setText(caption)  # Set the caption to label_5
            self.label_2.setText(self.current_username)  # Set the username to label_2
        else:
            print("No image found for the post.")  # Debug statement if no image is found
        connection.close()

        self.pushButton_2.clicked.connect(self.like_post)
        self.pushButton_3.clicked.connect(self.open_comments_window)

        self.update_like_count()
        self.update_comment_count()

    def display_image(self, image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            image = QPixmap()
            image.loadFromData(BytesIO(response.content).read())
            # Resize the image to fit the label while maintaining aspect ratio
            scaled_image = image.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.label.setPixmap(scaled_image)
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Image Load Failed", f"Failed to load image: {e}")
            # Set a default image or placeholder
            self.label.setPixmap(QPixmap("path/to/default/image.png"))

    def update_like_count(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.likes WHERE photo_id = ?", (self.post_id,))
        result = cursor.fetchone()
        if result:
            self.label_3.setText(f"Likes: {result[0]}")
        connection.close()

    def update_comment_count(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.comments WHERE photo_id = ?", (self.post_id,))
        result = cursor.fetchone()
        if result:
            self.label_4.setText(f"Comments: {result[0]}")
        connection.close()

    def like_post(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.likes WHERE user_id = ? AND photo_id = ?", (self.current_user_id, self.post_id))
        result = cursor.fetchone()
        if result[0] > 0:
            QMessageBox.warning(self, "Already Liked", "You have already liked this post!")
        else:
            cursor.execute("INSERT INTO dbo.likes (user_id, photo_id, created_at) VALUES (?, ?, ?)", (self.current_user_id, self.post_id, datetime.now()))
            connection.commit()
            self.update_like_count()
        connection.close()

    def open_comments_window(self):
        self.comments_window = CommentWindow(self.post_id, self.current_user_id, self.label_2.text())
        self.comments_window.show()

    def close_window(self):
        self.close()

class EditProfileWindow(QMainWindow):
    def __init__(self, current_user_id):
        super(EditProfileWindow, self).__init__()
        uic.loadUi("EditProfileFINAL.ui", self)
        self.current_user_id = current_user_id
        self.pushButton.clicked.connect(self.apply_changes)
        self.pushButton_2.clicked.connect(self.close_window)

    def apply_changes(self):
        username = self.lineEdit.text().strip()
        profilepic_url = self.lineEdit_2.text().strip()
        email = self.lineEdit_3.text().strip()

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        if username:
            cursor.execute("UPDATE dbo.users SET username = ? WHERE id = ?", (username, self.current_user_id))
        if profilepic_url:
            cursor.execute("UPDATE dbo.users SET profilepic = ? WHERE id = ?", (profilepic_url, self.current_user_id))
        if email:
            cursor.execute("UPDATE dbo.users SET email = ? WHERE id = ?", (email, self.current_user_id))

        connection.commit()
        connection.close()

        QMessageBox.information(self, "Profile Updated", "Your profile has been updated successfully!")
        self.close()

    def close_window(self):
        self.close()

class CommentWindow(QMainWindow):
    def __init__(self, photo_id, current_user_id, followee_username):
        super().__init__()
        uic.loadUi("CommentsFINAL.ui", self)
        self.photo_id = photo_id
        self.current_user_id = current_user_id
        self.followee_username = followee_username
        self.lineEdit.setPlaceholderText("Type your comment here...")
        self.pushButton.clicked.connect(self.post_comment)
        self.pushButton_2.clicked.connect(self.close_window)
        self.load_comments()

    def post_comment(self):
        comment_text = self.lineEdit.text().strip()
        if comment_text:
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO dbo.comments (comment_text, user_id, photo_id, created_at) VALUES (?, ?, ?, ?)", 
                           (comment_text, self.current_user_id, self.photo_id, datetime.now()))
            connection.commit()
            connection.close()
            self.lineEdit.clear()
            self.load_comments()
        else:
            QMessageBox.warning(self, "Empty Comment", "Please enter a comment before posting.")

    def load_comments(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT u.username, c.comment_text FROM dbo.comments c JOIN dbo.users u ON c.user_id = u.id WHERE c.photo_id = ?", (self.photo_id,))
        self.listWidget.clear()
        for row in cursor.fetchall():
            username, comment_text = row
            list_item = QListWidgetItem(f"{username}: {comment_text}")
            self.listWidget.addItem(list_item)
        connection.close()

    def close_window(self):
        self.close()

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        uic.loadUi("MainPageFINAL.ui", self)

        self.label_3.setText(f"Welcome, {username}!")

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM dbo.users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            self.current_user_id = result[0]
        connection.close()

        self.populate_table(username)

        self.pushButton_9.clicked.connect(self.open_profile_page)
        self.pushButton_7.clicked.connect(self.open_new_post)
        self.pushButton_11.clicked.connect(self.logout_and_open_login)
        self.pushButton_8.clicked.connect(self.open_search_users)

        self.listWidget.itemClicked.connect(self.open_post_screen)

    def populate_table(self, username):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        self.listWidget.clear()

        select_query = """
        SELECT u2.username, p.created_at
        FROM follow f
        JOIN photos p ON f.followee_id = p.user_id
        JOIN users u1 ON f.follower_id = u1.id
        JOIN users u2 ON f.followee_id = u2.id
        WHERE u1.username = ?
        ORDER BY p.created_at DESC
        """
        cursor.execute(select_query, (username,))

        added_followees = set()

        for row_data in cursor.fetchall():
            followee_username, created_at = row_data
            if followee_username not in added_followees:
                formatted_string = f"{followee_username} uploaded a new photo! {created_at}"
                list_item = QListWidgetItem(formatted_string)
                list_item.setData(Qt.ItemDataRole.UserRole, followee_username)
                self.listWidget.addItem(list_item)
                added_followees.add(followee_username)

        connection.close()

    def check_and_open_comment_window(self):
        if self.listWidget.currentItem() is not None:
            self.open_comment_window()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an item from the list before commenting.")

    def open_new_post(self):
        self.new_post_window = NewPostWindow(self.current_user_id)
        self.new_post_window.show()

    def open_post_screen(self, item):
        followee_username = item.data(Qt.ItemDataRole.UserRole)
        self.post_screen_window = PostScreenWindow(followee_username, self.current_user_id)
        self.post_screen_window.show()

    def like_post(self):
        print("Liked the post!")

    def open_comment_window(self):
        self.comment_window = CommentWindow()
        self.comment_window.show()

    def open_profile_page(self):
        self.profile_page = ProfilePage(self.current_user_id)
        self.profile_page.show()

    def open_search_users(self):
        self.search_users_window = SearchUsersWindow(self.current_user_id)
        self.search_users_window.show()

    def logout_and_open_login(self):
        self.close()
        self.login_screen = LoginScreen()
        self.login_screen.show()

    # def unmapped_function(self):
    #     pass

class SearchUsersWindow(QMainWindow):
    def __init__(self, current_user_id):
        super(SearchUsersWindow, self).__init__()
        uic.loadUi("SearchUsersFINAL.ui", self)
        self.current_user_id = current_user_id
        self.pushButton.clicked.connect(self.close_window)  # Map pushButton to close the window
        self.pushButton_2.clicked.connect(self.search_users)  # Map pushButton_2 to search users
        self.listWidget.itemClicked.connect(self.open_user_profile)  # Map listWidget item click to open user profile

    def search_users(self):
        search_text = self.lineEdit.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Empty Search", "Please enter a username to search.")
            return

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM dbo.users WHERE username LIKE ?", (search_text + '%',))
        results = cursor.fetchall()
        connection.close()

        self.listWidget.clear()
        for result in results:
            username = result[0]
            list_item = QListWidgetItem(username)
            self.listWidget.addItem(list_item)

    def open_user_profile(self, item):
        followee_username = item.text()
        self.following_profile_window = FollowingProfileWindow(followee_username, self.current_user_id)
        self.following_profile_window.show()

    def close_window(self):
        self.close()

class NewPostWindow(QMainWindow):
    def __init__(self, current_user_id):
        super(NewPostWindow, self).__init__()
        uic.loadUi("NewPostFINAL.ui", self)
        self.current_user_id = current_user_id
        self.pushButton_3.clicked.connect(self.upload_post)  # Map pushButton_3 to handle the upload process
        self.pushButton.clicked.connect(self.close_window)  # Map pushButton to close the window

    def upload_post(self):
        image_url = self.lineEdit.text().strip()
        caption = self.lineEdit_2.text().strip()

        if not image_url or not caption:
            QMessageBox.warning(self, "Incomplete Fields", "Please enter both an image URL and a caption.")
            return

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO dbo.photos (user_id, image_url, caption, created_at) VALUES (?, ?, ?, ?)",
                           (self.current_user_id, image_url, caption, datetime.now()))
            connection.commit()
            QMessageBox.information(self, "Photo Uploaded", "Your photo has been uploaded successfully!")
            self.close()
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Upload Failed", f"Failed to upload photo: {e}")
        finally:
            connection.close()

    def close_window(self):
        self.close()

class PostScreenWindow(QMainWindow):
    def __init__(self, followee_username, current_user_id):
        super(PostScreenWindow, self).__init__()
        uic.loadUi("PostScreenFINAL.ui", self)
        self.label_2.setText(followee_username)
        self.current_user_id = current_user_id
        self.pushButton.clicked.connect(self.close_window)

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT p.id, p.image_url, p.caption FROM dbo.photos p JOIN dbo.users u ON p.user_id = u.id WHERE u.username = ?", (followee_username,))
        result = cursor.fetchone()
        if result:
            self.photo_id = result[0]
            image_url = result[1]
            caption = result[2]
            print(f"Image URL: {image_url}")  # Debug statement to check the image URL
            self.display_image(image_url)
            self.label_5.setText(caption)  # Set the caption to label_5
        else:
            print("No image found for the user.")  # Debug statement if no image is found
        connection.close()

        self.pushButton_2.clicked.connect(self.like_post)
        self.pushButton_3.clicked.connect(self.open_comments_window)

        self.update_like_count()
        self.update_comment_count()

    def display_image(self, image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            image = QPixmap()
            image.loadFromData(BytesIO(response.content).read())
            # Resize the image to fit the label while maintaining aspect ratio
            scaled_image = image.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.label.setPixmap(scaled_image)
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Image Load Failed", f"Failed to load image: {e}")
            # Set a default image or placeholder
            self.label.setPixmap(QPixmap("path/to/default/image.png"))

    def update_like_count(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.likes WHERE photo_id = ?", (self.photo_id,))
        result = cursor.fetchone()
        if result:
            self.label_3.setText(f"Likes: {result[0]}")
        connection.close()

    def update_comment_count(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.comments WHERE photo_id = ?", (self.photo_id,))
        result = cursor.fetchone()
        if result:
            self.label_4.setText(f"Comments: {result[0]}")
        connection.close()

    def like_post(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.likes WHERE user_id = ? AND photo_id = ?", (self.current_user_id, self.photo_id))
        result = cursor.fetchone()
        if result[0] > 0:
            QMessageBox.warning(self, "Already Liked", "You have already liked this post!")
        else:
            cursor.execute("INSERT INTO dbo.likes (user_id, photo_id, created_at) VALUES (?, ?, ?)", (self.current_user_id, self.photo_id, datetime.now()))
            connection.commit()
            self.update_like_count()
        connection.close()

    def open_comments_window(self):
        self.comments_window = CommentWindow(self.photo_id, self.current_user_id, self.label_2.text())
        self.comments_window.show()

    def close_window(self):
        self.close()

class FollowingPage(QMainWindow):
    def __init__(self, current_user_id, label_text="Following"):
        super(FollowingPage, self).__init__()
        uic.loadUi("FollowingPageFINAL.ui", self)
        self.current_user_id = current_user_id
        self.label.setText(label_text)
        self.populate_following_list()
        self.listWidget.itemClicked.connect(self.open_following_profile)
        self.back.clicked.connect(self.close_window)

    def populate_following_list(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT u.username
            FROM follow f
            JOIN users u ON f.followee_id = u.id
            WHERE f.follower_id = ?
        """, (self.current_user_id,))
        self.listWidget.clear()
        for row in cursor.fetchall():
            username = row[0]
            list_item = QListWidgetItem(username)
            self.listWidget.addItem(list_item)
        connection.close()

    def open_following_profile(self, item):
        followee_username = item.text()
        self.following_profile_window = FollowingProfileWindow(followee_username, self.current_user_id)
        self.following_profile_window.show()

    def close_window(self):
        self.close()

class FollowersPage(QMainWindow):
    def __init__(self, current_user_id, label_text="Followers"):
        super(FollowersPage, self).__init__()
        uic.loadUi("FollowingPageFINAL.ui", self)  # Reusing the same UI for followers
        self.current_user_id = current_user_id
        self.label.setText(label_text)
        self.populate_followers_list()
        self.listWidget.itemClicked.connect(self.open_follower_profile)
        self.back.clicked.connect(self.close_window)

    def populate_followers_list(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT u.username
            FROM follow f
            JOIN users u ON f.follower_id = u.id
            WHERE f.followee_id = ?
        """, (self.current_user_id,))
        self.listWidget.clear()
        for row in cursor.fetchall():
            username = row[0]
            list_item = QListWidgetItem(username)
            self.listWidget.addItem(list_item)
        connection.close()

    def open_follower_profile(self, item):
        follower_username = item.text()
        self.follower_profile_window = FollowingProfileWindow(follower_username, self.current_user_id)
        self.follower_profile_window.show()

    def close_window(self):
        self.close()

class FollowingProfileWindow(QMainWindow):
    def __init__(self, followee_username, current_user_id):
        super(FollowingProfileWindow, self).__init__()
        uic.loadUi("FollowingProfileFINAL.ui", self)
        self.followee_username = followee_username
        self.current_user_id = current_user_id
        self.populate_profile()
        self.pushButton_2.clicked.connect(self.follow_user)
        self.pushButton.clicked.connect(self.close_window)
        self.listWidget.itemClicked.connect(self.open_post_screen)  # Map listWidget item click to open post screen

    def populate_profile(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Fetch the followee's user ID and profile picture URL
        cursor.execute("SELECT id, profilepic FROM dbo.users WHERE username = ?", (self.followee_username,))
        result = cursor.fetchone()
        if result:
            followee_id = result[0]
            profilepic_url = result[1]
            self.username.setText(self.followee_username)
            self.display_profile_picture(profilepic_url)

            cursor.execute("SELECT COUNT(*) FROM dbo.photos WHERE user_id = ?", (followee_id,))
            result = cursor.fetchone()
            if result:
                self.label.setText(f"Posts: {result[0]}")

            cursor.execute("SELECT COUNT(*) FROM dbo.follow WHERE followee_id = ?", (followee_id,))
            result = cursor.fetchone()
            if result:
                self.label_2.setText(f"Followers: {result[0]}")

            cursor.execute("SELECT COUNT(*) FROM dbo.follow WHERE follower_id = ?", (followee_id,))
            result = cursor.fetchone()
            if result:
                self.label_3.setText(f"Following: {result[0]}")

            self.populate_posts(followee_id)

        connection.close()

    def populate_posts(self, followee_id):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("SELECT id, caption, created_at FROM dbo.photos WHERE user_id = ? ORDER BY created_at DESC", (followee_id,))
        posts = cursor.fetchall()
        connection.close()

        self.listWidget.clear()
        for post in posts:
            post_id, caption, created_at = post
            list_item = QListWidgetItem(f"{caption} - {created_at}")
            list_item.setData(Qt.ItemDataRole.UserRole, post_id)
            self.listWidget.addItem(list_item)

    def open_post_screen(self, item):
        post_id = item.data(Qt.ItemDataRole.UserRole)
        self.post_screen_window = AltPostScreenWindow(post_id, self.current_user_id, self.followee_username)
        self.post_screen_window.show()

    def display_profile_picture(self, image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            image = QPixmap()
            image.loadFromData(BytesIO(response.content).read())
            # Resize the image to fit the label while maintaining aspect ratio
            label_size = self.profilepic.size()
            side_length = min(label_size.width(), label_size.height())
            scaled_image = image.scaled(side_length, side_length, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.profilepic.setPixmap(scaled_image)
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Image Load Failed", f"Failed to load profile picture: {e}")
            # Set a default image or placeholder
            self.profilepic.setPixmap(QPixmap("path/to/default/profilepic.png"))

    def follow_user(self):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Get the followee's user ID
        cursor.execute("SELECT id FROM dbo.users WHERE username = ?", (self.followee_username,))
        followee_id = cursor.fetchone()[0]

        # Check if the current user already follows the followee
        cursor.execute("SELECT COUNT(*) FROM dbo.follow WHERE follower_id = ? AND followee_id = ?", (self.current_user_id, followee_id))
        result = cursor.fetchone()
        if result[0] > 0:
            QMessageBox.warning(self, "Already Following", "You already follow this account.")
        else:
            # Insert a new follow record with the current timestamp
            cursor.execute("INSERT INTO dbo.follow (follower_id, followee_id, created_at) VALUES (?, ?, ?)", 
                           (self.current_user_id, followee_id, datetime.now()))
            connection.commit()
            QMessageBox.information(self, "Followed", f"You are now following {self.followee_username}.")

            # Update the followers count label
            cursor.execute("SELECT COUNT(*) FROM dbo.follow WHERE followee_id = ?", (followee_id,))
            result = cursor.fetchone()
            if result:
                self.label_2.setText(f"Followers: {result[0]}")

        connection.close()

    def close_window(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_screen = LoginScreen()
    login_screen.show()

    sys.exit(app.exec())