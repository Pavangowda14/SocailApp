
SocialApp is a Django-based web application that serves as a social platform, offering features similar to popular social media platforms like Instagram.

Features

- **User Authentication:** Secure user authentication system with login and registration.
- **Profiles:** User profiles with customizable avatars and bio information.
- **Posts:** Create posts with images and captions.
- **Feed:** Personalized feed displaying posts from followed users.
- **Likes:** Interact with posts through likes.
- **Follow/Unfollow:** Follow or unfollow other users to customize your feed.


## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Pavangowda14/SocialApp.git
    cd SocialApp
    ```

2. **Set Up Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Create Superuser (Optional):**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the App:**
   Open your web browser and go to [http://localhost:8000/](http://localhost:8000/)
