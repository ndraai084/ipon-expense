
from werkzeug.security import generate_password_hash, check_password_hash
from firebase_config import db


def register_user(username, email, password):

    try:

        username = username.strip().lower()
        email = email.strip().lower()

        existing_username = (
            db.collection("users")
            .where("username", "==", username)
            .get()
        )

        if existing_username:

            print("Username already exists")
            return None

        existing_email = (
            db.collection("users")
            .where("email", "==", email)
            .get()
        )

        if existing_email:

            print("Email already exists")
            return None

        user_ref = (
            db.collection("users")
            .document()
        )

        user_doc = {

            "uid": user_ref.id,

            "username": username,

            "email": email,

            "password":
                generate_password_hash(
                    password
                )
        }

        user_ref.set(user_doc)

        return {
            "uid": user_ref.id,
            "username": username,
            "email": email
        }

    except Exception as e:

        print(
            "Registration Error:",
            e
        )

        return None


def login_user(identifier, password):

    try:

        identifier = (
            identifier
            .strip()
            .lower()
        )

        users = []

        if "@" in identifier:

            users = (
                db.collection("users")
                .where(
                    "email",
                    "==",
                    identifier
                )
                .get()
            )

        else:

            users = (
                db.collection("users")
                .where(
                    "username",
                    "==",
                    identifier
                )
                .get()
            )

        if not users:

            print(
                "User not found"
            )

            return None

        user_snapshot = users[0]

        user_data = (
            user_snapshot
            .to_dict()
        )

        stored_password = (
            user_data
            .get(
                "password"
            )
        )

        if check_password_hash(
            stored_password,
            password
        ):

            return {

                "uid":
                    user_snapshot.id,

                "username":
                    user_data.get(
                        "username"
                    ),

                "email":
                    user_data.get(
                        "email"
                    )
            }

        print(
            "Wrong password"
        )

        return None

    except Exception as e:

        print(
            "Login Error:",
            e
        )

        return None