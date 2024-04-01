## Flask Application Design for a Sports Channel Management Platform

### HTML Files

**1. signup.html:**
- Contains a form for users to register and create a profile.
- Includes fields for username, email, password, and profile information.

**2. profile.html:**
- Displays a user's profile, including their uploaded videos and subscribed channels.
- Provides options to edit profile information and upload videos.

**3. video_upload.html:**
- Form for users to upload and manage their sports videos.
- Includes fields for video title, description, and tags.

**4. channel_list.html:**
- Lists all available channels on the platform.
- Displays channel names, descriptions, and subscription counts.

**5. channel_page.html:**
- Displays a specific channel's videos, subscribers, and other information.
- Allows users to subscribe to the channel.

**6. admin_dashboard.html:**
- Provides an interface for administrators to manage videos, channels, and users.
- Includes options for approving/rejecting videos, deleting channels, and suspending users.

### Routes

**1. @app.route('/signup', methods=['GET', 'POST']):**
- GET: Displays the signup form (signup.html).
- POST: Processes user registration and creates a new user account.

**2. @app.route('/login', methods=['GET', 'POST']):**
- GET: Presents a login form.
- POST: Validates user credentials and logs the user in.

**3. @app.route('/profile', methods=['GET']):**
- GET: Fetches the user's profile information and displays the profile page (profile.html).

**4. @app.route('/video_upload', methods=['GET', 'POST']):**
- GET: Shows the video upload form (video_upload.html).
- POST: Handles video upload and stores it in the database.

**5. @app.route('/channels', methods=['GET']):**
- GET: Retrieves all channels from the database and displays the channel list (channel_list.html).

**6. @app.route('/channel/<channel_id>', methods=['GET']):**
- GET: Fetches a specific channel's information and displays the channel page (channel_page.html).

**7. @app.route('/admin', methods=['GET']):**
- GET: Validates the user's admin privileges and displays the admin dashboard (admin_dashboard.html).

**8. @app.route('/admin/videos', methods=['GET']):**
- GET: Lists all uploaded videos and allows admins to approve/reject them.

**9. @app.route('/admin/channels', methods=['GET']):**
- GET: Displays all channels and provides options for managing and deleting them.

**10. @app.route('/admin/users', methods=['GET']):**
- GET: Lists all users and allows admins to suspend or delete accounts.