CREATE EVENT delete_reset_token
ON SCHEDULE EVERY 60 SECOND
DO DELETE FROM quiz.quiz_app_request_reset_password_class WHERE  NOW() > quiz.quiz_app_request_reset_password_class.token_expiry;
#DROP EVENT myevent