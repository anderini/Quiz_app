CREATE EVENT delete_login_refresh_token
ON SCHEDULE EVERY 3600 SECOND
DO DELETE FROM quiz.token_blacklist_outstandingtoken WHERE NOW() > quiz.token_blacklist_outstandingtoken.expires_at;
#DROP EVENT myevent