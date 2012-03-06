# -*- coding: utf-8 -*-

from app.models import User, PasswordToken
from app.tests import dbfixture, UserData, PasswordTokenData, UserTokenData
from app.tests.controllers import ControllerTestCase, HTTP_OK, HTTP_SEE_OTHER, \
    HTTP_FORBIDDEN
from app.utils.session import to_md5
from application import app
from sqlalchemy.orm.exc import NoResultFound
from web import config
import copy

class TestAccount(ControllerTestCase):
    
    def setUp(self):
        
        super(TestAccount, self).setUp()
        self.data = dbfixture.data(UserData, PasswordTokenData, UserTokenData)
        self.data.setup()
    
    def tearDown(self):
        super(TestAccount, self).tearDown()
        self.data.teardown()
        
    def test_logout_notlogged(self):
        
        response = app.request("/logout") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
 
    def test_logout(self):
        
        self.login()
        self.assertEquals(config.session_manager.user, UserData.franck_l)
        response = app.request("/logout") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertIsNone(config.session_manager.user)

    def test_login_GET(self):
        
        response = app.request("/login", method="GET") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Identification requise", response.data)
 
    def test_login_POST(self):

        self.assertIsNone(config.session_manager.user)
        response = app.request("/login", method="POST", data={"email" : "jo@gmail.com", "password" : "secret4"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertEquals(config.session_manager.user, UserData.jo)

    def test_login_POST_wrongpassword(self):

        self.assertIsNone(config.session_manager.user)
        response = app.request("/login", method="POST", data={"email" : "jo@gmail.com", "password" : "secret2"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIsNone(config.session_manager.user)
        
    def test_login_POST_inactiveuser(self):

        self.assertIsNone(config.session_manager.user)
        response = app.request("/login", method="POST", data={"email" : "zoe@gmail.com", "password" : "secret7"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIsNone(config.session_manager.user)
    
    def test_view_account_notlogged(self):
        
        response = app.request("/admin/account") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
 
    def test_view_account(self):
        
        self.login()
        response = app.request("/admin/account") #@UndefinedVariable
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
        
        response = app.request("/update/user", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_update_user(self):
        
        updated_user = User(
            first_name=UserData.franck_l.first_name + "_new",
            last_name=UserData.franck_l.last_name + "_new",
            pseudonym=UserData.franck_l.pseudonym+ "_new",
            email="new." + UserData.franck_l.email,
            password=UserData.franck_l.password,
            level=UserData.franck_l.level
        )

        updated_user_data = {
            "User-1-pseudonym" : updated_user.pseudonym,
            "User-1-first_name" : updated_user.first_name,
            "User-1-last_name" : updated_user.last_name,
            "User-1-email" : updated_user.email
        }
        
        self.login()
        
        # Makes sure that the update fails with invalid data 
        for key in updated_user_data.keys():
            
            # Alters the submitted data
            invalid_user_data = copy.deepcopy(updated_user_data)
            invalid_user_data[key] = ""
            
            # Makes sure the server rejects the update
            response = app.request("/update/user", method="POST", data=invalid_user_data) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)
            self.assertIn("Please enter a value", response.data)
            self.assertEqual(config.session_manager.user, UserData.franck_l)
            self.assertNotEqual(config.session_manager.user, updated_user)
        
        # Makes sure that the update works with valid data        
        response = app.request("/update/user", method="POST", data=updated_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertEqual(config.session_manager.user, updated_user)
        self.assertNotEqual(config.session_manager.user, UserData.franck_l)
        
    def test_update_password_notlogged(self):
        
        response = app.request("/update/password", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        
    def test_update_password(self):
        
        NEW_PASSWORD = "%!new_password_42"
        
        updated_user = User(
            first_name=UserData.franck_l.first_name,
            last_name=UserData.franck_l.last_name,
            pseudonym=UserData.franck_l.pseudonym,
            email=UserData.franck_l.email,
            password=to_md5(NEW_PASSWORD),
            level=UserData.franck_l.level
        )


        updated_user_data = {
            "User-1-old_password" : "secret1",
            "User-1-new_password" : NEW_PASSWORD,
            "User-1-new_password_confirm" : NEW_PASSWORD
        }
        
        self.login()
        
        # Makes sure that the update fails with invalid data (1)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-old_password"] = ""
        response = app.request("/update/password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Please enter a value", response.data)
        self.assertNotIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)
        
        # Makes sure that the update fails with invalid data (2)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-old_password"] = "invalid"
        response = app.request("/update/password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Invalid value", response.data)
        self.assertNotIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)        

        # Makes sure that the update fails with invalid data (3)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-new_password"] = ""
        response = app.request("/update/password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Please enter a value", response.data)
        self.assertIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)
        
        # Makes sure that the update fails with invalid data (4)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-new_password"] = "a"
        response = app.request("/update/password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Value must be at least 4 characters long", response.data)
        self.assertIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)
        
        # Makes sure that the update fails with invalid data (5)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-1-new_password"] = NEW_PASSWORD + "a"
        response = app.request("/update/password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertNotIn("Value must be at least 4 characters long", response.data)
        self.assertIn("Passwords do not match", response.data)
        self.assertEqual(config.session_manager.user, UserData.franck_l)
        self.assertNotEqual(config.session_manager.user, updated_user)   
            
        # Makes sure that the update works with valid data        
        response = app.request("/update/password", method="POST", data=updated_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertEqual(config.session_manager.user, updated_user)
        self.assertNotEqual(config.session_manager.user, UserData.franck_l)

    def test_recover_password_inactiveuser(self):
        
        response = app.request("/recover/password", method="POST", data={"email" : UserData.zoe.email}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertIn("Utilisateur inconnu", response.data)
        
    def test_recover_password_invaliduser(self):
        
        response = app.request("/recover/password", method="POST", data={"email" : "invalid@domain.com"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertIn("Utilisateur inconnu", response.data)
        
    def test_recover_password_emptyuser(self):
        
        response = app.request("/recover/password", method="POST", data={"email" : ""}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertIn("Utilisateur inconnu", response.data)
        
    def test_recover_password_nouser(self):
        
        response = app.request("/recover/password", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertIn("Utilisateur inconnu", response.data)

    def test_recover_password_alreadyasked(self):
        
        response = app.request("/recover/password", method="POST", data={"email" : UserData.jo.email}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        self.assertIn("Demande similaire", response.data)
    
    def test_recover_password_newrequest(self):

        try:

            old_tokens = [password_token.token for password_token in PasswordToken.all()]
            self.assertEqual(len(old_tokens), 2)
            
            response = app.request("/recover/password", method="POST", data={"email" : UserData.nico.email}) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)
            self.assertIn(UserData.nico.email, response.data)
            
            new_password_token = config.orm.query(PasswordToken).filter(~PasswordToken.token.in_(old_tokens)).one() #@UndefinedVariable
            self.assertEquals(new_password_token.user, UserData.nico)
            self.assertFalse(new_password_token.expired)

            response = app.request("/recover/password", method="POST", data={"email" : UserData.nico.email}) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_FORBIDDEN)
            self.assertIn("Demande similaire", response.data)
        
        finally:
            
            #TODO: should be done by the fixture
            new_password_token = config.orm.query(PasswordToken).filter(~PasswordToken.token.in_(old_tokens)).one() #@UndefinedVariable
            config.orm.delete(new_password_token)
            config.orm.commit()
            
    def test_recover_password(self):

        try:

            old_tokens = [password_token.token for password_token in PasswordToken.all()]
            self.assertEqual(len(old_tokens), 2)
            
            response = app.request("/recover/password", method="POST", data={"email" : UserData.franck_p.email}) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_OK)
            self.assertIn(UserData.franck_p.email, response.data)
            
            new_password_token = config.orm.query(PasswordToken).filter(~PasswordToken.token.in_(old_tokens)).one() #@UndefinedVariable
            self.assertEquals(new_password_token.user, UserData.franck_p)
            self.assertFalse(new_password_token.expired)

            response = app.request("/recover/password", method="POST", data={"email" : UserData.franck_p.email}) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_FORBIDDEN)
            self.assertIn("Demande similaire", response.data)
        
        finally:
            
            #TODO: should be done by the fixture
            new_password_token = config.orm.query(PasswordToken).filter(~PasswordToken.token.in_(old_tokens)).one() #@UndefinedVariable
            config.orm.delete(new_password_token)
            config.orm.commit()

    def test_reset_password_GET_notoken(self):
        
        response = app.request("/reset/password") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
    
    def test_reset_password_GET_invalidtoken(self):

        response = app.request("/reset/password?token=invalid") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)

    def test_reset_password_GET_wrongtokentype(self):

        response = app.request("/reset/password?token=%s" % UserTokenData.user_token_active.token) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
    
    def test_reset_password_GET_expiredtoken(self):

        response = app.request("/reset/password?token=%s" % PasswordTokenData.password_token_expired.token) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)

    def test_reset_password_GET(self):

        response = app.request("/reset/password?token=%s" % PasswordTokenData.password_token_active.token) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Nouveau mot de passe", response.data)

    def test_reset_password_POST_notoken(self):
        
        response = app.request("/reset/password", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
    
    def test_reset_password_POST_invalidtoken(self):

        response = app.request("/reset/password", method="POST", data={"token" : "invalid"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)

    def test_reset_password_POST_wrongtokentype(self):

        response = app.request("/reset/password", method="POST", data={"token" : UserTokenData.user_token_active.token}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
    
    def test_reset_password_POST_expiredtoken(self):

        response = app.request("/reset/password", method="POST", data={"token" : PasswordTokenData.password_token_expired.token}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)

    def test_reset_password_POST(self):

        NEW_PASSWORD = "%!new_password_42"
        
        updated_user = User(
            first_name=UserData.jo.first_name,
            last_name=UserData.jo.last_name,
            pseudonym=UserData.jo.pseudonym,
            email=UserData.jo.email,
            password=to_md5(NEW_PASSWORD),
            level=UserData.jo.level
        )


        db_user = config.orm.query(User).filter(User.first_name == "Jonathan").one() #@UndefinedVariable

        updated_user_data = {
            "token" : PasswordTokenData.password_token_active.token,
            "User-4-new_password" : NEW_PASSWORD,
            "User-4-new_password_confirm" : NEW_PASSWORD
        }
    
        # Makes sure that the update fails with invalid data (1)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-4-new_password"] = ""
        response = app.request("/reset/password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Please enter a value", response.data)
        self.assertIn("Passwords do not match", response.data)
        self.assertEqual(db_user, UserData.jo)
        self.assertNotEqual(db_user, updated_user)
        
        # Makes sure that the update fails with invalid data (2)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-4-new_password"] = "a"
        response = app.request("/reset/password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("Value must be at least 4 characters long", response.data)
        self.assertIn("Passwords do not match", response.data)
        self.assertEqual(db_user, UserData.jo)
        self.assertNotEqual(db_user, updated_user)
        
        # Makes sure that the update fails with invalid data (3)
        invalid_user_data = copy.deepcopy(updated_user_data)
        invalid_user_data["User-4-new_password"] = NEW_PASSWORD + "a"
        response = app.request("/reset/password", method="POST", data=invalid_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertNotIn("Value must be at least 4 characters long", response.data)
        self.assertIn("Passwords do not match", response.data)
        self.assertEqual(db_user, UserData.jo)
        self.assertNotEqual(db_user, updated_user)   
            
        # Makes sure that the update works with valid data        
        response = app.request("/reset/password", method="POST", data=updated_user_data) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_SEE_OTHER)
        self.assertEqual(db_user, updated_user)
        self.assertNotEqual(db_user, UserData.jo)
        
    def test_create_account_GET_notoken(self):
        
        response = app.request("/create/account") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
    
    def test_create_account_GET_invalidtoken(self):

        response = app.request("/create/account?token=invalid") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)

    def test_create_account_GET_wrongtokentype(self):

        response = app.request("/create/account?token=%s" % PasswordTokenData.password_token_active.token) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
    
    def test_create_account_GET_expiredtoken(self):

        response = app.request("/create/account?token=%s" % UserTokenData.user_token_expired.token) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)

    def test_create_account_GET(self):

        response = app.request("/create/account?token=%s" % UserTokenData.user_token_active.token) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_OK)
        self.assertIn(UserTokenData.user_token_active.email, response.data)

    def test_create_account_POST_notoken(self):
        
        response = app.request("/create/account", method="POST") #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
    
    def test_create_account_POST_invalidtoken(self):

        response = app.request("/create/account", method="POST", data={"token" : "invalid"}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)

    def test_create_account_POST_wrongtokentype(self):

        response = app.request("/create/account", method="POST", data={"token" : PasswordTokenData.password_token_active.token}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
    
    def test_create_account_POST_expiredtoken(self):

        response = app.request("/create/account", method="POST", data={"token" : UserTokenData.user_token_expired.token}) #@UndefinedVariable
        self.assertEqual(response.status, HTTP_FORBIDDEN)
        
    def test_create_account_POST(self):
        
        try:
            
            old_user_emails = [user.email for user in User.all()]
            self.assertEqual(len(old_user_emails), 7)
            
            NEW_PASSWORD = "%!new_password_42"
            
            expected_new_user = User(
                first_name="Dorian",
                last_name="Gray",
                pseudonym="Dorian G",
                email=UserTokenData.user_token_active.email,
                password=to_md5(NEW_PASSWORD),
                level=UserTokenData.user_token_active.level
            )
    
            new_user_data = {
                "token" : UserTokenData.user_token_active.token,
                "User--pseudonym" : expected_new_user.pseudonym,
                "User--first_name" : expected_new_user.first_name,
                "User--last_name" : expected_new_user.last_name,
                "User--new_email" : expected_new_user.email,
                "User--new_password" : NEW_PASSWORD,
                "User--new_password_confirm" : NEW_PASSWORD
            }
            
            # Makes sure that the insert fails with invalid data
            alterable_keys = [key for key in new_user_data.keys() if key != "token"]
            for key in alterable_keys:
                
                # Alters the submitted data
                invalid_user_data = copy.deepcopy(new_user_data)
                invalid_user_data[key] = ""
                
                # Makes sure the server rejects the insert
                response = app.request("/create/account", method="POST", data=invalid_user_data) #@UndefinedVariable
                self.assertEqual(response.status, HTTP_OK)
                self.assertIn("Please enter a value", response.data)
                self.assertEqual(len(User.all()), len(old_user_emails))
                self.assertRaises(NoResultFound, config.orm.query(User).filter(~User.email.in_(old_user_emails)).one) #@UndefinedVariable
            
            # Makes sure that the insert works with valid data        
            response = app.request("/create/account", method="POST", data=new_user_data) #@UndefinedVariable
            self.assertEqual(response.status, HTTP_SEE_OTHER)
            self.assertEqual(len(User.all()), 1 + len(old_user_emails))
            new_user = config.orm.query(User).filter(~User.email.in_(old_user_emails)).one() #@UndefinedVariable
            self.assertEquals(new_user, expected_new_user)

        finally:
            
            #TODO: should be done by the fixture
            new_user = config.orm.query(User).filter(~User.email.in_(old_user_emails)).one() #@UndefinedVariable
            config.orm.delete(new_user)
            config.orm.commit()
