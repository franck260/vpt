# -*- coding: utf-8 -*-


from app.models import User
from app.tests import dbfixture, UserData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER
from app.utils.session import to_md5
from application import app
from web import config
import copy



class TestAccount(ControllerTestCase):
    
    def setUp(self):
        
        super(TestAccount, self).setUp()
        self.data = dbfixture.data(UserData)
        self.data.setup()
    
    def tearDown(self):
        super(TestAccount, self).tearDown()
        self.data.teardown()
        
    def test_logout_notlogged(self):
        
        response = app.request("/logout") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
 
    def test_logout(self):
        
        self.login()
        self.assertTrue(config.session_manager.is_logged)
        response = app.request("/logout") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertFalse(config.session_manager.is_logged)

    def test_login_GET(self):
        
        response = app.request("/login", method="GET") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Identification requise", response.data)
 
    def test_login_POST_OK(self):

        self.assertFalse(config.session_manager.is_logged)
        response = app.request("/login", method="POST", data={"email" : "jolevy23@gmail.com", "password" : "secret4"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertTrue(config.session_manager.is_logged)  

    def test_login_POST_KO(self):

        self.assertFalse(config.session_manager.is_logged)
        response = app.request("/login", method="POST", data={"email" : "jolevy23@gmail.com", "password" : "secret2"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertFalse(config.session_manager.is_logged)
    
    def test_account_notlogged(self):
        
        response = app.request("/account") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
 
    def test_account(self):
        
        self.login()
        response = app.request("/account") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        
        self.assertIn("Mon compte", response.data)
        self.assertIn("Mon mot de passe", response.data)
        self.assertIn(UserData.franck_l.pseudonym, response.data)
        self.assertIn(UserData.franck_l.first_name, response.data)
        self.assertIn(UserData.franck_l.last_name, response.data)
        self.assertIn(UserData.franck_l.email, response.data)
        
        self.assertNotIn(UserData.franck_l.password, response.data)
        self.assertNotIn("Please enter a value", response.data)
        
    def test_update_user_notlogged(self):
        
        response = app.request("/update_user", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_update_user(self):
        
        updated_user = User(first_name=UserData.franck_l.first_name + "_new",
                            last_name=UserData.franck_l.last_name + "_new",
                            pseudonym=UserData.franck_l.pseudonym+ "_new",
                            email="new." + UserData.franck_l.email,
                            is_admin=UserData.franck_l.is_admin,
                            password=UserData.franck_l.password)


        updated_user_data = {"User-1-pseudonym" : updated_user.pseudonym,
                             "User-1-first_name" : updated_user.first_name,
                             "User-1-last_name" : updated_user.last_name,
                             "User-1-email" : updated_user.email}
        
        self.login()
        
        # Makes sure that the update fails with invalid data 
        for key in updated_user_data.keys():
            
            # Alters the submitted data
            invalid_user_data = copy.deepcopy(updated_user_data)
            invalid_user_data[key] = ""
            
            # Makes sure the server rejects the update
            response = app.request("/update_user", method="POST", data=invalid_user_data) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)
            self.assertIn("Please enter a value", response.data)
            self.assertEqual(config.session_manager.user, UserData.franck_l)
            self.assertNotEqual(config.session_manager.user, updated_user)
        
        # Makes sure that the update works with valid data        
        response = app.request("/update_user", method="POST", data=updated_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertEqual(config.session_manager.user, updated_user)
        self.assertNotEqual(config.session_manager.user, UserData.franck_l)
        
    def test_update_password_notlogged(self):
        
        response = app.request("/update_password", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_update_password(self):
        
        NEW_PASSWORD = "%!new_password_42"
        
        updated_user = User(first_name=UserData.franck_l.first_name,
                            last_name=UserData.franck_l.last_name,
                            pseudonym=UserData.franck_l.pseudonym,
                            email=UserData.franck_l.email,
                            is_admin=UserData.franck_l.is_admin,
                            password=to_md5(NEW_PASSWORD))


        updated_user_data = {"User-1-old_password" : "secret1",
                             "User-1-new_password" : NEW_PASSWORD,
                             "User-1-new_password_confirm" : NEW_PASSWORD}
        
        self.login()
        
        # Makes sure that the update fails with invalid data (1)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-old_password"] = ""
        response = app.request("/update_password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Please enter a value", response.data)
        self.assertNotIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)
        
        # Makes sure that the update fails with invalid data (2)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-old_password"] = "invalid"
        response = app.request("/update_password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Invalid value", response.data)
        self.assertNotIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)        

        # Makes sure that the update fails with invalid data (3)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-new_password"] = ""
        response = app.request("/update_password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Please enter a value", response.data)
        self.assertIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)
        
        # Makes sure that the update fails with invalid data (4)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-new_password"] = "a"
        response = app.request("/update_password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Value must be at least 4 characters long", response.data)
        self.assertIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)
        
        # Makes sure that the update fails with invalid data (5)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-new_password"] = NEW_PASSWORD + "a"
        response = app.request("/update_password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertNotIn("Value must be at least 4 characters long", response.data)
        self.assertIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)   
            
        # Makes sure that the update works with valid data        
        response = app.request("/update_password", method="POST", data = updated_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertEqual(config.session_manager.user, updated_user)
        self.assertNotEqual(config.session_manager.user, UserData.franck_l)
