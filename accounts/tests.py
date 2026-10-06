from django.contrib.auth import get_user_model
from django.test import TestCase

class AccountTests(TestCase):
    def test_registration_signs_in_and_password_is_hashed(self):
        response = self.client.post("/accounts/register/", {
            "username": "newcustomer", "first_name": "Alex", "last_name": "River",
            "email": "alex@example.com", "password1": "AValidPassword778!", "password2": "AValidPassword778!",
        })
        self.assertRedirects(response, "/accounts/profile/")
        user = get_user_model().objects.get(username="newcustomer")
        self.assertNotEqual(user.password, "AValidPassword778!")
        self.assertTrue(user.check_password("AValidPassword778!"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_registration_rejects_invalid_and_duplicate_email(self):
        get_user_model().objects.create_user("existing", "alex@example.com", "Password888!")
        response = self.client.post("/accounts/register/", {
            "username": "newcustomer", "first_name": "Alex", "last_name": "River", "email": "ALEX@example.com",
            "password1": "123", "password2": "different",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_blank_registration_displays_errors(self):
        response = self.client.post("/accounts/register/", {})
        self.assertTrue(response.context["form"].errors)

    def test_login_logout_and_protected_profile(self):
        get_user_model().objects.create_user("customer", "customer@example.com", "Password888!")
        self.assertRedirects(self.client.get("/accounts/profile/"), "/accounts/login/?next=/accounts/profile/")
        self.assertRedirects(self.client.post("/accounts/login/", {"username": "customer", "password": "Password888!"}), "/")
        self.assertEqual(self.client.get("/accounts/profile/").status_code, 200)
        self.assertEqual(self.client.get("/accounts/logout/").status_code, 405)
        self.assertRedirects(self.client.post("/accounts/logout/"), "/")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_rejects_external_next_url(self):
        get_user_model().objects.create_user("customer", password="Password888!")
        response = self.client.post("/accounts/login/?next=https://evil.example/", {"username": "customer", "password": "Password888!"})
        self.assertRedirects(response, "/")

    def test_profile_updates_and_duplicate_email_rejected(self):
        user = get_user_model().objects.create_user("customer", "customer@example.com", "Password888!")
        get_user_model().objects.create_user("other", "taken@example.com", "Password888!")
        self.client.force_login(user)
        self.client.post("/accounts/profile/", {"first_name": "Jordan", "last_name": "Stone", "email": "jordan@example.com"})
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Jordan")
        response = self.client.post("/accounts/profile/", {"first_name": "Jordan", "last_name": "Stone", "email": "taken@example.com"})
        self.assertIn("email", response.context["form"].errors)
