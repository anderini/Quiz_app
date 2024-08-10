CREATE EVENT delete_otp_event
ON SCHEDULE EVERY 60 SECOND
DO DELETE FROM quiz.quiz_app_user WHERE id IN(SELECT quiz.quiz_app_otp_class.user_id FROM quiz.quiz_app_otp_class WHERE  NOW() > quiz.quiz_app_otp_class.otp_expiry) and is_validate=False;
#DROP EVENT myevent